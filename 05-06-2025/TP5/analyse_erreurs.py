import re
import sys
import pandas as pd
import matplotlib.pyplot as plt

# 1. Parsing avec user_agent extrait manuellement
def parse_logs(filename):
    pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3}) "(?P<user_agent>[^"]*)"'
    )
    records = []

    with open(filename, encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                data = match.groupdict()
                records.append(data)

    df = pd.DataFrame(records)
    return df

# 2. Filtrer les erreurs 404
def filter_404(df):
    df_404 = df[df['status'] == '404']
    print(f"Nombre d'erreurs 404 : {len(df_404)}")
    return df_404

# 3. Top 5 des IPs générant le plus d’erreurs 404
def top_5_ips(df_404):
    top_ips = df_404['ip'].value_counts().head(5)
    print("Top 5 IPs générant des erreurs 404 :")
    print(top_ips)
    return top_ips

# 4. Visualisation
def plot_top_ips(top_ips):
    plt.figure(figsize=(8,5))
    top_ips.plot(kind='bar', color='tomato')
    plt.title("Top 5 IPs générant des erreurs 404")
    plt.xlabel("Adresse IP")
    plt.ylabel("Nombre d'erreurs 404")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# 5. Détection de bots
def detect_bots(df_404):
    bot_keywords = ['bot', 'crawler', 'spider']
    mask = df_404['user_agent'].str.lower().str.contains('|'.join(bot_keywords), na=False)
    bots_df = df_404[mask]
    print(f"Nombre d'erreurs 404 provenant de bots : {len(bots_df)}")
    print("Exemple d'IPs suspectes (bots) :")
    print(bots_df['ip'].value_counts().head())
    percent_bots = 100 * len(bots_df) / len(df_404) if len(df_404) > 0 else 0
    print(f"Pourcentage d'erreurs 404 provenant de bots : {percent_bots:.2f}%")
    return bots_df, percent_bots

# 6. Main avec argument
def main():
    if len(sys.argv) != 2:
        print("Usage: python analyse_erreurs.py weblog.log")
        sys.exit(1)

    log_path = sys.argv[1]
    df = parse_logs(log_path)
    df_404 = filter_404(df)
    top_ips = top_5_ips(df_404)
    plot_top_ips(top_ips)
    bots_df, percent_bots = detect_bots(df_404)

if __name__ == "__main__":
    main()
