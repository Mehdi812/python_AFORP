import random
import string

def generer_mot_de_passe(taille=12) :
    pwd = ""
    caracteres = string.ascii_letters + string.punctuation
    if taille < 12:
        return None
    pwd = ''.join(random.choice(caracteres) for _ in range(taille))
    return pwd
while True:
    try:
        longeur = int(input("saisissez la longeur sougaitée : "))
    except ValueError:
        print("Enrée invalide, Veuillez saisir un nombre entrier")
        continue
    mot_de_passe = generer_mot_de_passe(longeur)
    if mot_de_passe is not None:
        break
    print("la long du mdp doit etre d'au moins 12 cara")

print(f"mdp generer: {mot_de_passe}")