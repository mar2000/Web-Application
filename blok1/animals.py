import requests
from bs4 import BeautifulSoup
import os
from googlesearch import search  # Używamy googlesearch do wyszukiwania linków
import time

# Ściąganie strony internetowej
url = "https://afryka.biz.pl/zwierzeta-afryki/"
response = requests.get(url)
html_content = response.text

# Przetwarzanie strony internetowej
soup = BeautifulSoup(html_content, 'html.parser')

# Znajdź wszystkie zwierzęta
animals = []
for h2 in soup.find_all('h2'):
    name = h2.text.strip()
    
    # Szukaj opisu (pierwszy paragraf po nagłówku h2)
    description_tag = h2.find_next('p')
    description = description_tag.text.strip() if description_tag else "Brak opisu"
    
    # Szukaj obrazka (pierwszy obrazek po nagłówku h2)
    image = h2.find_next('img')
    image_url = image['src'] if image and 'src' in image.attrs else "Brak obrazka"
    
    animals.append((name, description, image_url))

print(f"Znaleziono {len(animals)} zwierząt.")

# Generowanie pliku Markdown
with open('animals.md', 'w') as f:
    f.write("# Lista Zwierząt Afryki\n\n")
    for name, description, image_url in animals:
        # Wyszukaj link dla danego zwierzęcia
        query = f"{name} zwierzę Afryka"
        try:
            results = list(search(query, num=1, stop=1, pause=10))  # Zwraca tylko 1 wynik
            link = results[0] if results else "#"  # Użyj "#", jeśli nie znaleziono linku
        except Exception as e:
            print(f"Błąd podczas wyszukiwania informacji dla {name}: {e}")
            link = "#"
        
        # Nagłówek z linkiem
        f.write(f'<h2><a href="{link}" target="_blank">{name}</a></h2>\n')
        f.write(f"{description}\n\n")
        if image_url != "Brak obrazka":
            f.write(f"![Obrazek]({image_url})\n")
        f.write("\n")

# Pobieranie obrazków
if not os.path.exists('images'):
    os.makedirs('images')

for i, (name, description, image_url) in enumerate(animals):
    if image_url != "Brak obrazka":
        try:
            # Poprawienie URL, jeśli brakuje schematu
            if not image_url.startswith(('http://', 'https://')):
                image_url = 'https://afryka.biz.pl' + image_url
            response = requests.get(image_url)
            response.raise_for_status()
            with open(f'images/animal_{i}.jpg', 'wb') as f:
                f.write(response.content)
            print(f"Zapisano obrazek: animal_{i}.jpg")
        except Exception as e:
            print(f"Nie udało się pobrać obrazka {image_url}: {e}")
