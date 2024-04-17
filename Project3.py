import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Assumptions
gamma_gransoil = 20  # kN/m^3, unit weight of soil
gamma_claysoil = 24  # kN/m^3, unit weight of soil below groundwater table

def quadratic_roots(c, height, p1):
    a = 4 * c - gamma_gransoil * height
    b = 2 * p1
    c1 = (p1 * (p1 + 12 * c * (height / 3))) / (gamma_gransoil * height + 2 * c)

    # Calculate the discriminant
    discriminant = (b**2) - (4*a*c1)
    
    # Check if the discriminant is positive, negative, or zero
    if discriminant >= 0:
        # If the discriminant is non-negative, calculate roots
        root1 = (-b + np.sqrt(discriminant)) / (2*a)
        root2 = (-b - np.sqrt(discriminant)) / (2*a)
        return root1, root2
    else:
        # No real roots
        return None, None

def calculate_values():
    try:
        height = float(height_entry.get())
        initial_phi = float(phi_entry.get())
        initial_c = float(c_entry.get())

        # Calculate for the initial values
        calculate_for_phi_and_c(initial_phi, initial_c, height)

        # Ask for range of c values for sensitivity analysis
        c_range_window = tk.Toplevel(root)
        c_range_window.title("Sensitivity Analysis Range for Cohesion (c)")
        tk.Label(c_range_window, text="Enter the range of c values for sensitivity analysis (e.g., '0,100'):", padx=10, pady=10).pack()
        c_range_entry = tk.Entry(c_range_window)
        c_range_entry.pack()
        c_sensitivity_btn = tk.Button(c_range_window, text="Run Sensitivity Analysis for c", command=lambda: run_sensitivity_analysis(c_range_entry.get(), initial_phi, height, "c"))
        c_sensitivity_btn.pack()

        # Ask for range of phi values for sensitivity analysis
        phi_range_window = tk.Toplevel(root)
        phi_range_window.title("Sensitivity Analysis Range for Angle of Internal Friction (phi)")
        tk.Label(phi_range_window, text="Enter the range of phi values for sensitivity analysis (e.g., '0,45'):", padx=10, pady=10).pack()
        phi_range_entry = tk.Entry(phi_range_window)
        phi_range_entry.pack()
        phi_sensitivity_btn = tk.Button(phi_range_window, text="Run Sensitivity Analysis for phi", command=lambda: run_sensitivity_analysis(phi_range_entry.get(), initial_c, height, "phi"))
        phi_sensitivity_btn.pack()

        plot_lateral_earth_pressure_diagram(initial_phi, initial_c, height)

    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")

def run_sensitivity_analysis(range_str, initial_value, height, parameter):
    try:
        start, end = map(float, range_str.split(','))
        num_values = 10  # You can adjust the number of values as needed

        # Generate a range of parameter values
        parameter_values = np.linspace(start, end, num_values)

        # Perform sensitivity analysis for each parameter value
        embedment_depths = []
        max_moments = []

        for value in parameter_values:
            if parameter == "c":
                depth, moment = calculate_for_phi_and_c(initial_value, value, height)
            elif parameter == "phi":
                depth, moment = calculate_for_phi_and_c(value, initial_value, height)
            embedment_depths.append(depth)
            max_moments.append(moment)

        # Plot sensitivity analysis results
        plt.figure(figsize=(8, 6))
        plt.plot(parameter_values, embedment_depths, label='Embedment Depth')
        plt.plot(parameter_values, max_moments, label='Max Moment')
        if parameter == "c":
            plt.xlabel('Cohesion (kPa)')
        elif parameter == "phi":
            plt.xlabel('Angle of Internal Friction (\u03C6) (degrees)')
        plt.ylabel('Value')
        plt.title('Sensitivity Analysis')
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Invalid range format. Please enter the range in the format 'start,end'.")

def calculate_for_phi_and_c(phi, c, height):
    phi_rad = np.radians(phi)
    Ka = np.tan(np.radians(45) - phi_rad / 2) ** 2
    p1 = 0.5 * ((height ** 2) * Ka * gamma_gransoil)
    z1 = height / 3
    root1, root2 = quadratic_roots(c, height, p1)

    if root1 is None and root2 is None:
        messagebox.showerror("Error", "No positive real root found. Please review your inputs.")
        return None, None

    # Choose the correct root
    if root1 and root1 >= 0:
        D_actual = 1.5 * root1
    elif root2 and root2 >= 0:
        D_actual = 1.5 * root2
    else:
        messagebox.showerror("Error", "No valid root found.")
        return None, None

    # Additional calculations for moment
    sigma6 = (4 * c) - (gamma_gransoil * height)
    M_max_location = p1 / sigma6
    M_max = p1 * (M_max_location + z1) - (sigma6 * (M_max_location ** 2) / 2)

    # Formatting and displaying results
    D_actual_rounded = "{:.3g}".format(D_actual)
    M_max_rounded = "{:.3g}".format(M_max)
    message = f"For phi = {phi} degrees and c = {c} kPa:\n\nRequired Embedment Depth: {D_actual_rounded} meters\n\nMaximum Bending Moment: {M_max_rounded} kilonewton-meters"
    messagebox.showinfo("Results", message)

    return D_actual, M_max

        
def plot_lateral_earth_pressure_diagram(D_actual, p1, sigma6, sigma7, Ka, height, sigma2, c):
    l4 = D_actual * (4 * c - (gamma_gransoil * height) - (0.5 * gamma_gransoil * height ** 2 * Ka)) / 2
    l3 = D_actual - l4
    side_b_small_triangle = l4 - l3  
    rectangle_height = D_actual - l4
    
    # Plotting the lateral earth pressure distribution
    plt.figure(figsize=(8, 6))
    
    # Plotting triangular part of the pressure distribution
    plt.fill_between([0, sigma2], 0, -height, color='lightblue', label='Granular Soil Pressure')
    plt.fill_between([0, -sigma6, 0], -height, -(height+l3), color='lightblue')
    
    # Plotting trapezoidal part of the pressure distribution
    plt.fill_between([-sigma6, sigma7, 0], -(height+l3), -(height + l3 + rectangle_height), color='lightgreen', label='Clay Soil Pressure')

    # Additional lines to indicate key depths
    plt.axhline(y=0, color='grey', linestyle='--', label='Ground Surface')
    plt.axhline(y=-D_actual, color='red', linestyle='--', label='D_actual Depth')
    
    # Annotating key pressures and depths
    plt.text(sigma6 + 1, -(height + l3 / 2), f'Sigma6: {sigma6} kPa', verticalalignment='center')
    plt.text(sigma7 + 1, -(height + l3 + l4 - l3 / 3), f'Sigma7: {sigma7} kPa', verticalalignment='center')
        
    # Customizing plot
    plt.xlabel('Lateral Earth Pressure (kPa)')
    plt.ylabel('Depth (m)')
    plt.title('Lateral Earth Pressure Distribution')
    plt.legend()
    plt.grid(True)
    plt.gca().invert_yaxis()  # Invert y-axis to show depth increasing downwards

    # Call plt.show() only once after all plots are created
    plt.show()

# Sensitivity Analysis on shear strength parameters + their effect on max moment and embedment depth

# GUI setup
root = tk.Tk()
root.title("Sheet Pile Calculator")

tk.Label(root, text="Soil Parameters").pack()
tk.Label(root, text="Enter sheet pile height above the soil (m):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Enter angle of internal friction of the granular soil (degrees):").pack()
phi_entry = tk.Entry(root)
phi_entry.pack()

tk.Label(root, text="Enter the cohesion of the clay layer (kPa):").pack()
c_entry = tk.Entry(root)
c_entry.pack()

calculate_btn = tk.Button(root, text="Calculate", command=calculate_values)
calculate_btn.pack()

root.mainloop()
