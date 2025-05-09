import pandas as pd
from datetime import datetime 
import os
from openpyxl import load_workbook

def ietaupi_naudu():
    print("Vēlies ietaupīt naudu? SĀKAM!")
    ienakumi = float(input("Ievadi budžetu šim mēnesim(€):"))
    atlikusi_nauda = ienakumi  # Lai sekotu, cik naudas paliek
    kategorijas = [
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
    limiti = []
    atlikumi = []
    print("\nIevadi savus mēneša limitus (€):")

    neparsniegts = False
    for kategorija in kategorijas:
        if atlikusi_nauda == 0:
            if not neparsniegts:
                print(f"Esi pārsniedzis budzetu. Atlikušajam limitam tiek piešķirts 0€")
                neparsniegts = True
            limiti.append(0)
            atlikumi.append(0)
            continue

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

    budzeta_fails = "budzeta_limitu_kopsavilkums.xlsx"
    limitu_dati = pd.DataFrame({
        'Kategorija': kategorijas,
        'Mēneša limits': limiti,
        'Atlikums': atlikumi
    })

    with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="w") as writer:
        limitu_dati.to_excel(writer, sheet_name="Limiti", index=False)

    print(f"\n Tavi limiti ir saglabāti! Tos vari atrast : {budzeta_fails}")

    if atlikusi_nauda > 0:
        print(f"\nPēc budžeta sastādīšanas Tev vēl paliek brīvi {atlikusi_nauda:.2f}€")
    else:
        print("\nVisi ienākumi ir sadalīti pa kategorijām!")
    try:
        wb = load_workbook(budzeta_fails)
        if "Izdevumi" in wb.sheetnames:
            izdevumi_df = pd.read_excel(budzeta_fails, sheet_name="Izdevumi")
        else:
            izdevumi_df = pd.DataFrame({
                "Datums": pd.Series(dtype='str'),
                "Kategorija": pd.Series(dtype='str'),
                "Izdevums": pd.Series(dtype='float')
            })
    except:
        izdevumi_df = pd.DataFrame({
            "Datums": pd.Series(dtype='str'),
            "Kategorija": pd.Series(dtype='str'),
            "Izdevums": pd.Series(dtype='float')
        })
        
    while True:
        print("\n Vai vēlies reģistrēt izdevumus?(jā/nē)")
        izvele = input(">> ").strip().lower()
        if izvele != "jā":
            print("Uz tikšanos!")
            break

        print("\nIevadi savus šī mēneša izdevumus: ")
        for i, kat in enumerate(kategorijas):
            while True:
                try:
                    iztērēts = float(input(f"Ievadi, cik esi iztērējis kategorijā '{kategorijas[i]}': "))
                    if iztērēts < 0:
                        print("Tēriņš nevar būt negatīvs.")
                        continue
                    jauns_atlikums = atlikumi[i] - iztērēts
                    if jauns_atlikums < 0:
                        parsniedz_budzetu = abs(jauns_atlikums);atlikusi_nauda -= parsniedz_budzetu
                        print(f"Izdevumi pārsniedza kategorijas limitu par {parsniedz_budzetu:.2f}€. Atlikušie kopējie ienākumi: {atlikusi_nauda:.2f}")
                        atlikumi[i] = 0
                    else:
                        atlikumi[i] = jauns_atlikums
                    print(f"Atjaunots atlikuns: {atlikumi[i]:.2f}€ kategorijā '{kategorijas[i]}'")

                    jauns_ieraksts = pd.DataFrame([{
                        "Datums": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kategorija": kategorijas[i],
                        "Izdevums": iztērēts
                    }])
                    izdevumi_df = pd.concat([izdevumi_df, jauns_ieraksts], ignore_index=True)

                    wb = load_workbook(budzeta_fails)
                    if "Izdevumi" in wb.sheetnames:
                        del wb["Izdevumi"]
                    wb.save(budzeta_fails)
                    wb.close()

                    with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="a") as writer:
                        izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)

                    break
                except ValueError:
                    print("Lūdzu ievadi derīgus skaitļus!")

            print("Visi izdevumi veiksmīgi pievienoti!")
if __name__ == "__main__":
    ietaupi_naudu()
