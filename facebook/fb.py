import pandas as pd
from pymongo import MongoClient

# Étape 1 : Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Remplacez par l'URI MongoDB si nécessaire
db = client['facebook']  # Nom de la base de données
collection = db['comments']  # Nom de la collection

# Étape 2 : Charger les données depuis le fichier CSV
csv_file = "csv.csv"  # Chemin vers votre fichier CSV
data = pd.read_csv(csv_file, skipinitialspace=True)

# Étape 3 : Renommer les colonnes pour MongoDB (facultatif)
data.columns = [
    col.strip().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").lower()
    for col in data.columns
]

# Étape 4 : Gérer les valeurs manquantes (facultatif)
data.fillna("", inplace=True)

# Étape 5 : Convertir et insérer les données dans MongoDB
records = data.to_dict(orient='records')
collection.insert_many(records)

# Étape 6 : Vérification
print(f"{len(records)} documents insérés dans la base de données MongoDB 'facebook'.")

# Étape 7 : Exemple de lecture des données depuis MongoDB
for comment in collection.find().limit(5):
    print(comment)
