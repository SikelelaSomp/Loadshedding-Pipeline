import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("ESP_API_KEY")

response = requests.get(
    "https://developer.sepush.co.za/business/2.0/areas_search?text=durban",
    headers={"Token": API_KEY}
)

print(json.dumps(response.json(), indent=2))