"""enum.py - enumerare spre root din capturi (SUID, sudo, cron).

Rulare din folderul Laboratorul_8:
    python -m arsenal.privesc.enum arsenal/privesc/start
    python -m arsenal.privesc.enum arsenal/privesc/start --json
"""
import argparse
import json
import os

# binare care, cu bit SUID sau prin sudo, dau usor root (stil GTFOBins)
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

AICI = os.path.dirname(os.path.abspath(__file__))


def citeste_linii(cale):
    """Liniile curate din fisier: fara spatii la capete, fara goale, fara comentarii."""
    with open(cale, encoding="utf-8") as f:
        return [ln.strip() for ln in f
                if ln.strip() and not ln.strip().startswith("#")]


def nume(cale):
    """Numele fisierului: ce e dupa ultimul '/'."""
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    cai = citeste_linii(cale)
    return [{"cale": c,
             "nume": nume(c),
             "risc": "mare" if nume(c) in GTFO else "normal"}
            for c in sorted(set(cai))]


def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        out.append({"user": user.strip(),
                    "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out


def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda})
    return out


def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


def main():
    p = argparse.ArgumentParser(description="Enumerare spre root din capturi")
    p.add_argument("capturi", help="folderul cu suid.txt, sudo.txt, crontab.txt")
    p.add_argument("--json", action="store_true", help="scoate raportul ca JSON")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    # userii unici din sudo reuniti cu cei din cron
    utilizatori = {c["user"] for c in raport["sudo"]} | {c["user"] for c in raport["cron"]}
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    # raportul se salveaza langa unealta: arsenal/privesc/enum.json
    with open(os.path.join(AICI, "enum.json"), "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
