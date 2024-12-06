from pymongo import MongoClient
import matplotlib.pyplot as plt

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["TwitterDB"]
collection = db["Tweets"]

# Fonction pour récupérer les tweets stockés
def fetch_tweets_from_db():
    tweets = list(collection.find())
    if not tweets:
        print("Aucun tweet trouvé dans la base de données.")
        return []
    return tweets

# Fonction pour tracer la courbe des likes
def plot_likes_from_db(tweets):
    # Extraire les textes et le nombre de likes
    texts = [tweet.get("text", "Tweet")[:30] + "..." for tweet in tweets]  # Texte limité à 30 caractères
    likes = [tweet.get("public_metrics", {}).get("like_count", 0) for tweet in tweets]

    # Tracer la courbe
    plt.figure(figsize=(10, 6))
    plt.plot(texts, likes, marker="o", linestyle="-", color="blue", label="Nombre de likes")
    plt.xlabel("Tweets")
    plt.ylabel("Nombre de likes")
    plt.title("Nombre de likes par tweet depuis la base de données")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Processus principal
if __name__ == "__main__":
    print("Extraction des données depuis TwitterDB...")
    tweets = fetch_tweets_from_db()
    if tweets:
        print(f"{len(tweets)} tweets récupérés depuis la base de données.")
        plot_likes_from_db(tweets)
