
## Laboratorul 6 - Arsenal Forensics
## A1 - Text și octeți
s = "Salut"
b = s.encode()

print("Bytes:", b)
print("Primul octet:", b[0])

hex_text = b.hex()
print("Hex:", hex_text)

b_reconstruit = bytes.fromhex(hex_text)
print("Bytes reconstruiti:", b_reconstruit)
print("Text original:", b_reconstruit.decode())

# A2 - Recunoasterea tipului de codare

import re

def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9A-Fa-f]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"

    return "necunoscut"


print("\nEXERCITIUL A2")
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(ghici_strat("Salut!"))

# A3 - Decodarea datelor

import base64
from urllib.parse import unquote

def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat


print("\nEXERCITIUL A3")

print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%53%61%6C%75%74"))

# A4 - Decodarea mai multor straturi

def citibil(b):
    return all(32 <= c < 127 for c in b)


def decodeaza_straturi(val):
    for i in range(8):
        strat = ghici_strat(val)

        if strat == "necunoscut":
            print("Text final:", val)
            break

        try:
            strat, b = desfa(val)
            rezultat = b.decode("utf-8")

            print(f"Pasul {i + 1}: {strat} -> {rezultat}")

            val = rezultat

            if ghici_strat(val) == "necunoscut":
                print("Mesaj decodat:", val)
                break

        except (ValueError, UnicodeDecodeError):
            print("Decodarea s-a oprit.")
            break


print("\nEXERCITIUL A4")

val = "NTM1OTU3NTk="
decodeaza_straturi(val)

# A5 - XOR Brute Force

from pathlib import Path

print("\nEXERCITIUL A5")

cale = Path("probe/xor.bin")

if cale.exists():
    date = cale.read_bytes()

    for k in range(256):
        clar = bytes(b ^ k for b in date)

        if citibil(clar):
            print("Cheie:", k)
            print("Mesaj:", clar.decode("ascii"))
else:
    print("Fisierul probe/xor.bin nu exista!")

    # A6 - Spargerea hashurilor prin dictionar

import hashlib
from pathlib import Path

print("\nEXERCITIUL A6")

cale_hash = Path("probe/hashuri.txt")
cale_wordlist = Path("probe/wordlist.txt")

if cale_hash.exists() and cale_wordlist.exists():

    tinta = cale_hash.read_text().splitlines()[0].strip().lower()

    algoritmi = {
        32: "md5",
        40: "sha1",
        64: "sha256"
    }

    algoritm = algoritmi.get(len(tinta))

    if algoritm:
        print("Algoritm probabil:", algoritm)

        gasit = False

        for cuv in cale_wordlist.read_text(encoding="latin1").splitlines():

            hash_calculat = hashlib.new(
                algoritm, cuv.encode()
            ).hexdigest()

            if hash_calculat == tinta:
                print("Parola gasita:", cuv)
                gasit = True
                break

        if not gasit:
            print("Parola nu a fost gasita in dictionar.")

    else:
        print("Algoritm necunoscut.")

else:
    print("Fisierele hashuri.txt sau wordlist.txt lipsesc!")

# A7 - Argumente CLI si export JSON

import argparse
import json
from pathlib import Path

def main():
    print("\nEXERCITIUL A7")

    parser = argparse.ArgumentParser(
        description="Decoder universal - Laboratorul 6"
    )

    parser.add_argument(
        "intrare",
    nargs="?",
    default="U2FsdXQ=",
    help="Textul codificat sau calea catre fisier"
    )

    parser.add_argument(
        "--fisier",
        action="store_true",
        help="Citeste datele dintr-un fisier"
    )

    args = parser.parse_args()

    if args.fisier:
        date = Path(args.intrare).read_bytes()
        text = date.decode("utf-8")
    else:
        text = args.intrare

    strat, rezultat = desfa(text)

    print("Tip codare:", strat)
    print("Rezultat:", rezultat.decode("utf-8", errors="replace"))

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode("utf-8", errors="replace")
    }

    cale = Path("arsenal/forensics/fisa.json")
    cale.parent.mkdir(parents=True, exist_ok=True)

    with open(cale, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)

    print("Rezultatul a fost salvat in fisa.json")


if __name__ == "__main__":
    main()