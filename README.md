# python_AFORP
# TP3

## Fonctionnalités

- Scan d'une plage de ports d'une IP donnée
- Version multithreadée pour plus de rapidité
- Option `--verbose` pour afficher les ports fermés
- Sauvegarde des ports ouverts dans un fichier `.txt` ou `.csv`

## Exemples d’utilisation

## Scan rapide
python TP.3.py --ip 127.0.0.1 --start-port 1 --end-port 100

## Scan verbeux (voir aussi les ports fermés)
python TP.3.py --ip 192.168.1.1 --start-port 20 --end-port 80 --verbose

## Scan + sauvegarde CSV
python TP.3.py --ip 192.168.1.1 --start-port 1 --end-port 100 --output resultat.csv