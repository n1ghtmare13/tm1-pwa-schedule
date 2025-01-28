import requests
from datetime import datetime
import json
import os

def fetch_and_save_data():
    urls = {
        "schedule.html": "https://planlekcji.staff.edu.pl/plany/o21.html",
        "substitutions.html": "https://zastepstwa.staff.edu.pl/"
    }

    for filename, url in urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Successfully fetched and saved {filename} at {datetime.now()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")


def send_fcm_notification():
    fcm_server_key = os.environ.get("FCM_SERVER_KEY")
    fcm_sender_id = os.environ.get("FCM_SENDER_ID")

    if not fcm_server_key or not fcm_sender_id:
        print("FCM server key or sender ID not found in environment variables.")
        return

    headers = {
        'Authorization': 'key=' + fcm_server_key,
        'Content-Type': 'application/json'
    }

    message = {
        "to": "/topics/all", # wysyła powiadomienie do wszystkich urządzeń
        "notification": {
            "title": "Nowe dane!",
            "body": "Plan lekcji lub zastępstwa zostały zaktualizowane.",
            "icon": "assets/icon.png",
        }
    }

    try:
       response = requests.post("https://fcm.googleapis.com/fcm/send",
                              data=json.dumps(message),
                              headers=headers)
       response.raise_for_status()
       print(f"FCM notification sent successfully: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send FCM notification: {e}")


if __name__ == "__main__":
    fetch_and_save_data()
    send_fcm_notification()
