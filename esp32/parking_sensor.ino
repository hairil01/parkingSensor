#include <WiFi.h>
#include <HTTPClient.h>
#include <NewPing.h>

// Replace with your Wi-Fi credentials
const char* ssid = "D-03-07";
const char* password = "fxlfmoQe";

// Flask server URL (use local IP if testing locally)
const char* serverUrl = "http://192.168.100.13:5000/api/sensors";  // Replace with your Flask IP

#define TRIGGER_PIN_1 32
#define ECHO_PIN_1    33
#define TRIGGER_PIN_2 25
#define ECHO_PIN_2    26
#define MAX_DISTANCE  100 // Max distance in cm

NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned int distance1 = sonar1.ping_cm();
  unsigned int distance2 = sonar2.ping_cm();

  bool occupied1 = distance1 > 0 && distance1 < 10;
  bool occupied2 = distance2 > 0 && distance2 < 10;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{";
    jsonData += "\"sensor1\": {\"distance\": \"" + String(distance1) + " cm\", \"occupied\": " + (occupied1 ? "true" : "false") + "},";
    jsonData += "\"sensor2\": {\"distance\": \"" + String(distance2) + " cm\", \"occupied\": " + (occupied2 ? "true" : "false") + "}";
    jsonData += "}";

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("POST Success, code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("POST Failed, error: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }

  delay(3000);  // Delay between readings
}
