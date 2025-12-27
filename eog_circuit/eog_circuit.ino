
const int numChannels = 6;
const int ledPin = 7;
unsigned long lastSendMillis = 0;
const unsigned long sendIntervalMillis = 2000UL; 

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  randomSeed(analogRead(A5));
}

void loop() {
  unsigned long now = millis();
  if (now - lastSendMillis >= sendIntervalMillis) {
    lastSendMillis = now;
    int vals[numChannels];
    for (int i = 0; i < numChannels; i++) {
      int noise = random(-30, 30);
      int base = 512 + noise;
      if (random(0, 1000) < 5) base += random(60, 180); 
      if (base < 0) base = 0;
      if (base > 1023) base = 1023;
      vals[i] = base;
    }
    unsigned long tms = millis();
    for (int i = 0; i < numChannels; i++) {
      Serial.print(vals[i]);
      Serial.print(',');
    }
    Serial.println(tms);
  }

  // Listen for selection command 'S'
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'S') {
      digitalWrite(ledPin, HIGH);
      delay(80);
      digitalWrite(ledPin, LOW);
    }
  }
}
