"""diferenta.py - ce SUID au aparut fata de un sistem curat.

Rulare din folderul Laboratorul_8:
    python -m arsenal.privesc.diferenta
"""
import os

from arsenal.privesc.enum import citeste_linii, nume, GTFO

START = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")


def cai(fisier):
    """Multimea cailor din fisier (dublurile dispar singure)."""
    return set(citeste_linii(fisier))


def main():
    baza = cai(os.path.join(START, "baza_suid.txt"))
    acum = cai(os.path.join(START, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))

    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    print("risc:", dict(sorted(risc.items())))
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
