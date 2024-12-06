import requests
from pymongo import MongoClient

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPMxxQEAAAAAUAi%2FrAovXgD7gCmxL1czFmrjzUo%3DiU7bXfXAg3T2at70dZkyUwSd2L3pSwqztXgN9UbvLeVO2Np2hw"


USERNAME = "netflix"
 # Endpoint pour récupérer les tweets
BASE_URL = "https://api.twitter.com/2"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# Fonction pour récupérer l'ID d'un utilisateur à partir de son username
def get_user_id(username):
    url = f"{BASE_URL}/users/by/username/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

# Fonction pour récupérer les tweets d'un utilisateur
def get_tweets(user_id, max_results=5):
    url = f"{BASE_URL}/users/{user_id}/tweets"
    params = {"max_results": max_results, "tweet.fields": "created_at,public_metrics"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return []

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["TwitterDB"]
collection = db["Tweets"]

# Processus principal
if __name__ == "__main__":
    print("Authentification réussie!")
    user_id = get_user_id(USERNAME)
    if user_id:
        print(f"ID de l'utilisateur {USERNAME}: {user_id}")
        tweets = get_tweets(user_id, max_results=50)
        if tweets:
            print("\n--- Tweets récupérés ---\n")
            for tweet in tweets:
                # Extraire les informations du tweet
                text = tweet.get("text", "Texte non disponible")
                created_at = tweet.get("created_at", "Date inconnue")
                metrics = tweet.get("public_metrics", {})
                likes = metrics.get("like_count", 0)
                retweets = metrics.get("retweet_count", 0)

                # Affichage dans le terminal
                print(f"Tweet : {text}")
                print(f"Likes : {likes} - Retweets : {retweets}")
                print(f"Date de création : {created_at}")
                print("-" * 50)

                # Stocker dans MongoDB
                collection.insert_one(tweet)
            print("\nLes tweets ont été stockés dans MongoDB.")
        else:
            print("Aucun tweet trouvé.")
    else:
        print("Impossible de récupérer l'ID de l'utilisateur.")