# BRAC UNIVERSITY
## Department of Computer Science and Engineering
### CSE260: Digital Logic Design
#### Lab Project Report

---

# Title: AUTONOMOUS OBSTACLE AVOIDING ROBOT

### Group Members:
- **Md. Ahnaf Iqbal**
- **Abir Hasan**
- **Hironmoy Sikder**
- **Muhammad Ashfaq Tahmeed**

**Department of Computer Science and Engineering**  
**BRAC University**  
**Submission Date: 2023**

---

## Abstract

The Autonomous Obstacle Avoiding Robot project presents the design, analysis, and hardware realization of an autonomous mobile robotic vehicle capable of collision-free navigation without relying on high-cost computational microcontrollers. Developed in accordance with digital logic synthesis principles and robotic actuation, the system employs dual active-low Infrared (IR) obstacle proximity sensors, a combinational logic decision network based on 74-series TTL integrated circuits (7404 Hex Inverter), and an L298N dual H-Bridge motor driver module controlling two independent direct-current (DC) gear motors. The primary objective is to demonstrate how fundamental Boolean logic gates, differential steering mechanics, and hardware interfacing can solve complex autonomous navigation tasks with zero software overhead, minimal latency, and high energy efficiency. The system was experimentally tested within a constrained arena, demonstrating real-time obstacle detection, dynamic path redirection, and recovery maneuvers from dead-ends. This report provides an in-depth exploration of the system architecture, Boolean algebraic minimization, circuit schematics, cost analysis, sustainability impacts, and experimental performance evaluations.

**Keywords:** Combinational Digital Logic, Obstacle Avoidance, Infrared Proximity Sensing, L298N H-Bridge Driver, Autonomous Mobile Robot, TTL Integrated Circuits.

---

## 1. Introduction

Autonomous mobile robotics has become a cornerstone of contemporary automation, playing pivotal roles in warehouse logistics (Automated Guided Vehicles - AGVs), planetary rovers, automated vacuum systems, and unmanned industrial transport. Conventional robotic navigation systems frequently rely on powerful microcontrollers (e.g., ARM Cortex, ATmega328P) or microprocessors executing intensive software routines. While highly adaptable, microcontroller-based approaches introduce software execution overhead, clock cycle latencies, firmware vulnerabilities, and increased power dissipation—factors that can be suboptimal for lightweight, ultra-low-cost, or safety-critical industrial applications.

In contrast, pure hardware-based combinational logic controllers process sensory feedback instantaneously at gate-propagation speeds (typically under 15 nanoseconds for standard TTL logic). The scope of this project falls directly within the domain of **Computer Interfacing and Digital Logic Design (CSE260)**. The goal is to engineer an autonomous, two-wheel differential drive robotic platform that uses dual forward-facing optical infrared sensors to detect obstructions and instantaneously translates these digital inputs into motor driving vectors using combinational logic gates.

The design emphasizes structural simplicity, rapid hardware deployment, cost minimization, and transparent digital logic behavior. The project validates how foundational Boolean algebra ($AND$, $OR$, $NOT$) directly dictates mechanical motion in the real world, bridging the gap between theoretical truth tables and practical physical robotics.

---

## 2. Related Work / Inspiration

Commercial autonomous platforms, such as the Roomba robotic vacuum cleaner and industrial AGVs used by Amazon Robotics, employ multi-layered sensor arrays (including LiDAR, ultrasonic transducers, and machine-vision cameras) coupled with complex SLAM (Simultaneous Localization and Mapping) algorithms. While these solutions deliver high precision, they demand significant computational resources, complex PCB layouts, and substantial financial investment.

In academic and DIY engineering environments, obstacle-avoiding robots are commonly prototyped using an Arduino Uno paired with an HC-SR04 ultrasonic sensor mounted on an SG90 servo motor. However, existing literature reveals that many basic obstacle-avoidance routines do not require complex polling loops or microcontroller CPU cycles. Prototypical investigations by researchers in low-cost robotics demonstrate that dual infrared sensors paired with direct motor driver logic (such as L293D or L298N H-bridges) can achieve reliable differential steering. 

Our project builds upon these concepts by formalizing the digital logic design methodology taught in **BRAC University CSE260**. Rather than treating the robot as a "black-box" microcontroller sketch, we formulate the complete state transition matrix, synthesize the Boolean equations governing motor directions, implement the circuit using discrete TTL logic gates and breadboard wiring, and provide both hardware-gate and firmware-compatible implementations for verification.

---

## 3. Technical Approach

### 3.1 System Architecture

The robot architecture is structured into four primary subsystems:
1. **Sensory Subsystem:** Dual infrared reflectance modules (Left $S_L$ and Right $S_R$) operating with LM358 operational amplifier comparators.
2. **Digital Logic Decision Unit:** A 7404 Hex Inverter integrated circuit that conditions and synthesizes sensor output signals into active motor control vectors.
3. **Power & Motor Driver Subsystem:** An L298N dual H-Bridge driver that translates low-power TTL logic signals into high-current inductive drive signals for the motors.
4. **Actuation & Chassis:** Two 3–6V yellow TT DC gear motors with high-traction rubber wheels mounted on a lightweight wooden chassis with a rear omnidirectional caster/support.

```mermaid
flowchart TD
    subgraph SENSORY_INPUTS [Sensory Input Subsystem]
        IR_L["Left IR Sensor (S_L)\n[Digital Active-LOW]"]
        IR_R["Right IR Sensor (S_R)\n[Digital Active-LOW]"]
    end

    subgraph LOGIC_UNIT [Digital Logic Controller (7404 TTL / Logic Network)]
        TRUTH["Combinational Logic Synthesis\nIN1 = S_R | IN2 = ~S_R\nIN3 = S_L | IN4 = ~S_L"]
        ALERT["Obstacle Alert Gate\nAlert = ~S_L + ~S_R"]
    end

    subgraph MOTOR_DRIVER [L298N Dual H-Bridge Driver]
        H_BRIDGE["H-Bridge Switching Matrix\nENA = 5V (Active)\nENB = 5V (Active)"]
    end

    subgraph ACTUATION [Differential Drive Actuators]
        M_LEFT["Left TT DC Gear Motor\n(Wheel 1)"]
        M_RIGHT["Right TT DC Gear Motor\n(Wheel 2)"]
    end

    subgraph POWER [Power Subsystem]
        BATT["9V DC Battery / Power Switch"]
        REG["5V Onboard Regulator\n(Logic Bus)"]
    end

    IR_L --> TRUTH
    IR_R --> TRUTH
    IR_L --> ALERT
    IR_R --> ALERT

    TRUTH -->|IN1, IN2| H_BRIDGE
    TRUTH -->|IN3, IN4| H_BRIDGE

    H_BRIDGE -->|OUT1, OUT2| M_LEFT
    H_BRIDGE -->|OUT3, OUT4| M_RIGHT

    BATT -->|9V Raw| H_BRIDGE
    H_BRIDGE -->|5V Regulated| REG
    REG -.-> SENSORY_INPUTS
    REG -.-> LOGIC_UNIT
```

### 3.2 Boolean Logic & Truth Table Formulation

Standard active-low digital IR sensors produce a logic **HIGH (1)** when the path is unobstructed and switch to **LOW (0)** when an object reflects emitted infrared radiation back to the photodiode receiver.

To achieve robust differential steering:
- When both paths are clear ($S_L = 1, S_R = 1$), both motors drive forward ($IN_1 = 1, IN_2 = 0, IN_3 = 1, IN_4 = 0$).
- When an obstacle is detected on the left ($S_L = 0, S_R = 1$), the robot executes a right turn. The left motor drives forward while the right motor reverses or halts ($IN_1 = 1, IN_2 = 0, IN_3 = 0, IN_4 = 1$).
- When an obstacle is detected on the right ($S_L = 1, S_R = 0$), the robot pivots left ($IN_1 = 0, IN_2 = 1, IN_3 = 1, IN_4 = 0$).
- When obstacles are detected on both sensors ($S_L = 0, S_R = 0$), the robot reverses ($IN_1 = 0, IN_2 = 1, IN_3 = 0, IN_4 = 1$).

#### Complete Operational Truth Table:
| Case | Left IR ($S_L$) | Right IR ($S_R$) | IN1 (M1+) | IN2 (M1-) | IN3 (M2+) | IN4 (M2-) | Maneuver | Description |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | 1 | 1 | 1 | 0 | 1 | 0 | **FORWARD** | Path clear, linear translation |
| **2** | 0 | 1 | 1 | 0 | 0 | 1 | **PIVOT RIGHT** | Left sensor triggered; evasive clockwise turn |
| **3** | 1 | 0 | 0 | 1 | 1 | 0 | **PIVOT LEFT** | Right sensor triggered; counter-clockwise turn |
| **4** | 0 | 0 | 0 | 1 | 0 | 1 | **REVERSE** | Both triggered; retreat from dead-end |

#### Boolean Equations:
$$\begin{aligned}
IN_1 &= S_R \\
IN_2 &= \overline{S_R} \\
IN_3 &= S_L \\
IN_4 &= \overline{S_L} \\
\text{Alert} &= \overline{S_L} + \overline{S_R} = \overline{S_L \cdot S_R} \quad \text{(De Morgan's Theorem)}
\end{aligned}$$

This formulation requires only **two inverters (NOT gates)** from a standard 7404 IC to achieve full bidirectional differential steering.

---

### 3.3 Components Used

| Category | Component Description | Specific Model / Specification |
| :--- | :--- | :--- |
| **Logic & Processing** | TTL Hex Inverter IC / Breadboard | 7404 DIP-14 TTL Logic IC |
| **Sensors** | Dual Infrared Obstacle Sensors | LM358 Comparator Modules with Potentiometers |
| **Motor Driver** | Dual Full-Bridge Driver Module | L298N Dual H-Bridge (with heatsink) |
| **Actuators** | 2x DC TT Gear Motors | 3V–6V Dual Shaft BO Motor (1:48 Gear Ratio) |
| **Wheels & Mobility** | High-traction rubber wheels + caster | 65mm Diameter TT Wheels & omni-support |
| **Chassis / Frame** | Custom cut platform | Lightweight wooden chassis with cardboard battery cradle |
| **Power Supply** | Primary Battery Source | 9V 6F22 Heavy-Duty Zinc-Carbon / Alkaline Battery |
| **Ancillary** | Wiring & Switching | Solderless breadboard, SPST switch, jumper wires |

---

### 3.4 Cost Breakdown

The table below summarizes the component bill of materials (BOM) in Bangladeshi Taka (BDT):

| No. | Components | Quantity | Unit Cost (TK) | Total Cost (TK) |
| :---: | :--- | :---: | :---: | :---: |
| 1 | L298N Dual H-Bridge Motor Driver Module | 1 | 220 | 220 |
| 2 | TT DC Gear Motors with Rubber Wheels | 2 | 120 | 240 |
| 3 | Infrared (IR) Proximity Sensor Modules | 2 | 60 | 120 |
| 4 | 7404 Hex Inverter IC (DIP-14) | 1 | 35 | 35 |
| 5 | Mini Solderless Breadboard (400 Tie-Points) | 1 | 90 | 90 |
| 6 | 9V Battery (Heavy Duty 6F22) with Snap Clip | 1 | 70 | 70 |
| 7 | Wooden Chassis & Hardware Assembly | 1 | 150 | 150 |
| 8 | SPST Power Switch Box | 1 | 30 | 30 |
| 9 | Male-to-Male / Male-to-Female Jumper Wires (set) | 1 | 65 | 65 |
| **TOTAL** | **Complete System Cost** | | | **1020 TK** |

---

### 3.5 Circuit & Schematic Implementation

The hardware interconnection combines the low-voltage sensor/logic circuits with the high-current inductive motor driver circuit.

#### Key Wiring Connections:
1. **Power Circuit:**
   - 9V Battery Positive terminal $\rightarrow$ L298N `+12V` input screw terminal.
   - 9V Battery Negative terminal $\rightarrow$ L298N `GND` terminal (common reference ground).
   - L298N onboard 78M05 linear regulator provides regulated `+5V Out` to power the breadboard rail, the 7404 IC, and both IR sensor modules.
2. **Logic Circuit:**
   - Breadboard `+5V` $\rightarrow$ 7404 Pin 14 (VCC), Left IR VCC, Right IR VCC.
   - Breadboard `GND` $\rightarrow$ 7404 Pin 7 (GND), Left IR GND, Right IR GND.
3. **Signal Routing:**
   - Right IR Output ($S_R$) $\rightarrow$ L298N `IN1` (Direct) AND 7404 Pin 1 (1A).
   - 7404 Pin 2 (1Y, $\overline{S_R}$) $\rightarrow$ L298N `IN2`.
   - Left IR Output ($S_L$) $\rightarrow$ L298N `IN3` (Direct) AND 7404 Pin 3 (2A).
   - 7404 Pin 4 (2Y, $\overline{S_L}$) $\rightarrow$ L298N `IN4`.
   - Jumpers `ENA` and `ENB` remain connected to 5V on the L298N board to enable continuous 100% duty cycle motor output.

---

### 3.6 System Functionality

#### Functionality 1: Infrared Obstacle Detection & Signal Conditioning
- **Overview:** Detect physical boundaries and obstacles within a range of 2 cm to 15 cm.
- **Working Procedure:** Each sensor continually pulses infrared light from an IR emitter LED. When an obstacle is encountered, the reflected infrared radiation is focused onto an infrared photodiode receiver. The LM358 operational amplifier compares the photodiode voltage with an adjustable reference voltage tuned by an onboard multiturn potentiometer. Once reflected intensity exceeds the threshold, the sensor comparator flips its output from HIGH (5V) to LOW (0V) and illuminates an onboard SMD indicator LED.

#### Functionality 2: Real-Time Combinational Logic Steering
- **Overview:** Instantaneous translation of dual binary sensor outputs into motor direction commands.
- **Working Procedure:** Sensor signals feed directly into the 7404 Hex Inverter IC. The logic outputs directly drive the base switches of the L298N H-Bridge. When an obstacle appears on the left, the right motor is immediately driven in reverse while the left motor continues forward, creating a rapid clockwise pivot away from the detected boundary.

#### Functionality 3: Bidirectional Dual H-Bridge Motor Driving
- **Overview:** Controlled high-current driving of inductive DC gear motors.
- **Working Procedure:** The L298N module contains four high-voltage, high-current bipolar transistors configured in dual H-bridge topologies. By switching complementary diagonal pairs, the driver seamlessly reverses motor polarity without mechanical relays or complex circuitry. Internal flyback clamping diodes dissipate inductive back-EMF spikes generated when motor coils de-energize.

#### Functionality 4: Self-Contained Mobile Power Distribution
- **Overview:** Delivery of isolated inductive drive current and regulated digital logic voltages.
- **Working Procedure:** A 9V battery supplies the raw voltage required to drive the TT motors. The L298N module's onboard 5V linear regulator drops the 9V supply to a steady 5V rail for the sensitive optical sensors and TTL ICs, preventing motor electrical noise from inducing spurious logic resets.

---

### 3.7 Challenges & Technical Mitigations

1. **Inductive Motor Noise & False Logic Triggering:**
   - *Challenge:* TT DC brush motors generate significant electrical commutating noise and back-EMF spikes that propagated back into the common ground, causing the IR sensor LM358 comparators to falsely trigger.
   - *Resolution:* Implemented solid single-point star grounding, added decoupling across the logic power rail, and utilized the L298N onboard filtering capacitors.
2. **Sensor Optical Sensitivity to Ambient Light:**
   - *Challenge:* Ambient fluorescent lights and reflective floor tiles caused intermittent false obstacle detection.
   - *Resolution:* Tuned each sensor's onboard potentiometer specifically for cardboard reflection at an optimal distance of 8–10 cm and recessed the photodiode sensors slightly within opaque shrink tubing.
3. **9V Battery Voltage Sag Under High Motor Stall Currents:**
   - *Challenge:* When both motors start simultaneously or reverse during a sharp pivot, the internal impedance of standard 9V zinc-carbon batteries causes instantaneous voltage dips below 6.5V.
   - *Resolution:* Kept wiring runs short, verified minimum operating voltages, and recommended multi-cell 18650 Li-ion battery packs for extended duty cycles.

---

## 4. Sustainability & Impact

### 4.1 Sustainability
- **Ultra-Low Energy Footprint:** Eliminating high-speed microcontrollers reduces static quiescent power dissipation. TTL/CMOS combinational logic consumes milliwatts compared to microcontrollers running multi-megahertz crystal oscillators.
- **Repairability and Modular Recycling:** Every component (motors, chassis, ICs, driver module) is modular and solderless. Components can be disassembled, tested individually, and repurposed across multiple lab experiments with zero e-waste generation.

### 4.2 Socio-Economic & Industrial Impact
1. **Affordable Educational Robotics:** Offers an accessible entry point for students in resource-constrained environments to grasp digital logic design, truth tables, and robotics without expensive proprietary robotic kits.
2. **Industrial Material Handling (AGV):** Illustrates the foundational architecture of factory floor Automated Guided Vehicles (AGVs) that navigate industrial pathways safely without continuous human supervision.
3. **Safety and Fail-Safe Autonomous Mechanisms:** Demonstrates the value of pure hardware interlocks; in critical machinery, hardware-level collision avoidance provides un-hackable, software-crash-proof emergency obstacle stopping.

### 4.3 Future Work
1. **PWM Speed Modulation:** Integrating a 555-timer IC or PWM circuit to enable variable wheel speeds for smoother turns rather than sharp fixed-speed differential pivots.
2. **Ultrasonic Range Extension:** Augmenting the short-range optical IR sensors with an ultrasonic rangefinder for long-distance forward path planning.
3. **Rechargeable Lithium-Ion Integration:** Transitioning to a dual 18650 7.4V battery pack with onboard BMS (Battery Management System) for higher current capacity and rechargeable operation.

### 4.4 Limitations
1. **Line-of-Sight Sensitivity:** Infrared reflection depends heavily on surface reflectivity. Dark/black matte surfaces absorb IR light and may not be detected as reliably as light-colored cardboard obstacles.
2. **Non-Adaptive Trajectory:** The pure hardware logic executes fixed directional responses without memory or path optimization (lacks internal state history).
3. **Limited Battery Lifespan:** Small 9V batteries exhibit limited milliampere-hour (mAh) capacity under continuous dual-motor loads.

---

## 5. Results & Discussion

### 5.1 System Testing Outcomes

Experimental testing of the autonomous robot was performed inside a multi-angled cardboard arena (as recorded in the project demonstration video):

1. **Obstacle Detection Reliability:**
   - The dual IR sensors consistently detected cardboard obstacles at calibrated distances between 8 cm and 12 cm.
   - Active-low switching responded in under 1 millisecond.
2. **Maneuver Execution:**
   - **Straight Trajectory:** When clear, the robot maintained a straight trajectory with balanced motor rotation.
   - **Corner / Wall Avoidance:** When encountering walls at angles between $30^\circ$ and $90^\circ$, the single-sensor trigger executed a pivot turn away from the wall within 300 ms.
   - **Dead-End Recovery:** When driven head-on into a narrow corner where both sensors triggered simultaneously, the robot executed a reverse maneuver followed by an evasive spin, successfully extricating itself.
3. **Arena Navigation:**
   - Over a continuous 5-minute test run, the robot completed multiple perimeter circuits without colliding with the perimeter walls.

### 5.2 Comparative Analysis: Hardware Logic vs. Microcontroller Implementation

| Evaluation Metric | Combinational Logic Architecture (7404 + L298N) | Traditional Microcontroller (Arduino Uno) |
| :--- | :--- | :--- |
| **Response Latency** | **Instantaneous (< 20 ns gate propagation)** | Software loop delay (5–20 ms polling) |
| **BOM Cost** | **~1020 BDT** | ~1850–2200 BDT |
| **Code Vulnerabilities** | **Zero (Immune to firmware crashes or hangs)** | Susceptible to memory overflows / logic lockups |
| **Component Count** | Minimal (1 logic IC, 1 driver, 2 sensors) | Microcontroller board, shields, USB interface |
| **Behavioral Flexibility**| Fixed Boolean truth table | Easily re-programmable via software algorithms |

---

## 6. Conclusion

The Autonomous Obstacle Avoiding Robot demonstrates the practical application of combinational digital logic design in physical robotic automation. By using dual infrared sensors, a 7404 Hex Inverter IC, and an L298N H-bridge motor driver, the vehicle navigates constrained environments without an onboard software microcontroller. Experimental evaluations confirm that the robot reacts to environmental obstacles with zero computational latency and reliable differential steering maneuvers. The project connects the theoretical curriculum of **CSE260: Digital Logic Design** with practical robotics, proving that low-cost, energy-efficient hardware logic delivers high-performance autonomous navigation.

---

## References

1. Mano, M. M., & Ciletti, M. D. (2017). *Digital Design: With an Introduction to the Verilog HDL, VHDL, and SystemVerilog* (6th ed.). Pearson.
2. Floyd, T. L. (2015). *Digital Fundamentals* (11th ed.). Pearson Education.
3. Texas Instruments. (2015). *SN74LS04 Hex Inverter Datasheet*. Texas Instruments Incorporated.
4. STMicroelectronics. (2000). *L298 Dual Full-Bridge Driver Datasheet*. STMicroelectronics Group.
5. Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
6. Instructables. (2021). *Obstacle Avoiding Robot Without Microcontroller Using IR Sensor and L293D/L298N*. DIY Electronics Tutorials.
