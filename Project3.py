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
        phi = float(phi_entry.get())
        c = float(c_entry.get())

        # Validation for height
        if height > 6.01:
            messagebox.showerror("Error", "Sheet pile height exceeds cantilever limit (6 meters)")
            return

        # Calculations
        phi_rad = np.radians(phi)
        Ka = np.tan(np.radians(45) - phi_rad / 2) ** 2
        p1 = 0.5 * ((height ** 2) * Ka * gamma_gransoil)
        z1 = height / 3
        root1, root2 = quadratic_roots(c, height, p1)

        if root1 is None and root2 is None:
            messagebox.showerror("Error", "No positive real root found. Please review your inputs.")
            return

        # Choose the correct root
        if root1 and root1 >= 0:
            D_actual = 1.5 * root1
        elif root2 and root2 >= 0:
            D_actual = 1.5 * root2
        else:
            messagebox.showerror("Error", "No valid root found.")
            return

        # Additional calculations for moment
        sigma6 = 0.5 * gamma_claysoil  # Placeholder for sigma6 calculation
        M_max_location = p1 / sigma6
        M_max = p1 * (M_max_location + z1) - (sigma6 * (M_max_location ** 2) / 2)

        # Formatting and displaying results
        D_actual_rounded = "{:.3g}".format(D_actual)
        M_max_rounded = "{:.3g}".format(M_max)
        message = f"Required Embedment Depth: {D_actual_rounded} meters\n\nMaximum Bending Moment: {M_max_rounded} kilonewton-meters"
        messagebox.showinfo("Results", message)

    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")

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
