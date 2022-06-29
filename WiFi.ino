#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

ESP8266WebServer server(80);

char mystr[10];
String message;

void setup(void) {
  delay(1000);
  Serial.begin(115200);
  Serial.println("setup");

  pinMode(0,OUTPUT);
  pinMode(2,INPUT);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin("D-Link GO-DSL-AC750", "4r5t6y7u");
  //WiFi.begin("HUAWEI P8 lite 2017", "11111111");
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }
  //http://192.168.1.3/KEYWORD
  
  server.on("/on", alarm_on);
  server.on("/off", alarm_off);
  server.on("/stop", stop_sound);
  server.on("/log", logs);
  server.begin();  
}

void loop(void) {
  server.handleClient();
  MDNS.update();
  delay(100);
}

void alarm_on(){
  digitalWrite(0,LOW);
  server.send(200, "text/html", "led acceso");
  }

void alarm_off(){
  digitalWrite(0,HIGH);
  server.send(200, "text/plain", "alarm off");
  }

void stop_sound(){
  digitalWrite(0,HIGH);
  delay(1000);
  digitalWrite(0,LOW);
  server.send(200, "text/html", "Stop");
  }

void logs(){
  int input=analogRead(2);
  server.send(200, "text/html", String(input));
  }
