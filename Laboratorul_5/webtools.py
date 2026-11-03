# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import requests
import time
import re
import json
import socket
import ssl

from urllib.parse import urlparse, urljoin


BASE_URL = "https://cybercor.org"
TIMEOUT = 10

DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Bularga-Eduard"
}


# Exercitiul 44 - Crearea unui modul

def fetch(url, timeout=TIMEOUT):
    """Descarca o pagina web si returneaza raspunsul HTTP."""

    response = requests.get(
        url,
        headers=DEFAULT_HEADERS,
        timeout=timeout
    )

    return response


def get_status(url):
    """Returneaza codul de stare HTTP."""

    response = fetch(url)

    return response.status_code


def get_title(html):
    """Extrage titlul paginii din codul HTML."""

    start = html.find("<title>")
    end = html.find("</title>")

    if start != -1 and end != -1:
        start = start + len("<title>")

        return html[start:end].strip()

    return "Titlul nu a fost gasit."


def security_headers(url):
    """Verifica prezenta antetelor de securitate."""

    response = fetch(url)

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


# Exercitiul 47 - Constante de modul

# DEFAULT_HEADERS este o constanta de modul.
# Aceasta este folosita de functia fetch().
# Constantele sunt scrise de obicei cu litere mari.


# Exercitiul 49 - Verificarea cailor

def check_paths(base, paths):
    """Returneaza codurile HTTP pentru mai multe cai."""

    results = {}

    for path in paths:
        time.sleep(1)

        try:
            response = fetch(base.rstrip("/") + path)

            results[path] = response.status_code

        except requests.RequestException:
            results[path] = None

    return results


# Exercitiul 50 - Functii pentru raport


def score_headers(results):
    """Calculeaza scorul antetelor de securitate."""

    score = sum(results.values())
    total = len(results)

    return str(score) + "/" + str(total)


def resolve(hostname):
    """Returneaza adresa IPv4 a domeniului."""

    return socket.gethostbyname(hostname)


def cert_days_left(hostname):
    """Calculeaza zilele ramase pana la expirarea certificatului."""

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


def extract_links(html):
    """Extrage legaturile HTML fara duplicate."""

    links = re.findall(r'href="([^"]+)"', html)

    return list(dict.fromkeys(links))


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


def fetch_robots(base):
    """Returneaza continutul fisierului robots.txt."""

    try:
        response = fetch(base.rstrip("/") + "/robots.txt")

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage valorile Disallow din robots.txt."""

    paths = []

    if robots_text is None:
        return paths

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()

            paths.append(path)

    return paths


def get_redirects(url):
    """Returneaza lantul de redirectionari HTTP."""

    parsed = urlparse(url)

    http_url = parsed._replace(scheme="http").geturl()

    response = fetch(http_url)

    redirects = []

    for item in response.history:
        redirects.append({
            "status": item.status_code,
            "url": item.url
        })

    return redirects, response.url


def site_report(url):
    """Genereaza si salveaza raportul complet al unui site."""

    print("\nEXERCITIUL 50")
    print("\n=== RAPORT SITE:", url, "===")

    parsed = urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        print("URL invalid.")
        return

    try:
        # 1. Codul de stare si URL-ul final

        response = fetch(url)

        status = response.status_code
        final_url = response.url

        print("Cod de stare:", status)
        print("URL final:", final_url)

        # 2. Titlul paginii

        title = get_title(response.text)

        print("Titlu:", title)

        # 3. Adresa IP

        ip = resolve(hostname)

        print("Adresa IP:", ip)

        # 4. Redirectionari

        time.sleep(1)

        redirects, redirect_final = get_redirects(url)

        print("Redirectionari:")

        for item in redirects:
            print(item["status"], "->", item["url"])

        print("Destinatie:", redirect_final)

        # 5. Scorul antetelor de securitate

        time.sleep(1)

        headers = security_headers(url)

        score = score_headers(headers)

        print("Scor securitate:", score)

        # 6. Certificatul SSL

        days = cert_days_left(hostname)

        print("Certificat:", days, "zile ramase")

        # 7. Legaturi interne si externe

        links = extract_links(response.text)

        internal, external = split_links(links, hostname)

        print("Legaturi interne:", len(internal))
        print("Legaturi externe:", len(external))

        # 8. Cai interzise

        time.sleep(1)

        robots = fetch_robots(url)

        paths = disallowed_paths(robots)

        print("Cai interzise:", paths)

        # Salvarea raportului in JSON

        report = {
            "url": url,
            "status": status,
            "final_url": final_url,
            "title": title,
            "ip": ip,
            "redirects": redirects,
            "redirect_final": redirect_final,
            "security_headers": headers,
            "security_score": score,
            "certificate_days_left": days,
            "internal_links": len(internal),
            "external_links": len(external),
            "disallowed_paths": paths
        }

        with open("report.json", "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2, ensure_ascii=False)

        print("\nRaport salvat in report.json")

    except (requests.RequestException, OSError, ValueError, KeyError) as e:
        print("Eroare la generarea raportului:", e)


# Exercitiul 46 - Blocul main

if __name__ == "__main__":

    print("\nEXERCITIUL 46")

    try:
        print("Autotest:", get_status(BASE_URL))

    except requests.RequestException as e:
        print("Eroare la autotest:", e)

# Blocul de mai sus ruleaza doar daca executam direct webtools.py.
# Cand importam modulul in main.py, autotestul nu ruleaza.