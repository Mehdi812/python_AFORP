import re
from collections import Counter
import csv
import json
import matplotlib.pyplot as plt


# Ouvrir le fichier auth.log en lecture
with open('auth.log', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Extraire les lignes contenant "Failed password"
failed_lines = [line for line in lines if "Failed password" in line]

# Extraire les adresses IP avec une expression régulière
ip_pattern = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})')
ips = []
for line in failed_lines:
    match = ip_pattern.search(line)
    if match:
        ips.append(match.group(1))

# Compter les occurrences de chaque IP
ip_counts = Counter(ips)

# Afficher les 5 IPs ayant généré le plus d’échecs
for ip, count in ip_counts.most_common(5):
    print(f"{ip}: {count} échecs")





# Préparer les données pour le graphique
top_ips, top_counts = zip(*ip_counts.most_common(5))

plt.figure(figsize=(10, 6))
bars = plt.bar(top_ips, top_counts, color='salmon', label='Échecs de connexion')

plt.xlabel('Adresses IP')
plt.ylabel('Nombre d\'échecs')
plt.title('Top 5 des IPs avec le plus d\'échecs de connexion')
plt.legend()
plt.tight_layout()
plt.show()

# Bonus : Comparer avec les IPs ayant réussi
success_lines = [line for line in lines if "Accepted password" in line]
success_ips = []
for line in success_lines:
    match = ip_pattern.search(line)
    if match:
        success_ips.append(match.group(1))
success_ip_counts = Counter(success_ips)

# Préparer les données pour la comparaison
all_top_ips = list(set(top_ips) | set(success_ip_counts.keys()))
failed = [ip_counts.get(ip, 0) for ip in all_top_ips]
success = [success_ip_counts.get(ip, 0) for ip in all_top_ips]

x = range(len(all_top_ips))
plt.figure(figsize=(12, 7))
plt.bar(x, failed, width=0.4, label='Échecs', align='center', color='salmon')
plt.bar(x, success, width=0.4, label='Réussites', align='edge', color='seagreen')
plt.xticks(x, all_top_ips, rotation=45)
plt.xlabel('Adresses IP')
plt.ylabel('Nombre de tentatives')
plt.title('Comparaison des échecs et réussites par IP')
plt.legend()
plt.tight_layout()
plt.show()

# Créer une liste de dictionnaires pour chaque IP dans all_top_ips
results = []
for ip in all_top_ips:
    results.append({
        'ip': ip,
        'failed': ip_counts.get(ip, 0),
        'success': success_ip_counts.get(ip, 0)
    })

# Exporter au format CSV
with open('ip_attempts.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ip', 'failed', 'success']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

# Exporter au format JSON
with open('ip_attempts.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(results, jsonfile, ensure_ascii=False, indent=4)