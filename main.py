import pandas as pd
from datetime import datetime 
import os
from openpyxl import load_workbook

# galvenā izvēlne
def izvelne(): 
    print("\nIzvēlies darbību:")
    print("1. Izveidot budžetu")
    print("2. Pievienot izdevumu")
    print("3. Pabeigt visas darbības")
    return input (">> ").strip()

# galvenā funkcija
def ietaupi_naudu():
    #kategoriju definēšana
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
    budzeta_fails = "budzeta_limitu_kopsavilkums.xlsx" #fails, kurā glabāsies visi dati
    limiti = []  #saraksts ar lietotāja ievadītajiem limitiem
    atlikumi = []  #saraksts ar atlikumu katrai kategorijai
    izdevumi_df = pd.DataFrame({
        "Datums": pd.Series(dtype="str"),  # tukša kolonna, kurā būs teksts
        "Kategorija": pd.Series(dtype="str"),  # tukša kolonna, kurā būs teksts
        "Izdevums": pd.Series(dtype="float") # tukša kolonna, kurā būs skaitļi ar komatiem

    }) 
    kopējie_izdevumi = 0 # sākotnējie kopējie izdevumi
    sākotnējais_budžets = 0 #sākotnējais budzets

    while True:
        opcija = izvelne()

        if opcija == "1":
            print("Vēlies ietaupīt naudu? Sākam!")
            sākotnējais_budžets = float(input("Ievadi šī mēneša budžetu (EUR): ")) # float parvers input datus uz decimālskaitli
            atlikusi_nauda = sākotnējais_budžets # Izveido atsevišķu mainīgo, kas uzskaitīs vēl neatdalīto budžeta daļu.
                                                 # Tas sākumā ir vienāds ar sākotnējo budžetu, bet tiks samazināts,
                                                 # katru reizi piešķirot naudu kādai kategorijai.
                                                 # Sākotnējais budžets paliek nemainīgs pārskatiem un salīdzināšanai.

            limiti.clear()  # Notīra iepriekšējos ierakstus, ja budžets tiek veidots no jauna
            atlikumi.clear() # Citādāk iepriekšējie limiti saglabājas un veido kļūdainu DataFrame garumu

            print("\nIevadi savus mēneša limitus katrā kategorijā (EUR): ")
            for kategorija in visas_kategorijas:
                while True:
                    try:
                        limits = float(input(f"{kategorija} (Tev atlikuši {atlikusi_nauda:.2f}€): "))
                        if limits < 0:
                            print("Limits nevar būt negatīvs.  Ievadi no jauna.")
                        elif round(limits, 2) > round(atlikusi_nauda, 2): #Pārbauda, vai ievadītais limits pārsniedz atlikušo budžetu.
                                                                         # Abas vērtības tiek noapaļotas līdz 2 cipariem aiz komata (centiem),
                                                                        # lai izvairītos no floating point kļūdām (piem, 49.999999...).

                            print(f"Limits {limits:.2f}€ pārsniedz atlikušo budžetu! Ievadi mazāku summu!")
                        else:
                            #pievieno limitu sarakstam un samazina atlikumu
                            limiti.append(limits)
                            atlikumi.append(limits)
                            atlikusi_nauda = round(atlikusi_nauda - limits, 2)
                            break
                    except ValueError:
                        print("Lūdzu ievadi skaitli!")
            
            # izveidot DataFrame un saglabā excel failā
            limitu_dati = pd.DataFrame({
                'Kategorija': visas_kategorijas,
                'Mēneša limits': limiti,
                'Atlikums': atlikumi
            })
            with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="w") as writer: # ar mode w failu pārraksta (nevis papildina)
                limitu_dati.to_excel(writer, sheet_name="Limiti", index=False) #index=False nozimee, ka netiek pievienota lieka kolonna ar rindu indeksiem
                izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)
            print(f"\n Tavi limiti ir saglabāti! Tos vari atrast : {budzeta_fails}")

            #rediget savu budzetu/limitus, pirms tālākām darb;ib;a,
            rediget = input("Vai vēlies rediģēt savu budžetu, pirms turpinam tālāk? (Jā/Nē): ").strip().lower() # strip noņem lieko whitespace
            if rediget == "jā":
                while True:
                    print("Izvēlies kategoriju, kuru rediģēt:")
                    for i, kat in enumerate(visas_kategorijas, 1): # Cikls, kas iet cauri visām budžeta kategorijām.
                                                                   # 'i' ir kategorijas kārtas numurs (sākot no 1),
                                                                  # enumerate(..., 1) ļauj lietotājam rādīt numerētu sarakstu (1., 2., 3., ...)
                                                                   #sākot ar 1, nevis ar 0
                        print(f"{i}. {kat} (Pašreizējais limits kategorijai: {limiti[i-1]:.2f} EUR)")
                    try:
                       kat_izvele = int(input("Izvēlies kategorijas numuru: ").strip()) - 1
                       if 0 <= kat_izvele < len(visas_kategorijas): # Pārbaude, vai lietotāja izvēlētais indekss ir derīgā robežās
                                                                    # (ne mazāks par 0 un mazāks par kategoriju skaitu),
                                                                    # lai izvairītos no piekļuves kļūdām (IndexError).
                            jauns_limits = float(input(f"Ievadi jauno limitu kategorijai'{visas_kategorijas[kat_izvele]}': ").strip())
                            if jauns_limits < 0:
                                print("Izdevumi nevar būt negatīvi")
                            else:
                                atlikuma_starpiba = jauns_limits - limiti[kat_izvele]
                                atlikumi[kat_izvele] += atlikuma_starpiba
                                limiti[kat_izvele] = jauns_limits
                                print(f"Jaunais limits kategorijai '{visas_kategorijas[kat_izvele]}' ir {jauns_limits:.2f} EUR")

                                #Atjauno failā
                                limitu_dati["Mēneša limits"] = limiti
                                limitu_dati["Atlikums"] = atlikumi
                                with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="w") as writer:
                                    limitu_dati.to_excel(writer, sheet_name="Limiti", index=False)
                                    izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)
                                print("Limiti ir veiksmīgi atjaunoti")
                       else:
                           print("Nederīgs kategorijas numurs!")
                    except ValueError:
                        print("Nederīgs ievades formāts!")

                    papildus_rediget = input("Vai vēlies vēl ko rediģēt? (Jā/Nē): ").strip().lower()
                    if papildus_rediget != "jā":
                        break

        elif opcija == "2":
            if sākotnējais_budžets == 0 or not limiti:
                print("!!Bužeta fails netika atrasts. Vispirms norādi savu budžetu!!")
                continue 
            try:
                limitu_dati = pd.read_excel(budzeta_fails, sheet_name="Limiti") #Nolasa saglabāto limitu datus
                izdevumi_df = pd.read_excel(budzeta_fails, sheet_name="Izdevumi") # # Nolasa iepriekš saglabātos izdevumu datus no Excel lapas "Izdevumi"
                izdevumi_df = izdevumi_df.astype({ # Pārveido kolonnu datu tipus, lai nodrošinātu, ka:
                    "Datums": "str", # "Datums" un "Kategorija" ir teksts (str)
                    "Kategorija": "str", 
                    "Izdevums": "float" # "Izdevums" ir skaitlis (float)
                })                      # Tas novērš iespējamās kļūdas turpmākajā apstrādē un brīdinājumus par nesaderību.


                atlikumi = limitu_dati["Atlikums"].tolist()                       # Iegūst atlikumus kā sarakstu no Excel datiem
            except FileNotFoundError:
                print("!!Bužeta fails netika atrasts. Vispirms norādi savu budžetu!!") # Ja fails nav atrasts, informē lietotāju
                continue

            print("\nIzvēlies kategoriju:")
            for i, kat in enumerate(visas_kategorijas, 1): # enumerate() ļauj ciklā vienlaikus iegūt gan indeksu (i), gan vērtību (kat).
                                                           # Šeit i sākas no 1, lai lietotājam parādītu izvēles sākot no 1. pozīcijas.
                print(f"{i}. {kat}")        # Izvada kategorijas numuru un nosaukumu

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
                        parsniegums = abs(atlikumi[kat_izvele]) # Aprēķina pārsniegto summu kā pozitīvu vērtību (absolūto vērtību-abs), nevis negatīvu
                        print(f"! Izdevumi pārsniedz kategorijas limitu par {atlikumi[kat_izvele]:.2f} EUR!")
                        atlikumi[kat_izvele] = 0 
                        
                    print(f"Atjaunotais atlikums: {atlikumi[kat_izvele]:.2f} EUR kategorijā '{visas_kategorijas[kat_izvele]}'")

                    jauns_ieraksts = pd.DataFrame([{
                        "Datums": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Kategorija": visas_kategorijas[kat_izvele],
                        "Izdevums": iztērēts
                    }])
                    izdevumi_df = pd.concat([izdevumi_df, jauns_ieraksts], ignore_index=True) # pd.concat() ir pandas funkcija, kas apvieno vairākus DataFrame kopā
                                                                                              # - Apvieno esošo izdevumu tabulu ar jauno ierakstu.
                                                                                              # ignore_index=True pārindekse visu, lai indeksiem nav atkārtojumu.

                    with pd.ExcelWriter(budzeta_fails, engine="openpyxl", mode="w") as writer:
                        limitu_dati["Atlikums"] = atlikumi # Atjauno DataFrame kolonā 'Atlikums' aktuālās atlikumu vērtības
                                                           # no saraksta 'atlikumi' pēc izdevumu apstrādes.
                        limitu_dati.to_excel(writer, sheet_name="Limiti", index=False)
                        izdevumi_df.to_excel(writer, sheet_name="Izdevumi", index=False)
                    print("Izdevumi ir veiksmīgi saglabāti! :) ")
                else:
                    print("Nederīgs kategorijas numurs!")
            except ValueError:
                print("Nederīgs ievades formāts!")
                
        elif opcija == "3":
            print("Uz tikšanos!")
            print(f"\nSākotnējais budžets: {sākotnējais_budžets:.2f} EUR")
            print(f"\nKopējie izdevumi: {kopējie_izdevumi:.2f} EUR")
            if kopējie_izdevumi > sākotnējais_budžets:
                print(f"Tu pārsniedzi savu mēneša budžetu par {kopējie_izdevumi - sākotnējais_budžets:.2f} EUR")
            else:
                print(f"Tu šomēnes esi ietaupījis {sākotnējais_budžets - kopējie_izdevumi:.2f} EUR")
            break
        else:
            print("Nederīga izvēle! Lūdzu izvēlies starp 1, 2 vai 3!")
    
if __name__ == "__main__":
    ietaupi_naudu()