"""inventar.py - citeste o lista de tinte si face un mic inventar.

Grupeaza porturile dupa serviciu, gaseste masinile cu porturi peste un prag
si salveaza totul intr-un raport JSON.

Folosire:
    python inventar.py tinte.json --prag 1000
"""
import argparse
import json


def citeste_tinte(cale):
    with open(cale, encoding="utf-8") as f:
        tinte = json.load(f)
    return tinte


def port_valid(valoare):
    """Intoarce portul ca int sau None daca nu e un numar."""
    try:
        return int(valoare)
    except (TypeError, ValueError):
        return None


def grupeaza(tinte):
    grupuri = {}
    for t in tinte:
        port = port_valid(t["port"])
        if port is None:
            print("sar peste", t["ip"], ": port invalid", t["port"])
            continue
        serviciu = t.get("serviciu", "necunoscut")
        grupuri[serviciu] = []
        grupuri[serviciu].append(port)
    return grupuri


def peste_prag(tinte, prag):
    ipuri = []
    for t in tinte:
        port = port_valid(t["port"])
        if port is not None and port > prag and t["ip"] not in ipuri:
            ipuri.append(t["ip"])
        return ipuri


def salveaza_raport(grupuri, ipuri, prag, cale="raport_inventar.json"):
    raport = {"prag": prag, "servicii": grupuri, "peste_prag": ipuri}
    with open(cale, "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    return cale


def main():
    parser = argparse.ArgumentParser(description="Inventar de tinte")
    parser.add_argument("fisier", help="fisierul JSON cu tinte")
    parser.add_argument("--prag", default=1024, help="pragul pentru porturi")
    args = parser.parse_args()

    tinte = citeste_tinte(args.fisier)
    print(f"Tinte citite: {len(tinte)}")

    grupuri = grupeaza(tinte)
    for serviciu, porturi in grupuri.items():
        print(f"{serviciu}: {porturi}")

    ipuri = peste_prag(tinte, args.prag)
    print(f"Peste {args.prag}: {ipuri}")

    cale = salveaza_raport(grupuri, ipuri, args.prag)
    print("Raport salvat in", cale)


if __name__ == "__main__":
    main()
