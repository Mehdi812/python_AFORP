def calculatrice() :
    print("bienvenue dans la calculatrice")
    print("vous pouvez eff les op suivantes : ")
    print("option : +, -, *, /")
    op = input(("op ?"))
    a = float(input("entrer le premier nombre"))
    b = float(input("entrer le 2eme nombre"))
    
    if op =="+":
        print(f"resultat : {a + b}")
    elif op =="-":
        print(f"resultat : {a - b}")
    elif op=="*":
        print(f"resultat : {a * b}")
    elif op== "/":
        print(f"resultat : {a / b}")

calculatrice()