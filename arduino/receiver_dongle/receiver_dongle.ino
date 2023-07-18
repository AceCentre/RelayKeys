#include <bluefruit.h>
#include "Adafruit_TinyUSB.h"

//#define DEBUG // enables serial prints of received data, disables usb hid actions

// onboard buttons and status led defines
#if defined(_VARIANT_ITSY52840_)
  //Adafruit itsybitsy 
  #define USER_SW 4
  #include <Adafruit_DotStar.h>
  Adafruit_DotStar statusLED(1, 8, 6, DOTSTAR_BGR);
#elif defined(_VARIANT_FEATHER52840_)
  //Adafruit feather nrf52840
  #define USER_SW 7
  #include <Adafruit_NeoPixel.h>
  Adafruit_NeoPixel statusLED = Adafruit_NeoPixel(1, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);
#elif defined(_VARIANT_MDBT50Q_RX_)
  // raytac dongle
  #define USER_SW PIN_BUTTON1
    
#endif

#define BLE_NAME "AceRK receiver"

BLEClientHidAdafruit hid;

// Last checked report, to detect if there is changes between reports
//hid_keyboard_report_t last_kbd_report = { 0 };
//hid_mouse_report_t last_mse_report = { 0 };


enum
{
  RID_KEYBOARD = 1,
  RID_MOUSE,
  RID_CONSUMER_CONTROL,
};

uint8_t const desc_hid_report[] =
{
  TUD_HID_REPORT_DESC_KEYBOARD( HID_REPORT_ID(RID_KEYBOARD) ),
  TUD_HID_REPORT_DESC_MOUSE   ( HID_REPORT_ID(RID_MOUSE) ),
  TUD_HID_REPORT_DESC_CONSUMER( HID_REPORT_ID(RID_CONSUMER_CONTROL) )
};

Adafruit_USBD_HID usb_hid(desc_hid_report, sizeof(desc_hid_report), HID_ITF_PROTOCOL_NONE, 2, false);

void init_status_led(){
  #if defined(_VARIANT_ITSY52840_) || defined(_VARIANT_FEATHER52840_)
    statusLED.begin();
  #elif defined(_VARIANT_MDBT50Q_RX_)
    pinMode(LED_BLUE, OUTPUT);    
  #endif  
}

void set_connection_status(bool conn_status){  
  #if defined(_VARIANT_ITSY52840_) || defined(_VARIANT_FEATHER52840_)
    if(conn_status) {
      statusLED.setPixelColor(0, 0, 16, 0);    // set green color
    } else {
      statusLED.setPixelColor(0, 16, 16, 0);  // set yellow color
    }
  #elif defined(_VARIANT_MDBT50Q_RX_)
    if(conn_status) {
      digitalWrite(LED_BLUE, HIGH);
    } else {
      digitalWrite(LED_BLUE, LOW);
    }
  #endif  
}

void setup()
{
  Serial.begin(115200);
  delay(2000);
  //  while ( !Serial ) delay(10);   // for nrf52840 with native usb

  Serial.println("Relaykeys receiver dongle");
  
  // status led init
  init_status_led();
  set_connection_status(false);
  
  // Initialize Bluefruit with maximum connections as Peripheral = 0, Central = 1
  Bluefruit.begin(0, 1);
  
  // set dev name
  Bluefruit.setName(BLE_NAME);

  // Init BLE Central Hid Serivce
  hid.begin();

  // set callbacks for receiving keyboard and mouse data
  hid.setKeyboardReportCallback(keyboard_report_callback);
  hid.setMouseReportCallback(mouse_report_callback);

  // Increase Blink rate to different from PrPh advertising mode
  Bluefruit.setConnLedInterval(250);

  // Callbacks for Central
  Bluefruit.Central.setConnectCallback(connect_callback);
  Bluefruit.Central.setDisconnectCallback(disconnect_callback);

  // Set connection secured callback, invoked when connection is encrypted
  Bluefruit.Security.setSecuredCallback(connection_secured_callback);

  /* Start Central Scanning
   * - Enable auto scan if disconnected
   * - Interval = 100 ms, window = 80 ms
   * - Don't use active scan
   * - Filter only accept HID service in advertising
   * - Start(timeout) with timeout = 0 will scan forever (until connected)
   */
  Bluefruit.Scanner.setRxCallback(scan_callback);
  Bluefruit.Scanner.restartOnDisconnect(true);
  Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  Bluefruit.Scanner.filterService(hid);   // only report HID service
  Bluefruit.Scanner.useActiveScan(false);
  Bluefruit.Scanner.start(0);             // 0 = Don't stop scanning after n seconds

  usb_hid.begin();
}

void scan_callback(ble_gap_evt_adv_report_t* report)
{
  uint8_t name_buffer[32];
  memset(name_buffer, 0, sizeof(name_buffer));

  Serial.println("Scan callback: ");
  Serial.print("MAC: ");
  Serial.printBufferReverse(report->peer_addr.addr, 6, ':');
  Serial.println();
  
  if(Bluefruit.Scanner.parseReportByType(report, BLE_GAP_AD_TYPE_COMPLETE_LOCAL_NAME, name_buffer, sizeof(name_buffer)))
  {
    Serial.print("Name: ");
    Serial.println((char*)name_buffer);
    if(strcmp((char*)name_buffer, "AceRK") == 0) {
      Serial.println("Found RelayKeys dongle");
      Serial.println("Attempting connect");

      Bluefruit.Central.connect(report);
    }
  } else {
    Serial.println("Name not available");
  }
  Serial.println();
  
  Bluefruit.Scanner.resume();
}

void connect_callback(uint16_t conn_handle)
{
  BLEConnection* conn = Bluefruit.Connection(conn_handle);

  Serial.println("Connected");

  Serial.print("Discovering HID  Service ... ");

  if ( hid.discover(conn_handle) )
  {
    Serial.println("Found it");

    // HID device mostly require pairing/bonding
    conn->requestPairing();
  }else
  {
    Serial.println("Found NONE");
    
    // disconnect since we couldn't find blehid service
    conn->disconnect();
  }
}

void connection_secured_callback(uint16_t conn_handle)
{
  BLEConnection* conn = Bluefruit.Connection(conn_handle);

  if ( !conn->secured() )
  {
    // It is possible that connection is still not secured by this time.
    // This happens (central only) when we try to encrypt connection using stored bond keys
    // but peer reject it (probably it remove its stored key).
    // Therefore we will request an pairing again --> callback again when encrypted
    conn->requestPairing();
  }
  else
  {
    Serial.println("Secured");

    // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.hid_information.xml
    uint8_t hidInfo[4];
    hid.getHidInfo(hidInfo);

    Serial.printf("HID version: %d.%d\n", hidInfo[0], hidInfo[1]);
    Serial.print("Country code: "); Serial.println(hidInfo[2]);
    Serial.printf("HID Flags  : 0x%02X\n", hidInfo[3]);

    // BLEClientHidAdafruit currently only supports Boot Protocol Mode
    // for Keyboard and Mouse. Let's set the protocol mode on prph to Boot Mode
    hid.setBootMode(true);

    // Enable Keyboard report notification if present on prph
    if ( hid.keyboardPresent() ) hid.enableKeyboard();

    // Enable Mouse report notification if present on prph
    if ( hid.mousePresent() ) hid.enableMouse();

    Serial.println("Ready to receive from peripheral");

    set_connection_status(true);
  }
}

void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;
  
  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);

  set_connection_status(false);
}

void loop()
{
  
}


void mouse_report_callback(hid_mouse_report_t* report)
{
  #ifdef DEBUG
    Serial.println("Mouse report: ");
    Serial.print("Buttons: ");
    Serial.println(report->buttons);
    Serial.print("X movement: ");
    Serial.println(report->x);
    Serial.print("Y movement: ");
    Serial.println(report->y);
    Serial.print("Vertical scroll: ");
    Serial.println(report->wheel);
    Serial.print("Horizontal scroll: ");
    Serial.println(report->pan);
  #else
    while ( !usb_hid.ready() ) {};
    usb_hid.mouseReport(RID_MOUSE, report->buttons, report->x, report->y, report->wheel, report->pan);
  #endif
}

void keyboard_report_callback(hid_keyboard_report_t* report)
{
  #ifdef DEBUG
    Serial.print("Keyboard report: ");
    Serial.print(report->modifier);
    Serial.print(" ");
    for(uint8_t i=0; i<6; i++) {
      Serial.print(report->keycode[i]);
      Serial.print(" ");
    }
    Serial.println();
  #else
    while ( !usb_hid.ready() ) {};
    usb_hid.keyboardReport(RID_KEYBOARD, report->modifier, report->keycode);
  #endif
}
