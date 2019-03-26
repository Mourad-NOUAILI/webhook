int led_pin = 7;

char data;

void setup() {
  pinMode(led_pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.read();
    Serial.println(data);
    if (data == '1')
      digitalWrite(led_pin, HIGH);
    if (data == '0')
      digitalWrite(led_pin, LOW);
  }
    
}
