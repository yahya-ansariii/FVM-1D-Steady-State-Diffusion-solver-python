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
