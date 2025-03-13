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
    description = description_tag.text.strip() if description_tag and description_tag.text.strip() != "Brak opisu" else ""
    
    # Szukaj obrazka (pierwszy obrazek po nagłówku h2)
    image = h2.find_next('img')
    image_url = image['src'] if image and 'src' in image.attrs else ""
    
    animals.append((name, description, image_url))

print(f"Znaleziono {len(animals)} zwierząt.")

# Tworzenie katalogu animals, jeśli nie istnieje
if not os.path.exists('animals'):
    os.makedirs('animals')

# Funkcja do scrapowania informacji z Wikipedii
def scrape_wikipedia_info(wiki_url):
    try:
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Pobierz główną treść artykułu
        content = soup.find('div', class_='mw-parser-output')
        
        # Pobierz pierwsze trzy akapity
        paragraphs = []
        for p in content.find_all('p', recursive=False):
            text = p.text.strip()
            if text:  # Ignoruj puste akapity
                paragraphs.append(text)
            if len(paragraphs) >= 3:  # Ogranicz do 3 akapitów
                break
        
        # Pobierz informacje z tabeli bocznej, ignorując synonimy naukowe
        sidebar = soup.find('table', class_='infobox')
        sidebar_info = []
        if sidebar:
            for row in sidebar.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    th_text = th.text.strip()
                    td_text = td.text.strip()
                    # Ignoruj wiersze z synonimami naukowymi
                    if not any(word in th_text.lower() for word in ["synonimy", "synonym"]):
                        sidebar_info.append(f"- **{th_text}**: {td_text}")
        
        return paragraphs, sidebar_info
    except Exception as e:
        return [], []

# Funkcja do wyszukiwania filmu na YouTube
def find_youtube_video(query):
    try:
        search_query = f"{query} zwierzę Afryka YouTube"
        results = list(search(search_query, num=1, stop=1, pause=2))  # Zwraca tylko 1 wynik
        if results:
            return results[0]
        else:
            return None
    except Exception as e:
        print(f"Błąd podczas wyszukiwania filmu na YouTube: {e}")
        return None

# Generowanie plików Markdown dla każdego zwierzęcia
for name, description, image_url in animals:
    # Wyszukaj link do Wikipedii dla danego zwierzęcia
    query = f"{name} zwierzę Afryka wikipedia"
    try:
        results = list(search(query, num=1, stop=1, pause=2))  # Zwraca tylko 1 wynik
        wiki_link = results[0] if results else "#"  # Użyj "#", jeśli nie znaleziono linku
    except Exception as e:
        print(f"Błąd podczas wyszukiwania informacji dla {name}: {e}")
        wiki_link = "#"
    
    # Pobierz informacje z Wikipedii
    if wiki_link != "#":
        paragraphs, sidebar_info = scrape_wikipedia_info(wiki_link)
    else:
        paragraphs, sidebar_info = [], []
    
    # Wyszukaj film na YouTube
    youtube_link = find_youtube_video(name)
    youtube_embed = ""
    if youtube_link:
        # Konwersja linku YouTube na embed
        video_id = youtube_link.split("v=")[1].split("&")[0]  # Pobierz ID filmu
        youtube_embed = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    
    # Tworzenie pliku Markdown
    filename = f"animals/{name.replace(' ', '_')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"layout: default\n")
        f.write(f"title: \"{name.split()[0]}\"\n")
        f.write("---\n\n")
        f.write(f"# {name}\n\n")
        
        # Dodaj opis, jeśli istnieje
        if description:
            f.write(f"## Opis\n\n{description}\n\n")
        
        # Dodaj obrazek, jeśli istnieje
        if image_url:
            f.write(f"![Obrazek]({image_url})\n\n")
        
        # Dodaj informacje z Wikipedii, jeśli istnieją
        if paragraphs:
            f.write(f"## Informacje z Wikipedii\n\n")
            for paragraph in paragraphs:
                f.write(f"{paragraph}\n\n")
        
        # Dodaj informacje z tabeli bocznej, jeśli istnieją
        if sidebar_info:
            f.write(f"## Informacje dodatkowe\n\n")
            for info in sidebar_info:
                f.write(f"{info}\n")
        
        # Dodaj film z YouTube, jeśli znaleziono
        if youtube_embed:
            f.write(f"\n## Film na YouTube\n\n")
            f.write(f"{youtube_embed}\n\n")
        
        # Dodaj link do Wikipedii
        f.write(f"[Czytaj więcej na Wikipedii]({wiki_link})\n")

# Generowanie pliku animals.md w bieżącym katalogu
with open('animals.md', 'w', encoding='utf-8') as f:
    f.write("---\n")
    f.write(f"layout: scraped\n")
    f.write(f"title: Zwierzątka\n")
    f.write("---\n\n")
    f.write(f"# {name}\n\n")
        
    f.write("# Lista Zwierząt Afryki\n\n")
    for name, description, image_url in animals:
        # Link do pliku .md w folderze animals
        md_link = f'animals/{name.replace(" ", "_")}.html'
        
        # Nagłówek z linkiem do pliku .md
        f.write(f'<h2><a href="{md_link}" target="_blank">{name}</a></h2>\n')
        f.write(f"{description}\n\n")
        if image_url:
            f.write(f"![Obrazek]({image_url})\n")
        f.write("\n")

print("Pliki Markdown zostały wygenerowane w katalogu 'animals'.")
print("Plik animals.md został wygenerowany w bieżącym katalogu.")

# Pobieranie obrazków
if not os.path.exists('images'):
    os.makedirs('images')

for i, (name, description, image_url) in enumerate(animals):
    if image_url:
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
