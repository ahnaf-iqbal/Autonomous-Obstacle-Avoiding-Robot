"""
Simulation of Autonomous Obstacle Avoiding Robot
Course: CSE260 Digital Logic Design
Department of Computer Science and Engineering, BRAC University

This script models the kinematics of the differential drive robot
moving inside an enclosed cardboard arena (as observed in the project demo)
using dual forward-mounted infrared (IR) proximity sensors.
"""

import math
import matplotlib.pyplot as plt
import numpy as np

class ObstacleAvoidingRobot:
    def __init__(self, x=15.0, y=15.0, theta=0.5):
        self.x = x
        self.y = y
        self.theta = theta  # Heading angle in radians
        self.wheel_base = 12.0  # cm
        self.sensor_range = 10.0  # cm detection threshold
        self.sensor_angle_offset = 0.35  # radians (~20 deg from forward)
        self.speed = 1.8  # cm per step
        self.trajectory_x = [self.x]
        self.trajectory_y = [self.y]

    def get_sensor_endpoints(self):
        # Left sensor heading and endpoint
        theta_left = self.theta + self.sensor_angle_offset
        sx_left = self.x + self.sensor_range * math.cos(theta_left)
        sy_left = self.y + self.sensor_range * math.sin(theta_left)

        # Right sensor heading and endpoint
        theta_right = self.theta - self.sensor_angle_offset
        sx_right = self.x + self.sensor_range * math.cos(theta_right)
        sy_right = self.y + self.sensor_range * math.sin(theta_right)

        return (sx_left, sy_left), (sx_right, sy_right)

    def sense(self, obstacles, boundary_min=2.0, boundary_max=98.0):
        (sx_l, sy_l), (sx_r, sy_r) = self.get_sensor_endpoints()
        
        # 1 = Clear, 0 = Obstacle
        left_clear = 1
        right_clear = 1

        # Check boundary walls (simulating the cardboard arena)
        if sx_l <= boundary_min or sx_l >= boundary_max or sy_l <= boundary_min or sy_l >= boundary_max:
            left_clear = 0
        if sx_r <= boundary_min or sx_r >= boundary_max or sy_r <= boundary_min or sy_r >= boundary_max:
            right_clear = 0

        # Check internal obstacle circles
        for ox, oy, r in obstacles:
            dist_l = math.hypot(sx_l - ox, sy_l - oy)
            dist_r = math.hypot(sx_r - ox, sy_r - oy)
            if dist_l <= r:
                left_clear = 0
            if dist_r <= r:
                right_clear = 0

        return left_clear, right_clear

    def update_logic(self, left_clear, right_clear):
        """
        Implements the combinational logic:
        - (1, 1): Clear path -> Forward
        - (0, 1): Left blocked -> Turn Right
        - (1, 0): Right blocked -> Turn Left
        - (0, 0): Both blocked -> Reverse and pivot
        """
        if left_clear == 1 and right_clear == 1:
            # Move forward
            self.x += self.speed * math.cos(self.theta)
            self.y += self.speed * math.sin(self.theta)
            action = "FORWARD"
        elif left_clear == 0 and right_clear == 1:
            # Turn Right
            self.theta -= 0.28
            self.x += (self.speed * 0.4) * math.cos(self.theta)
            self.y += (self.speed * 0.4) * math.sin(self.theta)
            action = "TURN_RIGHT"
        elif left_clear == 1 and right_clear == 0:
            # Turn Left
            self.theta += 0.28
            self.x += (self.speed * 0.4) * math.cos(self.theta)
            self.y += (self.speed * 0.4) * math.sin(self.theta)
            action = "TURN_LEFT"
        else:
            # Both blocked -> Reverse & Spin
            self.x -= (self.speed * 0.8) * math.cos(self.theta)
            self.y -= (self.speed * 0.8) * math.sin(self.theta)
            self.theta += 0.65  # Sharp turn
            action = "REVERSE_PIVOT"

        self.trajectory_x.append(self.x)
        self.trajectory_y.append(self.y)
        return action


def run_simulation(steps=300):
    obstacles = [
        (35.0, 45.0, 8.0),
        (65.0, 70.0, 10.0),
        (70.0, 25.0, 7.0),
    ]

    robot = ObstacleAvoidingRobot(x=20.0, y=20.0, theta=0.8)

    print("Running Autonomous Obstacle Avoidance Simulation...")
    for step in range(steps):
        s_left, s_right = robot.sense(obstacles)
        action = robot.update_logic(s_left, s_right)
        if step % 50 == 0:
            print(f"Step {step:3d}: Sensor(L={s_left}, R={s_right}) -> Action: {action} at ({robot.x:.1f}, {robot.y:.1f})")

    # Plot simulation results
    plt.figure(figsize=(9, 9))
    plt.plot([2, 98, 98, 2, 2], [2, 2, 98, 98, 2], 'k-', lw=3, label="Arena Enclosure (Cardboard Wall)")

    # Plot obstacles
    for ox, oy, r in obstacles:
        circle = plt.Circle((ox, oy), r, color='gray', alpha=0.7)
        plt.gca().add_patch(circle)
    plt.plot([], [], 'o', color='gray', markersize=12, label="Obstacles")

    # Plot robot trajectory
    plt.plot(robot.trajectory_x, robot.trajectory_y, 'b-', lw=2, alpha=0.8, label="Robot Navigation Path")
    plt.plot(robot.trajectory_x[0], robot.trajectory_y[0], 'go', markersize=10, label="Start Position")
    plt.plot(robot.trajectory_x[-1], robot.trajectory_y[-1], 'ro', markersize=10, label="Final Position")

    plt.title("Autonomous Obstacle Avoiding Robot - Trajectory Simulation\nBRAC University - CSE260 Digital Logic Design", fontsize=12, fontweight='bold')
    plt.xlabel("X Position (cm)")
    plt.ylabel("Y Position (cm)")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper right")
    plt.tight_layout()

    out_file = "schematics/simulation_trajectory.png"
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"Simulation plot saved successfully to {out_file}")

if __name__ == "__main__":
    run_simulation()
