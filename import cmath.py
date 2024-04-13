import cmath
from math import sin
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


# Assumptions
gamma_gransoil = 20  # kN/m^3, unit weight of soil
gamma_claysoil = 24  # kN/m^3, unit weight of soil below groundwater table

def calculate_embedment_depth_and_moment(height, phi, c):

    if height > 6.01:  # Corrected for clarity: 6.1 meters is approximately 20 feet
        messagebox.showerror("Error", "Sheet pile height exceeds cantilever limit (6 meters)")
        return None, None
    phi_rad = np.radians(phi)
    Ka = np.tan(np.radians(45) - phi_rad / 2) ** 2
    sigma2 = gamma_gransoil * height * Ka
    p1 = 0.5 * ((height ** 2)* Ka * gamma_gransoil)
    z1 = height / 3
    # Call quadratic_roots function
    root1, root2 = quadratic_roots(c, height, p1)
    print("Root 1:", root1)
    print("Root 2:", root2)
    return root1, root2, p1

def quadratic_roots(c, height, p1):
    a = 4 * c - gamma_gransoil * height
    b = 2 * p1
    c1 = (p1 * (p1 + 12 * c * (height / 3))) / (gamma_gransoil * height + 2 * c)
    
    # Calculate the discriminant
    discriminant = (b**2) - (4*a*c1)
    
    # Check if the discriminant is positive, negative, or zero
    if discriminant > 0:
        # If the discriminant is positive, there are two real roots
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        return root1, root2
    
    elif discriminant == 0:
        # If the discriminant is zero, there is one real root (a repeated root)
        root = -b / (2*a)
        return root, root
    
    else:
        # If the discriminant is negative, there are two complex roots
        root1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        root2 = (-b - cmath.sqrt(discriminant)) / (2*a)
        return root1, root2


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
        message += f"l4: {l4}"
        messagebox.showinfo("Results", message)
        
        plot_lateral_earth_pressure_diagram(D_actual, l4, sigma6, sigma7, height, sigma2)
        
    except ValueError:
        messagebox.showerror("Error", "Please ensure all inputs are numeric.")
        
        
    
def plot_lateral_earth_pressure_diagram(D_actual, l4, sigma6, sigma7, height, sigma2):
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
    
    #plt.fill_between([0, 0], height, sigma2, color ='purple', label = 'granular')
    # Plotting rectangular part of the pressure distribution
   # plt.fill_between([0, sigma2], 0, height, color='lightblue', label='Granular Soil Pressure')
    
    # Plotting triangular part of the pressure distribution
# Define the vertices of the triangle
    x = [0, sigma2 , 0, 0]  # x-coordinates of the vertices
    y = [0, -height, -height, 0]  # y-coordinates of the vertices

# Plot the triangle
    plt.plot(x, y, color='blue')

# Fill the triangle
    plt.fill_between(x, y, color='lightblue', alpha=0.5)
####TRAPEZOID
# Customize the plot
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Filled Triangle')
    plt.grid(True)

    x = [0, -sigma6 , -sigma6, sigma7, 0]  # x-coordinates of the vertices
    y = [-height, -height, -(height+l3), -(height+l3+l4), -(height +l3+l4)]  # y-coordinates of the vertices

# Plot the triangle
    plt.plot(x, y, color='blue')

# Fill the triangle
    plt.fill_between(x, y, color='lightblue', alpha=0.5)

# Customize the plot
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Filled Triangle')
    plt.grid(True)

# Show the plot
    plt.show()

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
