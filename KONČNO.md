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

### 3.1 Najpogostejši vzroki za prometne nesreče

Ugotovili smo, da je top 5 vzrokov za prometne nesreče naslednje: premiki z vozilom, neupoštevanje pravil o prednosti, neprilagojena hitrost, neustrezna varnostna razdalja, nepravilna stran/smer vožnje. Ti vzroki predstavljajo 85% vseh nesreč. Prav tako smo prišli do spoznanja, da je leta 2020 število prometnih nesreč dokaj strmo upadlo, kar lahko logično povežemo z omejitvami COVID-19 pandemije. 

![image](https://github.com/user-attachments/assets/89efac20-7988-43b3-ba9c-a0975e9fcd3c)

### 3.2 Delež mladih voznikov med povzročitelji nesreč

Da bi preučili vlogo mladih voznikov kot povzročiteljev nesreč, smo ustvarili novo kategorijo 'MladiVoznik' za udeležence starosti med 18 in 24 let. Nato smo analizirali delež teh voznikov med vsemi, ki so bili označeni kot povzročitelji nesreče. Ugotovili smo, da je mladih povzročiteljev nesreč 14.2%. Pri mladih voznikih je razlog za nesreče največkrat neprilagojena hitrost, kar se razlikuje od 'starejših' voznikov, kjer je najpogostejši vzrok premik z vozilom.

![image](https://github.com/user-attachments/assets/d8dd0f8d-960c-4883-834d-abcc3d5ed413)

### 3.3 Geografska porazdeljenost prometnih nesreč

Na podlagi prostorske analize prometnih nesreč z uporabo “heatmap” vizualizacije ugotavljamo, da so prometne nesreče v Sloveniji izrazito skoncentrirane na območjih večjih urbanih središč, predvsem v Ljubljani in njeni okolici, kjer je gostota nesreč najvišja. Povečana gostota je opazna tudi v okolici Maribora ter vzdolž glavnih cest in avtocest, ki povezujejo večja mesta. V primerjavi s tem so prometne nesreče precej redkejše na podeželju in obmejnih območjih, kjer je prometna obremenitev manjša. 

![image](https://github.com/user-attachments/assets/b8350e94-7b1a-41eb-b809-1077c593ff92)

Prav tako nas je zanimalo, kateri cestni odsek je najnevarnejši, glede na prometnost ceste v primerjavi z nesrečami, ki se tam zgodijo. S tem pristopom dobimo bolj realno sliko o nevarnosti posameznih odsekov, saj primerjamo število nesreč na milijon vozil in tako izpostavimo tudi manj prometne, a statistično bolj nevarne ceste. Rezultati so pokazali, da so najbolj nevarne ceste v Sloveniji Murska Sobota, Rogatec in Nova Gorica.

![image](https://github.com/user-attachments/assets/01675d0c-0b72-4f2f-a95e-1c91fa227a91)

### 3.4 Vpliv alkohola na nesreče

Analizirali smo tudi vpliv alkohola na povzročanje prometnih nesreč. Ugotovili smo, da je bilo pod vplivom alkohola 10,94 % vseh povzročiteljev nesreč, pri čemer jih je 6,66 % prekoračilo zakonsko dovoljeno mejo alkohola v krvi. Posebej nas je zanimal delež huje poškodovanih udeležencev, ki so jih povzročili pijani vozniki; rezultati kažejo, da so ti vozniki odgovorni za skoraj tri četrtine tovrstnih nesreč.

![image](https://github.com/user-attachments/assets/7eb44b24-6f73-45d4-a930-2022c6dc10e7)

### 3.5 Uporaba varnostnega pasu

Rezultati jasno kažejo, da uporaba varnostnega pasu bistveno zmanjša tveganje za najhujše posledice prometnih nesreč. Med udeleženci, ki so uporabljali pas, je bila smrtnost le 0,21 %, medtem ko je bila pri tistih brez pasu kar 1,58 %. Prav tako je bil delež hudih telesnih poškodb pri neuporabi pasu več kot štirikrat večji kot pri uporabi. Poleg tega je bilo pri uporabnikih pasu precej več primerov, ko so nesrečo prestali brez poškodb. Ti podatki potrjujejo, da je uporaba varnostnega pasu eden najučinkovitejših ukrepov za zmanjšanje posledic prometnih nesreč.

![image](https://github.com/user-attachments/assets/7c00b75b-34f7-4480-ae66-b0d00ccb273e)

### 3.6 Vpliv spola na prometne nesreče

### 3.7 Vpliv letnega časa na prometne nesreče

Analiza pogostosti najpogostejših vzrokov prometnih nesreč po letnih časih kaže, da se največ nesreč zgodi v poletnih in jesenskih mesecih. Skoraj vsi glavni vzroki, kot so neupoštevanje pravil o prednosti, neprilagojena hitrost, neustrezna varnostna razdalja in premiki z vozilom, dosegajo vrhove v tem obdobju, medtem ko je število nesreč najnižje pozimi. Ti rezultati kažejo, da je tveganje za prometno nesrečo zaradi najpogostejših vzrokov večje v obdobjih, ko je na cestah več prometa in so pogoji za vožnjo boljši.

![image](https://github.com/user-attachments/assets/6d633814-4b6f-400f-aba7-4445a80fb89f)
