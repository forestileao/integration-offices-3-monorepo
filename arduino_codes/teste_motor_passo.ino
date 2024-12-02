#include <Servo.h>

Servo myservo;
int posMaxCaneta = 55;
int posCaneta = 0;
int incomingByte = 0;

int posCima = 0;
int posDireita = 0;

#define EN 9

// Direction pin
#define X_DIR 5
#define Y_DIR 7

// Step pin
#define X_STP 6
#define Y_STP 8

// A4988
int delayTime = 300;
int stps = 50;

void up(int steps) {
  Serial.print("Moving up with ");
  Serial.print(steps);
  Serial.println(" steps.");
  
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, true);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void down(int steps) {
  Serial.print("Moving down with ");
  Serial.print(steps);
  Serial.println(" steps.");
  
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, false);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void left(int steps) {
  Serial.print("Moving left with ");
  Serial.print(steps);
  Serial.println(" steps.");
  
  digitalWrite(X_DIR, true);
  digitalWrite(Y_DIR, true);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void right(int steps) {
  Serial.print("Moving right with ");
  Serial.print(steps);
  Serial.println(" steps.");
  
  digitalWrite(X_DIR, false);
  digitalWrite(Y_DIR, false);

  for (int i = 0; i < steps; i++) {
    digitalWrite(X_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(X_STP, LOW);
    delayMicroseconds(delayTime);
    digitalWrite(Y_STP, LOW);
    delayMicroseconds(delayTime);
  }
}

void setup() {
  pinMode(X_DIR, OUTPUT);
  pinMode(X_STP, OUTPUT);
  pinMode(Y_DIR, OUTPUT);
  pinMode(Y_STP, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);

  Serial.begin(9600);
}

void loop() {
  incomingByte = Serial.read();
  if (incomingByte == 'w') up(50);  // Move up
  if (incomingByte == 's') down(50);  // Move down
  if (incomingByte == 'a') left(50);  // Move left
  if (incomingByte == 'd') right(50);  // Move right

  delay(1);
}

// altura -> 2200 passos
// largura -> 1000 passos

// servo -> 15 graus : escrita
//         -> 40 graus : movimentação

// Observador olhando perto do Motor Y
// 2 antihorário -> cima
// 2 horário -> baixo
// X horário e Y antihorário -> direita
// Y horário e X antihorário -> esquerda
// X horário -> Baixo direita
// X antihorário -> Cima esquerda
// Y horário -> Baixo esquerda
// Y antihorário -> Cima direita
