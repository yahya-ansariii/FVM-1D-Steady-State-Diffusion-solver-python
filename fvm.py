import pandas as pd
print("\n\t\t Finite Volume Method for Steady State Diffusion \n")

#Switch case for type of numerical
choice = ""
while choice !="q":
    print("""\t[ 1 ] Diffusion without Source

        [ 2 ] Diffusion with source

        [ q ] Exit\n""")
    choice = input("\n\tEnter Choice :\t") 

    if choice == "1":
        print("Diffusion Withour Source")
        q = 0
        break
    elif choice == "2":
        print("Diffusion with Source")
        q = float(input("\n\tEnter uniform heat generation q in W/m2:   "))
        break
    elif choice == "q":
        exit()
    else :print("\n\n\tInvalid choice, Try again!")


#input from user
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

# add common value to list D beta and alpha
for i in range(2, n-1):
    D[i] = D[1]
    beta[i] = beta[1]
    alpha[i] = alpha[1]

print("\n")

# for i in range(0, n):
#     print("\t D%d is %f \t Beta %d is %f \t Alpha%d is %f \t C%d is %f" %
#           (i+1, D[i], i+1, beta[i], i+1, alpha[i], i+1, c[i]))
#     print("\n")

a = alpha[0]
A[0] = a/D[0]
C[0] = c[0]/D[0]
for i in range(1, n):
    A[i] = alpha[i]/(D[i] - beta[i]*A[i-1])
    C[i] = (beta[i]*C[i-1] + c[i])/(D[i] - beta[i]*A[i-1])

# for i in range(0, n):
#     print("\tA%d = %f \t\t C'%d = %f" % (i+1, A[i], i+1, C[i]))
#     print("\n")
# print("\n")

# Calculating Temperarure values
temp[n-1] = C[n-1]
j = n-2
while j >= 0:
    temp[j] = A[j] * temp[j+1] + C[j]
    j = j-1

# print("Temperature values are:\n")
# for i in range(0, n):
#     print("\t\t T%d = %f C \n" % (i+1, temp[i]))


#Exact Solution and error
A1 = (-q)/(2*tk)
A2 = tb/l - ta/l + (q*l)/(2*tk)
dx = l/n
for i in range (0,n):
    g[i] = dx*0.5 + ( dx *i)
    Texact[i] = A1 * g[i] * g[i] + A2 * g[i] + ta
    Err[i] = ((temp[i] - Texact[i]) *100*2)/ (temp[i] + Texact[i])

OUTPUT = list(zip(beta , D , alpha , c , A , C , temp, Texact, Err))
#create Pandas DataFrame
result = pd.DataFrame(data = OUTPUT, columns = ["\N{GREEK SMALL LETTER BETA}","Diagonal(D)","\N{GREEK SMALL LETTER ALPHA}","Constant(C)","A","C'","Temperature(T)","Temperature Exact(T exact)","% Error"])
#change index to 1,2,3,.....
result.index = result.index + 1

print(result)

