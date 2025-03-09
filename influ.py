import requests
from bs4 import BeautifulSoup
import os
from googlesearch import search
# from duckduckgo_search import ddg

# Ściąganie strony internetowej
url = "https://www.favikon.com/blog/the-20-most-famous-tiktok-influencers-in-the-world"
response = requests.get(url)
html_content = response.text

# Przetwarzanie strony internetowej
soup = BeautifulSoup(html_content, 'html.parser')

# Znajdź wszystkie nagłówki h2 (nazwy influencerów) i opisy
influencers = []
for h2 in soup.find_all('h2'):
    name = h2.text.strip()
    description = h2.find_next('p').text.strip() if h2.find_next('p') else "Brak opisu"
    image = h2.find_next('img')
    image_url = image['src'] if image and 'src' in image.attrs else "Brak obrazka"
    influencers.append((name, description, image_url))

print(f"Znaleziono {len(influencers)} influencerów.")

# Generowanie pliku Markdown
with open('influencers.md', 'w') as f:
    f.write("# Lista Influencerów na TikTok\n\n")
    for name, description, image_url in influencers:
        f.write(f"## {name}\n")
        f.write(f"**Opis:** {description}\n")
        if image_url != "Brak obrazka":
            f.write(f"![Obrazek]({image_url})\n")
        f.write("\n")

# Wyszukiwanie dodatkowych informacji
with open('influencers.md', 'a') as f:  # Otwórz plik w trybie dopisywania
    f.write("\n## Dodatkowe informacje\n\n")
    for name, description, image_url in influencers:
        query = f"{name} TikTok influencer"
        try:
            # Użyj poprawnego argumentu num_results
            for j in search(query, num_results=1):  # Zwraca tylko 1 wynik
                f.write(f"- [{name}]({j})\n")
                print(f"Znaleziono dodatkowe informacje dla {name}: {j}")
        except Exception as e:
            print(f"Błąd podczas wyszukiwania informacji dla {name}: {e}")

# Pobieranie obrazków
if not os.path.exists('images'):
    os.makedirs('images')

for i, (name, description, image_url) in enumerate(influencers):
    if image_url != "Brak obrazka":
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            with open(f'images/influencer_{i}.jpg', 'wb') as f:
                f.write(response.content)
            print(f"Zapisano obrazek: influencer_{i}.jpg")
        except Exception as e:
            print(f"Nie udało się pobrać obrazka {image_url}: {e}")
            
            
