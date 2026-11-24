"""amprente.py - tipul dupa magic bytes si amprenta SHA-256 a fisierelor ridicate.

Rulare din folderul Laboratorul_13:
    python -m arsenal.forensics.amprente arsenal/forensics/probe
"""
import argparse
import hashlib
import os

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    """Tipul fisierului dupa primii octeti; "necunoscut" daca nu se potriveste nimic."""
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"   # dupa bucla: abia acum stim ca nu s-a potrivit nimic


def amprenta_fisier(cale):
    """Fisa unui fisier: nume, tip si primele 16 caractere din SHA-256."""
    with open(cale, "rb") as f:   # "rb" = octeti; with inchide fisierul singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}


def scaneaza(folder):
    """Amprentele tuturor fisierelor din folder, in ordine alfabetica."""
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


def amprente_lenes(folder):
    """La fel ca scaneaza, dar da cate o fisa pe rand (generator)."""
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            yield amprenta_fisier(cale)


def main():
    p = argparse.ArgumentParser(description="Tip si amprenta SHA-256 pentru fisiere")
    p.add_argument("folder", help="folderul cu probe")
    a = p.parse_args()
    for f in scaneaza(a.folder):
        print(f"{f['nume']:14} {f['tip']:11} {f['sha256']}")


if __name__ == "__main__":
    main()
