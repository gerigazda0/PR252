# VMESNO POROČILO: Prometne nesreče v Sloveniji med leti 2009 in 2023

**Datum:** 14. april 2025

**Avtorji:** Nejc Gerkšič, Nik Likar, Eva Simonič, Jan Slanc in Tomaž Aleksander Udovič

**Projekt:** Analiza prometnih nesreč v Sloveniji

## 1. Uvod in opis problema

Namen te projektne naloge je analizirati podatke o prometnih nesrečah v Sloveniji v obdobju od leta 2009 do vključno leta 2023. Razumevanje vzrokov, značilnosti in geografske porazdelitve prometnih nesreč je lahko ključnega pomena za izboljšanje prometne varnosti. S pomočjo analize obsežnega nabora podatkov želimo odgovoriti na zastavljena raziskovalna vprašanja, ki se osredotočajo na najpogostejše vzroke nesreč, vlogo mladih voznikov, regionalne razlike, vpliv alkohola, sezonske trende in uporabo varnostnih pasov.

## 2. Podatki

Podatke za našo analizo smo pridobili s spletne strani OPSI (https://podatki.gov.si/dataset/mnzpprometne-nesrece-od-leta-2009-dalje). Zajemajo informacije o vseh prometnih nesrečah v Sloveniji od leta 2009 do 2023 in so dostopni v formatu CSV datotek, ločenih po letih. Vsaka datoteka vsebuje podrobne informacije o posamezni nesreči, vključno z datumom, uro, lokacijo, vzrokom, udeleženci in posledicami. Stolpci, ki so ključni za našo dosedanjo analizo, vključujejo: `VzrokNesrece`, `Starost`, `Spol`, `UpravnaEnotaStoritve`, `VrednostAlkotesta`, `DatumPN`, `PoskodbaUdelezenca`, `UporabaVarnostnegaPasu`, `GeoKoordinataX`, `GeoKoordinataY`. Za potrebe analize smo posamezne letne datoteke prenesli in jih s pomočjo knjižnice `pandas` v programskem jeziku Python združili v enoten DataFrame. Ta korak je omogočil lažjo in učinkovitejšo analizo celotnega časovnega obdobja.

## 3. Izvedene analize in glavne ugotovitve

V dosedanji iteraciji smo izvedli nekaj temeljnih analiz, da bi dobili vpogled v podatke in odgovorili na del naših raziskovalnih vprašanj.

### 3.1. Najpogostejši vzroki za prometne nesreče

Z analizo stolpca `VzrokNesrece` smo identificirali deset najpogostejših vzrokov prometnih nesreč v analiziranem obdobju.

![image](https://github.com/user-attachments/assets/65acbc71-301a-4131-b425-a6b902f33422)

Naredili smo tudi trende glavnih vzrokov prometnih nesreč po letih.

![image](https://github.com/user-attachments/assets/92ee68a9-b999-4b21-805c-ef047870f664)

### 3.2. Delež mladih voznikov med povzročitelji nesreč

Da bi preučili vlogo mladih voznikov kot povzročiteljev nesreč, smo ustvarili novo kategorijo 'MladiVoznik' za udeležence starosti med 18 in 24 let. Nato smo analizirali delež teh voznikov med vsemi, ki so bili označeni kot povzročitelji nesreče. Prav tako smo primerjali povprečno vrednost alkotesta po starostnih skupinah.

![image](https://github.com/user-attachments/assets/b1165874-0334-450e-83ec-d8213dfeff37)


### 3.3. Geografska porazdeljenost prometnih nesreč

Zanimalo nas je tudi, na katerih območjih Slovenije se zgodi največ nesreč. Takšna analiza nam omogoča, da prepoznamo kritične točke v prometni infrastrukturi, kjer bi bilo morda smiselno uvesti dodatne varnostne ukrepe, izboljšati prometno signalizacijo ali prilagoditi cestno ureditev. Za ta namen smo uporabili koordinatne podatke, zapisane v CSV datoteki, in jih prikazali na zemljevidu Slovenije s pomočjo interaktivne toplotne karte. Na tej karti so območja z večjo koncentracijo nesreč prikazana z intenzivnejšimi barvami.

![image](https://github.com/user-attachments/assets/b8350e94-7b1a-41eb-b809-1077c593ff92)

## 4. Nadaljnje analize in načrti

V nadaljevanju našega dela se bomo osredotočili na odgovore na preostala raziskovalna vprašanja. Načrtujemo naslednje analize:

* **Primerjava po spolu:** Preučili bomo, ali je večji delež povzročiteljev moškega ali ženskega spola.
* **Vpliv alkohola:** Analizirali bomo delež povzročiteljev nesreč, ki so bili pod vplivom alkohola, na podlagi stolpca `VrednostAlkotesta`.
* **Sezonski trendi:** Raziskali bomo, ali obstaja povezava med letnim časom (izpeljanim iz stolpca `DatumPN`) in številom prometnih nesreč.
* **Uporaba varnostnega pasu in posledice:** Analizirali bomo, kolikšen delež udeležencev s hudimi poškodbami ni uporabljal varnostnega pasu, s primerjavo stolpcev `PoskodbaUdelezenca` in `UporabaVarnostnegaPasu`.

## 5. Zaključek

Naša dosedanja analiza je omogočila prve vpoglede v najpogostejše vzroke prometnih nesreč, geografsko porazdelitev nesreč ter vlogo mladih voznikov kot povzročiteljev. Glavne ugotovitve doslej kažejo na pomembnost dejavnikov, kot so neprilagojena hitrost, neupoštevanje pravil o prednosti, ter vožnja pod vplivom alkohola, ki predstavljajo največji delež med povzročitelji nesreč. Opazili smo tudi določene razlike med mlajšimi vozniki (18–24 let) in ostalimi vozniki, tako glede njihovega deleža med povzročitelji kot tudi pri povprečni izmerjeni vrednosti alkohola. Na podlagi teh začetnih vpogledov bomo v nadaljevanju poglobili naše raziskovanje z namenom, da bi celoviteje odgovorili na zastavljena raziskovalna vprašanja in s tem prispevali k boljšemu razumevanju prometne varnosti v Sloveniji.

## 6. Viri kode

Za analizo podatkov smo uporabili programski jezik Python in naslednje knjižnice:

* `pandas` (za obdelavo in analizo podatkov)
* `matplotlib.pyplot` (za osnovno vizualizacijo podatkov)
* `geopandas` (delo z geografskimi podatki)
* `folium` (knjižnica za ustvarjanje interaktivnih zemljevidov na osnovi OpenStreetMap)
