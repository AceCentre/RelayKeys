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

#define BLE_NAME "RelayKeys"
#define ADD_NEW_DEV_PROCESS_TIMEOUT 30000 // in millseconds
#define SWAP_CONN_PROCESS_TIMEOUT 30000   // in millseconds

BLEDis bledis;
BLEHidAdafruit blehid;

volatile uint32_t addDevProsStartTicks = 0;
volatile uint8_t flag_addDevProsStarted = 0;
char bleDeviceNameList[15][32] = {0};
volatile uint8_t bleDeviceNameListIndex = 0;
volatile uint8_t flag_bleSwapConnProsStarted = 0;
volatile uint32_t swapConnProsStartTicks = 0;
volatile uint8_t maxBleDevListSize = 3;
volatile uint8_t switchBleConnStartIndex = 0;
volatile uint8_t switchBleConnCurrIndex = 0;

#define DEFAULT_CONN_HANDLE BLE_CONN_HANDLE_INVALID

///
using namespace Adafruit_LittleFS_Namespace;
#define FILENAME "/devNameList.txt"
File file(InternalFS);
volatile bool flag_saveListToFile = false;
///

void set_keyboard_led(uint8_t led_bitmap);

void save_devList_toFile(void)
{
  file.open(FILENAME, FILE_O_WRITE);

  // file existed
  if (file)
  {

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

    // file.truncate(file.size());
    file.seek(0);
    file.write((const uint8_t *)bleDeviceNameList, sizeof(bleDeviceNameList));
    file.write((const uint8_t *)&bleDeviceNameListIndex, 1);

    Serial.print("Saving Device List to file ");
    Serial.print(file.size());
    Serial.println();
    file.close();
  }
  else
  {
    Serial.print(FILENAME " Write Failed");
  }
}

void load_devList_fromFile(void)
{
  file.open(FILENAME, FILE_O_READ);

  // file existed
  if (file)
  {
    Serial.print("Loading Device List from file ");
    Serial.print(file.size());
    Serial.println();

    bleDeviceNameListIndex = 0;
    memset(bleDeviceNameList, 0, sizeof(bleDeviceNameList));

    file.read((void *)bleDeviceNameList, sizeof(bleDeviceNameList));
    file.read((void *)&bleDeviceNameListIndex, 1);

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
    file.close();
  }
  else
  {
    Serial.print(FILENAME " Read Failed");
  }
}

void setup()
{
  Serial.begin(115200);
  //while ( !Serial && millis() < 2000) delay(10);   // for nrf52840 with native usb

  Bluefruit.begin();
  Bluefruit.setTxPower(4); // Check bluefruit.h for supported values
  Bluefruit.setName(BLE_NAME);
  Bluefruit.Periph.setConnectCallback(bleConnectCallback);

  // Configure and Start Device Information Service
  bledis.setManufacturer("Ace Centre");
  bledis.setModel("RelayKeysv1");
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

  //
  load_devList_fromFile();
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
  Bluefruit.Advertising.setInterval(32, 244); // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);   // number of seconds in fast mode
  Bluefruit.Advertising.start(0);             // 0 = Don't stop advertising after n seconds

  Serial.println("RelayKeys UP & Running");
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

void sendBLEMouseMove(char *line)
{
  char buff[256];
  err_t ret = 1;
  int32_t x = 0;
  int32_t y = 0;
  int32_t wy = 0;
  int32_t wx = 0;
  // expected input, X,Y,WY,WX
  char *p = strtok(line, ",");
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
      Serial.println("INVALID_INPUT");
      return;
    }
    p = strtok(NULL, ",");
  }
  if (x != 0 || y != 0)
  {
    ret = blehid.mouseMove(DEFAULT_CONN_HANDLE, x, y);
  }
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d", (int)ret);
    Serial.println(buff);
  }
  else
  {
    if (wy != 0)
    {
      ret = blehid.mouseScroll(DEFAULT_CONN_HANDLE, wy);
    }
    if ((int)ret != 1)
    {
      snprintf(buff, sizeof(buff), "ERROR %d", (int)ret);
      Serial.println(buff);
      return;
    }
    if (wx != 0)
    {
      ret = blehid.mousePan(DEFAULT_CONN_HANDLE, wx);
    }
    if ((int)ret != 1)
    {
      snprintf(buff, sizeof(buff), "ERROR %d", (int)ret);
      Serial.println(buff);
      return;
    }
    Serial.println("OK");
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
  char *p = strtok(line, ",");
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
      if (strcmp(p, "click"))
      {
        mode = 1;
      }
      else if (strcmp(p, "doubleclick"))
      {
        mode = 2;
      }
      // PRESS/HOLD and no action all are PRESS action
    }
    else
    {
      // Invalid input
      Serial.println("INVALID_INPUT");
      return;
    }
    p = strtok(NULL, ",");
  }
  if (b != 0 && mode == 1)
  { // CLICK
    ret = blehid.mouseButtonPress(DEFAULT_CONN_HANDLE, b);
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(DEFAULT_CONN_HANDLE);
    }
  }
  else if (b != 0 && mode == 2)
  { // DOUBLECLICK
    ret = blehid.mouseButtonPress(DEFAULT_CONN_HANDLE, b);
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(DEFAULT_CONN_HANDLE);
    }
    if (ret == 1)
    {
      ret = blehid.mouseButtonPress(DEFAULT_CONN_HANDLE, b);
    }
    if (ret == 1)
    {
      delay(40);
      ret = blehid.mouseButtonRelease(DEFAULT_CONN_HANDLE);
    }
  }
  else
  { // PRESS/RELEASE
    if (b == 0)
    {
      ret = blehid.mouseButtonRelease(DEFAULT_CONN_HANDLE);
    }
    else
    {
      ret = blehid.mouseButtonPress(DEFAULT_CONN_HANDLE, b);
    }
  }
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d", (int)ret);
    Serial.println(buff);
  }
  else
  {
    Serial.println("OK");
  }
}

void sendBLEKeyboardCode(char *myLine)
{
  char buff[256];
  err_t ret;
  uint8_t keys[8]; // USB keyboard HID report

  memset(keys, 0, sizeof(keys));
  // myLine example: "00-00-04-00-00-00-00-00"
  char *p = strtok(myLine, "-");
  for (size_t i = 0; p && (i < sizeof(keys)); i++)
  {
    keys[i] = strtoul(p, NULL, 16);
    p = strtok(NULL, "-");
  }
  ret = blehid.keyboardReport(DEFAULT_CONN_HANDLE, keys[0], &keys[2]);
  if ((int)ret != 1)
  {
    snprintf(buff, sizeof(buff), "ERROR %d", (int)ret);
    Serial.println(buff);
  }
  else
  {
    Serial.println("OK");
  }
}

void sendBleSendCurrentDeviceName(char *myLine)
{
  Serial.println("at+blecurrentdevicename");
  if (!Bluefruit.connected())
  {
    Serial.println("NONE");
  }
  else
  {
    uint16_t connectionHandle = 0;
    BLEConnection *connection = NULL;
    char bleDeviceName[32] = {0};

    connectionHandle = Bluefruit.connHandle();
    connection = Bluefruit.Connection(connectionHandle);
    connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

    Serial.println(bleDeviceName);
  }
}

void addNewBleDevice(char *myLine)
{
  Serial.println("at+bleaddnewdevice");

  if (bleDeviceNameListIndex >= maxBleDevListSize)
  {
    Serial.println("ERROR: Device list is full");
  }
  else
  {
    uint16_t connectionHandle = 0;
    BLEConnection *connection = NULL;
    char bleDeviceName[32] = {0};

    connectionHandle = Bluefruit.connHandle();
    connection = Bluefruit.Connection(connectionHandle);
    connection->getPeerName(bleDeviceName, sizeof(bleDeviceName));

    delay(500);
    connection->disconnect();
    //Serial.println("Disconnected from " + String(bleDeviceName));

    flag_addDevProsStarted = 1;
    addDevProsStartTicks = millis();

    Serial.println("Connect your device with " + String(BLE_NAME));
  }
}

void removeBleDevice(char *myLine)
{
  Serial.println("at+bleremovedevice");
  char tempName[32] = {0};
  char tempNameIndex = 0;
  char flag_start = 0;
  char i = 0;
  uint16_t connectionHandle = 0;
  BLEConnection *connection = NULL;
  char bleDeviceName[32] = {0};

  if (strlen(myLine) == 0)
  {
    Serial.println("ERROR: Syntax");
    return;
  }

  connectionHandle = Bluefruit.connHandle();
  connection = Bluefruit.Connection(connectionHandle);
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
    Serial.println("ERROR: Syntax");
    return;
  }

  //Serial.println("Remove Device: " + String(tempName));

  if (!strcmp((char *)tempName, (char *)bleDeviceName))
  {
    connection->disconnect();
  }

  flag_start = 0;

  for (i = 0; i < maxBleDevListSize; i++)
  {
    if (!strcmp((char *)tempName, (char *)bleDeviceNameList[i]))
    {
      //Serial.println("Device found in list - " + String(tempName));
      Serial.println("SUCCESS");
      flag_start = 1;
      bleDeviceNameListIndex--;
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
    Serial.println("ERROR: Name not found in the list");
  }
}

void switchBleConnection(char *myLine)
{
  Serial.println("at+switchconn");

  if (!Bluefruit.connected())
  {
    switchBleConnStartIndex = 1;
    //Serial.println("Current Dev Index: " + String(switchBleConnStartIndex));
    switchBleConnCurrIndex = 1;
    flag_bleSwapConnProsStarted = 1;
    swapConnProsStartTicks = millis();
    Serial.println("Trying to connect with - " + String(bleDeviceNameList[switchBleConnCurrIndex - 1]));
  }
  else
  {
    uint16_t connectionHandle = 0;
    BLEConnection *connection = NULL;
    char tempBleDevName[32] = {0};

    connectionHandle = Bluefruit.connHandle();
    connection = Bluefruit.Connection(connectionHandle);
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
          Serial.println("ERROR: No other device present in list");
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
        Serial.println("Trying to connect with - " + String(bleDeviceNameList[switchBleConnCurrIndex - 1]));
        break;
      }
    }
  }
}

void printBleDevList(char *myLine)
{
  Serial.println("at+printdevlist");
  for (char j = 0; j < maxBleDevListSize; j++)
  {
    Serial.print(char(j + '1'));
    Serial.println(":" + String(bleDeviceNameList[j]));
  }
  //Serial.println("Index:" + String(bleDeviceNameListIndex));
}

void setBleMaxDevListSize(char *myLine)
{
  Serial.println("at+blemaxdevlistsize");

  uint8_t tempNum = atoi(myLine);
  if (tempNum > 15 || tempNum < 1)
  {
    maxBleDevListSize = 3;
    Serial.println("ERROR: Invalid Value");
  }
  else
  {
    maxBleDevListSize = tempNum;
    Serial.println("SUCCESS");
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
};

void execute(char *myLine)
{
  if (myLine == NULL || *myLine == '\0')
    return;
  char *cmd = strtok(myLine, "=");
  if (cmd == NULL || *cmd == '\0')
    return;
  toLower(cmd);
  for (size_t i = 0; i < sizeof(commands) / sizeof(commands[0]); i++)
  {
    if (strcmp(cmd, commands[i].command) == 0)
    {
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
  static char myLine[80 + 1];

  while (Serial.available() > 0)
  {
    int b = Serial.read();
    if (b != -1)
    {
      switch (b)
      {
      case '\n':
        break;
      case '\r':
        myLine[bytesIn] = '\0';
        execute(myLine);
        bytesIn = 0;
        break;
      case '\b': // backspace
        if (bytesIn > 0)
        {
          bytesIn--;
        }
        break;
      default:
        myLine[bytesIn++] = (char)b;
        if (bytesIn >= sizeof(myLine) - 1)
        {
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
      Serial.println("ERROR: Timeout");
    }
  }

  if (flag_bleSwapConnProsStarted == 1)
  {
    if (millis() - swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT)
    {
      Serial.println("ERROR: Timeout");

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
      Serial.println("Trying to connect with - " + String(bleDeviceNameList[switchBleConnCurrIndex - 1]));
    }
  }
  else if (flag_bleSwapConnProsStarted == 2)
  {
    if (millis() - swapConnProsStartTicks >= SWAP_CONN_PROCESS_TIMEOUT)
    {
      flag_bleSwapConnProsStarted = 0;
      Serial.println("ERROR: Timeout");
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

  connection = Bluefruit.Connection(conn_handle);
  connection->getPeerName(central_name, sizeof(central_name));

  if (flag_bleSwapConnProsStarted == 1)
  {
    if (!strcmp((char *)central_name, (char *)bleDeviceNameList[switchBleConnCurrIndex - 1]))
    {
      flag_bleSwapConnProsStarted = 0;
      Serial.println("SUCCESS");
    }
    else
    {
      connection->disconnect();
      //Serial.println("Disconnected - Other device");
    }
  }
  else if (flag_bleSwapConnProsStarted == 2)
  {
    if (!strcmp((char *)central_name, (char *)bleDeviceNameList[switchBleConnStartIndex - 1]))
    {
      flag_bleSwapConnProsStarted = 0;
      Serial.println("Reconnected to last device");
    }
    else
    {
      connection->disconnect();
      //Serial.println("Disconnected - Other device");
    }
  }
  else
  {
    i = 0;

    for (i = 0; i < maxBleDevListSize; i++)
    {
      if (!strcmp((char *)central_name, (char *)bleDeviceNameList[i]))
      {
        //Serial.println("Device found in list - " + String(central_name));
        if (flag_addDevProsStarted)
        {
          connection->disconnect();
          //Serial.println("Disconnected - Device already present in list");
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
          Serial.println("ERROR: Device list is full");
        }
        else
        {
          Serial.println("SUCCESS");
          //Serial.println(String(central_name) + " Connected and Name added into list");
          strcpy(bleDeviceNameList[bleDeviceNameListIndex++], central_name);
          flag_saveListToFile = true;
        }
      }
      else
      {
        connection->disconnect();
        //Serial.println(String(central_name) + " Disconnected - Not present in the list");
      }
    }
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
