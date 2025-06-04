import socket
import argparse

def scan_ports(ip, start_port, end_port):
    print(f" Scan de l'IP {ip} de {start_port} à {end_port}...")
    open_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # timeout court pour ne pas bloquer
        try:
            result = s.connect_ex((ip, port))  # retourne 0 si le port est ouvert
            if result == 0:
                print(f" Port {port} ouvert")
                open_ports.append(port)
            s.close()
        except socket.gaierror:
            print(" Adresse IP invalide")
            break
        except socket.timeout:
            print(f" Timeout sur le port {port}")
        except Exception as e:
            print(f" Erreur sur le port {port} : {e}")

    return open_ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner de ports TCP")
    parser.add_argument("--ip", required=True, help="Adresse IP à scanner (ex: 192.168.1.1)")
    parser.add_argument("--start-port", type=int, default=1, help="Port de début (ex: 20)")
    parser.add_argument("--end-port", type=int, default=1024, help="Port de fin (ex: 1024)")
    
    args = parser.parse_args()

    try:
        scan_ports(args.ip, args.start_port, args.end_port)
    except KeyboardInterrupt:
        print("\n Scan interrompu par l'utilisateur.")