import re

# Expression régulière pour IPv4
ipv4_regex = r"^(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9]?\d)){3}$"

# Ouvrir le fichier texte contenant les adresses IP
with open('ip.txt', 'r', encoding='utf-8') as ipfile:
    for line in ipfile:
        ip = line.strip()  # enlever espaces et retours à la ligne
        if re.match(ipv4_regex, ip):
            print(f"{ip} est une adresse IPv4 valide.")
        else:
            print(f"{ip} n'est PAS une adresse IPv4 valide.")
