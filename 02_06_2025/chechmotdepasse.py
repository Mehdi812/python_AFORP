mot_de_passe = input("Entrez un mot de passe : ")

if len(mot_de_passe) < 12:
    print("Le mot de passe doit contenir au moins 12 caractères.")
elif not any(c.isupper() for c in mot_de_passe):
    print("Le mot de passe doit contenir au moins une lettre majuscule.")
else:
    print("Mot de passe valide.")