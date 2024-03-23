import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


# Assumptions
gamma_gransoil = 10  # kN/m^3, unit weight of soil
gamma_claysoil = 19  # kN/m^3, unit weight of soil below groundwater table


def calculate_embedment_depth_and_moment(height, phi, c):

    if height > 6.01:  # Corrected for clarity: 6.1 meters is approximately 20 feet
        messagebox.showerror("Error", "Sheet pile height exceeds cantilever limit (6 meters)")
        return None, None
    phi_rad = np.radians(phi)
    Ka = np.tan(np.radians(45) - phi_rad / 2) ** 2
    sigma2 = gamma_gransoil * height * Ka
    p1 = (0.5 * ((height ** 2)* ( Ka) * (gamma_gransoil)))
    z1 = (height / 3)
    #breaking down D positive into smaller pieces to solve
    sqrt_term = np.sqrt(((8*c)**2)*p1*z1 - (2*c*height*p1*gamma_gransoil*z1) + (c * p1**2))
    denominator = np.sqrt((2 * c) + (height*gamma_gransoil))
    numerator = p1 + (((6 ** 0.5) * sqrt_term) / denominator)
    D_positive = numerator / ((4 * c) - (height * gamma_gransoil))
    L4 = D_positive * ((4*c) - (gamma_gransoil * height) - (0.5 * gamma_gransoil * height ** 2 * Ka)) / (4 * c)
    sigma6 = (4*c) - (gamma_gransoil * height)
    sigma7 = (4*c) + (gamma_gransoil * height)
    D_actual = 1.5 * D_positive
    z_prime = (p1 / sigma6) # location of the maximum bending moment
    M_max = (p1* (z_prime + z1)) - ((sigma6 * (z_prime ** 2)) / 2) # converted to Newtons from kiloNewtons
    print(type(D_positive), D_positive)
    return M_max, p1, z1, D_positive, L4, sigma2, sigma6, sigma7, D_actual, z_prime
    


def on_calculate():
    try:
        height = float(height_entry.get())
        phi = float(phi_entry.get())
        c = float(c_entry.get())
        
        results = calculate_embedment_depth_and_moment(height, phi, c)
        D_actual = results[8]  # Assuming D_positive is the fourth item in the tuple
        D_actual_rounded = "{:.3g}".format(D_actual)
        messagebox.showinfo("Result", f"The actual depth of penetration for your wall is approximately: {D_actual_rounded} meters")

        M_max = results[0]
        M_max_rounded = "{:.3g}".format(M_max)
        messagebox.showinfo("Result", f"The maximum moment for your wall is approximately: {M_max_rounded} kilonewton meters")
        
    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")

root = tk.Tk()
root.title("Sheet Pile Calculator")

# Granular Soil Inputs
tk.Label(root, text="Soil Parameters").pack()

tk.Label(root, text="Enter sheet pile height (m):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Enter angle of internal friction of the granular soil (degrees):").pack()
phi_entry = tk.Entry(root)
phi_entry.pack()

tk.Label(root, text="Enter the cohesion of the clay layer (kPa):").pack()
c_entry = tk.Entry(root)
c_entry.pack()

calculate_btn = tk.Button(root, text="Calculate", command=on_calculate)
calculate_btn.pack()

root.mainloop()