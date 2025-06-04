import socket
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(ip, port, timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
        s.close()
        return port, (result == 0)
    except Exception:
        return port, False

def scan_ports(ip, start_port, end_port, verbose=False, threads=100):
    open_ports = []
    print(f" Scan de {ip} de {start_port} à {end_port} avec {threads} threads...")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f" Port {port} ouvert")
                open_ports.append(port)
            elif verbose:
                print(f" Port {port} fermé")
    return open_ports

def save_to_file(filename, ip, open_ports):
    if filename.endswith(".csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "Port ouvert"])
            for port in open_ports:
                writer.writerow([ip, port])
    else:
        with open(filename, "w") as f:
            f.write(f"Résultats du scan sur {ip} :\n")
            for port in open_ports:
                f.write(f"Port ouvert : {port}\n")

    print(f"Résultats sauvegardés dans {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner de ports TCP avancé")
    parser.add_argument("--ip", required=True, help="Adresse IP à scanner (ex: 192.168.1.1)")
    parser.add_argument("--start-port", type=int, default=1, help="Port de début")
    parser.add_argument("--end-port", type=int, default=1024, help="Port de fin")
    parser.add_argument("--verbose", action="store_true", help="Afficher aussi les ports fermés")
    parser.add_argument("--output", help="Fichier de sortie (ex: resultats.txt ou .csv)")
    parser.add_argument("--threads", type=int, default=100, help="Nombre de threads pour le scan")

    args = parser.parse_args()

    try:
        open_ports = scan_ports(args.ip, args.start_port, args.end_port, args.verbose, args.threads)
        if args.output:
            save_to_file(args.output, args.ip, open_ports)
    except KeyboardInterrupt:
        print("\n Interruption manuelle du scan.")
