# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import requests
import time
import re
import hashlib
import json
import socket
import ssl

from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 35 - Descompunerea unui URL

print("\nEXERCITIUL 35")

def parse_url(url):
    """Descompune un URL in componente."""
    return urlparse(url)


url = "https://cybercor.org/path?x=1#top"

result = parse_url(url)

print("Scheme:", result.scheme)
print("Netloc:", result.netloc)
print("Path:", result.path)
print("Query:", result.query)
print("Fragment:", result.fragment)

# scheme reprezinta protocolul.
# netloc reprezinta domeniul.
# path reprezinta calea resursei.
# query reprezinta parametrii URL-ului.
# fragment reprezinta sectiunea paginii.


# Exercitiul 36 - Compunerea URL-urilor

print("\nEXERCITIUL 36")

def build_urls(base, links):
    """Transforma legaturile relative in URL-uri complete."""
    results = []

    for link in links:
        full_url = urljoin(base, link)
        results.append(full_url)

    return results


links = [
    "/about",
    "contact.html",
    "../index.html"
]

results = build_urls(BASE_URL, links)

for url in results:
    print(url)

# urljoin() combina URL-ul de baza cu o legatura relativa.


# Exercitiul 37 - Extragerea legaturilor

print("\nEXERCITIUL 37")

def extract_links(html):
    """Extrage legaturile HTML fara duplicate."""
    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))


response = requests.get(BASE_URL, timeout=TIMEOUT)

links = extract_links(response.text)

print("Numarul de legaturi:", len(links))

for link in links:
    print(link)

# re.findall() cauta toate potrivirile expresiei regulate.
# dict.fromkeys() elimina duplicatele si pastreaza ordinea.


# Exercitiul 38 - Legaturi interne si externe

print("\nEXERCITIUL 38")

def split_links(links, domain):
    """Separa legaturile interne de cele externe."""
    internal = []
    external = []

    base = "https://" + domain

    for link in links:
        full_url = urljoin(base, link)

        parsed = urlparse(full_url)

        if parsed.netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


internal, external = split_links(links, "cybercor.org")

print("Legaturi interne:", len(internal))
print("Legaturi externe:", len(external))

# Legaturile interne apartin aceluiasi domeniu.
# Legaturile externe apartin altor domenii.


# Exercitiul 39 - Propriile metode

print("\nEXERCITIUL 39")

class ImageFinder(HTMLParser):
    """Gaseste sursele imaginilor din codul HTML."""

    def __init__(self):
        """Initializeaza lista imaginilor."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Colecteaza atributul src al tag-urilor img."""

        if tag == "img":
            src = dict(attrs).get("src")

            if src is not None:
                self.images.append(src)


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fara src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print("Imagini din test:", finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a gasit exact imaginile asteptate"

print("Testul a trecut!")

# HTMLParser apeleaza automat handle_starttag().
# Metoda verifica daca tag-ul este img.
# Daca exista atributul src, il adauga in lista.

time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

finder = ImageFinder()
finder.feed(response.text)

print("Imagini gasite:", len(finder.images))

for src in finder.images:
    print(src)

print(
    "Numar tag-uri img in HTML:",
    response.text.lower().count("<img")
)

# Rezultatul poate fi verificat si in browser cu Ctrl+U.
# Unele imagini pot fi afisate prin CSS sau SVG.


# Exercitiul 40 - Amprenta paginii

print("\nEXERCITIUL 40")

def page_fingerprint(url):
    """Calculeaza amprenta SHA-256 a paginii."""
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(response.content).hexdigest()


time.sleep(1)

hash1 = page_fingerprint(BASE_URL)

time.sleep(1)

hash2 = page_fingerprint(BASE_URL)

print("Prima amprenta:", hash1)
print("A doua amprenta:", hash2)

if hash1 == hash2:
    print("Continutul paginii este identic.")
else:
    print("Continutul paginii s-a modificat.")

# SHA-256 genereaza o amprenta a continutului.
# Amprentele difera daca se modifica datele paginii.


# Exercitiul 41 - Salvarea in JSON

print("\nEXERCITIUL 41")

def save_headers(url):
    """Salveaza antetele HTTP intr-un fisier JSON."""
    response = requests.get(url, timeout=TIMEOUT)

    with open("headers.json", "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)

    print("Antetele au fost salvate in headers.json")

    with open("headers.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    print("Content-Type:", data.get("Content-Type", "lipseste"))


time.sleep(1)

save_headers(BASE_URL)

# json.dump() salveaza datele intr-un fisier JSON.
# json.load() citeste datele din fisier.


# Exercitiul 42 - Interogare DNS

print("\nEXERCITIUL 42")

def resolve(hostname):
    """Returneaza adresa IPv4 a domeniului."""
    return socket.gethostbyname(hostname)


try:
    ip = resolve("cybercor.org")

    print("Adresa IP:", ip)

except socket.gaierror as e:
    print("Eroare DNS:", e)

# DNS transforma numele domeniului intr-o adresa IP.


# Exercitiul 43 - Expirarea certificatului

print("\nEXERCITIUL 43")

def cert_days_left(hostname):
    """Returneaza numarul de zile pana la expirarea certificatului."""

    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:

            certificate = secure_sock.getpeercert()

            expiry = certificate["notAfter"]

            expiry_seconds = ssl.cert_time_to_seconds(expiry)

            current_seconds = time.time()

            days_left = (expiry_seconds - current_seconds) / 86400

            return int(days_left)


try:
    days = cert_days_left("cybercor.org")

    print("Zile ramase:", days)

except (OSError, ssl.SSLError, KeyError, ValueError) as e:
    print("Eroare la verificarea certificatului:", e)

# ssl.create_default_context() creeaza un context TLS securizat.
# socket.create_connection() deschide conexiunea la portul 443.
# wrap_socket() securizeaza conexiunea.
# getpeercert() obtine informatiile certificatului.
# notAfter reprezinta data expirarii.
# Impartim secundele ramase la 86400 pentru a obtine zilele.