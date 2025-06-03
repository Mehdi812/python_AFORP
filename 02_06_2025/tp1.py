import random

mot_de_passe = ["123456", "password", "admin", "123456789", "qwerty", "abc123", "letmein", "welcome", "monkey", "football"]
password = random.choice(mot_de_passe)
essais = 0

while True:
    entree_user = input("Devinez quel est le mot de passe -_- : ")
    essais += 1
    if entree_user == password:
        print(f"Bien joué ! Vous avez trouvé en {essais} essai(s).")
        break
    else:
        if len(entree_user) < len(password):
            print("Le mot de passe est plus long.")
        elif len(entree_user) > len(password):
            print("Le mot de passe est plus court.")
        else:
            print("Le mot de passe a la même longueur.")

        # 1ere lettre
        if entree_user and password and entree_user[0] == password[0]:
            print("Le mot de passe commence par la même lettre.")

        # lettres communes
        lettres_communes = set(entree_user) & set(password)
        print(f"Nombre de lettres communes : {len(lettres_communes)}")
