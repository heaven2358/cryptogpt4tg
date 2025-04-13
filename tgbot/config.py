from collections import defaultdict, deque
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AI_ORACLE_API_TEMPLATE = (
    "https://api-ai-oracle.apro.com/v1/ticker/currency/price?name={name}&quotation=usd&type=median"
)

user_contexts = defaultdict(lambda: deque(maxlen=50))
