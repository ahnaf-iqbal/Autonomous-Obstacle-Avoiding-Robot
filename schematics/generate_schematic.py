"""
Generate Detailed Circuit Schematic Diagram
Course: CSE260 Digital Logic Design - BRAC University
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_circuit_schematic():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=200)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FAFAFA')

    # Color palette
    c_wire_vcc = '#D32F2F'  # Red
    c_wire_gnd = '#212121'  # Black
    c_wire_sig1 = '#1976D2' # Blue
    c_wire_sig2 = '#388E3C' # Green
    c_wire_sig3 = '#F57C00' # Orange
    c_wire_sig4 = '#7B1FA2' # Purple

    # 1. 9V Battery Block
    b_bat = patches.FancyBboxPatch((0.6, 3.8), 1.8, 2.4, boxstyle="round,pad=0.08", fc="#FFE082", ec="#333", lw=1.5)
    ax.add_patch(b_bat)
    ax.text(1.5, 5.0, "9V Battery\n(Power Supply)", ha='center', va='center', weight='bold', fontsize=9)
    ax.text(2.1, 5.6, "(+)", color=c_wire_vcc, weight='bold', fontsize=9)
    ax.text(2.1, 4.4, "(-)", color=c_wire_gnd, weight='bold', fontsize=9)

    # 2. L298N Motor Driver Block
    b_l298 = patches.FancyBboxPatch((3.5, 3.0), 3.4, 4.2, boxstyle="round,pad=0.1", fc="#FFCDD2", ec="#B71C1C", lw=2)
    ax.add_patch(b_l298)
    ax.text(5.2, 6.8, "L298N Dual H-Bridge Driver", ha='center', va='center', weight='bold', fontsize=10, color="#B71C1C")
    
    # L298N Terminals
    terminals = [
        (3.7, 6.2, "OUT1 (M1+)"), (3.7, 5.6, "OUT2 (M1-)"),
        (6.7, 6.2, "OUT3 (M2+)"), (6.7, 5.6, "OUT4 (M2-)"),
        (3.8, 3.5, "+12V (Vin)"), (4.7, 3.5, "GND"), (5.6, 3.5, "+5V Out"),
        (4.3, 4.5, "IN1"), (4.8, 4.5, "IN2"), (5.4, 4.5, "IN3"), (5.9, 4.5, "IN4"),
        (3.9, 4.5, "ENA"), (6.3, 4.5, "ENB")
    ]
    for tx, ty, tlabel in terminals:
        ax.text(tx, ty, tlabel, fontsize=7.5, ha='center', va='center', family='monospace', weight='bold')

    # 3. Breadboard with 7404 Hex Inverter IC Block
    b_bb = patches.FancyBboxPatch((8.0, 3.0), 3.6, 4.2, boxstyle="round,pad=0.1", fc="#E1F5FE", ec="#0277BD", lw=2)
    ax.add_patch(b_bb)
    ax.text(9.8, 6.8, "Breadboard (Logic IC)", ha='center', va='center', weight='bold', fontsize=10, color="#01579B")

    # 7404 IC DIP package inside breadboard
    b_ic = patches.Rectangle((8.6, 4.2), 2.4, 2.0, fc="#37474F", ec="#212121", lw=1.5)
    ax.add_patch(b_ic)
    ax.text(9.8, 5.2, "7404 Hex Inverter\n(NOT Gates)", color="white", ha='center', va='center', weight='bold', fontsize=8.5)

    # 4. Left IR Sensor (Bottom left)
    b_irl = patches.FancyBboxPatch((1.2, 0.6), 2.6, 1.4, boxstyle="round,pad=0.08", fc="#DCEDC8", ec="#33691E", lw=1.5)
    ax.add_patch(b_irl)
    ax.text(2.5, 1.4, "Left IR Sensor (S_L)", ha='center', va='center', weight='bold', fontsize=9, color="#1B5E20")
    ax.text(2.5, 0.9, "VCC | GND | OUT", ha='center', va='center', fontsize=8, family='monospace')

    # 5. Right IR Sensor (Bottom right)
    b_irr = patches.FancyBboxPatch((8.2, 0.6), 2.6, 1.4, boxstyle="round,pad=0.08", fc="#DCEDC8", ec="#33691E", lw=1.5)
    ax.add_patch(b_irr)
    ax.text(9.5, 1.4, "Right IR Sensor (S_R)", ha='center', va='center', weight='bold', fontsize=9, color="#1B5E20")
    ax.text(9.5, 0.9, "VCC | GND | OUT", ha='center', va='center', fontsize=8, family='monospace')

    # 6. Left and Right DC Gear Motors (Top)
    b_m1 = patches.Circle((2.0, 7.8), 0.7, fc="#CFD8DC", ec="#37474F", lw=1.5)
    ax.add_patch(b_m1)
    ax.text(2.0, 7.8, "Left Motor\n(M1)", ha='center', va='center', weight='bold', fontsize=8)

    b_m2 = patches.Circle((6.7, 7.8), 0.7, fc="#CFD8DC", ec="#37474F", lw=1.5)
    ax.add_patch(b_m2)
    ax.text(6.7, 7.8, "Right Motor\n(M2)", ha='center', va='center', weight='bold', fontsize=8)

    # Motor Wiring lines
    ax.plot([3.4, 2.5, 2.5], [6.2, 6.2, 7.3], color=c_wire_gnd, lw=1.5)
    ax.plot([3.4, 2.0, 2.0], [5.6, 5.6, 7.1], color=c_wire_vcc, lw=1.5)

    ax.plot([7.0, 6.7], [6.2, 7.1], color=c_wire_vcc, lw=1.5)
    ax.plot([7.0, 7.2, 7.2, 6.9], [5.6, 5.6, 7.2, 7.2], color=c_wire_gnd, lw=1.5)

    # Battery to L298N lines
    ax.plot([2.4, 3.8], [5.6, 3.8], color=c_wire_vcc, lw=2, label="VCC (+9V)")
    ax.plot([2.4, 4.7], [4.4, 3.8], color=c_wire_gnd, lw=2, label="Common GND")

    # Breadboard power from L298N 5V Out
    ax.plot([5.6, 8.2], [3.3, 3.3], color=c_wire_vcc, lw=1.5, ls="--", label="Logic +5V")

    # Signal connections annotations
    ax.plot([3.8, 9.0], [1.3, 4.0], color=c_wire_sig1, lw=1.5, label="Sensor S_L OUT")
    ax.plot([9.5, 9.8], [2.0, 4.0], color=c_wire_sig2, lw=1.5, label="Sensor S_R OUT")

    # Logic to IN1..IN4
    ax.plot([8.6, 6.0], [4.8, 4.8], color=c_wire_sig3, lw=1.8, label="Control Vectors (IN1-IN4)")

    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 8.8)
    ax.legend(loc="upper right", frameon=True, fontsize=8)
    plt.title("Hardware Schematic & Interconnection Wiring Diagram\nCSE260 Digital Logic Design - BRAC University", fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig("schematics/circuit_schematic.png", dpi=200)
    plt.close()
    print("Circuit schematic image saved successfully!")

if __name__ == "__main__":
    draw_circuit_schematic()
