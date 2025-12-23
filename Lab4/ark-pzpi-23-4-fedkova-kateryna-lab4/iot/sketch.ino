#include <WiFi.h>
#include <HTTPClient.h>
#include <Preferences.h>
#include <ArduinoJson.h>

#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASS ""

#define SERVER_URL "https://ark-pzpi-23-4-fedkova-kateryna-lab4.onrender.com/api"

#define DEVICE_TITLE "ESP32-coffee-01"
#define ORG_ID 1
#define SENSOR_TYPE_LEVEL 1

#define PIN_TEMP  34
#define PIN_WATER 35
#define PIN_MILK  32
#define PIN_BEANS 33

#define MIN_VALUE 0.0
#define MAX_VALUE 100.0

Preferences prefs;
int deviceId = -1;

struct SensorConfig {
  const char* name;
  int pin;
  const char* sensorIdPref;
  float minValue;
  float maxValue;
  float criticalLow;
};

SensorConfig sensors[] = {
  { "Water", PIN_WATER, "sensor_water", 0, 100, 5 },
  { "Milk",  PIN_MILK,  "sensor_milk", 0, 100, 5 },
  { "Beans", PIN_BEANS, "sensor_beans", 0, 100, 5 },
  { "Temp",  PIN_TEMP,  "sensor_temp", 0, 100, -1 }
};

const int SENSOR_COUNT = sizeof(sensors) / sizeof(SensorConfig);

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void registerDevice() {
  if (deviceId != -1) {
    Serial.println("Device already registered");
    return;
  }

  HTTPClient http;
  http.begin(String(SERVER_URL) + "/devices/");
  http.addHeader("Content-Type", "application/json");

  String body = "{";
  body += "\"title\":\"" DEVICE_TITLE "\",";
  body += "\"organisation\":" + String(ORG_ID);
  body += "}";

  int code = http.POST(body);

  Serial.print("HTTP response code: ");
  Serial.println(code);

  String response = http.getString();
  Serial.print("Server response: ");
  Serial.println(response);

  if (code == 201) {
    DynamicJsonDocument doc(512);
    deserializeJson(doc, response);

    deviceId = doc["device_id"];
    prefs.putInt("device_id", deviceId);

    Serial.print("Registered with device_id = ");
    Serial.println(deviceId);
  }

  http.end();
}

int registerSensor(const char* title, int sensorType) {
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/sensors/");
  http.addHeader("Content-Type", "application/json");

  String payload = "{";
  payload += "\"title\":\"" + String(title) + "\",";
  payload += "\"unit\":\"%\",";
  payload += "\"min_value\":" + String(MIN_VALUE) + ",";
  payload += "\"max_value\":" + String(MAX_VALUE) + ",";
  payload += "\"device\":" + String(deviceId) + ",";
  payload += "\"sensor_type\":" + String(sensorType) + ",";
  payload += "\"organisation\":" + String(ORG_ID);
  payload += "}";

  int code = http.POST(payload);
  int sensorId = -1;

  Serial.print("HTTP code: ");
  Serial.println(code);

  String resp = http.getString();
  Serial.print("Server response: ");
  Serial.println(resp);

  if (code == 201) {
    StaticJsonDocument<128> doc;
    deserializeJson(doc, resp);
    sensorId = doc["sensor_id"];
    http.end();
    return sensorId;
  }

  http.end();
  return sensorId;
}

void registerAllSensors() {
  int successCount = 0;

  int waterId = registerSensor("Water level", SENSOR_TYPE_LEVEL);
  if (waterId > 0) {
    prefs.putInt("sensor_water", waterId);
    successCount++;
  }
  
  int milkId  = registerSensor("Milk level", SENSOR_TYPE_LEVEL);
  if (milkId > 0) {
    prefs.putInt("sensor_milk", milkId);
    successCount++;
  }
  
  int beansId = registerSensor("Beans level", SENSOR_TYPE_LEVEL);
  if (beansId > 0) {
    prefs.putInt("sensor_beans", beansId);
    successCount++;
  }

  int tempId  = registerSensor("Temperature", SENSOR_TYPE_LEVEL);
  if (tempId > 0) {
    prefs.putInt("sensor_temp", tempId);
    successCount++;
  }

  prefs.putInt("sensor_count", successCount);
  if (successCount == 4) {
    prefs.putBool("sensors_registered", true);
  } else {
    prefs.putBool("sensors_registered", false);
  }
}

void sendStatus() {
  if (deviceId == -1) return;

  HTTPClient http;
  http.begin(String(SERVER_URL) + "/devices/");
  http.addHeader("Content-Type", "application/json");

  String body = "{";
  body += "\"device_id\":" + String(deviceId);
  body += "}";

  http.POST(body);
  http.end();

  Serial.println("Status sent: online");
}

bool sendDeviceLog(int sensorId, float value) {
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/device-logs/");
  http.addHeader("Content-Type", "application/json");

  String payload = "{";
  payload += "\"value\":" + String(round(value)) + ",";
  payload += "\"sensor\":" + String(sensorId) + ",";
  payload += "\"organisation\":" + String(ORG_ID);
  payload += "}";

  int code = http.POST(payload);
  String response = http.getString();
  Serial.println(code);
  Serial.print("Response: ");
  Serial.println(response);

  if (code == 200 || code == 201) {
    http.end();
    return true;
  }

  Serial.print("Log send failed, code: ");
  Serial.println(code);
  http.end();
  return false;
}

float readSensorValue(int pin, float maxValue) {
  int raw = analogRead(pin);
  if (raw < 0 || raw > 4095) return NAN;
  return raw * maxValue / 4095.0;
}

void checkAndSendEvent(int idx, float value) {
  SensorConfig& s = sensors[idx];

  if (s.criticalLow >= 0 && value < s.criticalLow) {
    sendEvent(String("WARNING! ") + s.name + " level is too low");
  }

  if (value > s.maxValue) {
    sendEvent(String("WARNING! ") + s.name + " level is too high");
  }
}

void processSensors() {
  for (int i = 0; i < SENSOR_COUNT; i++) {
    SensorConfig& s = sensors[i];

    float value = readSensorValue(s.pin, s.maxValue);
    if (!validValue(value, s.minValue, s.maxValue)) {
      sendEvent(String("Invalid value from ") + s.name + " sensor");
      continue;
    }

    sendDeviceLog(prefs.getInt(s.sensorIdPref), value);
    checkAndSendEvent(i, value);

    Serial.print(s.name);
    Serial.print(": ");
    Serial.println(value);
  }
}

bool validValue(float v, float minV, float maxV) {
  return !isnan(v) && v >= minV && v <= maxV;
}

bool sendEvent(const String& message) {
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/events/");
  http.addHeader("Content-Type", "application/json");

  String payload = "{";
  payload += "\"message\":\"" + message + "\",";
  payload += "\"device\":" + String(deviceId) + ",";
  payload += "\"organisation\":" + String(ORG_ID);
  payload += "}";

  int code = http.POST(payload);
  String response = http.getString();
  Serial.println(code);
  Serial.print("Response: ");
  Serial.println(response);

  if (code == 200 || code == 201) {
    http.end();
    return true;
  }

  http.end();
  return false;
}

void setup() {
  Serial.begin(115200);

  prefs.begin("iot", false);
  deviceId = prefs.getInt("device_id", -1);
  
  connectWiFi();
  registerDevice();

  deviceId = prefs.getInt("device_id", -1);

  if (!prefs.getBool("sensors_registered", false) || prefs.getInt("sensor_count", 0) != 4) {
    registerAllSensors();
  }
}

void loop() {
  sendStatus();
  processSensors();
  delay(10000);
}