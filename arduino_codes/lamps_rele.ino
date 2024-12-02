// Define o pino de controle da fan
int lampadaPin = 10;
int ledPin1 = 8;
int ledPin2 = 9;

void setup() {
  // Configura o pino de controle como saída
  pinMode(lampadaPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
}

void loop() {
  // Ligar a fan (enviar 1, HIGH)
  digitalWrite(ledPin1, HIGH);
  digitalWrite(ledPin2, HIGH);
  digitalWrite(lampadaPin, LOW);
  delay(500); // Espera por 1 segundo
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(lampadaPin, HIGH);
  delay(2000); // Espera por 1 segundo
}