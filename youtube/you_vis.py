import matplotlib.pyplot as plt
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['youtube_data']
video_collection = db['videos']

# Récupérer les données depuis MongoDB
videos = list(video_collection.find({}, {"_id": 0, "title": 1, "views": 1}))

# Extraire les titres et les vues
titles = [video['title'] for video in videos]
views = [int(video['views']) for video in videos]

# Limiter le nombre de vidéos pour une visualisation claire
titles = titles[:10]  # Les 10 premières vidéos
views = views[:10]

# Création de la courbe
plt.figure(figsize=(10, 6))
plt.plot(titles, views, marker='o', linestyle='-', color='b')

# Ajouter des étiquettes et un titre
plt.title('Nombre de Vues par Vidéo', fontsize=16)
plt.xlabel('Titres des Vidéos', fontsize=12)
plt.ylabel('Nombre de Vues', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotation des titres pour lisibilité
plt.grid(True)

# Afficher la courbe
plt.tight_layout()
plt.show()
