import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
csv_file = "csv.csv"  # Remplacez par le chemin vers votre fichier CSV
data = pd.read_csv(csv_file)

# Nettoyer les données
data.fillna("", inplace=True)  # Remplir les valeurs manquantes avec des chaînes vides
data["Likes"] = pd.to_numeric(data["Likes"], errors="coerce").fillna(0)  # Convertir les likes en nombres
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")  # Convertir les dates en format datetime

# Grouper par date et compter le nombre de commentaires et de likes
grouped_data = data.groupby(data["Date"].dt.date).agg(
    likes_total=("Likes", "sum"),  # Total des likes par jour
    comments_total=("Comment", "count")  # Nombre de commentaires par jour
).reset_index()

# Tracer la courbe
plt.figure(figsize=(12, 6))
plt.plot(grouped_data["Date"], grouped_data["likes_total"], color="red", label="Nombre de Likes")
plt.plot(grouped_data["Date"], grouped_data["comments_total"], color="green", label="Nombre de Commentaires")

# Personnalisation du graphique
plt.title("Nombre de Likes et de Commentaires par Date", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Nombre", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)

# Afficher le graphique
plt.tight_layout()
plt.show()
