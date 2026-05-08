import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ESP_API_KEY")

response = requests.get(
    "https://developer.sepush.co.za/business/2.0/status",
    headers={"Token": api_key}
)

print(response.status_code)
print(response.json())