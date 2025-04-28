import pandas as pd

def ietaupi_naudu():
    print("Vēlies ietaupīt naudu? SĀKAM!")
    ienakumi = float(input("Ievadi savus mēneša ienākumus(€):"))
    kategorijas = [
        "pārtika",
        "ēšana ārpus mājas (restorāni/fast food/kafejnīcas)","mājas izdevumi (komunālie + īre / nekustamā īpašuma nodoklis)",
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

    print("\nIevadi savus mēneša limitus (€):")
    for kategorija in kategorijas:
        while True:
            try:
                limits = float(input(f"{kategorija}: "))
                limiti.append(limits)
                break 
            except ValueError:
                print("Lūdzu ievadi skaitli!")

    dati = pd.DataFrame({
        'Kategorija': kategorijas,
        'Mēneša limits (€)': limiti
    })

    faila_nosaukums = "naudas_kopsavilkums.xlsx"
    dati.to_excel(faila_nosaukums, index=False)

    print (f"\n Tavi limiti ir saglabāti! Tos vari atrast : {faila_nosaukums}")

if __name__ == "__main__":
       ietaupi_naudu() 
