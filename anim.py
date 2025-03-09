import requests
from bs4 import BeautifulSoup
import os
from duckduckgo_search import DDGS
import time  # Dodano moduł time

# Tworzenie obiektu DDGS
ddgs = DDGS()

# Ściąganie strony internetowej
url = "https://slaskiezoo.pl/page/nasze-zwierz%C4%99ta/37"
response = requests.get(url)
html_content = response.text

# Przetwarzanie strony internetowej
soup = BeautifulSoup(html_content, 'html.parser')

# Znajdź wszystkie zwierzęta
animals = []
for tile in soup.find_all('app-tile'):
    name = tile.find('span', class_='tile-title-text').text.strip()
    image = tile.find('img')
    image_url = image['src'] if image and 'src' in image.attrs else "Brak obrazka"
    animals.append((name, image_url))

print(f"Znaleziono {len(animals)} zwierząt.")

# Generowanie pliku Markdown
with open('animals.md', 'w') as f:
    f.write("# Lista Zwierząt w Śląskim Zoo\n\n")
    for name, image_url in animals:
        f.write(f"## {name}\n")
        if image_url != "Brak obrazka":
            f.write(f"![Obrazek]({image_url})\n")
        f.write("\n")

# Wyszukiwanie dodatkowych informacji za pomocą DuckDuckGo
with open('animals.md', 'a') as f:  # Otwórz plik w trybie dopisywania
    f.write("\n## Dodatkowe informacje\n\n")
    for name, image_url in animals:
        query = f"{name} zwierzę Śląskie Zoo"
        try:
            # Wyszukiwanie za pomocą DuckDuckGo
            results = ddgs.text(query, max_results=1)  # Zwraca tylko 1 wynik
            if results:
                f.write(f"- **DuckDuckGo:** [{name}]({results[0]['link']})\n")
                print(f"Znaleziono dodatkowe informacje dla {name}: {results[0]['link']}")
            else:
                print(f"Nie znaleziono wyników dla {name}")
        except Exception as e:
            print(f"Błąd podczas wyszukiwania informacji dla {name}: {e}")
        
        # Dodaj opóźnienie między zapytaniami, aby uniknąć przekroczenia limitu
        time.sleep(5)  # 5 sekund opóźnienia

# Pobieranie obrazków
if not os.path.exists('images'):
    os.makedirs('images')

for i, (name, image_url) in enumerate(animals):
    if image_url != "Brak obrazka":
        try:
            # Poprawienie URL, jeśli brakuje schematu
            if not image_url.startswith(('http://', 'https://')):
                image_url = 'https://slaskiezoo.pl' + image_url
            response = requests.get(image_url)
            response.raise_for_status()
            with open(f'images/animal_{i}.jpg', 'wb') as f:
                f.write(response.content)
            print(f"Zapisano obrazek: animal_{i}.jpg")
        except Exception as e:
            print(f"Nie udało się pobrać obrazka {image_url}: {e}")
