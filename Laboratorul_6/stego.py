from PIL import Image
from pathlib import Path


# B5 - Ascunderea unui mesaj intr-o imagine folosind LSB

def ascunde_mesaj(cale_intrare, cale_iesire, mesaj):
    imagine = Image.open(cale_intrare).convert("RGB")

    # Transformam mesajul in bytes
    date = mesaj.encode("utf-8")

    # Primii 32 de biti reprezinta lungimea mesajului
    lungime = len(date)

    biti = f"{lungime:032b}"

    # Transformam fiecare byte in 8 biti
    for byte in date:
        biti += f"{byte:08b}"

    pixeli = list(imagine.get_flattened_data())

    capacitate = len(pixeli) * 3

    if len(biti) > capacitate:
        raise ValueError("Mesajul este prea lung pentru imagine!")

    pixeli_noi = []
    pozitie = 0

    for pixel in pixeli:
        canale = list(pixel)

        for i in range(3):
            if pozitie < len(biti):
                # Modificam ultimul bit
                canale[i] = (canale[i] & 254) | int(biti[pozitie])
                pozitie += 1

        pixeli_noi.append(tuple(canale))

    imagine.putdata(pixeli_noi)
    imagine.save(cale_iesire, format="PNG")

    print("Mesajul a fost ascuns cu succes!")
    print("Imagine salvata:", cale_iesire)
    print("Mesaj original:", mesaj)


print("\nEXERCITIUL B5")

cale_intrare = Path("probe/ascuns.png")
cale_iesire = Path("stego.png")

if cale_intrare.exists():
    ascunde_mesaj(
        cale_intrare,
        cale_iesire,
        "Salut! Acesta este un mesaj secret."
    )
else:
    print("Imaginea de intrare nu exista!")

    # B6 - Extragerea mesajului ascuns folosind LSB

def extrage_mesaj(cale_imagine):
    with Image.open(cale_imagine) as imagine:
        imagine = imagine.convert("RGB")

        pixeli = list(imagine.get_flattened_data())

    biti = ""

    # Citim ultimul bit din fiecare canal RGB
    for pixel in pixeli:
        for canal in pixel:
            biti += str(canal & 1)

    # Primii 32 de biti reprezinta lungimea mesajului
    lungime = int(biti[:32], 2)

    # Extragem doar bitii mesajului
    biti_mesaj = biti[32:32 + lungime * 8]

    # Transformam bitii inapoi in bytes
    date = bytes(
        int(biti_mesaj[i:i + 8], 2)
        for i in range(0, len(biti_mesaj), 8)
    )

    return date.decode("utf-8")


print("\nEXERCITIUL B6")

cale = Path("stego.png")

if cale.exists():
    mesaj = extrage_mesaj(cale)

    print("Imagine analizata:", cale)
    print("Mesaj extras:", mesaj)
else:
    print("Imaginea stego.png nu exista!")