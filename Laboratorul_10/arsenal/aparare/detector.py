"""detector.py - detecteaza adresele care fac brute force pe ssh.

Rulare din folderul Laboratorul_10:
    python -m arsenal.aparare.detector arsenal/aparare/start/auth.log
    python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2
    python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --json
"""
import argparse
import json

from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    """Adresele cu cel putin `prag` esecuri, ca (ip, n), de la mare la mic."""
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(((ip, n) for ip, n in counts.items() if n >= prag),
                  key=lambda x: x[1], reverse=True)


def main():
    p = argparse.ArgumentParser(description="Detector de brute force din auth.log")
    p.add_argument("log", help="calea catre auth.log")
    p.add_argument("--prag", type=int, default=10, help="esecuri de la care o adresa e suspecta")
    p.add_argument("--json", action="store_true", help="scoate raportul ca JSON")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    try:
        sus = suspecti(counts, a.prag)
    except ValueError as e:
        p.error(str(e))   # mesaj clar si iesire, fara traceback

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts.most_common()),
            "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print("Esecuri de autentificare:", len(esecuri))
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")
    print(f"Suspecti (prag {a.prag}):")
    for ip, n in sus:
        print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
