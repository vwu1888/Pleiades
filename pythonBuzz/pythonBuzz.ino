#define LEFT_BUZZ 5
#define RIGHT_BUZZ 3
#define NUM_BUZZ 2
const int buzzers[NUM_BUZZ] = {LEFT_BUZZ, RIGHT_BUZZ};

void setup() {
  Serial.begin(9600);
  while(!Serial);

  for(int i = 0; i < NUM_BUZZ; i++) {
    pinMode(buzzers[i], OUTPUT);
  }
}

void loop() {
  while(!Serial.available());
  int freq = Serial.parseInt();
  Serial.read();
  int pose = Serial.parseInt();
  while(Serial.available()) {
    Serial.read();
  }
  Serial.println(freq);
  Serial.println(pose);

  if (pose < 0) {
    setAllBuzz(freq);
  } else {
    setBuzzer(freq, pose);
  }
}

void setAllBuzz(int freq) {
  for (int i = 0; i < NUM_BUZZ; i++) {
    setBuzzer(freq, i);
  }
}

void setBuzzer(int freq, int pose) {
  if (pose > NUM_BUZZ) {
    return;
  }
  if (freq <= 0) {
    noTone(buzzers[pose]);
  }
  tone(buzzers[pose], freq);
}
