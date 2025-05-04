import pandas as pd

def ietaupi_naudu():
    print("Vēlies ietaupīt naudu? SĀKAM!")
    ienakumi = float(input("Ievadi savus mēneša ienākumus(€):"))
    atlikusi_nauda = ienakumi #Lai sekotu, cik naudas paliek
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

    neparsniegts = False
    for kategorija in kategorijas:
        if atlikusi_nauda == 0:
             if not neparsniegts:
                print(f"Esi pārsniedzis budetu. Atlikušajam limitam tiek piešķirts 0€")
                neparsniegts = True
             limiti.append(0)
             continue
        
        while True:
            try:
                limits = float(input(f"{kategorija} (Tev atlikuši {atlikusi_nauda:.2f}€): "))
                if limits < 0:
                     print("Limits nevar būt negatīvs.  Ievadi no jauna.")
                elif round(limits,2) > round(atlikusi_nauda, 2):
                     print(f"Limits {limits:.2f}€ pārsniedz atlikušos ienākumus! Ievadi mazāku summu!")
                else:
                     limiti.append(limits)
                     atlikusi_nauda = round(atlikusi_nauda - limits, 2)
                     break 
            except ValueError:
                print("Lūdzu ievadi skaitli!")

    dati = pd.DataFrame({
        'Kategorija': kategorijas,
        'Mēneša limits (€)': limiti
    })

    faila_nosaukums = "budzeta_limitu_kopsavilkums.xlsx"
    dati.to_excel(faila_nosaukums, index=False)

    print (f"\n Tavi limiti ir saglabāti! Tos vari atrast : {faila_nosaukums}")

    if atlikusi_nauda > 0:
         print(f"\nPēc budeta sastādīšanas Tev vēl paliek brīvi {atlikusi_nauda:.2f}€")
    else:
         print("\nVisi ienākumi ir sadalīti pa kategorijām!")

     while True:
          print("\n Vai vēlies reģistrēt izdevumus?(jā/nē)")
          izvele = input (">> ").strip().lower()
          if izvele != "jā":
               print("Uz tikšanos!")
               break
     print("\nPieejamās kategorijas: ")
     for i, kat in enumerate(kategorijas):
          print(f"{i+1}. {kat} (atlikums:{atlikumi[i]:.2f}€)")
     try:
          izveleta_index = int(input("Ievadi kategorijas numuru: ")) - 1
          iztērēts = float (input(f"Ievadi, cik esi iztēŗējis kategorijā' {kategorijas[izveleta_index]}':"))
          if iztērēts < 0:
               print("Tēriņš nevar būt negatīvs.")
               continue
          if iztērēts > atlikumi[izveleta_index]:
               print(f"Ievadītā summa pārsniedz atlikumu({atlikumi[izveleta_index]:.2f}€)! Ievadi mazāku summu.")
               continue
          atlikumi[izveleta_index]=round(atlikumi[izveleta_index] - iztērēts, 2)
          print(f"Atjaunots atlikums: {atlikumi[izveleta_index]:.2f}€ kategorijā '{kategorijas[izveleta_index]}'")

     except ValueError:
          print("Lūdzu ievadi derīgus skaitļus!")
          
if __name__ == "__main__":
       ietaupi_naudu() 
