
# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 9 - Elementele raspunsului

print("\nEXERCITIUL 9")

response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Status:", response.status_code)  # atribut
print("OK:", response.ok)                # atribut
print("URL:", response.url)              # atribut
print("Encoding:", response.encoding)    # atribut


# Exercitiul 10 - Tratarea erorilor

print("\nEXERCITIUL 10")

response.raise_for_status()
print("Pagina principala nu are erori HTTP.")

time.sleep(1)

try:
    response_error = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )
    response_error.raise_for_status()
    print("Pagina exista.")

except requests.HTTPError as e:
    print("Pagina nu a putut fi accesata:", e)


# Exercitiul 11 - Toate antetele

print("\nEXERCITIUL 11")

for name, value in response.headers.items():
    print(name + ":", value)


# Exercitiul 12 - Metode de dictionar

print("\nEXERCITIUL 12")

print("Server:", response.headers.get("Server", "lipseste"))
print("Content-Type:", response.headers.get("Content-Type", "lipseste"))
print("content-type:", response.headers.get("content-type", "lipseste"))

# Numele antetelor HTTP nu sunt sensibile la majuscule.
# Content-Type si content-type returneaza aceeasi valoare.


# Exercitiul 13 - Metode de sir

print("\nEXERCITIUL 13")

count = response.text.lower().count("cyber")

print("Cuvantul cyber apare de", count, "ori.")

# lower() transforma textul in litere mici.
# count() numara aparitiile cuvantului.
# Putem inlantui metodele deoarece lower() returneaza un sir.


# Exercitiul 14 - Gasirea titlului

print("\nEXERCITIUL 14")

html = response.text

start = html.find("<title>")
end = html.find("</title>")

if start != -1 and end != -1:
    start = start + len("<title>")
    title = html[start:end].strip()
    print("Titlul paginii:", title)
else:
    print("Titlul nu a fost gasit.")


# Exercitiul 15 - Numararea liniilor

print("\nEXERCITIUL 15")

lines = html.splitlines()

print("Numarul de linii:", len(lines))

if lines:
    longest = max(lines, key=len)
    print("Lungimea celei mai lungi linii:", len(longest))
else:
    print("Pagina nu contine linii.")


# Exercitiul 16 - Verificarea HTTPS

print("\nEXERCITIUL 16")

if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")


# Exercitiul 17 - Redirectionari

print("\nEXERCITIUL 17")

time.sleep(1)

redirect_response = requests.get(
    "http://cybercor.org",
    timeout=TIMEOUT
)

for redirect in redirect_response.history:
    print("Redirectionare:", redirect.status_code, redirect.url)

print("URL final:", redirect_response.url)


# Exercitiul 18 - HEAD versus GET

print("\nEXERCITIUL 18")

time.sleep(1)

head_response = requests.head(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

get_response = requests.get(BASE_URL, timeout=TIMEOUT)

print("HEAD:", len(head_response.content), "bytes")
print("GET:", len(get_response.content), "bytes")

# HEAD returneaza antetele, fara corpul paginii.
# GET returneaza antetele si continutul paginii.


# Exercitiul 19 - Cookie-uri

print("\nEXERCITIUL 19")

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat.")


# Exercitiul 20 - Sesiuni

print("\nEXERCITIUL 20")

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Bularga-Eduard"
})

time.sleep(1)

try:
    result = session.get(
        ECHO_URL + "/headers",
        timeout=TIMEOUT
    )

    result.raise_for_status()

    data = result.json()
    print("Antetele primite:", data)

    user_agent = data.get("headers", {}).get("User-Agent", "")

    if user_agent == "WebLab-Bularga-Eduard":
        print("User-Agent confirmat.")
    else:
        print("User-Agent diferit sau neconfirmat.")

except requests.RequestException as e:
    print("Eroare la cerere:", e)

except ValueError:
    print("Raspunsul nu contine JSON valid.")

finally:
    session.close()
