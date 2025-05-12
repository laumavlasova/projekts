import pandas as pd
from datetime import datetime 
import os
from openpyxl import load_workbook

def izvelne(): 
    print("\nIzvēlies darbību:")
    print("1. Izveidot budžetu")
    print("2. Pievienot izdevumu")
    print("3. Pabeigt visas darbības")
    return input (">> ").strip()


def ietaupi_naudu():
    visas_kategorijas = [
        "pārtika",
        "ēšana ārpus mājas (restorāni/fast food/kafejnīcas)",
        "mājas izdevumi (komunālie + īre / nekustamā īpašuma nodoklis)",
        "hobiji",
        "mājdzīvnieki",
        "apģērbs",
        "higēnas preces",
        "medicīniskie izdevumi",
        "transports",
        "izklaide (kino, teātris, klubs)",
        "abonementi",
        "dāvanas"
    ]
    budzeta_fails = "budzeta_limitu_kopsavilkums.xlsx"
    limiti = []
    atlikumi = []
    izdevumi_df = pd.DataFrame(columns= ["Datums", "Kategorija" "Izdevums"])
    kopējie_izdevumi = 0
    sākotnējais_budžets = 0

    while True:
        opcija = izvelne()

        if opcija == "1":
            print("Vēlies ietaupīt naudu? Sākam!")
            sākotnējais_budžets = float(input("Ievadi šī mēneša budžetu (EUR): "))
            atlikusi_nauda = sākotnējais_budžets

            print("\nIevadi savus mēneša limitus katrā kategorijā (EUR): ")
            for kategorija in visas_kategorijas:
                while True:
                    try:
                        limits = float(input(f"{kategorija} (Tev atlikuši {atlikusi_nauda:.2f}€): "))
                        if limits < 0:
                            print("Limits nevar būt negatīvs.  Ievadi no jauna.")
                        elif round(limits, 2) > round(atlikusi_nauda, 2):
                            print(f"Limits {limits:.2f}€ pārsniedz atlikušos ienākumus! Ievadi mazāku summu!")
                        else:
                            limiti.append(limits)
                            atlikumi.append(limits)
                            atlikusi_nauda = round(atlikusi_nauda - limits, 2)
                            break
                    except ValueError:
                        print("Lūdzu ievadi skaitli!")

            limitu_dati = pd.DataFrame({
                'Kategorija': visas_kategorijas,
                'Mēneša limits': limiti,
                'Atlikums': atlikumi
            })
            with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="w") as writer:
                limitu_dati.to_excel(writer, sheet_name="Limiti", index=False)
                izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)
            print(f"\n Tavi limiti ir saglabāti! Tos vari atrast : {budzeta_fails}")

        elif opcija == "2":
            try:
                limitu_dati = pd.read_excel(budzeta_fails, sheet_name="Limiti")
                izdevumi_df = pd.read_excel(budzeta_fails, sheet_name="Izdevumi")
            except FileNotFoundError:
                print("!!Bužeta fails netika atrasts. Vispirms norādi savu budžetu!!")
                continue

            print("\nIzvēlies kategoriju:")
            for i, kat in enumerate(visas_kategorijas, 1):
                print(f"{i}. {kat}")

            try:
                kat_izvele = int(input("Izvēlies kategorijas numuru: ").strip()) - 1
                if 0 <= kat_izvele < len(visas_kategorijas):
                    iztērēts = float(input(f"Ievadi savus izdevumus kategorijā '{visas_kategorijas[kat_izvele]}': ").strip())
                    if iztērēts < 0:
                        print("Izdevumi nevar būt negatīvi!")
                        continue
                   
                    kopējie_izdevumi += iztērēts
                    atlikumi[kat_izvele] -= iztērēts
                    if atlikumi[kat_izvele] < 0:
                        parsniegums = abs(atlikumi[kat_izvele])
                        print(f"! Izdevumi pārsniedz kategorijas limitu par {atlikumi[kat_izvele]:.2f} EUR!")
                        atlikumi[kat_izvele] = 0 
                        
                    print(f"Atjaunotais atlikums: {atlikumi[kat_izvele]:.2f} EUR kategorijā '{visas_kategorijas[kat_izvele]}'")

                    jauns_ieraksts = pd.DataFrame([{
                        "Datums": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kategorija": visas_kategorijas[kat_izvele],
                        "Izdevums": iztērēts
                    }])
                    izdevumi_df = pd.concat([izdevumi_df, jauns_ieraksts], ignore_index=True)

                    with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="a") as writer:
                        limitu_dati["Atlikums"] = atlikumi
                        limitu_dati.to_excel(writer, sheet_name="Limiti", index=False)
                        izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)
                    print("Izdevumi ir veiksmīgi saglabāti! :) ")
                else:
                    print("Nederīgs kategorijas numurs!")
            except ValueError:
                print("Nederīgs ievades formāts!")
                
        elif opcija == "3":
            atlikusais_budzets = sum(atlikumi)
            print("Uz tikšanos!")
            print(f"\nSākotnējais budžets: {sākotnējais_budžets:.2f} EUR")
            print(f"\nSKopējie izdevumi: {kopējie_izdevumi:.2f} EUR")
            if kopējie_izdevumi > sākotnējais_budžets:
                print(f"Tu pārsniedzi savu mēneša budžetu par {kopējie_izdevumi - sākotnējais_budžets:.2f} EUR")
            else:
                print(f"Tu šomēnes esi ietaupījis {sākotnējais_budžets - kopējie_izdevumi:.2f} EUR")
            break
        else:
            print("Nederīga izvēle! Lūdzu izvēlies starp 1, 2 vai 3!")
    
if __name__ == "__main__":
    ietaupi_naudu()