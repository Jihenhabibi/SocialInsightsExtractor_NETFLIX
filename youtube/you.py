from pymongo import MongoClient
import requests

# Votre clé API YouTube
API_KEY = "AIzaSyAPWpFgluT875Ll4SIHMacdrsc_Wi3Ug_4"

# ID de la chaîne Netflix
CHANNEL_ID = "UCWOA1ZGywLbqmigxE4Qlvuw"

# Fonction pour obtenir les détails de la chaîne
def get_channel_details(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}'
    response = requests.get(url)
    return response.json()

# Fonction pour obtenir les vidéos récentes d'une chaîne
def get_recent_videos(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&order=date&maxResults=10&type=video&key={API_KEY}'
    response = requests.get(url)
    return response.json()

# Fonction pour obtenir les statistiques d'une vidéo (vues, likes, etc.)
def get_video_stats(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}'
    response = requests.get(url)
    return response.json()

# Configuration de MongoDB
def setup_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['youtube_data']  # Base de données
    return db

# Insérer les données dans MongoDB
def insert_data(db, channel_info, videos_data):
    # Collection pour la chaîne
    channel_collection = db['channels']
    channel_collection.update_one(
        {"_id": CHANNEL_ID},
        {"$set": channel_info},
        upsert=True
    )

    # Collection pour les vidéos
    videos_collection = db['videos']
    for video in videos_data:
        videos_collection.update_one(
            {"_id": video['id']},
            {"$set": video},
            upsert=True
        )

# Récupérer les détails de la chaîne
channel_details = get_channel_details(CHANNEL_ID)

if 'items' in channel_details and len(channel_details['items']) > 0:
    channel = channel_details['items'][0]
    channel_info = {
        "_id": CHANNEL_ID,
        "title": channel['snippet']['title'],
        "description": channel['snippet']['description'],
        "subscribers": channel['statistics'].get('subscriberCount', 'Non disponible'),
        "total_views": channel['statistics'].get('viewCount', 'Non disponible'),
        "total_videos": channel['statistics'].get('videoCount', 'Non disponible')
    }
    print("Détails de la chaîne Netflix récupérés.")
else:
    print("Impossible de récupérer les détails de la chaîne.")
    exit()

# Récupérer les vidéos récentes de la chaîne
videos = get_recent_videos(CHANNEL_ID)
videos_data = []

if 'items' in videos:
    for video in videos['items']:
        video_id = video['id']['videoId']
        title = video['snippet']['title']
        published_at = video['snippet']['publishedAt']

        # Obtenir les statistiques de la vidéo
        stats = get_video_stats(video_id)

        # Vérifier si des statistiques sont disponibles
        if 'items' in stats and len(stats['items']) > 0:
            statistics = stats['items'][0]['statistics']
            views = statistics.get('viewCount', 0)
            likes = statistics.get('likeCount', 0)
            dislikes = statistics.get('dislikeCount', 0)  # Peut ne pas être disponible
        else:
            views = likes = dislikes = 0

        # Ajouter les données de la vidéo
        videos_data.append({
            "id": video_id,
            "title": title,
            "published_at": published_at,
            "views": views,
            "likes": likes,
            "dislikes": dislikes
        })
    print("Détails des vidéos récupérés.")
else:
    print("Aucune vidéo trouvée pour cette chaîne.")
    exit()

# Configurer MongoDB et insérer les données
db = setup_mongo()
insert_data(db, channel_info, videos_data)

print("Les données ont été enregistrées dans MongoDB.")
