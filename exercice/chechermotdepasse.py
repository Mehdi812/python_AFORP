special_characters = "\"!@#$%^&*()-+?_=,<>/\""

def main():
   
    def validatepassword():
        valid = True
        pwd = input("Faites entrer votre password :")
                      
        if len(pwd) < 12:
            print("votre mot de passe comporte moins de 12 characteres")
            valid = False
        
        countMaj = sum(1 for c in pwd if c.isupper()) 
        countMin = sum(1 for c in pwd if c.islower())
        countChiffre = sum(1 for c in pwd if c.isdigit())
        coutSpec = sum(1 for c in pwd if c in special_characters)
            
        print("Nombre de Majuscule",countMaj)
        print("Nombre de Miniscule",countMin)
        print("Nombre de numero",countChiffre)
        print("Nombre character Special",coutSpec)
        if valid ==  True:
            print("Mot de Passe correct")
        else:
            print("Mot de Passe faux")
    validatepassword()  

if __name__ == '__main__':
   main()