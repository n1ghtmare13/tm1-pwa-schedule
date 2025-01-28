import requests
from datetime import datetime
import json
import os
import firebase_admin
from firebase_admin import credentials, messaging
from bs4 import BeautifulSoup

def fetch_and_save_data():
    urls = {
        "schedule.html": "https://planlekcji.staff.edu.pl/plany/o21.html",
        "substitutions.html": "https://zastepstwa.staff.edu.pl/"
    }

    for filename, url in urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8' # Ustawienie UTF-8 dla pobranych danych
            text = response.text # Pobierz tekst odpowiedzi

            if filename == "substitutions.html":  # specjalne traktowanie dla strony z zastępstwami
                soup = BeautifulSoup(text, 'html.parser')
                # Znajdź tag meta z informacją o kodowaniu
                meta_tag = soup.find('meta', attrs={'http-equiv': 'content-type'})

                if meta_tag:
                     # Pobierz kodowanie
                     content = meta_tag.get('content', '').lower()
                     if 'charset=iso-8859-2' in content:
                        # Ustaw poprawne kodowanie (iso-8859-2) i dekoduj do utf-8
                        text = response.text.encode('iso-8859-2', errors='ignore').decode('utf-8', errors='replace')


            with open(filename, "w", encoding="utf-8") as file:  # Zapisz z kodowaniem UTF-8
                file.write(text)
            print(f"Successfully fetched and saved {filename} at {datetime.now()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occured {e}")

def send_fcm_notification():
    try:
        # Pobierz klucz konta usługi z zmiennej środowiskowej
        service_account_key_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
        if not service_account_key_json:
            print("Firebase service account key not found in environment variables.")
            return

        # Parsuj dane json do słownika
        service_account_key = json.loads(service_account_key_json)


        # Zainicjuj Firebase Admin SDK
        cred = credentials.Certificate(service_account_key)
        firebase_admin.initialize_app(cred)

        # Utwórz wiadomość FCM
        message = messaging.Message(
            notification=messaging.Notification(
                title="Nowe dane!",
                body="Plan lekcji lub zastępstwa zostały zaktualizowane.",
                image="assets/icon.png",
            ),
            topic="all",
        )

        # Wyślij wiadomość
        response = messaging.send(message)
        print(f"FCM notification sent successfully: {response}")
    except Exception as e:
        print(f"Failed to send FCM notification: {e}")


if __name__ == "__main__":
    fetch_and_save_data()
    send_fcm_notification()
