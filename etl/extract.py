import requests
import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

API_KEY = os.getenv("ESP_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def fetch_status():
    response = requests.get(
        "https://developer.sepush.co.za/business/2.0/status",
        headers={"Token": API_KEY}
    )
    response.raise_for_status()
    return response.json()


def save_raw(data):
    os.makedirs("raw_backup", exist_ok=True)
    filename = f"raw_backup/status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Raw backup saved to {filename}")


def load_to_db(data):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    for area_key, area_data in data["status"].items():
        cur.execute("""
            INSERT INTO raw.stage_events (
                area_key,
                area_name,
                stage,
                stage_updated,
                next_stages,
                retrieved_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (area_key, stage_updated) DO NOTHING
        """, (
            area_key,
            area_data["name"],
            int(area_data["stage"]),
            area_data["stage_updated"],
            json.dumps(area_data["next_stages"]),
            datetime.now(timezone.utc)
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded to raw.stage_events")


if __name__ == "__main__":
    data = fetch_status()
    save_raw(data)
    load_to_db(data)