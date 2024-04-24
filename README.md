# CE462-Project-3
Cantilever Walls

This program will be completed in Python and aims to accomplish the following:

1. Allow the user to input the shear strength parameter, angle of internal frition (ϕ) of the soil as well as the height of the sheet pile above the dredge line. 
3. Check if the height of the sheet pile exceeds the cantilever limit (6 meters).
4. Compute the required embedment depth (actual depth) and maximum moment for the sheet pile.
5. Plot the lateral earth pressure distribution.
6. Perform a sensitivity analysis on the specified shear strength parameter (ϕ),  within a reasonable range to observe how the embedment depth and maximum moment are affected.
7. Plot the results of the sensitivity analysis.
   
For extra fun the program will aslo do the following:

1. Include the factored moment method
   
Assumptions and methodologies:
- This program covers a scenario where the sheetpiles penetrates and embeds in granular soil
- For the lateral earth pressure calculations, the Rankine Theory is utilized
- Actual depth = 1.3 ( l3 + l4)
- There is no groundwater table accounted for in this model
- Unit weight of the granular soil is assumed to be 20 kN/m^3
- Assumed to be cohesionless

A basic diagram of the type of scenario the model seeks to represent can be seen below:

![image](https://github.com/JessikaSolleder/CE462-Project-3/assets/156147848/656dec7f-3a4b-49b4-a17e-94ee2573b339)




