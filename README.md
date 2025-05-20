# Vienkāršs mājas budžeta plānotājs - Projekts mācību nolūkiem
### Izstrādātāji-Lauma Vlasova un Henriete Čupāne ###
## Īss projekta apraksts

Šī projekta mērķis ir izveidot Python programmu, kas palīdz lietotājam pārvaldīt personīgo budžetu. Programma paredzēta izmantošanai ikdienā, lai palīdzētu lietotājam sekot līdzi tēriņiem dažādās izdevumu kategorijās, kā arī saglabātu datus strukturētā veidā Excel failā, lai lietotajs varētu redzēt savus izdevumus šomēnes un pielietot informāciju lai nākotnes budžetu plānus varētu sastādīt gudrāk. Šāds rīks ļauj vieglāk plānot, taupīt un redzēt, kurā kategorijā tiek tērēts visvairāk.

Lietotājam ir iespēja:
- norādīt mēneša budžetu
- sadalīt to pa 12 iepriekš definētām izdevumu kategorijām (piemēram, pārtika, mājdzīvnieki, transports u.c.)
- pievienot mēneša izdevumus noteiktai kategorijai
- redzēt, cik naudas atlikums ir palicis katrā kategorijā pēc izdevumu reģistrēšanas
- saņemt brīdinājumu, ja tiek pārsniegts kategorijas limits
- saglabāt informāciju Excel failā pārskatīšanai nākotnē

---

## Projektā izmantotās Python bibliotēkas
Visas bibliotēkas ir piemērotas datu glabāšanai, pārskatīšanai un manipulācijai.

- **`pandas`**  
  Izmantota datu glabāšanai tabulas formātā (DataFrame), datu apstrādei, lasīšanai no un rakstīšanai uz Excel failiem. Bibliotēka ir būtiska, lai saglabātu tēriņu informāciju un rēķinātu atlikumus.

- **`datetime`**  
  Nepieciešama, lai saglabātu precīzu datumu un laiku, kad tiek pievienots katrs izdevums.

- **`openpyxl`**  
  Šī bibliotēka tiek izmantota kopā ar `pandas`, lai strādātu ar Excel `.xlsx` failiem un pārvaldītu darblapas (sheet'us).

- **`os`**  
  Izmantojama, lai pārbaudītu faila esamību un strādātu ar failu ceļiem, ja nepieciešams (piemēram, nākotnē paplašinot projektu).

---

## Pašdefinētas datu struktūras

Programma veido un izmanto vairākas datu struktūras:

- **Saraksts `visas_kategorijas`**  
  Glabā 12 iepriekš definētās budžeta kategorijas. Lietotājs var piešķirt katrai no tām individuālu limitu un reģistrēt tēriņus.

- **Saraksti `limiti` un `atlikumi`**  
  Glabā katras kategorijas maksimālo mēneša limitu un aktuālo atlikumu.

- **`pandas.DataFrame` `izdevumi_df`**  
  Glabā katru izdevumu ar šādām kolonnām: “Datums”, “Kategorija”, “Izdevums”. Šī struktūra tiek papildināta ar katru jaunu ievadīto tēriņu.

---

### Programmas darbības:

Kad programma tiek palaista, tā parāda izvēlni:

Izvēlies darbību:
1. Izveidot budžetu
2. Pievienot izdevumu
3. Pabeigt visas darbības
---

## Ko dara katra funkcija?
### 1. Izveido budžetu

1. Ievadi kopējo mēneša budžetu
2. Programma pēc kārtas jautās par katru no 12 kategorijām
3. Ja ievadītā summa pārsniedz budžetu vai ir negatīva, programma paziņos: `pārsniedz atlikušo budžetu! Ievadi mazāku summu!`
4. Kad visi limiti ievadīti, tie tiek saglabāti failā **budzeta_limitu_kopsavilkums.xlsx` (lapā “Limiti”)**
5. Programma piedāvā iespēju `rediģēt limitus`, ja ir vēlme tos mainīt.
---
### 2. Pievieno izdevumus

1. Izvēlies kategoriju no saraksta
2. Ievadi izdevumu:
3. Ja summa pārsniedz atlikumu kategorijā, programma brīdina:` ! Izdevumi pārsniedz kategorijas limitu par ... EUR!`
4. Tiek automātiski atjaunināts atlikums un izdevums pierakstīts:
   - Excel failā, lapā “Izdevumi” ;
   - Kolonnas: Datums, Kategorija, Izdevums.
---
### 3. Pabeigt visas darbības

1. Programma izvada kopsavilkumu
2. Ja budžets ir pārsniegts: `Tu pārsniedzi savu mēneša budžetu par 5.00 EUR`
---

## Kur dati tiek saglabāti?

Failā **budzeta_limitu_kopsavilkums.xlsx**:

- **Lapa "Limiti"** – glabā katras kategorijas piešķirto limitu un aktuālo atlikumu.
- **Lapa "Izdevumi"** – glabā visus izdevumu ierakstus ar datumu, kategoriju un summu.
---

### Lietotāja kļūdu apstrāde

Programma pati pārbauda ievadīto datu korektumu:

- Nepareizi ievadīts teksts `input()` vietā rada: `Nederīgs ievades formāts!`
- Pārāk liels limits rada: `Limits 50.00€ pārsniedz atlikušo budžetu! Ievadi mazāku summu!`
- Negatīvi izdevumi vai limiti nav atļauti.
