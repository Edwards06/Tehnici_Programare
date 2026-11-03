# Laborator: functii, metode si importuri pe web
# Student: Bularga Eduard

import webtools
import argparse
import csv
import time

from datetime import datetime
from webtools import get_title, security_headers, DEFAULT_HEADERS


BASE_URL = "https://cybercor.org"
TIMEOUT = 10


# Exercitiul 44 - Importarea modulului

print("\nEXERCITIUL 44")

response = webtools.fetch(BASE_URL)

title = webtools.get_title(response.text)

print("Titlul paginii:", title)

# import webtools permite accesarea functiilor cu webtools.nume_functie.


# Exercitiul 45 - Importarea anumitor nume

print("\nEXERCITIUL 45")

title = get_title(response.text)

print("Titlu:", title)

time.sleep(1)

headers = security_headers(BASE_URL)

print("Antete securitate:", headers)

# from webtools import permite apelarea directa a functiilor.
# Daca main.py ar defini o functie get_title(),
# aceasta ar inlocui numele importat in spatiul global.


# Exercitiul 46 - Blocul main

print("\nEXERCITIUL 46")

print("Autotestul din webtools.py nu ruleaza la import.")

# __name__ este egal cu "__main__" doar cand fisierul
# este executat direct, nu cand este importat.


# Exercitiul 47 - Constante de modul

print("\nEXERCITIUL 47")

print("DEFAULT_HEADERS:", DEFAULT_HEADERS)

# Constanta este importata din webtools.py.


# Exercitiul 48 - Argumente din linia de comanda

print("\nEXERCITIUL 48")

parser = argparse.ArgumentParser(
    description="Raport pentru un site web"
)

parser.add_argument(
    "url",
    help="Adresa site-ului verificat"
)

args = parser.parse_args()

url = args.url

print("URL primit:", url)


# Exercitiul 49 - Raport CSV

print("\nEXERCITIUL 49")

paths = ["/", "/robots.txt", "/sitemap.xml"]

results = webtools.check_paths(url, paths)

with open("report.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "path",
        "status",
        "checked_at"
    ])

    for path, status in results.items():

        writer.writerow([
            path,
            status,
            datetime.now().isoformat()
        ])

print("Raportul CSV a fost salvat in report.csv")


# Exercitiul 50 - Proiectul final

webtools.site_report(url)