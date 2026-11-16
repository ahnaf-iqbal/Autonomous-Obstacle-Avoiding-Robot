/*
 * Project: Autonomous Obstacle Avoiding Robot
 * Course: CSE260 (Digital Logic Design)
 * Department of Computer Science and Engineering, BRAC University
 *
 * Description:
 * Autonomous mobile robot utilizing dual infrared (IR) proximity sensors
 * and an L298N dual H-bridge motor driver to detect obstacles and execute
 * evasive steering maneuvers.
 *
 * Hardware Pin Mapping:
 * - Left IR Sensor (Digital OUT)  -> Arduino Pin 2
 * - Right IR Sensor (Digital OUT) -> Arduino Pin 3
 * - Motor A (Left) IN1            -> Arduino Pin 8
 * - Motor A (Left) IN2            -> Arduino Pin 9
 * - Motor B (Right) IN3           -> Arduino Pin 10
 * - Motor B (Right) IN4           -> Arduino Pin 11
 * - Motor A Enable (ENA)          -> Arduino Pin 5 (PWM)
 * - Motor B Enable (ENB)          -> Arduino Pin 6 (PWM)
 */

// ================= Pin Definitions =================
const int PIN_IR_LEFT   = 2;  // Left IR Obstacle Sensor OUT
const int PIN_IR_RIGHT  = 3;  // Right IR Obstacle Sensor OUT

const int PIN_MOTOR_IN1 = 8;  // Left Motor Forward
const int PIN_MOTOR_IN2 = 9;  // Left Motor Backward
const int PIN_MOTOR_IN3 = 10; // Right Motor Forward
const int PIN_MOTOR_IN4 = 11; // Right Motor Backward

const int PIN_MOTOR_ENA = 5;  // Left Motor Speed (PWM)
const int PIN_MOTOR_ENB = 6;  // Right Motor Speed (PWM)

// Optional status LED and buzzer pins
const int PIN_LED_ALERT = 13; // Builtin LED or alert indicator

// ================= Speed Constants =================
// PWM speed values range from 0 (halt) to 255 (maximum speed)
const int SPEED_NORMAL = 180; // Standard cruising speed
const int SPEED_TURN   = 160; // Controlled pivot / turning speed

// Sensor logic definitions
// Standard active-low IR modules:
// LOW (0) = Obstacle detected (light reflected)
// HIGH (1) = Clear path (no reflection)
const int OBSTACLE_DETECTED = LOW;
const int PATH_CLEAR        = HIGH;

void setup() {
  // Initialize Serial interface for debugging
  Serial.begin(9600);
  Serial.println("==================================================");
  Serial.println("  AUTONOMOUS OBSTACLE AVOIDING ROBOT INITIALIZING ");
  Serial.println("  Department of CSE - BRAC University             ");
  Serial.println("==================================================");

  // Configure Sensor Inputs
  pinMode(PIN_IR_LEFT, INPUT);
  pinMode(PIN_IR_RIGHT, INPUT);

  // Configure Motor Control Outputs
  pinMode(PIN_MOTOR_IN1, OUTPUT);
  pinMode(PIN_MOTOR_IN2, OUTPUT);
  pinMode(PIN_MOTOR_IN3, OUTPUT);
  pinMode(PIN_MOTOR_IN4, OUTPUT);

  pinMode(PIN_MOTOR_ENA, OUTPUT);
  pinMode(PIN_MOTOR_ENB, OUTPUT);

  pinMode(PIN_LED_ALERT, OUTPUT);

  // Initial stop state
  stopMotors();
  delay(1000);
  Serial.println("[SYSTEM READY] Autonomous navigation starting...");
}

void loop() {
  // Read sensor states
  int leftStatus  = digitalRead(PIN_IR_LEFT);
  int rightStatus = digitalRead(PIN_IR_RIGHT);

  // Digital Logic Decision Tree
  // Case 1: Both Paths Clear (Left = HIGH, Right = HIGH)
  if (leftStatus == PATH_CLEAR && rightStatus == PATH_CLEAR) {
    digitalWrite(PIN_LED_ALERT, LOW);
    moveForward();
    Serial.println("[NAV] Path Clear -> Moving Forward");
  }
  // Case 2: Obstacle on Left (Left = LOW, Right = HIGH)
  // Action: Steer Right to avoid obstacle
  else if (leftStatus == OBSTACLE_DETECTED && rightStatus == PATH_CLEAR) {
    digitalWrite(PIN_LED_ALERT, HIGH);
    pivotRight();
    Serial.println("[NAV] Obstacle on LEFT -> Pivoting RIGHT");
    delay(200); // Brief turn duration for trajectory correction
  }
  // Case 3: Obstacle on Right (Left = HIGH, Right = LOW)
  // Action: Steer Left to avoid obstacle
  else if (leftStatus == PATH_CLEAR && rightStatus == OBSTACLE_DETECTED) {
    digitalWrite(PIN_LED_ALERT, HIGH);
    pivotLeft();
    Serial.println("[NAV] Obstacle on RIGHT -> Pivoting LEFT");
    delay(200); // Brief turn duration for trajectory correction
  }
  // Case 4: Obstacle Directly Ahead (Both Sensors Detect Obstacle)
  // Action: Reverse and make an evasive spin
  else {
    digitalWrite(PIN_LED_ALERT, HIGH);
    Serial.println("[NAV] Obstacle AHEAD (Both Sensors) -> Reversing & Turning");
    moveBackward();
    delay(400); // Reverse away from dead-end
    pivotRight();
    delay(350); // Spin 90-180 degrees
  }

  delay(20); // Loop pacing
}

// ================= Movement Primitive Functions =================

void setMotorSpeeds(int leftSpeed, int rightSpeed) {
  analogWrite(PIN_MOTOR_ENA, leftSpeed);
  analogWrite(PIN_MOTOR_ENB, rightSpeed);
}

void moveForward() {
  setMotorSpeeds(SPEED_NORMAL, SPEED_NORMAL);
  digitalWrite(PIN_MOTOR_IN1, HIGH);
  digitalWrite(PIN_MOTOR_IN2, LOW);
  digitalWrite(PIN_MOTOR_IN3, HIGH);
  digitalWrite(PIN_MOTOR_IN4, LOW);
}

void moveBackward() {
  setMotorSpeeds(SPEED_TURN, SPEED_TURN);
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, HIGH);
  digitalWrite(PIN_MOTOR_IN3, LOW);
  digitalWrite(PIN_MOTOR_IN4, HIGH);
}

void pivotLeft() {
  // Left motor reversed/stopped, Right motor forward
  setMotorSpeeds(SPEED_TURN, SPEED_TURN);
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, HIGH);
  digitalWrite(PIN_MOTOR_IN3, HIGH);
  digitalWrite(PIN_MOTOR_IN4, LOW);
}

void pivotRight() {
  // Left motor forward, Right motor reversed/stopped
  setMotorSpeeds(SPEED_TURN, SPEED_TURN);
  digitalWrite(PIN_MOTOR_IN1, HIGH);
  digitalWrite(PIN_MOTOR_IN2, LOW);
  digitalWrite(PIN_MOTOR_IN3, LOW);
  digitalWrite(PIN_MOTOR_IN4, HIGH);
}

void stopMotors() {
  setMotorSpeeds(0, 0);
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, LOW);
  digitalWrite(PIN_MOTOR_IN3, LOW);
  digitalWrite(PIN_MOTOR_IN4, LOW);
}
