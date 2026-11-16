# Autonomous Obstacle Avoiding Robot - Hardware & Wiring Guide
**Department of Computer Science and Engineering, BRAC University**  
**Course:** CSE260: Digital Logic Design

---

## 1. System Overview & Architecture

The system operates using dual forward-mounted Infrared (IR) obstacle proximity sensors, a digital logic decision-making circuit (implemented using standard 74-series TTL logic ICs such as the 7404 Hex Inverter on a breadboard), and an L298N dual H-Bridge motor driver powering two independent DC gear motors.

---

## 2. Pin-to-Pin Interconnection Guide

### A. Power Distribution
| Source Component | Pin / Terminal | Destination Component | Pin / Terminal | Voltage / Signal Type |
| :--- | :--- | :--- | :--- | :--- |
| **9V Battery** | Positive (+) | **L298N Module** | 12V Screw Terminal | +9.0V DC Main Power |
| **9V Battery** | Negative (-) | **L298N Module** | GND Screw Terminal | System Common Ground |
| **L298N Module** | +5V Out Screw Terminal | **Breadboard Rail** | Positive (+) Bus | +5.0V Regulated Logic Power |
| **L298N Module** | GND Screw Terminal | **Breadboard Rail** | Negative (-) Bus | Common Ground Bus |

---

### B. IR Proximity Sensor Modules (Left & Right)
Both IR modules operate on active-low digital comparator logic (LM358):
- **Output = HIGH (5V)**: Path is CLEAR (no reflection detected).
- **Output = LOW (0V)**: Obstacle DETECTED within range (reflection detected).

| Sensor Module | Sensor Pin | Connection Point | Description |
| :--- | :--- | :--- | :--- |
| **Left IR Sensor** | VCC | Breadboard (+5V) Rail | Power Supply |
| **Left IR Sensor** | GND | Breadboard (GND) Rail | Common Ground |
| **Left IR Sensor** | OUT ($S_L$) | Breadboard Logic Input | Sensor Signal Left |
| **Right IR Sensor**| VCC | Breadboard (+5V) Rail | Power Supply |
| **Right IR Sensor**| GND | Breadboard (GND) Rail | Common Ground |
| **Right IR Sensor**| OUT ($S_R$)| Breadboard Logic Input | Sensor Signal Right |

---

### C. Digital Logic Implementation (CSE260 Pure Hardware Logic)

Using a standard **7404 Hex Inverter IC** (14-pin DIP):
- **Pin 14:** VCC (+5V from Breadboard bus)
- **Pin 7:** GND (Common GND from Breadboard bus)

#### Combinational Routing to L298N Inputs:
| Logic Input / Gate | 7404 Pin | L298N Input Pin | Logic Expression | Motor Action |
| :--- | :--- | :--- | :--- | :--- |
| **Right Sensor ($S_R$)** | Direct bypass wire | **IN1** (Left Motor Forward) | $IN_1 = S_R$ | Drives Left Motor forward when Right is clear |
| **Right Sensor ($S_R$)** | Pin 1 (1A) $\rightarrow$ Pin 2 (1Y) | **IN2** (Left Motor Reverse) | $IN_2 = \overline{S_R}$ | Reverses Left Motor when Right detects obstacle |
| **Left Sensor ($S_L$)** | Direct bypass wire | **IN3** (Right Motor Forward) | $IN_3 = S_L$ | Drives Right Motor forward when Left is clear |
| **Left Sensor ($S_L$)** | Pin 3 (2A) $\rightarrow$ Pin 4 (2Y) | **IN4** (Right Motor Reverse) | $IN_4 = \overline{S_L}$ | Reverses Right Motor when Left detects obstacle |
| **Jumper ENA** | Internal jumper placed | ENA | Active (HIGH) | Enables Motor Channel A at 100% duty |
| **Jumper ENB** | Internal jumper placed | ENB | Active (HIGH) | Enables Motor Channel B at 100% duty |

---

### D. Motor Actuator Wiring
| L298N Terminal | Connected Component | Functionality |
| :--- | :--- | :--- |
| **OUT1** | Left TT Gear Motor Lead 1 | Left Motor Phase A |
| **OUT2** | Left TT Gear Motor Lead 2 | Left Motor Phase B |
| **OUT3** | Right TT Gear Motor Lead 1 | Right Motor Phase A |
| **OUT4** | Right TT Gear Motor Lead 2 | Right Motor Phase B |

---

### E. Microcontroller Pinout (Optional Arduino Uno Mode)
If deploying with an Arduino Uno (e.g. for enhanced PWM control or robotic coursework):
| Arduino Uno Pin | Connected Device / Pin | Function |
| :--- | :--- | :--- |
| **D2** | Left IR Sensor OUT ($S_L$) | Digital Input |
| **D3** | Right IR Sensor OUT ($S_R$) | Digital Input |
| **D5 (PWM)** | L298N ENA (Jumper removed) | Left Motor Speed Control |
| **D6 (PWM)** | L298N ENB (Jumper removed) | Right Motor Speed Control |
| **D8** | L298N IN1 | Left Motor Forward |
| **D9** | L298N IN2 | Left Motor Backward |
| **D10** | L298N IN3 | Right Motor Forward |
| **D11** | L298N IN4 | Right Motor Backward |
| **GND** | System Common GND Rail | Reference Ground |

---

## 3. Operational Truth Table & Maneuver Matrix

| $S_L$ (Left IR) | $S_R$ (Right IR) | IN1 (M1 Fwd) | IN2 (M1 Rev) | IN3 (M2 Fwd) | IN4 (M2 Rev) | Robot Maneuver | Description |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1 (Clear)** | **1 (Clear)** | 1 | 0 | 1 | 0 | **FORWARD** | Both motors forward at full speed |
| **0 (Obstacle)** | **1 (Clear)** | 1 | 0 | 0 | 1 | **PIVOT RIGHT** | Left motor forward, Right motor backward |
| **1 (Clear)** | **0 (Obstacle)** | 0 | 1 | 1 | 0 | **PIVOT LEFT** | Left motor backward, Right motor forward |
| **0 (Obstacle)** | **0 (Obstacle)** | 0 | 1 | 0 | 1 | **REVERSE** | Both motors backward to escape corner/wall |

---

## 4. Hardware Calibration & Troubleshooting

1. **IR Detection Threshold Tuning:**
   - Place an obstacle (such as the cardboard wall) ~8–12 cm in front of the sensor.
   - Adjust the onboard potentiometer with a screwdriver until the indicator LED just turns ON.
   - Verify that when the obstacle is removed, the indicator LED turns OFF.

2. **Motor Direction Verification:**
   - If a motor rotates backward during forward motion, simply swap the OUT1/OUT2 or OUT3/OUT4 wires at the screw terminal.

3. **Power Stability:**
   - Ensure the battery provides adequate current (>7.5V under load). If motors stutter or reset the sensors, install a 100µF decoupling capacitor across the 5V logic power rail.
