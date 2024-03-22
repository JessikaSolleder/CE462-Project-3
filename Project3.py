import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Constants
gamma_soil = 10  # kN/m^3, unit weight of soil
gamma_submerged = 18  # kN/m^3, unit weight of soil below groundwater table

def calculate_embedment_depth_and_moment(height, phi, c):
    if height > 6.1:  # Corrected for clarity: 6.1 meters is approximately 20 feet
        messagebox.showerror("Error", "Sheet pile height exceeds cantilever limit (6 meters)")
        return None, None
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi / 4 - phi_rad / 2) ** 2
    D = height * (2 * Ka)  # Simplified assumption
    M_max = 0.5 * gamma_soil * Ka * height ** 2 * D  # Simplified assumption
    return D, M_max

def plot_lateral_earth_pressure_and_displacement(height, phi):
    phi_rad = np.radians(phi)
    Ka = np.tan(np.pi / 4 - phi_rad / 2) ** 2
    depths = np.linspace(0, height, 100)
    pressures = gamma_soil * depths * Ka
    D, _ = calculate_embedment_depth_and_moment(height, phi, None)  # Calculate D here
    displacements = []
    for depth in depths:
        displacement = depth * (1 + (2 / 3) * np.sqrt(D / depth))
        displacements.append(displacement)
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(pressures, -depths)
    plt.xlabel('Lateral Earth Pressure (kPa)')
    plt.ylabel('Depth (m)')
    plt.title('Lateral Earth Pressure Distribution')
    plt.grid(True)
    plt.subplot(1, 2, 2)
    plt.plot(displacements, -depths)
    plt.xlabel('Displacement (m)')
    plt.ylabel('Depth (m)')
    plt.title('Displacement Distribution')
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

def prompt_phi_range(height, c):
    # Pop-up window for phi range input
    phi_range_window = tk.Toplevel(root)
    phi_range_window.title("Phi Range Input")
    
    tk.Label(phi_range_window, text="Enter start of angle of internal friction range (degrees):").pack()
    global phi_start_entry
    phi_start_entry = tk.Entry(phi_range_window)
    phi_start_entry.pack()

    tk.Label(phi_range_window, text="Enter end of angle of internal friction range (degrees):").pack()
    global phi_end_entry
    phi_end_entry = tk.Entry(phi_range_window)
    phi_end_entry.pack()

    tk.Label(phi_range_window, text="Enter angle of internal friction step size (degrees):").pack()
    global phi_step_entry
    phi_step_entry = tk.Entry(phi_range_window)
    phi_step_entry.pack()

    # Button to proceed with sensitivity analysis after input
    proceed_button = tk.Button(phi_range_window, text="Proceed", command=lambda: on_phi_range_entered(phi_range_window, height, c))
    proceed_button.pack()

def on_phi_range_entered(phi_range_window, height, c):
    try:
        phi_start = float(phi_start_entry.get())
        phi_end = float(phi_end_entry.get())
        phi_step = float(phi_step_entry.get())
        phi_range_window.destroy()  # Close the pop-up window

        # Generate a detailed range for phi based on user input for sensitivity analysis
        phi_range = np.linspace(phi_start, phi_end, int((phi_end - phi_start) / phi_step) + 1)
        sensitivity_analysis(height, phi_range, c)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values in the Phi range fields.")

# Adjust the on_calculate function to include calling the pop-up for phi range after the first graph
def on_calculate():
    try:
        height = float(height_entry.get())
        phi = float(phi_entry.get())
        c = float(c_entry.get())

        embedment_depth, max_moment = calculate_embedment_depth_and_moment(height, phi, c)
        if embedment_depth and max_moment:
            messagebox.showinfo("Result", f"Required Embedment Depth: {embedment_depth:.2f}m, Maximum Moment: {max_moment:.2f}kNm")
            plot_lateral_earth_pressure_and_displacement(height, phi)

        prompt_phi_range(height, c)  # Now passing height and c

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
