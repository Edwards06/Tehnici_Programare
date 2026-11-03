from pathlib import Path


# B1 - Identificarea tipului real al fisierelor

def identifica_fisier(cale):
    semnaturi = {
        b"\xFF\xD8\xFF": "JPEG",
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"%PDF": "PDF",
        b"PK\x03\x04": "ZIP",
        b"GIF87a": "GIF",
        b"GIF89a": "GIF"
    }

    with open(cale, "rb") as f:
        inceput = f.read(16)

    for semnatura, tip in semnaturi.items():
        if inceput.startswith(semnatura):
            return tip

    return "Tip necunoscut"


print("\nEXERCITIUL B1")

cale = Path("probe/foto.jpg")

if cale.exists():
    tip = identifica_fisier(cale)

    print("Fisier:", cale)
    print("Tip identificat:", tip)
else:
    print("Fisierul probe/foto.jpg nu exista!")

    # B2 - Extragerea textelor lizibile din fisiere binare

import re


def extrage_texte(cale, lungime_minima=4):
    with open(cale, "rb") as f:
        date = f.read()

    # Cautam secvente de minimum 4 caractere ASCII imprimabile
    texte = re.findall(
        rb"[\x20-\x7E]{4,}",
        date
    )

    return [
        text.decode("ascii")
        for text in texte
        if len(text) >= lungime_minima
    ]


print("\nEXERCITIUL B2")

cale = Path("probe/foto.jpg")

if cale.exists():
    texte = extrage_texte(cale)

    print("Fisier analizat:", cale)
    print("Numar texte gasite:", len(texte))

    for text in texte[:20]:
        print(text)
else:
    print("Fisierul probe/foto.jpg nu exista!")

    # B3 - Extragerea metadatelor EXIF si GPS

from PIL import Image, ExifTags


def extrage_exif(cale):
    with Image.open(cale) as imagine:
        exif = imagine.getexif()

        if not exif:
            return {}, {}

        metadate = {}

        for cheie, valoare in exif.items():
            nume = ExifTags.TAGS.get(cheie, cheie)
            metadate[nume] = valoare

        gps = {}

        try:
            gps = exif.get_ifd(ExifTags.IFD.GPSInfo)

            gps = {
                ExifTags.GPSTAGS.get(cheie, cheie): valoare
                for cheie, valoare in gps.items()
            }
        except (KeyError, AttributeError):
            pass

        return metadate, gps


print("\nEXERCITIUL B3")

cale = Path("probe/foto.jpg")

if cale.exists():
    metadate, gps = extrage_exif(cale)

    if metadate:
        print("Metadate EXIF:")

        for cheie, valoare in metadate.items():
            print(f"{cheie}: {valoare}")
    else:
        print("Nu au fost gasite metadate EXIF.")

    if gps:
        print("\nInformatii GPS:")

        for cheie, valoare in gps.items():
            print(f"{cheie}: {valoare}")
    else:
        print("Nu au fost gasite informatii GPS.")
else:
    print("Fisierul probe/foto.jpg nu exista!")

    # B4 - File Carving: recuperarea unei arhive ZIP

import io
import zipfile


def recupereaza_zip(cale):
    date = Path(cale).read_bytes()

    # Semnatura de inceput a unei arhive ZIP
    semnatura = b"PK\x03\x04"

    pozitie = date.find(semnatura)

    if pozitie == -1:
        print("Nu a fost gasita o arhiva ZIP.")
        return

    print("Semnatura ZIP gasita la offset:", pozitie)

    # Extragem datele incepand cu semnatura ZIP
    date_zip = date[pozitie:]

    try:
        with zipfile.ZipFile(io.BytesIO(date_zip)) as arhiva:
            print("Arhiva ZIP este valida.")
            print("Fisiere gasite:")

            for nume in arhiva.namelist():
                print("-", nume)

        # Salvam arhiva recuperata
        destinatie = Path("probe/recuperat.zip")
        destinatie.write_bytes(date_zip)

        print("Arhiva recuperata:", destinatie)

    except zipfile.BadZipFile:
        print("Semnatura exista, dar arhiva ZIP nu este valida.")


print("\nEXERCITIUL B4")

cale = Path("probe/ascuns.png")

if cale.exists():
    recupereaza_zip(cale)
else:
    print("Fisierul probe/ascuns.png nu exista!")