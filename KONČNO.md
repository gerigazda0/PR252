# KONČNO POROČILO: Prometne nesreče v Sloveniji med leti 2009 in 2023

**Datum:** 1. junij 2025

**Avtorji:** Nejc Gerkšič, Nik Likar, Eva Simonič, Jan Slanc in Tomaž Aleksander Udovič

**Projekt:** Analiza prometnih nesreč v Sloveniji

## 1. Uvod in opis problema

Prometne nesreče predstavljajo resno tveganje za javno zdravje in varnost v Sloveniji. Osrednji namen tega projekta je bil celovito analizirati podatke o prometnih nesrečah, zbranih med letoma 2009 in 2023, z namenom boljšega razumevanja ključnih vzrokov, trendov in dejavnikov, ki vplivajo na njihovo pogostost in resnost. Poseben poudarek smo namenili prepoznavanju kritičnih območij in dejavnikov tveganja, kar lahko pomembno prispeva k oblikovanju učinkovitih ukrepov za izboljšanje prometne varnosti v prihodnje.

**Glavna raziskovalna vprašanja:**
- Kateri so najpogostejši vzroki za prometne nesreče?
- Ali mladi vozniki pogosteje povzročajo nesreče?
- Na katerem območju Slovenije se zgodi največ nesreč?
- Kolikšen delež vseh povzročiteljev nesreč je bilo pod vplivom alkohola?
- V katerem letnem času je največ nesreč?
- Koliko odstotkov udeležencev s hudimi poškodbami ni uporabljalo varnostnega pasu?
- Ali je več povzročiteljev nesreč moškega ali ženskega spola?

## 2. Podatki in metodologija

### 2.1 Podatki
Podatke za našo analizo smo pridobili s spletne strani OPSI (https://podatki.gov.si/dataset/mnzpprometne-nesrece-od-leta-2009-dalje). Zajemajo informacije o vseh prometnih nesrečah v Sloveniji od leta 2009 do 2023 in so dostopni v formatu CSV datotek, ločenih po letih. Vsaka datoteka vsebuje podrobne informacije o posamezni nesreči, vključno z datumom, uro, lokacijo, vzrokom, udeleženci in posledicami.Stolpci, ki so bili ključni za našo analizo, vključujejo: VzrokNesrece, Starost, Spol, UpravnaEnotaStoritve, VrednostAlkotesta, DatumPN, PoskodbaUdelezenca, UporabaVarnostnegaPasu, GeoKoordinataX, GeoKoordinataY, Povzrocitelj, VrstaUdelezenca, ZaporednaStevilkaOsebeVPN ter KlasifikacijaNesrece. Ti podatki so nam omogočili podrobno analizo vzrokov, okoliščin in posledic prometnih nesreč, kot tudi identifikacijo vzorcev tveganega vedenja med udeleženci. Za potrebe analize smo posamezne letne datoteke prenesli in jih s pomočjo knjižnice `pandas` v programskem jeziku Python združili v enoten DataFrame. Ta korak je omogočil lažjo in učinkovitejšo analizo celotnega časovnega obdobja.

### 2.2 Metodologija
Pri obdelavi in analizi podatkov smo uporabili orodja in knjižnice programskega jezika Python. Za manipulacijo, čiščenje in združevanje podatkov smo uporabili knjižnico pandas, za izvajanje matematičnih in statističnih operacij pa numpy. Prostorske oziroma geografske analize in vizualizacije smo izvajali s pomočjo knjižnic geopandas in folium, ki omogočata prikaz in obdelavo prostorskih podatkov ter interaktivno vizualizacijo lokacij prometnih nesreč na zemljevidih. Za pripravo različnih vrst grafov smo uporabili knjižnico matplotlib.

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

Na podlagi prostorske analize prometnih nesreč z uporabo “heatmap” vizualizacije ugotavljamo, da so prometne nesreče v Sloveniji izrazito skoncentrirane na območjih večjih urbanih središč, predvsem v Ljubljani in njeni okolici, kjer je gostota nesreč najvišja. Povečana gostota je opazna tudi v okolici Maribora ter vzdolž glavnih cest in avtocest, ki povezujejo večja mesta. V primerjavi s tem so prometne nesreče precej redkejše na podeželju in obmejnih območjih, kjer je prometna obremenitev manjša.

![image](https://github.com/user-attachments/assets/b8350e94-7b1a-41eb-b809-1077c593ff92)

### 3.4. Vpliv alkohola na nesreče

### 3.5. 
