import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Constants
gamma_soil = 10  # kN/m^3, unit weight of soil
gamma_submerged = 18 # kN/m^3, unit weight of soil below groundwater table

def calculate_embedment_depth_and_moment(height, phi, c):
    if height > 6.1:  # Corrected for clarity: 6.1 meters is approximately 20 feet
        messagebox.showerror("Error", "Sheet pile height exceeds cantilever limit (6 meters)")
        return None, None
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi/4 - phi_rad/2)**2
    D = height * (2 * Ka)  # Simplified assumption
    M_max = 0.5 * gamma_soil * Ka * height**2 * D  # Simplified assumption
    return D, M_max

def plot_lateral_earth_pressure(height, phi):
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi/4 - phi_rad/2)**2
    depths = np.linspace(0, height, 100)
    pressures = gamma_soil * depths * Ka
    plt.figure()
    plt.plot(pressures, -depths)
    plt.xlabel('Lateral Earth Pressure (kPa)')
    plt.ylabel('Depth (m)')
    plt.title('Lateral Earth Pressure Distribution')
    plt.grid(True)
    plt.show()

def sensitivity_analysis(height, phi_range, c):
    embedment_depths = []
    max_moments = []
    for phi in phi_range:
        D, M = calculate_embedment_depth_and_moment(height, phi, c)
        if D is not None and M is not None:
            embedment_depths.append(D)
            max_moments.append(M)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(phi_range, embedment_depths)
    plt.xlabel('Angle of Internal Friction (degrees)')
    plt.ylabel('Embedment Depth (m)')
    plt.title('Sensitivity: Embedment Depth')
    plt.grid(True)
    plt.subplot(1, 2, 2)
    plt.plot(phi_range, max_moments)
    plt.xlabel('Angle of Internal Friction (degrees)')
    plt.ylabel('Maximum Moment (kNm)')
    plt.title('Sensitivity: Maximum Moment')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def on_calculate():
    try:
        height = float(height_entry.get())
        phi = float(phi_entry.get())
        c = float(c_entry.get())
        embedment_depth, max_moment = calculate_embedment_depth_and_moment(height, phi, c)
        if embedment_depth and max_moment:
            messagebox.showinfo("Result", f"Required Embedment Depth: {embedment_depth:.2f}m, Maximum Moment: {max_moment:.2f}kNm")
            plot_lateral_earth_pressure(height, phi)
            phi_range = np.linspace(20, 40, 21)  # Detailed range for phi
            sensitivity_analysis(height, phi_range, c)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

# GUI setup
root = tk.Tk()
root.title("Sheet Pile Calculator")

tk.Label(root, text="Enter sheet pile height (m):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Enter angle of internal friction (degrees):").pack()
phi_entry = tk.Entry(root)
phi_entry.pack()

tk.Label(root, text="Enter cohesion (kPa):").pack()
c_entry = tk.Entry(root)
c_entry.pack()

calculate_btn = tk.Button(root, text="Calculate", command=on_calculate)
calculate_btn.pack()

root.mainloop()
