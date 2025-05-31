# VMESNO POROČILO: Prometne nesreče v Sloveniji med leti 2009 in 2023

**Datum:** 14. april 2025

**Avtorji:** Nejc Gerkšič, Nik Likar, Eva Simonič, Jan Slanc in Tomaž Aleksander Udovič

**Projekt:** Analiza prometnih nesreč v Sloveniji

## 1. Uvod in opis problema

Prometne nesreče predstavljajo pomembno grožnjo za javno zdravje in varnost. Namen tega projekta je analizirati podatke o prometnih nesrečah v Sloveniji med letoma 2009 in 2023, da bi razumeli ključne vzroke, trende in dejavnike, ki vplivajo na njihovo pojavnost. Glavni cilj je identificirati kritična območja in dejavnike tveganja, kar lahko prispeva k izboljšanju prometne varnosti.

**Glavna raziskovalna vprašanja:**
- Kateri so najpogostejši vzroki nesreč?
- Ali mladi vozniki (18–24 let) pogosteje povzročajo nesreče?
- Kje se zgodi največ nesreč? (geografska analiza)
- Kakšen je vpliv alkohola na prometne nesreče?
- Ali obstajajo sezonski trendi?
- Kako uporaba varnostnih pasov vpliva na resnost posledic?

## 2. Podatki in metodologija

### 2.1 Vir podatkov
Podatki pridobljeni iz [OPSI](https://podatki.gov.si), ki vključujejo:
- 15 let prometnih nesreč (2009-2023)
- 50+ spremenljivk na nesrečo
- Geografske koordinate

### 2.2 Metode
- Združevanje podatkov (pandas)
- Vizualizacija (matplotlib, folium)
- Statistična analiza

## 3. Glavne ugotovitve

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