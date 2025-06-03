import re
import csv

# Expression régulière IPv4
ipv4_regex = r"^(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4][0-9]|1\d{2}|[1-9]?\d)){3}$"

# ^
#    (25[0-5]           -> 250-255
#   |2[0-4][0-9]        -> 200-249
#   |1\d{2}             -> 100-199
#   |[1-9]?\d)          -> 0-99 (sans zéros en tête)
# (\. ... ){3}          -> trois autres nombres identiques
# $

# Liste des adresses à tester
ip_addresses = [
    "192.168.1.1",
    "10.0.0.255",
    "172.16.254.1",
    "abc.def.ghi.jkl",
    "256.256.256.256",
    "192.168.1.",
    "192.168.1.01",
    "0.0.0.0"
]


for ip in ip_addresses:
    if re.match(ipv4_regex, ip):
        print(f"{ip} est une adresse IPv4 valide.")
    else:
        print(f"{ip} n'est PAS une adresse IPv4 valide.")
