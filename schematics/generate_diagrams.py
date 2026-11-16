"""
Generate System Diagrams and Circuit Schematics for Project Documentation
Course: CSE260 Digital Logic Design - BRAC University
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_block_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    ax.axis('off')

    # Color palette
    c_input = "#E3F2FD"
    c_logic = "#FCE4EC"
    c_driver = "#FFF9C4"
    c_output = "#E8F5E9"
    c_power = "#EDE7F6"
    c_border = "#37474F"

    # Input Devices
    p1 = patches.FancyBboxPatch((0.5, 5.5), 2.2, 1.2, boxstyle="round,pad=0.1", fc=c_input, ec=c_border, lw=1.5)
    ax.add_patch(p1)
    ax.text(1.6, 6.1, "Left IR Sensor\n(LM358 Active LOW)", ha='center', va='center', fontsize=9, weight='bold')

    p2 = patches.FancyBboxPatch((0.5, 3.5), 2.2, 1.2, boxstyle="round,pad=0.1", fc=c_input, ec=c_border, lw=1.5)
    ax.add_patch(p2)
    ax.text(1.6, 4.1, "Right IR Sensor\n(LM358 Active LOW)", ha='center', va='center', fontsize=9, weight='bold')

    # Logic Processing Block (7404 Hex Inverter / Decision Logic)
    p3 = patches.FancyBboxPatch((3.5, 3.2), 2.8, 3.8, boxstyle="round,pad=0.15", fc=c_logic, ec=c_border, lw=2)
    ax.add_patch(p3)
    ax.text(4.9, 6.4, "DIGITAL LOGIC UNIT", ha='center', va='center', fontsize=10, weight='bold', color="#880E4F")
    ax.text(4.9, 5.7, "7404 Hex Inverter /\nCombinational Routing", ha='center', va='center', fontsize=8.5)
    ax.text(4.9, 4.8, "Boolean Synthesis:\nIN1 = S_R\nIN2 = ~S_R\nIN3 = S_L\nIN4 = ~S_L", ha='center', va='center', fontsize=8, family='monospace')
    ax.text(4.9, 3.7, "Alert Flag Logic:\nAlert = ~S_L + ~S_R", ha='center', va='center', fontsize=8, family='monospace')

    # Motor Driver
    p4 = patches.FancyBboxPatch((7.0, 3.5), 2.4, 3.2, boxstyle="round,pad=0.1", fc=c_driver, ec=c_border, lw=1.5)
    ax.add_patch(p4)
    ax.text(8.2, 5.9, "MOTOR DRIVER", ha='center', va='center', fontsize=10, weight='bold', color="#F57F17")
    ax.text(8.2, 5.2, "L298N Dual H-Bridge\nModule", ha='center', va='center', fontsize=8.5)
    ax.text(8.2, 4.2, "ENA, ENB = 5V\nIN1..IN4 Control\nDual H-Bridges", ha='center', va='center', fontsize=8, family='monospace')

    # Actuators
    p5 = patches.FancyBboxPatch((10.2, 5.5), 2.2, 1.2, boxstyle="round,pad=0.1", fc=c_output, ec=c_border, lw=1.5)
    ax.add_patch(p5)
    ax.text(11.3, 6.1, "Left TT DC Motor\n+ Rubber Wheel", ha='center', va='center', fontsize=9, weight='bold')

    p6 = patches.FancyBboxPatch((10.2, 3.5), 2.2, 1.2, boxstyle="round,pad=0.1", fc=c_output, ec=c_border, lw=1.5)
    ax.add_patch(p6)
    ax.text(11.3, 4.1, "Right TT DC Motor\n+ Rubber Wheel", ha='center', va='center', fontsize=9, weight='bold')

    # Power Supply Unit
    p7 = patches.FancyBboxPatch((4.5, 0.8), 3.8, 1.4, boxstyle="round,pad=0.1", fc=c_power, ec=c_border, lw=1.5)
    ax.add_patch(p7)
    ax.text(6.4, 1.7, "POWER SUBSYSTEM", ha='center', va='center', fontsize=10, weight='bold', color="#4A148C")
    ax.text(6.4, 1.2, "9V Battery / Regulated 5V Rail\nCommon System Ground", ha='center', va='center', fontsize=8.5)

    # Signal arrows
    ax.annotate('', xy=(3.5, 6.1), xytext=(2.7, 6.1), arrowprops=dict(facecolor='black', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(3.5, 4.1), xytext=(2.7, 4.1), arrowprops=dict(facecolor='black', arrowstyle="->", lw=1.5))
    ax.text(3.1, 6.3, "S_L", fontsize=8, weight='bold')
    ax.text(3.1, 4.3, "S_R", fontsize=8, weight='bold')

    ax.annotate('', xy=(7.0, 5.1), xytext=(6.3, 5.1), arrowprops=dict(facecolor='black', arrowstyle="->", lw=1.5))
    ax.text(6.65, 5.3, "IN1..4", fontsize=8, weight='bold')

    ax.annotate('', xy=(10.2, 6.1), xytext=(9.4, 6.1), arrowprops=dict(facecolor='black', arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(10.2, 4.1), xytext=(9.4, 4.1), arrowprops=dict(facecolor='black', arrowstyle="->", lw=1.5))
    ax.text(9.8, 6.3, "OUT1/2", fontsize=8, weight='bold')
    ax.text(9.8, 4.3, "OUT3/4", fontsize=8, weight='bold')

    # Power connections
    ax.annotate('', xy=(6.4, 3.2), xytext=(6.4, 2.2), arrowprops=dict(facecolor='#4A148C', edgecolor='#4A148C', arrowstyle="->", lw=1.5, ls='--'))
    ax.annotate('', xy=(8.2, 3.5), xytext=(7.5, 2.2), arrowprops=dict(facecolor='#4A148C', edgecolor='#4A148C', arrowstyle="->", lw=1.5, ls='--'))
    ax.annotate('', xy=(1.6, 3.5), xytext=(5.0, 2.2), arrowprops=dict(facecolor='#4A148C', edgecolor='#4A148C', arrowstyle="->", lw=1.5, ls='--'))

    ax.set_xlim(0, 13)
    ax.set_ylim(0.5, 7.5)
    plt.title("System Block Diagram: Autonomous Obstacle Avoiding Robot\nBRAC University - CSE260 Digital Logic Design", fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("schematics/system_block_diagram.png", dpi=200)
    plt.close()
    print("System block diagram saved successfully!")

if __name__ == "__main__":
    draw_block_diagram()
