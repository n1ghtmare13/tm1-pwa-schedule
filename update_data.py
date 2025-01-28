import requests
from datetime import datetime
import os
import json
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

            # Detect encoding based on file
            if filename == "substitutions.html":
                response.encoding = 'ISO-8859-2'  # Explicitly set encoding for substitutions.html
            else:
                response.encoding = 'UTF-8'  # Default encoding for schedule.html

            text = response.text

            if filename == "substitutions.html":
                soup = BeautifulSoup(text, 'html.parser')

                # Remove existing meta tags with content-type
                for meta in soup.find_all('meta', attrs={'http-equiv': 'Content-Type'}):
                    meta.decompose()

                # Add a UTF-8 meta tag at the top
                utf8_meta = soup.new_tag('meta', **{'http-equiv': 'Content-Type', 'content': 'text/html; charset=UTF-8'})
                soup.head.insert(0, utf8_meta)

                # Usuń stopkę
                footer = soup.find('small')
                if footer:
                  footer.decompose()
                text = soup.prettify()

            elif filename == "schedule.html":
                # Remove inline styles, scripts, and links (bez zmian)
                for tag in soup(['style', 'script', 'link']):
                    tag.decompose()

                # Usuwanie tabeli z klasą 'tabtytul'
                footer_table_tabtytul = soup.find('table', class_='tabtytul')
                if footer_table_tabtytul:
                    print("Znaleziono tabelę z klasą 'tabtytul'. Usuwam ją.")
                    footer_table_tabtytul.extract()
                    print("Usunięto tabelę z klasą 'tabtytul'.")
                else:
                    print("Nie znaleziono tabeli z klasą 'tabtytul'.")
                    
                    
                utf8_meta = soup.new_tag('meta', **{'http-equiv': 'Content-Type', 'content': 'text/html; charset=utf-8'})
                soup.head.insert(0, utf8_meta)
                text = soup.prettify()
            # Save files with proper encoding
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            print(f"Successfully fetched and saved {filename} at {datetime.now()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def send_fcm_notification():
    try:
        service_account_key_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
        if not service_account_key_json:
            print("Firebase service account key not found in environment variables.")
            return

        service_account_key = json.loads(service_account_key_json)

        cred = credentials.Certificate(service_account_key)
        firebase_admin.initialize_app(cred)

        message = messaging.Message(
            notification=messaging.Notification(
                title="Nowe dane!",
                body="Plan lekcji lub zastępstwa zostały zaktualizowane.",
                image="assets/icon.png",
            ),
            topic="all",
        )

        response = messaging.send(message)
        print(f"FCM notification sent successfully: {response}")
    except Exception as e:
        print(f"Failed to send FCM notification: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
    send_fcm_notification()
