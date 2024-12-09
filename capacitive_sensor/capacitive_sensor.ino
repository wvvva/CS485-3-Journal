#include <CapacitiveSensor.h>

CapacitiveSensor p1 = CapacitiveSensor(3, 2);
CapacitiveSensor p2 = CapacitiveSensor(5, 4);
int p1_status = 0;
int p2_status = 0;

void setup() {
  Serial.begin(9600);
  p1_status = 0;
  p2_status = 0;
}

void loop() {
  long measurement1 = p1.capacitiveSensor(60);
  long measurement2 = p2.capacitiveSensor(60);

  // Update statuses based on measurements
  if (p1_status == 0 && measurement1 > 10) {
    p1_status = 1;
    p2_status = 0;
    Serial.println("play_video_1");

  } else if (p2_status == 0 && measurement2 > 10 && measurement2 < 300) {
    p2_status = 1;
    p1_status = 0;
    Serial.println("play_video_2");
  }

  delay(10); 
}
