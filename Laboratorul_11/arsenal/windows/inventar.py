"""inventar.py - procesele si evenimentele unei masini Windows, ca obiecte.

Rulare din folderul Laboratorul_11:
    python -m arsenal.windows.inventar arsenal/windows/start
    python -m arsenal.windows.inventar arsenal/windows/start --json
"""
import argparse
import json
import os
from dataclasses import dataclass, asdict

# procesele care ruleaza din folderul utilizatorului sunt un semn clasic
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

# 4625 logon esuat, 1102 jurnal sters, 7045 serviciu instalat
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        """True daca procesul ruleaza dintr-un folder suspect (Temp, Roaming)."""
        return any(c in self.cale for c in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        """True daca ID-ul e unul de alarma sau nivelul e critical."""
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        """Procesele care se declara singure suspecte."""
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        """Dictionar user -> lista de nume de procese."""
        grupuri = {}
        for p in self.procese:
            grupuri.setdefault(p.user, []).append(p.nume)
        return grupuri


def main():
    p = argparse.ArgumentParser(description="Inventar de procese si alarme Windows")
    p.add_argument("capturi", help="folderul cu procese.json si evenimente.json")
    p.add_argument("--json", action="store_true", help="scoate raportul ca JSON")
    a = p.parse_args()

    inv = Inventar.din_json(os.path.join(a.capturi, "procese.json"))
    ev = evenimente_din_json(os.path.join(a.capturi, "evenimente.json"))
    suspecte = inv.suspecte()
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese": len(inv),
            "procese_suspecte": [asdict(x) for x in suspecte],
            "evenimente": len(ev),
            "alarma": [asdict(e) for e in alarma],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
    for x in suspecte:
        print(f"  [{x.pid}] {x.nume}  ({x.user})  {x.cale}")
    print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
    for e in alarma:
        print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()
