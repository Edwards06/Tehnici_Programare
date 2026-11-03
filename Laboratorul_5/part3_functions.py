# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 21 - Prima functie

print("\nEXERCITIUL 21")

def fetch(url):
    """Returneaza raspunsul HTTP pentru URL-ul primit."""
    return requests.get(url, timeout=TIMEOUT)


response = fetch(BASE_URL)

print("Status:", response.status_code)


# Exercitiul 22 - Returnarea unei singure valori

print("\nEXERCITIUL 22")

def get_status(url):
    """Returneaza codul de stare HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


paths = ["/", "/robots.txt", "/sitemap.xml"]

for path in paths:
    time.sleep(1)

    status = get_status(BASE_URL + path)
    print(path, ":", status)


# Exercitiul 23 - Parametri impliciti

print("\nEXERCITIUL 23")

def fetch(url, timeout=10):
    """Returneaza raspunsul HTTP folosind un timeout implicit."""
    return requests.get(url, timeout=timeout)


time.sleep(1)

response = fetch(BASE_URL)
print("Timeout implicit:", response.status_code)

time.sleep(1)

response = fetch(BASE_URL, timeout=3)
print("Timeout 3 secunde:", response.status_code)

# Daca nu transmitem timeout, functia foloseste valoarea 10.
# Daca transmitem timeout=3, valoarea implicita este inlocuita.


# Exercitiul 24 - O singura sarcina pe functie

print("\nEXERCITIUL 24")

def get_title(html):
    """Extrage si returneaza titlul din codul HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start != -1 and end != -1:
        start = start + len("<title>")
        return html[start:end].strip()

    return "Titlul nu a fost gasit."


time.sleep(1)

response = fetch(BASE_URL)

title = get_title(response.text)

print("Titlul paginii:", title)

# fetch() descarca pagina.
# get_title() analizeaza HTML-ul.
# Fiecare functie are o singura responsabilitate.


# Exercitiul 25 - Docstring-uri

print("\nEXERCITIUL 25")

help(get_title)

# Docstring-ul explica scopul unei functii.
# Acesta poate fi afisat folosind help().


# Exercitiul 26 - Adnotari de tip

print("\nEXERCITIUL 26")

def get_status(url: str) -> int:
    """Returneaza codul HTTP pentru URL-ul primit."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


time.sleep(1)

print("Status:", get_status(BASE_URL))

try:
    print(get_status(123))

except (requests.RequestException, TypeError, ValueError) as e:
    print("Eroare:", e)

# str indica faptul ca parametrul url ar trebui sa fie text.
# int indica faptul ca functia ar trebui sa returneze un numar intreg.
# Adnotarile nu opresc automat transmiterea unui tip gresit.


# Exercitiul 27 - Tratarea erorilor

print("\nEXERCITIUL 27")

def page_exists(url):
    """Verifica daca pagina exista si poate fi accesata."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False


time.sleep(1)

print("Pagina principala:", page_exists(BASE_URL))

time.sleep(1)

print(
    "Domeniu inexistent:",
    page_exists("https://this-domain-does-not-exist.invalid")
)

# Functia returneaza True daca cererea reuseste.
# Returneaza False daca apare o eroare HTTP sau de conexiune.


# Exercitiul 28 - Returnarea unui dictionar

print("\nEXERCITIUL 28")

def check_paths(base, paths):
    """Verifica mai multe cai si returneaza codurile HTTP."""
    results = {}

    for path in paths:
        time.sleep(1)

        try:
            response = requests.get(
                base + path,
                timeout=TIMEOUT
            )

            results[path] = response.status_code

        except requests.RequestException:
            results[path] = None

    return results


paths = ["/", "/robots.txt", "/sitemap.xml"]

results = check_paths(BASE_URL, paths)

for path, status in results.items():
    print(path, ":", status)


# Exercitiul 29 - Argumente cu nume

print("\nEXERCITIUL 29")

def get_header(url, name, default="lipseste"):
    """Returneaza valoarea unui antet HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)


time.sleep(1)

server = get_header(BASE_URL, name="Server")

print("Server:", server)

# name="Server" este un argument transmis cu nume.
# default="lipseste" este folosit daca antetul nu exista.


# Exercitiul 30 - Antete de securitate

print("\nEXERCITIUL 30")

def security_headers(url):
    """Verifica prezenta a cinci antete de securitate."""
    response = requests.get(url, timeout=TIMEOUT)

    headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    results = {}

    for header in headers:
        results[header] = header in response.headers

    return results


time.sleep(1)

results = security_headers(BASE_URL)

for header, exists in results.items():
    print(header, ":", exists)

# True inseamna ca antetul exista.
# False inseamna ca antetul lipseste.


# Exercitiul 31 - Functii care apeleaza functii

print("\nEXERCITIUL 31")

def score_headers(results):
    """Calculeaza scorul antetelor de securitate."""
    score = sum(results.values())
    total = len(results)

    return str(score) + "/" + str(total)


time.sleep(1)

score = score_headers(security_headers(BASE_URL))

print("Scor securitate:", score)

# security_headers() returneaza un dictionar cu True si False.
# sum() numara valorile True deoarece True este echivalent cu 1.
# score_headers() returneaza rezultatul sub forma 3/5.


# Exercitiul 32 - Doua functii, o sarcina

print("\nEXERCITIUL 32")

def fetch_robots(base):
    """Returneaza continutul fisierului robots.txt."""
    try:
        response = requests.get(
            base + "/robots.txt",
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage toate caile marcate cu Disallow."""
    paths = []

    if robots_text is None:
        return paths

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            paths.append(path)

    return paths


time.sleep(1)

robots = fetch_robots(BASE_URL)

paths = disallowed_paths(robots)

print("Cai interzise:")

for path in paths:
    print(path)

# Prima functie descarca robots.txt.
# A doua functie extrage valorile Disallow.
# Daca robots.txt lipseste, returnam o lista goala.


# Exercitiul 33 - Oricate argumente

print("\nEXERCITIUL 33")

def response_times(*urls):
    """Returneaza timpul de raspuns pentru fiecare URL."""
    results = {}

    for url in urls:
        time.sleep(1)

        try:
            start = time.perf_counter()

            response = requests.get(
                url,
                timeout=TIMEOUT
            )

            end = time.perf_counter()

            results[url] = end - start

        except requests.RequestException:
            results[url] = None

    return results


times = response_times(
    BASE_URL,
    BASE_URL + "/robots.txt"
)

for url, seconds in times.items():
    print("URL:", url)
    print("Timp:", seconds, "secunde")

# *urls permite transmiterea mai multor URL-uri.
# perf_counter() masoara durata cererii.


# Exercitiul 34 - Argumente cu nume colectate

print("\nEXERCITIUL 34")

def log(message, **details):
    """Afiseaza mesajul si detaliile transmise."""
    result = message

    for key, value in details.items():
        result += " | " + key + "=" + str(value)

    print(result)


log(
    "verificat",
    url=BASE_URL,
    status=200
)

# **details colecteaza argumentele cu nume intr-un dictionar.
# Functia poate primi oricate detalii suplimentare.