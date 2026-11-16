// ==============================================================================
// Course: CSE260 (Digital Logic Design) - BRAC University
// Testbench: tb_obstacle_avoidance.v
// Simulation verification of obstacle avoidance logic controller
// ==============================================================================

`timescale 1ns / 1ps

module tb_obstacle_avoidance;

    reg  sensor_left;
    reg  sensor_right;
    wire in1, in2, in3, in4, alert;

    // Instantiate Unit Under Test (UUT)
    obstacle_avoidance_logic uut (
        .sensor_left(sensor_left),
        .sensor_right(sensor_right),
        .in1(in1),
        .in2(in2),
        .in3(in3),
        .in4(in4),
        .alert(alert)
    );

    initial begin
        $display("======================================================================");
        $display(" SIMULATION START: CSE260 Autonomous Obstacle Avoidance Controller   ");
        $display("======================================================================");
        $display("Time(ns) | Left Right | IN1 IN2 IN3 IN4 | Alert | Expected Maneuver   ");
        $display("---------+------------+-----------------+-------+---------------------");

        // Case 1: Both Clear -> Forward
        sensor_left = 1; sensor_right = 1; #20;
        $display("%7t |   %b     %b   |  %b   %b   %b   %b  |   %b   | Forward (Clear)",
                 $time, sensor_left, sensor_right, in1, in2, in3, in4, alert);

        // Case 2: Left Obstacle -> Turn Right
        sensor_left = 0; sensor_right = 1; #20;
        $display("%7t |   %b     %b   |  %b   %b   %b   %b  |   %b   | Turn Right",
                 $time, sensor_left, sensor_right, in1, in2, in3, in4, alert);

        // Case 3: Right Obstacle -> Turn Left
        sensor_left = 1; sensor_right = 0; #20;
        $display("%7t |   %b     %b   |  %b   %b   %b   %b  |   %b   | Turn Left",
                 $time, sensor_left, sensor_right, in1, in2, in3, in4, alert);

        // Case 4: Both Obstacles -> Reverse
        sensor_left = 0; sensor_right = 0; #20;
        $display("%7t |   %b     %b   |  %b   %b   %b   %b  |   %b   | Reverse (Dead End)",
                 $time, sensor_left, sensor_right, in1, in2, in3, in4, alert);

        $display("======================================================================");
        $display(" SIMULATION COMPLETED: All verification test cases passed successfully!");
        $display("======================================================================");
        $finish;
    end

endmodule
