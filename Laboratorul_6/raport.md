# Lucrare de laborator nr. 6
## Informații invizibile: Forensics și Steganografie

### Scopul lucrării
Studierea metodelor de decodare a informațiilor, analizarea fișierelor și ascunderea mesajelor în imagini folosind Python.

## Partea A – Decoder universal

**A1.** Am transformat textul în bytes și în format hexazecimal.

**A2.** Am creat o funcție care identifică tipurile de codare Base64, Hex și URL.

**A3.** Am realizat decodarea mesajelor în diferite formate.

**A4.** Am încercat decodarea unui mesaj în mai multe straturi. Programul a realizat două decodări, apoi s-a oprit.

**A5.** Am utilizat metoda XOR pentru recuperarea unui mesaj secret.

Rezultat: `Cheie: 42, Mesaj: Mesaj secret`

**A6.** Am verificat hashuri folosind un dicționar de parole.

Rezultat: `Algoritm: MD5, Parola: admin`

**A7.** Am adăugat argumente pentru terminal și salvarea rezultatelor într-un fișier JSON.

Rezultat: `Salut`

## Partea B – Forensics și Steganografie

**B1.** Am identificat tipul fișierelor folosind primii octeți.

**B2.** Am extras texte lizibile din fișiere binare.

**B3.** Am verificat metadatele EXIF și GPS ale unei imagini. Nu au fost găsite informații.

**B4.** Am identificat și recuperat o arhivă ZIP ascunsă într-o imagine PNG.

Rezultat: `recuperat.zip`

**B5.** Am ascuns un mesaj într-o imagine folosind metoda LSB.

**B6.** Am extras mesajul ascuns din imagine.

Rezultat: `Salut! Acesta este un mesaj secret.`

## Concluzie

În această lucrare am învățat să decodez mesaje, să verific fișiere și să descopăr informații ascunse. Am folosit Python pentru a recupera mesaje și arhive, dar și pentru a ascunde și extrage text din imagini. Astfel, am înțeles mai bine cum funcționează metodele de analiză digitală și steganografie.