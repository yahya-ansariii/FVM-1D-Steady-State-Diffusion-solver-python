'''   Copyright 2021 MOHAMMED YAHYA ANSARI

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import pandas as pd
import matplotlib.pyplot as plt

print("\n\t\t Finite Volume Method for 1D Steady State Diffusion \n")

# Switch case for type of numerical
choice = ""
while choice != "q":
    print("""\t[ 1 ] Diffusion without Source

        [ 2 ] Diffusion with uniform source

        [ q ] Exit\n""")
    choice = input("\n\tEnter Choice :\t")

    if choice == "1":
        print("\n\t\tDiffusion Without Source\n")
        q = 0
        break
    elif choice == "2":
        print("\n\t\tDiffusion with Uniform Source\n")
        q = float(input("\n\tEnter uniform heat generation q in W/m2:   "))
        break
    elif choice == "q":
        exit()
    else:
        print("\n\n\tInvalid choice, Try again!\n")

# input from user
n = int(input("\n\tEnter the number of grid points:   "))
l = float(input("\n\tEnter length of plate in m:   "))
tk = float(input("\n\tEnter thermal conductivity of plate in W/mK or W/mC:   "))
ta = float(input("\n\tEnter temperature at left face Ta in C:   "))
tb = float(input("\n\tEnter temperature at right face Tb in C:   "))

# create empty list
D = [0]*n
beta = [0]*n
alpha = [0]*n
c = [0]*n
A = [0]*n
C = [0]*n
temp = [0]*n

Err = [0]*n
Texact = [0]*n
g = [0]*n
g1 = [0]*n

# setting up equations in tdma format
dx = l/n
D[0] = (3*tk)/dx
D[1] = (2*tk)/dx
D[n-1] = (3*tk)/dx
beta[1] = tk/dx
alpha[1] = tk/dx
c[0] = ((2*tk*ta)/dx)+(q*dx)

for i in range(1, n-1):
    c[i] = q*dx

c[n-1] = ((2*tk*tb)/dx)+(q*dx)
beta[0] = 0
beta[n-1] = beta[1]
alpha[0] = alpha[1]
alpha[n-1] = 0

# add common value to list D, beta and alpha
for i in range(2, n-1):
    D[i] = D[1]
    beta[i] = beta[1]
    alpha[i] = alpha[1]

# Calculating intermediate terms by forward substitution
for i in range(0, n):
    A[i] = alpha[i]/(D[i] - beta[i]*A[i-1])
    C[i] = (beta[i]*C[i-1] + c[i])/(D[i] - beta[i]*A[i-1])

# equating last value for back substitution
temp[n-1] = C[n-1]
# Calculating Temperarure values by backward substitution
j = n-2
while j >= 0:
    temp[j] = A[j] * temp[j+1] + C[j]
    j = j-1

# Calculating Exact Solution and error
A1 = (-q)/(2*tk)
A2 = tb/l - ta/l + (q*l)/(2*tk)
dx = l/n

for i in range(0, n):
    g[i] = dx*0.5 + (dx * i)
    Texact[i] = A1 * g[i] * g[i] + A2 * g[i] + ta
    Err[i] = ((temp[i] - Texact[i]) * 100*2) / (temp[i] + Texact[i])
    g1[i]=g[i]#create copy of g for excel

# create output tuple
OUTPUT = list(zip(beta, D, alpha, c, A, C, temp, Texact, Err))

# create Pandas DataFrame
result = pd.DataFrame(data=OUTPUT, columns=["\N{GREEK SMALL LETTER BETA}", "Diagonal(D)", "\N{GREEK SMALL LETTER ALPHA}",
                      "Constant(C)", "A", "C'", "Temperature(T)", "Temperature Exact(T exact)", "% Error"])
# change index to 1,2,3,.....
result.index = result.index + 1

# print table
print("\n\n")
print(result)

#plot and show graph
# adding initial and final conditions to the list, as list contains values at nodes
temp.insert(0, ta)
temp.append(tb)
Texact.insert(0, ta)
Texact.append(tb)
g.insert(0, 0)
g.append(l)

graph = pd.DataFrame({'Temperature Numerical': temp, 'Temperature Exact': Texact}, index=g)
# graph.plot()
plt.plot(graph , marker = '.')
plt.title("Temperature-Distance Graph")
plt.xlabel("Distance(m)")
plt.ylabel("Temperature")
plt.grid()
plt.legend(['Temperature Numerical', 'Temperature Exact(Analytical)'])
figure = plt.gcf()
print('''\n********** Plot Graph complete **********

* * * * *   Graph Displayed   * * * * *

*****     Close Graph to Continue     *****\n''')
plt.show()



# save choice
while choice != "q":
    print('''\n\t[ y ] Save result to excel file and graph to png file.
    
        [ q ] Exit without saving result
        ''')
    choice = input("\nEnter your choice :\t")
    if choice == "y":
        result.insert(0, 'Distance(x)', g1)
        result.insert(0, 'Node no.', range(1, 1 + len(result))) #add serial no  column at the start of the DataFrame
        result.to_excel("output/FVM.xlsx", sheet_name = 'Output', index = False) #.to_excel to export excel file
        figure.savefig("output/graph.png") #save graph
        print("\n\n*************** Export complete! Check output folder. ***************\n\n")
        break
    elif choice == "q":
        print("\n***** Result not saved *****")
        break
    else:
        print("\n Invalid Choice, Try again !")


# hold window
input("\n\nPress Enter to Exit")
