import os
import tweepy
import requests
import time
import logging
import random
import string
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET_KEY,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    bearer_token=TWITTER_BEARER_TOKEN
)

HASHTAGS = {
    "AI": ["AI", "ArtificialIntelligence", "MachineLearning", "DeepLearning", "GPT", "NeuralNetwork", "OpenAI",
           "ChatGPT", "AIGenerated", "AIResearch", "AIRevolution", "FutureAI", "AIForGood", "SuperAI"],
    "CyberSecurity": ["Cybersecurity", "Hacking", "DataBreach", "CyberAttack", "EthicalHacking", "Infosec", "Malware",
                      "Ransomware", "ZeroDay", "Pentesting", "SecurityBreach", "CyberDefense"],
    "SpaceTech": ["NASA", "SpaceX", "Mars", "Satellite", "Rocket", "Starship", "Artemis", "BlueOrigin", "Astrobiology",
                  "Interstellar", "SpaceExploration", "LunarMission", "BlackHole", "Astrophysics", "SpaceInnovation"],
    "QuantumComputing": ["QuantumComputing", "Qubit", "Superposition", "QuantumAI", "QuantumSupremacy", "Schrodinger",
                         "QuantumPhysics", "QuantumTech", "QuantumRevolution"],
    "Gadgets": ["Smartphone", "Laptop", "Wearable", "Smartwatch", "Headset", "GadgetNews", "TechTrends", "FutureTech",
                "5G", "SmartGlasses", "TechGadgets", "BestTech", "VRHeadset", "NextGenTech"],
    "Blockchain": ["Blockchain", "Crypto", "Web3", "Bitcoin", "Ethereum", "NFT", "DeFi", "SmartContracts", "CryptoNews",
                   "Metaverse", "CryptoCommunity", "Decentralization", "BitcoinMining", "Tokenomics"],
    "VRAR": ["VR", "AR", "VirtualReality", "AugmentedReality", "Metaverse", "MixedReality", "Oculus", "HoloLens",
             "VisionPro", "ImmersiveTech", "VRGaming", "ARMarketing"],
    "Robotics": ["Robotics", "AIrobot", "Automation", "BostonDynamics", "AIandRobots", "FutureOfWork", "HumanoidRobot",
                 "SelfDriving", "TeslaBot", "SmartMachines"],
    "Automotive": ["EV", "ElectricVehicle", "Tesla", "AutonomousCars", "SelfDriving", "CarTech", "EVFuture",
                   "Hyperloop", "TeslaCybertruck", "EVMobility"],
    "Innovation": ["TechNews", "Innovation", "TechTrends", "FutureTech", "DisruptiveTech", "Technology", "Breakthrough",
                   "NextBigThing", "HighTech", "TechForGood"]
}

COMPANIES = {
    "Tesla": "#Tesla #EV #AutonomousCars #SelfDriving",
    "SpaceX": "#SpaceX #NASA #Starship #RocketScience",
    "Microsoft": "#Microsoft #Azure #Windows #AI #CloudComputing",
    "Apple": "#Apple #iPhone #MacBook #iOS #VisionPro",
    "Google": "#Google #Android #AI #DeepMind #SearchEngine",
    "Amazon": "#Amazon #AWS #ECommerce #Alexa",
    "Facebook": "#Meta #Facebook #SocialMedia #Metaverse",
    "NVIDIA": "#NVIDIA #AI #GPU #RTX #GamingPC",
    "Samsung": "#Samsung #Galaxy #Smartphones #TechGiant",
    "Intel": "#Intel #Corei9 #Chipset #AIComputing",
    "AMD": "#AMD #Ryzen #GamingCPU #TechHardware",
    "IBM": "#IBM #QuantumComputing #CloudAI #Supercomputing",
    "Twitter": "#Twitter #SocialMedia #TechNews",
    "OpenAI": "#OpenAI #GPT #ArtificialIntelligence #AGI",
    "Sony": "#Sony #PS5 #Gaming #Tech",
    "Huawei": "#Huawei #5G #Smartphones #ChinaTech",
    "Meta": "#Meta #Metaverse #AI #SocialNetworking",
    "Netflix": "#Netflix #Streaming #TechEntertainment",
    "TikTok": "#TikTok #ViralTech #ShortVideos",
    "Snapchat": "#Snapchat #AR #Filters",
    "Discord": "#Discord #GamingCommunity #VoiceChat",
    "BostonDynamics": "#BostonDynamics #Robotics #AIandRobots",
    "Ford": "#Ford #EV #AutomotiveTech",
    "Porsche": "#Porsche #LuxuryCars #EV",
    "Hyundai": "#Hyundai #Mobility #EV",
    "BMW": "#BMW #GermanEngineering #FutureCars",
    "Mercedes": "#MercedesBenz #LuxuryCars #AutonomousDriving",
    "Rivian": "#Rivian #ElectricTrucks #FutureEV"
}

DEFAULT_HASHTAGS = [
    "#TechNews", "#FutureTech", "#Innovation", "#AI", "#BigTech", "#TrendingTech", "#Gadgets",
    "#CyberSecurity", "#Science", "#SpaceTech", "#TechWorld", "#QuantumComputing"
]

LAST_TWEET_FILE = "last_tweet.txt"

def was_already_tweeted(url):
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r") as f:
            last_url = f.read().strip()
            return last_url == url
    return False

def save_last_tweet(url):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(url)

def get_hashtags(title):
    base_tags = DEFAULT_HASHTAGS[:]
    for tag, keywords in HASHTAGS.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            base_tags.append(f"#{tag}")
    company_tags = [COMPANIES[name] for name in COMPANIES if name.lower() in title.lower()]
    all_tags = list(set(base_tags + company_tags))
    return " ".join(random.sample(all_tags, min(6, len(all_tags))))

def generate_dynamic_hashtag(description):
    if not description:
        return None
    words = description.split()
    clean_words = []
    for w in words:
        w_clean = w.strip(string.punctuation).lower()
        if len(w_clean) >= 5 and not w_clean.isdigit():
            clean_words.append(w_clean)
    if not clean_words:
        return None
    chosen_word = random.choice(clean_words)
    if chosen_word.startswith("#"):
        return chosen_word
    return f"#{chosen_word.capitalize()}"

def get_tech_news():
    logging.info("Fetching latest Tech news...")
    keywords = (
        "technology OR AI OR robotics OR space OR quantum computing OR "
        "cybersecurity OR gadgets OR blockchain OR web3 OR innovation"
    )
    sources = "the-verge,ars-technica,techcrunch,engadget,wired,cnet,ieee-spectrum"
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={keywords}&sources={sources}&sortBy=publishedAt&pageSize=3&language=en&apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        valid_articles = [a for a in articles if a.get("title") and a.get("url")]
        logging.info(f"Found {len(valid_articles)} relevant Tech news.")
        return valid_articles
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []

def post_tweet():
    articles = get_tech_news()
    if not articles:
        logging.info("No relevant news found. Skipping tweet.")
        return
    article = articles[0]
    article_url = article["url"]
    if was_already_tweeted(article_url):
        logging.info("News already posted. Skipping.")
        return
    hashtags = get_hashtags(article["title"])
    dynamic_tag = generate_dynamic_hashtag(article.get("description", ""))
    if dynamic_tag:
        hashtags += f" {dynamic_tag}"
    tweet_text = f"{article['title']}\n{article_url}\n{hashtags}"
    try:
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data["id"]
        logging.info(f"Tweet posted: https://twitter.com/your_account/status/{tweet_id}")
        save_last_tweet(article_url)
    except tweepy.TweepyException as e:
        logging.error(f"Error posting tweet: {e}")

if __name__ == "__main__":
    while True:
        post_tweet()
        sleep_time = 10800
        logging.info(f"Waiting {sleep_time / 3600:.1f} hours before next tweet.")
        time.sleep(sleep_time)
