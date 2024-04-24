# CE462-Project-3
Cantilever Walls: Project Memo

Hello Dr. Hudyma, you may notice that this project is a bit different than the one I mentioned in my memo on Canvas. I was struggling so much with this program and after meeting with you for office hours and talking to the python programmers at my work I still hitting walls! So I decided I had to move on for the sake of time and submit what I had. However I got a lot of work done last week and this project was begging me to readdress it. I decided to completely start over and use the fully granular scenario. This worked a lot better, and a fresh start seemed to help me approach this in a better way. I believe in office hours with you, you mentioned that it didn't matter when we finished this so long as it was by May 1st, but the assignment was closed when I went to resubmit it. However I have made this README.md to serve as a standard project overview as per usual, but also a new project memo. I hope that is okay, if not I completely understand.

PROJECT OVERVIEW:
This program will be completed in Python and aims to accomplish the following:

1. Allow the user to input the shear strength parameter, angle of internal frition (ϕ) of the soil as well as the height of the sheet pile above the dredge line. 
3. Check if the height of the sheet pile exceeds the cantilever limit (6 meters).
4. Compute the required embedment depth (actual depth) and maximum moment for the sheet pile.
5. Plot the lateral earth pressure distribution.
6. Perform a sensitivity analysis on the specified shear strength parameter (ϕ),  within a reasonable range to observe how the embedment depth and maximum moment are affected.
7. Plot the results of the sensitivity analysis.
   
For extra fun the program will also do the following:

1. Include the factored moment method
   
Assumptions and methodologies:
- This program covers a scenario where the sheetpiles penetrates and embeds in granular soil
- For the lateral earth pressure calculations, the Rankine Theory is utilized
- Actual depth = 1.3 ( l3 + l4)
- There is no groundwater table accounted for in this model
- Unit weight of the granular soil is assumed to be 20 kN/m^3
- Soil is assumed to be cohesionless

A basic diagram of the type of scenario the model seeks to represent can be seen below:

![image](https://github.com/JessikaSolleder/CE462-Project-3/assets/156147848/656dec7f-3a4b-49b4-a17e-94ee2573b339)


This project performed a sensitivity analysis comparing a change in the internal friction and its impact on the maximum moment and embedment depth as seen in the figures below. For both analyses, it can be seen that an increased angle of internal friction will cause in increase in maximum moment as well as required embedment depth. This model performs this test on a range from 2 to 50 degrees and runs the analysis over 40 points incrementally between this range. Increasing the model may have an effect on the relationship between the factors aforementioned, but it is unlikely. 

This project also will present the user with a pop-up window that presents the passive and active factored moment based on user inputs. This should appear after the pressure diagram is exited.

![image](https://github.com/JessikaSolleder/CE462-Project-3/assets/156147848/096737d4-a519-4d22-8c5c-a204535ec70f)

![image](https://github.com/JessikaSolleder/CE462-Project-3/assets/156147848/67e987c8-3ee8-470d-8872-f29d85da3cd2)






