/*********************************************************************
 This is an example for our nRF52 based Bluefruit LE modules

 Pick one up today in the adafruit shop!

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!

 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/
#include <bluefruit.h>

/*
 * Implement the Bluefruit command AT+BLEKEYBOARDCODE command.
 * Nothing else useful. Useful for testing a Python program designed to work
 * with a BF LE UART Friend. Lots of this code is from an Adafruit example.
 */

BLEDis bledis;
BLEHidAdafruit blehid;

void setup() 
{
  Serial.begin(115200);
  while ( !Serial && millis() < 2000) delay(10);   // for nrf52840 with native usb

  Serial.println("Bluefruit52 HID Keyboard Example");
  Serial.println("--------------------------------\n");

  Serial.println();
  Serial.println("Go to your phone's Bluetooth settings to pair your device");
  Serial.println("then open an application that accepts keyboard input");

  Bluefruit.begin();
  // Set max power. Accepted values are: -40, -30, -20, -16, -12, -8, -4, 0, 4
  Bluefruit.setTxPower(4);
  Bluefruit.setName("RelayKeys");

  // Configure and Start Device Information Service
  bledis.setManufacturer("AceCentre");
  bledis.setModel("RelayKeys 1 / Feather 52");
  bledis.begin();

  /* Start BLE HID
   * Note: Apple requires BLE device must have min connection interval >= 20m
   * ( The smaller the connection interval the faster we could send data).
   * However for HID and MIDI device, Apple could accept min connection interval 
   * up to 11.25 ms. Therefore BLEHidAdafruit::begin() will try to set the min and max
   * connection interval to 11.25  ms and 15 ms respectively for best performance.
   */
  blehid.begin();

  // Set callback for set LED from central
  blehid.setKeyboardLedCallback(set_keyboard_led);

  /* Set connection interval (min, max) to your perferred value.
   * Note: It is already set by BLEHidAdafruit::begin() to 11.25ms - 15ms
   * min = 9*1.25=11.25 ms, max = 12*1.25= 15 ms 
   */
  /* Bluefruit.setConnInterval(9, 12); */

  // Set up and start advertising
  startAdv();
}

void startAdv(void)
{  
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
  
  // Include BLE HID service
  Bluefruit.Advertising.addService(blehid);

  // There is enough room for the dev name in the advertising packet
  Bluefruit.Advertising.addName();
  
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

typedef void (*action_func_t)(char *myLine);

typedef struct {
  char command[32+1];    // max 32 characters plus '\0' terminator
  action_func_t action;
} command_action_t;

// force lower case
void toLower(char *s) {
  while (*s) {
    if (isupper(*s)) {
      *s += 0x20;
    }
    s++;
  }
}

void sendHIDReport(char *myLine) {
  uint8_t keys[8];  // USB keyboard HID report

  memset(keys, 0, sizeof(keys));
  // myLine example: "00-00-04-00-00-00-00-00"
  char *p = strtok(myLine, "-");
  for (size_t i = 0; p && (i < sizeof(keys)); i++) {
    keys[i] = strtoul(p, NULL, 16);
    p = strtok(NULL, "-");
  }
  blehid.keyboardReport(keys[0], &keys[2]);
  Serial.println("OK");
}

const command_action_t commands[] = {
  // Name of command user types, function that implements the command.
  // TODO add other commands, some day
  {"at+blekeyboardcode", sendHIDReport},
};

void execute(char *myLine) {
  if (myLine == NULL || *myLine == '\0') return;
  char *cmd = strtok(myLine, "=");
  if (cmd == NULL || *cmd == '\0') return;
  toLower(cmd);
  for (size_t i = 0; i < sizeof(commands)/sizeof(commands[0]); i++) {
    if (strcmp(cmd, commands[i].command) == 0) {
      commands[i].action(strtok(NULL, "="));
      return;
    }
  }
  // Command not found so just send OK. Should send ERROR at some point.
  Serial.println("OK");
}

void cli_loop()
{
  static uint8_t bytesIn;
  static char myLine[80+1];

  while (Serial.available() > 0) {
    int b = Serial.read();
    if (b != -1) {
      switch (b) {
        case '\n':
          break;
        case '\r':
          Serial.println();
          myLine[bytesIn] = '\0';
          execute(myLine);
          bytesIn = 0;
          break;
        case '\b':  // backspace
          if (bytesIn > 0) {
            bytesIn--;
            Serial.print((char)b); Serial.print(' '); Serial.print((char)b);
          }
          break;
        default:
          Serial.print((char)b);
          myLine[bytesIn++] = (char)b;
          if (bytesIn >= sizeof(myLine)-1) {
            myLine[bytesIn] = '\0';
            execute(myLine);
            bytesIn = 0;
          }
          break;
      }
    }
  }
}

void loop() 
{
  cli_loop();
  // Request CPU to enter low-power mode until an event/interrupt occurs
  waitForEvent();  
}

/**
 * Callback invoked when received Set LED from central.
 * Must be set previously with setKeyboardLedCallback()
 *
 * The LED bit map is as follows: (also defined by KEYBOARD_LED_* )
 *    Kana (4) | Compose (3) | ScrollLock (2) | CapsLock (1) | Numlock (0)
 */
void set_keyboard_led(uint8_t led_bitmap)
{
  // light up Red Led if any bits is set
  if ( led_bitmap )
  {
    ledOn( LED_RED );
  }
  else
  {
    ledOff( LED_RED );
  }
}
