// ==============================================================================
// Course: CSE260 (Digital Logic Design) - BRAC University
// Module: obstacle_avoidance_logic.v
// Project: Autonomous Obstacle Avoiding Robot Controller
//
// Description:
// Combinational digital logic controller synthesizing dual IR proximity sensor
// inputs into directional control vectors for an H-Bridge motor driver (L298N).
//
// Truth Table:
// +-------------+--------------+-----+-----+-----+-----+-------+-----------------------+
// | sensor_left | sensor_right | in1 | in2 | in3 | in4 | alert | Robot Maneuver        |
// +-------------+--------------+-----+-----+-----+-----+-------+-----------------------+
// |      1      |      1       |  1  |  0  |  1  |  0  |   0   | Forward (Clear)       |
// |      0      |      1       |  1  |  0  |  0  |  1  |   1   | Turn Right (Pivot)    |
// |      1      |      0       |  0  |  1  |  1  |  0  |   1   | Turn Left (Pivot)     |
// |      0      |      0       |  0  |  1  |  0  |  1  |   1   | Reverse (Dead End)    |
// +-------------+--------------+-----+-----+-----+-----+-------+-----------------------+
//
// Boolean Minimization:
// in1 = sensor_right (Left motor moves forward when no right-side obstacle)
// in2 = ~sensor_right (Left motor moves reverse when right-side obstacle present)
// in3 = sensor_left  (Right motor moves forward when no left-side obstacle)
// in4 = ~sensor_left (Right motor moves reverse when left-side obstacle present)
// alert = ~(sensor_left & sensor_right) = ~sensor_left | ~sensor_right (De Morgan's)
// ==============================================================================

`timescale 1ns / 1ps

module obstacle_avoidance_logic (
    input  wire sensor_left,   // 1 = Clear, 0 = Obstacle
    input  wire sensor_right,  // 1 = Clear, 0 = Obstacle
    output wire in1,           // Left Motor Forward
    output wire in2,           // Left Motor Reverse
    output wire in3,           // Right Motor Forward
    output wire in4,           // Right Motor Reverse
    output wire alert          // Alert indicator (Obstacle detected)
);

    // Continuous assignment using Boolean algebra
    assign in1 = sensor_right;
    assign in2 = ~sensor_right;
    assign in3 = sensor_left;
    assign in4 = ~sensor_left;

    // Alert flag activates if either sensor detects an obstacle
    assign alert = ~sensor_left | ~sensor_right;

endmodule

// ==============================================================================
// Structural Gate-Level Representation (Using standard 74-series TTL logic gates)
// Demonstrates hardware implementation with 7404 (NOT) and 7400/7432 (NAND/OR)
// ==============================================================================
module obstacle_avoidance_structural (
    input  wire sensor_left,
    input  wire sensor_right,
    output wire in1,
    output wire in2,
    output wire in3,
    output wire in4,
    output wire alert
);

    // Direct buffer for forward signals
    buf b1 (in1, sensor_right);
    buf b2 (in3, sensor_left);

    // 7404 Inverters for reverse signals
    not n1 (in2, sensor_right);
    not n2 (in4, sensor_left);

    // 7400 NAND gate used for alert detection (active low detection)
    wire n_left, n_right;
    not n3 (n_left, sensor_left);
    not n4 (n_right, sensor_right);
    or  o1 (alert, n_left, n_right);

endmodule
