from math import sin
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
    if D_positive <= 0:
        messagebox.showerror("Error", "Calculated embedment depth is non-positive. Please check your inputs.")
        return None, None
    l4 = D_positive * ((4*c) - (gamma_gransoil * height) - (0.5 * gamma_gransoil * height ** 2 * Ka)) / (4 * c)
    sigma6 = (4*c) - (gamma_gransoil * height)
    sigma7 = (4*c) + (gamma_gransoil * height)
    D_actual = 1.5 * D_positive
    z_prime = (p1 / sigma6) # location of the maximum bending moment
    M_max = (p1* (z_prime + z1)) - ((sigma6 * (z_prime ** 2)) / 2) 
    print(type(D_positive), D_positive)
    return M_max, p1, z1, D_positive, l4, sigma2, sigma6, sigma7, D_actual, z_prime

def on_calculate():
    try:
        height = float(height_entry.get())
        phi = float(phi_entry.get())
        c = float(c_entry.get())
        
        results = calculate_embedment_depth_and_moment(height, phi, c)
        D_actual = results[8]  # Assuming D_actual is the ninth item in the tuple
        M_max = results[0]  # M_max is the first item in the tuple
        
        if results is None:  # Check if results are None, which indicates an error
            return

        # Unpacking results
        M_max, p1, z1, D_positive, l4, sigma2, sigma6, sigma7, D_actual, z_prime = results

        # Formatting values to 3 significant figures
        D_actual_rounded = "{:.3g}".format(D_actual)
        M_max_rounded = "{:.3g}".format(M_max)

        # Creating the message
        message = f"Required Embedment Depth: {D_actual_rounded} meters\n\n"
        message += f"Maximum Bending Moment: {M_max_rounded} kilonewton-meters"

        messagebox.showinfo("Results", message)
        
        plot_lateral_earth_pressure_diagram(D_actual, l4, sigma6, sigma7, height)
        
    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")
        
        
    
def plot_lateral_earth_pressure_diagram(D_actual, l4, sigma6, sigma7, height):
    l3 = D_actual - l4
    side_b_small_triangle = l4 - l3  
    
    # Calculating geometrical points for visualization
    pp_clay_rectangle = l3 * sigma6
    pp_clay_triangle = 0.5 * sigma6 * D_actual * side_b_small_triangle
    d_pp_clay_resultant_depth = height + (((1/3) * side_b_small_triangle) + (l3 / 2))
    pa_clay = 0.5 * sigma7 * (l4 - side_b_small_triangle)
    d_pa_clay_resultant_depth = (height + D_actual) - ((l4 - side_b_small_triangle) * (1/3))
    
    # Plotting the lateral earth pressure distribution
    plt.figure(figsize=(6, 8))
    
    # Plotting rectangular part of the pressure distribution
    plt.fill_between([0, sigma6], height, height + l3, color='lightblue', label='Granular Soil Pressure')
    
    # Plotting triangular part of the pressure distribution
    plt.fill_between([0, sigma7], height + l3, height + D_actual, color='lightgreen', label='Clay Soil Pressure')
    
    # Additional lines to indicate key depths
    plt.axhline(y=height, color='grey', linestyle='--', label='Ground Surface')
    plt.axhline(y=height + D_actual, color='red', linestyle='--', label='D_actual Depth')
    
    # Annotating key pressures and depths
    plt.text(sigma6 + 1, height + l3 / 2, f'Sigma6: {sigma6} kPa', verticalalignment='center')
    plt.text(sigma7 + 1, height + D_actual - (l4 - l3) / 3, f'Sigma7: {sigma7} kPa', verticalalignment='center')
    
    # Customizing plot
    plt.xlabel('Lateral Earth Pressure (kPa)')
    plt.ylabel('Depth (m)')
    plt.title('Lateral Earth Pressure Distribution')
    plt.legend()
    plt.grid(True)
    plt.gca().invert_yaxis()  # Invert y-axis to show depth increasing downwards
    plt.show()
    

    
root = tk.Tk()
root.title("Sheet Pile Calculator")

# Granular Soil Inputs
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

calculate_btn = tk.Button(root, text="Calculate", command=on_calculate)
calculate_btn.pack()

root.mainloop()