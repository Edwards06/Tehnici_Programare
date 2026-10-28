"""Aplicație de consolă pentru gestionarea unei liste de activități."""

import json
from datetime import datetime
from pathlib import Path


FISIER = Path(__file__).with_name("activitati.json")


def incarca_activitati():
	"""Citește activitățile din fișier; creează o listă dacă nu există."""
	if not FISIER.exists():
		return []
	try:
		with FISIER.open("r", encoding="utf-8") as f:
			date = json.load(f)
		if not isinstance(date, list):
			raise ValueError("datele trebuie să fie o listă")
		return date
	except (json.JSONDecodeError, ValueError) as eroare:
		print(f"Nu am putut citi lista: {eroare}")
		return []


def salveaza_activitati(activitati):
	with FISIER.open("w", encoding="utf-8") as f:
		json.dump(activitati, f, ensure_ascii=False, indent=2)


def afiseaza(activitati):
	if not activitati:
		print("Lista este goală.")
		return
	print("\nActivități:")
	for activitate in activitati:
		stare = "✓" if activitate["gata"] else " "
		print(f"{activitate['id']}. [{stare}] {activitate['text']} (adăugată {activitate['data']})")


def adauga(activitati):
	text = input("Descrierea activității: ").strip()
	if not text:
		print("Descrierea nu poate fi goală.")
		return
	urmatorul_id = max((a["id"] for a in activitati), default=0) + 1
	activitati.append({
		"id": urmatorul_id,
		"text": text,
		"gata": False,
		"data": datetime.now().strftime("%Y-%m-%d %H:%M"),
	})
	salveaza_activitati(activitati)
	print("Activitatea a fost adăugată.")


def marcheaza_gata(activitati):
	try:
		identificator = int(input("ID-ul activității: "))
	except ValueError:
		print("Introdu un ID numeric.")
		return
	for activitate in activitati:
		if activitate["id"] == identificator:
			activitate["gata"] = not activitate["gata"]
			salveaza_activitati(activitati)
			print("Starea activității a fost actualizată.")
			return
	print("Nu există o activitate cu acest ID.")


def sterge(activitati):
	try:
		identificator = int(input("ID-ul activității de șters: "))
	except ValueError:
		print("Introdu un ID numeric.")
		return
	ramase = [a for a in activitati if a["id"] != identificator]
	if len(ramase) == len(activitati):
		print("Nu există o activitate cu acest ID.")
		return
	salveaza_activitati(ramase)
	print("Activitatea a fost ștearsă.")


def main():
	activitati = incarca_activitati()
	optiuni = {
		"1": ("Afișează activitățile", lambda: afiseaza(activitati)),
		"2": ("Adaugă o activitate", lambda: adauga(activitati)),
		"3": ("Marchează/ demarchează ca terminată", lambda: marcheaza_gata(activitati)),
		"4": ("Șterge o activitate", lambda: sterge(activitati)),
	}
	while True:
		print("\n--- Manager de activități ---")
		for numar, (descriere, _) in optiuni.items():
			print(f"{numar}. {descriere}")
		print("0. Ieșire")
		alegere = input("Alege o opțiune: ").strip()
		if alegere == "0":
			print("La revedere!")
			break
		if alegere in optiuni:
			optiuni[alegere][1]()
		else:
			print("Opțiune invalidă. Încearcă din nou.")


if __name__ == "__main__":
	main()
