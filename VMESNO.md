# VMESNO POROČILO: Analiza prometnih nesreč v Sloveniji (2009-2023)

**Datum:** 14. april 2025

**Avtor:** 

**Projekt:** Analiza prometnih nesreč v Sloveniji

## 1. Uvod in Opis Problema

Namen te projektne naloge je analizirati podatke o prometnih nesrečah v Sloveniji v obdobju od leta 2009 do vključno leta 2023. Razumevanje vzrokov, značilnosti in geografske porazdelitve prometnih nesreč je lahko ključnega pomena za izboljšanje prometne varnosti. S pomočjo analize obsežnega nabora podatkov želimo odgovoriti na zastavljena raziskovalna vprašanja, ki se osredotočajo na najpogostejše vzroke nesreč, vlogo mladih voznikov, regionalne razlike, vpliv alkohola, sezonske trende in uporabo varnostnih pasov.

## 2. Podatki

Podatke za našo analizo smo pridobili s spletne strani OPSI (https://podatki.gov.si/dataset/mnzpprometne-nesrece-od-leta-2009-dalje). Zajemajo informacije o vseh prometnih nesrečah v Sloveniji od leta 2009 do 2023 in so dostopni v formatu CSV datotek, ločenih po letih. Vsaka datoteka vsebuje podrobne informacije o posamezni nesreči, vključno z datumom, uro, lokacijo, vzrokom, udeleženci in posledicami. Stolpci, ki so ključni za našo dosedanjo analizo, vključujejo: `VzrokNesrece`, `Starost`, `Spol`, `UpravnaEnotaStoritve`, `VrednostAlkotesta`, `DatumPN`, `PoskodbaUdelezenca` in `UporabaVarnostnegaPasu`.

Za potrebe analize smo posamezne letne datoteke prenesli in jih s pomočjo knjižnice `pandas` v programskem jeziku Python združili v enoten DataFrame. Ta korak je omogočil lažjo in učinkovitejšo analizo celotnega časovnega obdobja.

## 3. Izvedene Analize in Glavne Ugotovitve

V dosedanji iteraciji smo izvedli nekaj temeljnih analiz, da bi dobili vpogled v podatke in odgovorili na del naših raziskovalnih vprašanj.

### 3.1. Najpogostejši vzroki za prometne nesreče

Z analizo stolpca `VzrokNesrece` smo identificirali deset najpogostejših vzrokov prometnih nesreč v analiziranem obdobju.

Slika1

### 3.2. Delež mladih voznikov med povzročitelji nesreč

Da bi preučili vlogo mladih voznikov kot povzročiteljev nesreč, smo ustvarili novo kategorijo 'MladiVoznik' za udeležence starosti med 16 in 24 let. Nato smo analizirali delež teh voznikov med vsemi, ki so bili označeni kot povzročitelji nesreče.

Slika2


### 3.3. Spolna struktura povzročiteljev prometnih nesreč

Prav tako nas je zanimala spolna struktura povzročiteljev nesreč. Analizirali smo spol udeležencev.

Slika3

## 4. Nadaljnje Analize in Načrti

V nadaljevanju našega dela se bomo osredotočili na odgovore na preostala raziskovalna vprašanja. Načrtujemo naslednje analize:

* **Regionalna analiza:** Preučili bomo, ali obstajajo območja v Sloveniji, kjer se zgodi statistično značilno več prometnih nesreč, z uporabo stolpca `UpravnaEnotaStoritve` in potencialno `Lokacija` ali koordinat, če bo potrebno natančnejše kartiranje.
* **Vpliv alkohola:** Analizirali bomo delež povzročiteljev nesreč, ki so bili pod vplivom alkohola, na podlagi stolpca `VrednostAlkotesta`.
* **Sezonski trendi:** Raziskali bomo, ali obstaja povezava med letnim časom (izpeljanim iz stolpca `DatumPN`) in številom prometnih nesreč.
* **Uporaba varnostnega pasu in posledice:** Analizirali bomo, kolikšen delež udeležencev s hudimi poškodbami ni uporabljal varnostnega pasu, s primerjavo stolpcev `PoskodbaUdelezenca` in `UporabaVarnostnegaPasu`.

## 5. Zaključek

Naša dosedanja analiza je omogočila prve vpoglede v najpogostejše vzroke prometnih nesreč ter značilnosti povzročiteljev glede na starost in spol. Glavne ugotovitve kažejo na pomembnost dejavnikov, kot so [], ter na razlike med mladimi in ostalimi vozniki ter med spoloma pri povzročanju nesreč. V prihodnjih korakih bomo poglobili analizo z namenom, da bi celoviteje odgovorili na zastavljena raziskovalna vprašanja in prispevali k boljšemu razumevanju prometne varnosti v Sloveniji.


## 6. Viri Kode

Za analizo podatkov smo uporabili programski jezik Python in naslednje knjižnice:

* `pandas` (za obdelavo in analizo podatkov)
* `matplotlib.pyplot` (za osnovno vizualizacijo podatkov)
* `seaborn` (za naprednejšo statistično vizualizacijo)