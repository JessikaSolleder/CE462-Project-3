# CE462-Project-3
Cantilever Walls

This program will be completed in Python and aims to acomplish the following:

1. Allow the user to input the shear strength parameters of the soil as well as the height of the sheet pile.
     - c = cohesion and  ϕ = internal friction
3. Check if the height of the sheet pile exceeds the cantilever limit (6 meters).
4. Compute the required embedment depth (actual depth) and maximum moment for the sheet pile.
5. Plot the lateral earth pressure distribution.
6. Perform a sensitivity analysis on the shear strength parameters, altering them within a reasonable range to observe how the embedment depth and maximum moment are affected.
7. Plot the results of the sensitivity analysis.
   
For extra fun the program will aslo do the following:

1. Include the factored moment method
   
Assumptions and methodologies:
- This program covers a scenario where the sheetpiles penetrate granular soil and embeds into a clay layer
- For the lateral earth pressure calculations, the Rankine Theory is utilized
- Actual depth = 1.5 * theoretical depth

  The soil layers are subject to the following assumptions for the purpose of this model. All assumptions are reflected in the provided diagram below.
  
- Granular Soil Layer:
       - Unit weight of the granular soil is assumed to be 20 kN/m^3
       - Assumed to be cohesionless
- Unit weight of the clay soil is assumed to be 24 kN/m^3
       - Unit weight of the clay soil is assumed to be 19 kN/m^3
       - Angle of internal friction assumed to be zero


- ![image](https://github.com/JessikaSolleder/CE462-Project-3/assets/156147848/6778e634-5af6-404e-a758-ab8ada847e2a)



