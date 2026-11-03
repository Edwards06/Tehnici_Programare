
# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import requests
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

# Exercitiul 1 - Primul import

print("\nEXERCITIUL 1")

print("Versiunea requests:", requests.__version__)

# requests este o biblioteca externa si necesita pip install.
# urllib este inclus in biblioteca standard Python.


# Exercitiul 2 - Doua stiluri de import

print("\nEXERCITIUL 2")

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Primul stil:", response.status_code)

time.sleep(1)

from requests import get

response = get(BASE_URL, timeout=TIMEOUT)
print("Al doilea stil:", response.status_code)

# import requests arata clar de unde vine functia.
# from requests import get permite scrierea mai scurta.


# Exercitiul 3 - Alias-uri

print("\nEXERCITIUL 3")

import requests as rq

time.sleep(1)

response = rq.get(BASE_URL, timeout=TIMEOUT)
print("Codul de stare:", response.status_code)

# Aliasurile scurteaza numele lungi ale modulelor.
# Aliasurile neclare pot face codul greu de inteles.



# Exercitiul 4 - Biblioteca standard

print("\nEXERCITIUL 4")

time.sleep(1)

req = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        print("Status:", response.status)

        html = response.read().decode("utf-8")
        print("Primele 200 de caractere:")
        print(html[:200])

except urllib.error.HTTPError as e:
    print("Eroare HTTP:", e.code)

except urllib.error.URLError as e:
    print("Eroare de conexiune:", e.reason)



# Exercitiul 5 - Interiorul unui modul

print("\nEXERCITIUL 5")

print(dir(requests))

# requests.get este o functie.
# requests.Session este o clasa.
# requests.adapters este un modul.


# Exercitiul 6 - Documentatia

print("\nEXERCITIUL 6")

help(requests.get)

time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Codul de stare:", response.status_code)

# Parametrul timeout limiteaza timpul de asteptare.


# Exercitiul 7 - Cronometrarea cererii

print("\nEXERCITIUL 7")

time.sleep(1)

start = time.perf_counter()

response = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

durata = end - start

print("Durata perf_counter:", durata, "secunde")
print("Durata response.elapsed:",
      response.elapsed.total_seconds(), "secunde")

# perf_counter masoara durata totala a apelului.
# response.elapsed masoara timpul pana la primirea
# antetelor raspunsului, fara citirea intregului corp.


# Exercitiul 8 - Import esuat

print("\nEXERCITIUL 8")

try:
    import bs4
    print("Modulul bs4 este instalat.")

except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

# try incearca sa execute codul.
# except ImportError trateaza lipsa modulului.
