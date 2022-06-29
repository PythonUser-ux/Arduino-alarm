#include <NewPing.h>
#define trigPin 12 // define TrigPin.
#define echoPin 11 // define EchoPin.
#define MAX_DISTANCE 300 // Maximum sensor distance is rated at 400-500cm.
#define LOWER_BOUND 5 // Alarm lower bound distance (cm).
#define UPPER_BOUND 88 // Alarm upper bound distance (cm).
NewPing sonar(trigPin, echoPin, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

bool alarm_on=true;
int sus=0;
void(* Riavvia)(void) = 0;
extern unsigned long timer0_millis;
void resetMillis() {
  cli();
  timer0_millis = 0;
  sei();
}

void setup() {
 pinMode(8, OUTPUT);
 pinMode(7,OUTPUT);
 pinMode(6, INPUT);
 pinMode(5,OUTPUT);
 Serial.begin(9600);
 Serial.println("Restart");
 digitalWrite(7,1);
 delay(2000);
 
}

void loop(){
    if (digitalRead(6) == LOW){alarm_on=true;}
    while (alarm_on){
    int sonar_int = sonar.ping_cm();
    //Serial.println(sonar_int);
    if (LOWER_BOUND<sonar_int && sonar_int<UPPER_BOUND){ //&& millis()>2000){
        int sus_time=millis();
        while ((millis()-sus_time)<500){
            delay(50);
            int sonar_int = sonar.ping_cm();
            //Serial.println(sonar_int);
            if (LOWER_BOUND<sonar_int && sonar_int<UPPER_BOUND){
                sus++;
                if (sus==4){
                    analogWrite(5, map(100, 0, 100, 0, 255));
                    //digitalWrite(7,0);    // mantain sensor supply in order to not to loose powerbank
                    while (alarm_on){
                        for(int i=0;i<2;i++){
                        digitalWrite(8,1);
                        delay(100);
                        digitalWrite(8,0);
                        delay(50);}
                        if (digitalRead(6) == HIGH){alarm_on=false; analogWrite(5, map(0, 0, 100, 0, 255)); delay(4000);} // digitalWrite(7,1); was used to activeate the supply to the sensor
                }
            }
            }
        }
    sus=0;
    }
    if (millis()>19300){resetMillis();}
    }
}
