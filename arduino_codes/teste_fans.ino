// Define o pino de controle da fan
int fanPin = 13;

void setup() {
  // Configura o pino de controle como saída
  pinMode(fanPin, OUTPUT);
  
} 

void loop() {
  // Ligar a fan (enviar 1, HIGH)
  digitalWrite(fanPin, HIGH);
  delay(10000); // Espera por 1 segundo

  // Desligar a fan (enviar 0, LOW)
  digitalWrite(fanPin, LOW);
  delay(10000); // Espera por 1 segundo
}