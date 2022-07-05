/*********************************************************************
 This file was forked from https://github.com/adafruit/Adafruit_nRF52_Arduino/blob/master/libraries/Bluefruit52Lib/examples/Peripheral/hid_keyboard/hid_keyboard.ino

 Its quite different now as we have added connection commands, mouse commands and other bits

 Work is copyright Ace Centre 2020 - MIT Licence. If you go and use this in a commercial project - thats great. But we'd appreciate even an email thanks :) 

 Note: What follows is the original Adafruit comment code. 

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!
 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>

/*
 * Implement the Bluefruit command AT+BLEKEYBOARDCODE command.
 * Nothing else useful. Useful for testing a Python program designed to work
 * with a BF LE UART Friend. Lots of this code is from an Adafruit example.
 */

//#define DEBUG // uncomment this line to see additional prints in Serial monitor

#define BLE_NAME "RelayKeys"
#define ADD_NEW_DEV_PROCESS_TIMEOUT 30000 // in millseconds
#define SWAP_CONN_PROCESS_TIMEOUT 30000   // in millseconds


// The following defines which pin for the User button to go into BLE mode. 
// NB: using this neat trick: https://electronics.stackexchange.com/a/280379
#if defined(_VARIANT_ITSY52840_)
//Adafruit itsybitsy 
  #define USER_SW 4
#elif defined(_VARIANT_FEATHER52840_)
//Adafruit feather nrf52840
    #define USER_SW 7
#else
  #ifdef DEBUG
    Serial.print("Unsupported hardware. Possibly not critical unless you want to initiate BLE mode with a button");
  #endif
  // lazy - but going to pretend its a itsybitsy. Its the one with a wierd board name. 
  #define USER_SW 4
#endif


BLEDis bledis;
BLEHidAdafruit blehid;
BLEUart bleuart;

volatile uint32_t addDevProsStartTicks = 0;
volatile uint8_t flag_addDevProsStarted = 0;
char bleDeviceNameList[15][32] = {0};
volatile uint8_t bleDeviceNameListIndex = 0;
volatile uint8_t flag_bleSwapConnProsStarted = 0;
volatile uint32_t swapConnProsStartTicks = 0;
volatile uint8_t maxBleDevListSize = 3;
volatile uint8_t switchBleConnStartIndex = 0;
volatile uint8_t switchBleConnCurrIndex = 0;

///
using namespace Adafruit_LittleFS_Namespace;
#define FILENAME "/devNameList.txt"
#define MODE_FILENAME "/config.txt"

File file(InternalFS);

volatile bool flag_saveListToFile = false;
///

uint8_t max_prph_connection;
uint8_t connection_count;

bool ble_mode = false;

uint16_t target_ble_conn = 0;
uint16_t response_ble_conn = 0;

void set_keyboard_led(uint8_t led_bitmap);

uint8_t detect_click() {
  uint32_t press_time = millis();
  uint8_t click_counter = 0;
  
  while((millis() - press_time) < 500) {
    if(digitalRead(USER_SW) == false && (millis() - press_time) < 500) {
        click_counter++;
        delay(100);      
        while(digitalRead(USER_SW) == false) {
          delay(100); // wait until button released
        }
        press_time = millis();
    }
  }
  
  return click_counter;
    
}

void save_devList_toFile(void)
{
  file.open(FILENAME, FILE_O_WRITE);

  // file existed
  if (file)
  {
    #ifdef DEBUG
    Serial.print("List has ");
    Serial.print(bleDeviceNameListIndex);
    Serial.println(" devices");

    for (int i = 0; i < bleDeviceNameListIndex; i++)
    {
      Serial.print(i);
      Serial.print(". ");
      Serial.print(bleDeviceNameList[i]);
      Serial.println();
    }
    #endif
    
    // file.truncate(file.size());
    file.seek(0);
    file.write((const uint8_t *)bleDeviceNameList, sizeof(bleDeviceNameList));
    file.write((const uint8_t *)&bleDeviceNameListIndex, 1);

    #ifdef DEBUG
    Serial.print("Saving Device List to file ");
    Serial.print(file.size());
    Serial.println();
    #endif
    file.close();
  }
  else
  {
    #ifdef DEBUG
    Serial.print(FILENAME " Write Failed");
    #endif
  }
}

void load_devList_fromFile(void)
{
  file.open(FILENAME, FILE_O_READ);

  // file existed
  if (file)
  {
    #ifdef DEBUG
    Serial.print("Loading Device List from file ");
    Serial.print(file.size());
    Serial.println();
    #endif
    
    bleDeviceNameListIndex = 0;
    memset(bleDeviceNameList, 0, sizeof(bleDeviceNameList));

    file.read((void *)bleDeviceNameList, sizeof(bleDeviceNameList));
    file.read((void *)&bleDeviceNameListIndex, 1);

    if(bleDeviceNameListIndex > 15){
      bleDeviceNameListIndex = 0;
    }
    
    #ifdef DEBUG
    Serial.print("List has ");
    Serial.print(bleDeviceNameListIndex);
    Serial.println(" devices");
    
    for (int i = 0; i < bleDeviceNameListIndex; i++)
    {
      Serial.print(i);
      Serial.print(". ");
      Serial.print(bleDeviceNameList[i]);
      Serial.println();
    }
    #endif
    
    file.close();
  }
  else
  {
    #ifdef DEBUG
    Serial.print(FILENAME " Read Failed");
    #endif
  }
}

void load_mode_file(){
  file.open(MODE_FILENAME, FILE_O_READ);
  // file existed
  if (file)
  {
    file.read((void *)&ble_mode, 1);
    file.close();
  } else {
    #ifdef DEBUG
    Serial.println(MODE_FILENAME " Read Failed");
    #endif
  }
}

void change_mode() {
  #ifdef DEBUG
    Serial.print("Changing operating mode");
  #endif

  ble_mode = !ble_mode;

  file.open(MODE_FILENAME, FILE_O_WRITE);
  if(file) {
    file.seek(0);
    file.write((const uint8_t *)&ble_mode, 1);
    file.close();
  } else {
    #ifdef DEBUG
    Serial.print(MODE_FILENAME " Write Failed");
    #endif
  }

  BLEConnection *connection = NULL;
  for(int i=0;i<max_prph_connection;i++) {
    connection = Bluefruit.Connection(i);
    connection->disconnect();
  }
  
  delay(1000);
  NVIC_SystemReset();  
}

void setup()
{
  Serial.begin(115200);
  //while ( !Serial && millis() < 2000) delay(10);   // for nrf52840 with native usb

  // Initialize Internal File System
  InternalFS.begin();

  load_mode_file();

  pinMode(USER_SW, INPUT_PULLUP);
  
  if(ble_mode) {
    max_prph_connection = 2;    
  } else {
    max_prph_connection = 1;
  }
  
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);

  Bluefruit.begin(max_prph_connection, 0);
  Bluefruit.setTxPower(4); // Check bluefruit.h for supported values
  Bluefruit.setName(BLE_NAME);
  Bluefruit.Periph.setConnectCallback(bleConnectCallback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);

  // Configure and Start Device Information Service
  bledis.setManufacturer("Ace Centre");
  bledis.setModel("RelayKeysv1");
  bledis.begin();

  // Configure and Start BLE Uart Service
  bleuart.begin();
  bleuart.setRxCallback(prph_bleuart_rx_callback);

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

  //
  load_devList_fromFile();
}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);

  // Include BLE UART service
  //Bluefruit.Advertising.addService(bleuart);
  
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
  Bluefruit.Advertising.setInterval(32, 244); // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);   // number of seconds in fast mode
  Bluefruit.Advertising.start(0);             // 0 = Don't stop advertising after n seconds

  #ifdef DEBUG
  Serial.println("RelayKeys UP & Running");
  #endif
}

typedef void (*action_func_t)(char *myLine);

typedef struct
{
  char command[32 + 1]; // max 32 characters plus '\0' terminator
  action_func_t action;
} command_action_t;

// force lower case
void toLower(char *s)
{
  while (*s)
  {
    if (isupper(*s))
    {
      *s += 0x20;
    }
    s++;
  }
}

void deleteDevList(char *myLine)
{
  at_response("at+deletedevlist\n");
  
  InternalFS.remove(FILENAME);
  bleDeviceNameListIndex = 0;
  memset(bleDeviceNameList, 0, sizeof(bleDeviceNameList));

  BLEConnection *connection = NULL;
  for(int i=0;i<max_prph_connection;i++) {
    connection = Bluefruit.Connection(i);
    connection->disconnect();
  }
  
  at_response("SUCCESS.\n");
}

void sendBLEMouseMove(char *line)
{
  char buff[256];
  err_t ret = 1;
  int32_t x = 0;
  int32_t y = 0;
  int32_t wy = 0;
  int32_t wx = 0;
  // expected input, X,Y,WY,WX
  char *p = strtok(line, "=");
  p = strtok(NULL, ",");
  for (size_t i = 0; p != NULL; i++)
  {
    if (i == 0)
    { // X
      x = strtol(p, NULL, 10);
    }
    else if (i == 1)
    { // Y
      y = strtol(p, NULL, 10);
    }
    else if (i == 2)
    {
      wy = strtol(p, NULL, 10);
    }
    else if (i == 3)
    {
      wx = strtol(p, NULL, 10);
    }
    else
    {
      // Invalid input
      at_response("INVALID_INPUT\n");
      return;
    }
    p = strtok(NULL, ",");
  }
  if (x != 0 || y != 0)
  {
    ret = blehid.mouseMove(target_ble_conn, x, y);
  }
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
    at_response(buff);
  }
  else
  {
    if (wy != 0)
    {
      ret = blehid.mouseScroll(target_ble_conn, wy);
    }
    if ((int)ret != 1)
    {
      snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
      at_response(buff);
      return;
    }
    if (wx != 0)
    {
      ret = blehid.mousePan(target_ble_conn, wx);
    }
    if ((int)ret != 1)
    {
      snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
      at_response(buff);
      return;
    }
    at_response("OK\n");
  }
}

typedef struct
{
  char thechar;
  uint8_t button;
} mouse_button_map_t;

const mouse_button_map_t mouse_buttons_map[] = {
    {'l', MOUSE_BUTTON_LEFT},
    {'r', MOUSE_BUTTON_RIGHT},
    {'m', MOUSE_BUTTON_MIDDLE},
    {'b', MOUSE_BUTTON_BACKWARD},
    {'f', MOUSE_BUTTON_FORWARD},
    {'0', 0},
};

void sendBLEMouseButton(char *line)
{
  char buff[256];
  err_t ret;
  int b = 0;
  int mode = 0;
  // expected input, Button[,Action]
  char *p = strtok(line, "=");
  p = strtok(NULL, ",");
  for (size_t i = 0; p != NULL; i++)
  {
    if (i == 0)
    { // Button
      for (int c = 0; c < sizeof(mouse_buttons_map) / sizeof(mouse_buttons_map[0]);
           c++)
      {
        if (mouse_buttons_map[c].thechar == p[0])
        {
          b = mouse_buttons_map[c].button;
          break;
        }
      }
    }
    else if (i == 1)
    { // Action
      toLower(p);
      if (strcmp(p, "click") == 0)
      {
        mode = 1;
      }
      else if (strcmp(p, "doubleclick") == 0)
      {
        mode = 2;
      }
      // PRESS/HOLD and no action all are PRESS action
    }
    else
    {
      // Invalid input
      at_response("INVALID_INPUT\n");
      return;
    }
    p = strtok(NULL, ",");
  }
  if (b != 0 && mode == 1)
  { // CLICK
    ret = blehid.mouseButtonPress(target_ble_conn, b);
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(target_ble_conn);
    }
  }
  else if (b != 0 && mode == 2)
  { // DOUBLECLICK
    ret = blehid.mouseButtonPress(target_ble_conn, b);
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(target_ble_conn);
    }
    if (ret == 1)
    {
      ret = blehid.mouseButtonPress(target_ble_conn, b);
    }
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(target_ble_conn);
    }
  }
  else
  { // PRESS/RELEASE
    if (b == 0)
    {
      ret = blehid.mouseButtonRelease(target_ble_conn);
    }
    else
    {
      ret = blehid.mouseButtonPress(target_ble_conn, b);
    }
  }
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
    at_response(buff);
  }
  else
  {
    at_response("OK\n");
  }
}

void sendBLEKeyboardCode(char *myLine)
{
  char buff[256];
  err_t ret;
  uint8_t keys[8]; // USB keyboard HID report

  memset(keys, 0, sizeof(keys));

  // myLine example: "00-00-04-00-00-00-00-00"
  char *p = strtok(myLine, "=");
  p = strtok(NULL, "-");
  for (size_t i = 0; p && (i < sizeof(keys)); i++)
  {
    keys[i] = strtoul(p, NULL, 16);
    p = strtok(NULL, "-");
  }
  ret = blehid.keyboardReport(target_ble_conn, keys[0], &keys[2]);
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d\n", (int)ret);
    at_response(buff);
  }
  else
  {
    at_response("OK\n");
  }
}

void sendBleSendCurrentDeviceName(char *myLine)
{
  char buff[256];
  at_response("at+blecurrentdevicename\n");
  if (!Bluefruit.connected())
  {
    at_response("NONE\n");
  }
  else
  {
    BLEConnection *connection = NULL;
    char bleDeviceName[32] = {0};

    connection = Bluefruit.Connection(target_ble_conn);
    connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));
        if (strlen(bleDeviceName) == 0)
    {
      at_response("NONE\n");
    }else {
      snprintf(buff, sizeof(buff), "%s\n", bleDeviceName);
      at_response(buff);
    } 
  }
}

void addNewBleDevice(char *myLine)
{
  char buff[256];
  at_response("at+bleaddnewdevice\n");

  if (bleDeviceNameListIndex >= maxBleDevListSize)
  {
    at_response("ERROR: Device list is full\n");
  }
  else
  {
    BLEConnection *connection = NULL;
    char bleDeviceName[32] = {0};

    connection = Bluefruit.Connection(target_ble_conn);
    connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

    delay(500);
    connection->disconnect();
    //Serial.println("Disconnected from " + String(bleDeviceName));

    flag_addDevProsStarted = 1;
    addDevProsStartTicks = millis();

    snprintf(buff, sizeof(buff), "Connect your device with %s\n", BLE_NAME);
    at_response(buff);  
  }
}

void removeBleDevice(char *myLine)
{
  at_response("at+bleremovedevice\n");
  char tempName[32] = {0};
  char tempNameIndex = 0;
  char flag_start = 0;
  char i = 0;
  BLEConnection *connection = NULL;
  char bleDeviceName[32] = {0};
  char centralBleDeviceName[32] = {0};
  
  if (strlen(myLine) == 0)
  {
    at_response("ERROR: Syntax\n");
    return;
  }

  connection = Bluefruit.Connection(target_ble_conn);
  connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

  for (char i = 0; i < strlen(myLine); i++)
  {
    if (myLine[i] == '"')
    {
      flag_start = 1;
    }
    else
    {
      if (flag_start)
      {
        if (myLine[i] == '"')
        {
          flag_start = 0;
          break;
        }
        else
        {
          tempName[tempNameIndex++] = myLine[i];
        }
      }
    }
  }

  if (strlen(tempName) == 0)
  {
    at_response("ERROR: Syntax\n");
    return;
  }

  //Serial.println("Remove Device: " + String(tempName));

  if (!strcmp((char *)tempName, (char *)bleDeviceName))
  {
    connection->disconnect();
  }

  if(ble_mode) {    
    connection = Bluefruit.Connection(response_ble_conn);
    connection->getPeerName(centralBleDeviceName, sizeof(centralBleDeviceName));
    if (!strcmp((char *)tempName, (char *)centralBleDeviceName))
    {
      at_response("ERROR: Can't remove central device\n");
      return;
    }
  }

  flag_start = 0;

  for (i = 0; i < maxBleDevListSize; i++)
  {
    if (!strcmp((char *)tempName, (char *)bleDeviceNameList[i]))
    {
      //Serial.println("Device found in list - " + String(tempName));
      at_response("SUCCESS\n");
      flag_start = 1;
      bleDeviceNameListIndex--;
      flag_saveListToFile = true;
    }
    if (flag_start)
    {
      if (i < (maxBleDevListSize - 1))
      {
        memset(bleDeviceNameList[i], NULL, sizeof(bleDeviceNameList[i]));
        strcpy(bleDeviceNameList[i], bleDeviceNameList[i + 1]);
      }
      else
      {
        memset(bleDeviceNameList[maxBleDevListSize - 1], NULL, sizeof(bleDeviceNameList[maxBleDevListSize - 1]));
      }
    }
  }

  if (!flag_start)
  {
    at_response("ERROR: Name not found in the list\n");
  }
}

void switchBleConnection(char *myLine)
{
  char buff[256];
  
  at_response("at+switchconn\n");

  if (!Bluefruit.connected())
  {
    switchBleConnStartIndex = 1;
    //Serial.println("Current Dev Index: " + String(switchBleConnStartIndex));
    switchBleConnCurrIndex = 1;
    flag_bleSwapConnProsStarted = 1;
    swapConnProsStartTicks = millis();
    
    snprintf(buff, sizeof(buff), "Trying to connect with -  %s\n", bleDeviceNameList[switchBleConnCurrIndex - 1]);
    at_response(buff);
  }
  else
  {
    BLEConnection *connection = NULL;
    char tempBleDevName[32] = {0};

    connection = Bluefruit.Connection(target_ble_conn);
    connection->getPeerName(tempBleDevName, sizeof(tempBleDevName));

    //Serial.println("Current Dev Name: " + String(tempBleDevName));

    for (char i = 0; i < maxBleDevListSize; i++)
    {
      if (!strcmp((char *)tempBleDevName, (char *)bleDeviceNameList[i]))
      {
        switchBleConnStartIndex = i + 1;
        //Serial.println("Current Dev Index: " + String(switchBleConnStartIndex));

        if (bleDeviceNameListIndex == 1)
        {          
          at_response("ERROR: No other device present in list\n");
          break;
        }
        else
        {
          connection->disconnect();
        }

        if (switchBleConnStartIndex >= bleDeviceNameListIndex)
        {
          switchBleConnCurrIndex = 1;
        }
        else
        {
          switchBleConnCurrIndex = switchBleConnStartIndex + 1;
        }

        flag_bleSwapConnProsStarted = 1;
        swapConnProsStartTicks = millis();        
        
        snprintf(buff, sizeof(buff), "Trying to connect with -  %s\n", bleDeviceNameList[switchBleConnCurrIndex - 1]);
        at_response(buff);
        break;
      }
    }
  }
}

void printBleDevList(char *myLine)
{
  char buff[256];
  at_response("at+printdevlist\n");
  for (char j = 0; j < bleDeviceNameListIndex; j++)
  {
    snprintf(buff, sizeof(buff), "%d:%s\n", (j+1), bleDeviceNameList[j]);
    at_response(buff);
  }
  //Serial.println("Index:" + String(bleDeviceNameListIndex));
}

void setBleMaxDevListSize(char *myLine)
{
  at_response("at+blemaxdevlistsize\n");
  
  char *p = strtok(myLine, "=");
  p = strtok(NULL, "\0"); 
  uint8_t tempNum = atoi(p);  
  if (tempNum > 15 || tempNum < 1)
  {
    maxBleDevListSize = 3;
    at_response("ERROR: Invalid Value\n");
  }
  else
  {
    maxBleDevListSize = tempNum;
    at_response("SUCCESS\n");
  }
}

const command_action_t commands[] = {
    // Name of command user types, function that implements the command.
    // TODO add other commands, some day
    {"at+blekeyboardcode", sendBLEKeyboardCode},
    {"at+blehidmousemove", sendBLEMouseMove},
    {"at+blehidmousebutton", sendBLEMouseButton},
    {"at+blecurrentdevicename", sendBleSendCurrentDeviceName},
    {"at+bleaddnewdevice", addNewBleDevice},
    {"at+bleremovedevice", removeBleDevice},
    {"at+switchconn", switchBleConnection},
    {"at+printdevlist", printBleDevList},
    {"at+blemaxdevlistsize", setBleMaxDevListSize},
    {"at+resetdevlist", deleteDevList}
};

void update_connections(uint16_t conn_handle){
    target_ble_conn = 1;
    response_ble_conn = 0;
    if(connection_count == 2 && conn_handle == 1) {
      target_ble_conn = 0;      
      response_ble_conn = 1;
    }
}

void execute(uint16_t conn_handle, char *myLine)
{
  if (myLine == NULL || *myLine == '\0')
    return;

  char cmdTemp[100];
  
  memcpy(cmdTemp, myLine, 100);
  
  char *cmd = strtok(cmdTemp, "=");
  
  if (cmd == NULL || *cmd == '\0')
    return;

  toLower(cmd);
  
  for (size_t i = 0; i < sizeof(commands) / sizeof(commands[0]); i++)
  {
    if (strcmp(cmd, commands[i].command) == 0)
    {      
      if(ble_mode) {
        update_connections(conn_handle);
      }
      commands[i].action(myLine); //strtok(NULL, "=")
      if(!ble_mode) {
        delay(30);
      }
      return;
    }
  }

  // Command not found so just send OK. Should send ERROR at some point.
  at_response("OK\n");
}

void receive_char(uint16_t conn_handle, char receive_char)
{
  static uint8_t bytesIn;
  static char receive_buffer[256];

      switch (receive_char)
    {
    case '\n':      
      break;
    case '\r':     
      receive_buffer[bytesIn] = '\0';
      execute(conn_handle, receive_buffer);
      bytesIn = 0;
    case '\b': // backspace
      if (bytesIn > 0)
      {
        bytesIn--;
      }
      break;
    default:      
      receive_buffer[bytesIn++] = receive_char;
      if (bytesIn >= sizeof(receive_buffer) - 1)
      {
        receive_buffer[bytesIn] = '\0';
        execute(conn_handle, receive_buffer);
        bytesIn = 0;
      }
      break;
    }    
}

void at_response(char *msg) {
  int len = strlen(msg);

  if(ble_mode) {
    bleuart.write(response_ble_conn, (const uint8_t*)msg, len);    
  } else {
    Serial.write(msg, len);
  }
}

void prph_bleuart_rx_callback(uint16_t conn_handle)
{  
  if(ble_mode) {  
    while (bleuart.available())
    {
      receive_char(conn_handle, bleuart.read());
    }
  }
}

void loop()
{

  if(!ble_mode) {    
    if(Serial.available() > 0) {
      receive_char(0, Serial.read());
    }    
  }

  if(digitalRead(USER_SW) == false) {    
    if(detect_click() == 1){      
      addNewBleDevice("");
    } else {
      change_mode();
    }
  }

  if (flag_saveListToFile)
  {
    flag_saveListToFile = false;
    save_devList_toFile();
  }

  if (flag_addDevProsStarted)
  {
    if (millis() - addDevProsStartTicks >= ADD_NEW_DEV_PROCESS_TIMEOUT)
    {
      flag_addDevProsStarted = 0;
      
      #ifdef DEBUG
      Serial.println("ERROR: Timeout");
      #endif
    }
  }

  if (flag_bleSwapConnProsStarted == 1)
  {
    if (millis() - swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT)
    {
      #ifdef DEBUG
      Serial.println("ERROR: Timeout");
      #endif

      switchBleConnCurrIndex++;
      if (switchBleConnCurrIndex > bleDeviceNameListIndex)
      {
        switchBleConnCurrIndex = 1;
      }
      if (switchBleConnCurrIndex == switchBleConnStartIndex)
      {
        flag_bleSwapConnProsStarted = 2;
      }

      swapConnProsStartTicks = millis();

      #ifdef DEBUG
      Serial.println("Trying to connect with - " + String(bleDeviceNameList[switchBleConnCurrIndex - 1]));
      #endif
    }
  }
  else if (flag_bleSwapConnProsStarted == 2)
  {
    if (millis() - swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT)
    {
      flag_bleSwapConnProsStarted = 0;

      #ifdef DEBUG
      Serial.println("ERROR: Timeout");
      #endif
    }
  }

  // Request CPU to enter low-power mode until an event/interrupt occurs
  waitForEvent();
}

void bleConnectCallback(uint16_t conn_handle)
{
  static int i;
  uint16_t connectionHandle = 0;
  BLEConnection *connection = NULL;
  char central_name[32] = {0};
  uint8_t timeout_counter = 10;
  
  connection = Bluefruit.Connection(conn_handle);
  connection->getPeerName(central_name, sizeof(central_name));
  
  // when unpaired iPhone connects wait in while until it will pair and give its full device name
  while(!strcmp((char *)central_name, "iPhone")){
    if(connection->connected() && timeout_counter > 0) {
      delay(1000);
      connection->getPeerName(central_name, sizeof(central_name));
      timeout_counter--;            
    } else {
      connection->disconnect();
      return;
    }    
  }
    
  connection_count++;

  if (flag_bleSwapConnProsStarted == 1)
  {
    if (!strcmp((char *)central_name, (char *)bleDeviceNameList[switchBleConnCurrIndex - 1]))
    {
      flag_bleSwapConnProsStarted = 0;

      #ifdef DEBUG
      Serial.println("SUCCESS");
      #endif
    }
    else
    {
      connection->disconnect();

      #ifdef DEBUG
      Serial.print("Disconnected - Other device: ");
      Serial.println(central_name);
      #endif
    }
  }
  else if (flag_bleSwapConnProsStarted == 2)
  {
    if (!strcmp((char *)central_name, (char *)bleDeviceNameList[switchBleConnStartIndex - 1]))
    {
      flag_bleSwapConnProsStarted = 0;
      
      #ifdef DEBUG
      Serial.print("Reconnected to last device: ");
      Serial.println(central_name);
      #endif
    }
    else
    {
      connection->disconnect();

      #ifdef DEBUG
      Serial.println("Disconnected - Other device: ");
      Serial.println(central_name);
      #endif
    }
  }
  else
  {
    i = 0;

    for (i = 0; i < maxBleDevListSize; i++)
    {
      if (!strcmp((char *)central_name, (char *)bleDeviceNameList[i]))
      {
        #ifdef DEBUG
        Serial.println("Device found in list - " + String(central_name));
        #endif
        
        if (flag_addDevProsStarted)
        {
          connection->disconnect();

          #ifdef DEBUG
          Serial.print("Disconnected - Device already present in list");
          Serial.println(central_name);
          #endif
        }
        else
        {
        }
        break;
      }
    }

    if (i >= maxBleDevListSize)
    {
      if (flag_addDevProsStarted)
      {
        flag_addDevProsStarted = 0;
        if (bleDeviceNameListIndex > maxBleDevListSize)
        {
          connection->disconnect();

          #ifdef DEBUG
          Serial.println("ERROR: Device list is full");
          #endif
        }
        else
        {
          #ifdef DEBUG
          Serial.println("SUCCESS");
          Serial.println(String(central_name) + " Connected and Name added into list");
          #endif
          
          strcpy(bleDeviceNameList[bleDeviceNameListIndex++], central_name);
          flag_saveListToFile = true;
        }
      }
      else
      {
        connection->disconnect();

        #ifdef DEBUG
        Serial.println(String(central_name) + " Disconnected - Not present in the list");
        #endif
      }
    }
  }
  
  // Keep advertising if not reaching max
  if (connection_count < max_prph_connection)
  {
    //Serial.println("Keep advertising");
    Bluefruit.Advertising.start(0);
  }
  
}

void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  //Serial.println();
  //Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);

  connection_count--;
  // Keep advertising if not reaching max
  if (connection_count < max_prph_connection)
  {
    //Serial.println("Keep advertising");
    Bluefruit.Advertising.start(0);
  }
}

/**
 * Callback invoked when received Set LED from central.
 * Must be set previously with setKeyboardLedCallback()
 *
 * The LED bit map is as follows: (also defined by KEYBOARD_LED_* )
 *    Kana (4) | Compose (3) | ScrollLock (2) | CapsLock (1) | Numlock (0)
 */
void set_keyboard_led(uint16_t conn_handle, uint8_t led_bitmap)
{
  // light up Red Led if any bits is set
  if (led_bitmap)
  {
    ledOn(LED_RED);
  }
  else
  {
    ledOff(LED_RED);
  }
}
