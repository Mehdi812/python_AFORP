import os
import psutil
import time
import platform
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# === Dossiers & Fichiers ===
EXPORT_DIR = "TP6/system_monitor_export"
os.makedirs(EXPORT_DIR, exist_ok=True)

CSV_FILE = os.path.join(EXPORT_DIR, "system_metrics.csv")
GRAPH_FILE = os.path.join(EXPORT_DIR, "system_graphs.png")
HTML_REPORT = os.path.join(EXPORT_DIR, "system_report.html")

# === Initialisation du CSV ===
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "mem_used_GB", "mem_total_GB", "bytes_sent_MB", "bytes_recv_MB"])

# === Fonctions utilitaires ===
def ascii_bar(percent, length=20):
    filled = int(length * percent / 100)
    return "[" + "#" * filled + "-" * (length - filled) + "]"

def collect_and_log_metrics():
    timestamp = datetime.now().isoformat(timespec='seconds')
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()
    mem_used = mem.used / 1e9
    mem_total = mem.total / 1e9
    bytes_sent = net.bytes_sent / 1e6
    bytes_recv = net.bytes_recv / 1e6

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, cpu, mem_used, mem_total, bytes_sent, bytes_recv])

    return cpu, mem_used, mem_total, bytes_sent, bytes_recv

def collect_full_snapshot():
    lines = []
    lines.append("=== CPU Usage ===")
    total_cpu = psutil.cpu_percent()
    per_cpu = psutil.cpu_percent(percpu=True)
    for i, percent in enumerate(per_cpu):
        lines.append(f"Core {i}: {ascii_bar(percent)} {percent:.1f}%")
    lines.append(f"Total: {ascii_bar(total_cpu)} {total_cpu:.1f}%\n")

    mem = psutil.virtual_memory()
    lines.append("=== Memory ===")
    lines.append(f"Total: {mem.total / 1e9:.2f} GB")
    lines.append(f"Used:  {mem.used / 1e9:.2f} GB")
    lines.append(f"Free:  {mem.available / 1e9:.2f} GB\n")

    lines.append("=== Disk Usage ===")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            lines.append(f"{part.device} ({part.mountpoint}) - Total: {usage.total / 1e9:.2f} GB, "
                         f"Used: {usage.used / 1e9:.2f} GB, Free: {usage.free / 1e9:.2f} GB")
        except PermissionError:
            continue
    lines.append("")

    net = psutil.net_io_counters()
    lines.append("=== Network I/O ===")
    lines.append(f"Bytes Sent:     {net.bytes_sent / 1e6:.2f} MB")
    lines.append(f"Bytes Received: {net.bytes_recv / 1e6:.2f} MB")
    lines.append(f"Packets Sent:   {net.packets_sent}")
    lines.append(f"Packets Received: {net.packets_recv}\n")

    lines.append("=== Network per Interface ===")
    for iface, stats in psutil.net_io_counters(pernic=True).items():
        lines.append(f"{iface} - Sent: {stats.bytes_sent / 1e6:.2f} MB, Received: {stats.bytes_recv / 1e6:.2f} MB")

    lines.append("\nPress Ctrl+C to exit...\n")
    return "\n".join(lines)

def generate_report():
    df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), tight_layout=True)

    axs[0].plot(df["timestamp"], df["cpu_percent"], label="CPU (%)", color="blue")
    axs[0].set_title("Utilisation CPU (%)")
    axs[0].set_ylabel("%")

    axs[1].plot(df["timestamp"], df["mem_used_GB"], label="Mémoire utilisée", color="green")
    axs[1].plot(df["timestamp"], df["mem_total_GB"], label="Mémoire totale", linestyle="--", color="gray")
    axs[1].set_title("Utilisation mémoire (GB)")
    axs[1].set_ylabel("GB")
    axs[1].legend()

    axs[2].plot(df["timestamp"], df["bytes_sent_MB"], label="Envoyé (MB)", color="red")
    axs[2].plot(df["timestamp"], df["bytes_recv_MB"], label="Reçu (MB)", color="orange")
    axs[2].set_title("Activité réseau")
    axs[2].set_ylabel("MB")
    axs[2].legend()

    plt.xticks(rotation=45)
    plt.savefig(GRAPH_FILE)
    plt.close()

    with open(HTML_REPORT, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head>
            <title>Rapport Système</title>
        </head>
        <body>
            <h1>Rapport de Surveillance Système</h1>
            <p>Mis à jour : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <img src="system_graphs.png" alt="Graphiques système" style="width:100%;"/>
            <h2>Résumé</h2>
            <ul>
                <li>Échantillons : {len(df)}</li>
                <li>CPU moyen : {df['cpu_percent'].mean():.2f}%</li>
                <li>RAM moyenne utilisée : {df['mem_used_GB'].mean():.2f} GB</li>
                <li>Réseau envoyé : {df['bytes_sent_MB'].iloc[-1] - df['bytes_sent_MB'].iloc[0]:.2f} MB</li>
                <li>Réseau reçu : {df['bytes_recv_MB'].iloc[-1] - df['bytes_recv_MB'].iloc[0]:.2f} MB</li>
            </ul>
        """)

def generate_report_with_snapshot():
    generate_report()
    snapshot = collect_full_snapshot()
    snapshot_html = snapshot.replace(" ", "&nbsp;").replace("\n", "<br>")
    with open(HTML_REPORT, "a", encoding="utf-8") as f:
        f.write(f"""
        <h2>État système instantané</h2>
        <pre style="background:#f8f8f8; padding:10px; border:1px solid #ccc;">{snapshot_html}</pre>
        </body></html>
        """)

def run_monitor(duration_sec=60, interval=5):
    start_time = time.time()
    try:
        while time.time() - start_time < duration_sec:
            cpu, mem_used, mem_total, sent, recv = collect_and_log_metrics()
            snapshot = collect_full_snapshot()
            print(snapshot)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n Surveillance arrêtée par l'utilisateur.")
    generate_report_with_snapshot()
    print(f"\n Rapport HTML généré : {HTML_REPORT}")

if __name__ == "__main__":
    run_monitor(duration_sec=60, interval=5)
