import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Prometne nesreče v Sloveniji", layout="wide")

@st.cache_data
def load_data():
    file_path = "podatki/pn2009_2023.csv"
    try:
        df = pd.read_csv(file_path, sep=',')
        return df
    except Exception as e:
        st.error(f"Napaka pri nalaganju podatkov: {e}")
        return None

data = load_data()

st.sidebar.title("📊 Navigacija")
page = st.sidebar.radio("Izberi sklop:", [
    "📍 Toplotna karta",
    "🚧 Nevarni odseki",
    "⚠️ Vzroki nesreč",
    "👶 Mladi povzročitelji",
    "🍷 Alkohol",
    "🛡️Varnostni pas",
    "👩‍🦰👨‍🦱 Spol povzročiteljev",
    "🌱 Letni časi"
])

if data is not None:
    st.success("Podatki uspešno naloženi.")

    if page == "📍 Toplotna karta":
        st.title("📍 Toplotna karta prometnih nesreč")

        # Interaktivni filter po letih
        leto_min = int(data['Leto'].min())
        leto_max = int(data['Leto'].max())
        izbrano_leto = st.slider(
            "Izberi obdobje nesreč",
            min_value=leto_min,
            max_value=leto_max,
            value=(leto_min, leto_max)
        )

        sample = data[(data['Leto'] >= izbrano_leto[0]) & (data['Leto'] <= izbrano_leto[1])]
        sample = sample.dropna(subset=["GeoKoordinataX", "GeoKoordinataY"]).sample(n=3000, random_state=42)
        sample["GeoKoordinataX"] = sample["GeoKoordinataX"].astype(str).str.replace(",", ".").astype(float)
        sample["GeoKoordinataY"] = sample["GeoKoordinataY"].astype(str).str.replace(",", ".").astype(float)

        geometry = [Point(xy) for xy in zip(sample["GeoKoordinataY"], sample["GeoKoordinataX"])]
        gdf = gpd.GeoDataFrame(sample, geometry=geometry, crs="EPSG:3794").to_crs(epsg=4326)

        # Filtriraj na meje Slovenije
        gdf = gdf[
            (gdf.geometry.y >= 45.4) & (gdf.geometry.y <= 47.1) &
            (gdf.geometry.x >= 13.3) & (gdf.geometry.x <= 16.6)
        ]

        if len(gdf) > 0:
            heat_data = [[point.y, point.x] for point in gdf.geometry]
            m = folium.Map(location=[46.1512, 14.9955], zoom_start=8, tiles="CartoDB positron")
            HeatMap(heat_data, radius=10, blur=15, min_opacity=0.3).add_to(m)
            st_folium(m, width=1000)
        else:
            st.warning("Po filtriranju ni ostalo nobenih podatkov v Sloveniji.")

    elif page == "🚧 Nevarni odseki":
        st.title("🚧 Top 10 najbolj nevarnih cestnih odsekov glede na prometno obremenitev (2023)")

        # Interaktivni filter po upravni enoti
        ue_options = sorted(data['UpravnaEnotaStoritve'].dropna().unique())
        izbrana_ue = st.selectbox("Izberi upravno enoto", options=["Vse"] + ue_options)

        # Naloži podatke o prometnih obremenitvah (samo 1x, če je možno)
        pldp = pd.read_excel('podatki/pldp2023noo.xlsx')

        # Pripravi podatke o nesrečah (samo za leto 2023)
        nesrece_2023 = data[data["Leto"] == 2023].copy()
        if izbrana_ue != "Vse":
            nesrece_2023 = nesrece_2023[nesrece_2023['UpravnaEnotaStoritve'] == izbrana_ue]

        # Poveži tekstovno ime
        nesrece_2023['OpisOdseka'] = nesrece_2023['TekstCesteNaselja'].str.strip()
        pldp['Prometni odsek'] = pldp['Prometni odsek'].str.strip()
        pldp['AADT'] = pd.to_numeric(pldp['Vsa vozila (PLDP)'], errors='coerce')

        merged = nesrece_2023.merge(pldp, left_on='OpisOdseka', right_on='Prometni odsek', how='left')

        nesrece_na_odsek = (
            merged.groupby('OpisOdseka')
            .agg({'ZaporednaStevilkaPN': 'count', 'AADT': 'first'})
            .rename(columns={'ZaporednaStevilkaPN': 'SteviloNesrec'})
            .reset_index()
        )

        # Izračunaj standardizirano nevarnost
        nesrece_na_odsek['NesreceNaMilijonVozil'] = (
            nesrece_na_odsek['SteviloNesrec'] / (nesrece_na_odsek['AADT'] * 365) * 1_000_000
        )
        # Filtriraj na dovolj prometne/nevarne odseke
        nesrece_na_odsek = nesrece_na_odsek[nesrece_na_odsek['SteviloNesrec'] >= 20]
        # Top 10 po nevarnosti
        top10 = nesrece_na_odsek.sort_values('NesreceNaMilijonVozil', ascending=False).head(10)

        # Barvni, lep graf z legendami, črto, gridom in večjimi oznakami
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(top10['OpisOdseka'], top10['NesreceNaMilijonVozil'], color="#e15759")
        ax.set_title("Top 10 najbolj nevarnih cestnih odsekov glede na prometno obremenitev (2023)", fontsize=15, fontweight="bold")
        ax.set_xlabel("Nesreče na milijon vozil v letu 2023", fontsize=13)
        ax.set_ylabel("Cestni odsek", fontsize=13)
        ax.invert_yaxis()
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        # Dodaj vrednosti
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, f"{width:.1f}", va='center', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)

        # Opcijsko: Prikaži še tabelo pod grafom (podatke top10)
        st.markdown("#### Podatki za top 10 najbolj nevarnih odsekov:")
        st.dataframe(top10[['OpisOdseka', 'SteviloNesrec', 'AADT', 'NesreceNaMilijonVozil']].rename(
            columns={'OpisOdseka': 'Odsek', 'SteviloNesrec': 'Št. nesreč', 'AADT': 'Povpr. dnevni promet', 'NesreceNaMilijonVozil': 'Nesreč na milijon vozil'}), use_container_width=True)


    elif page == "⚠️ Vzroki nesreč":
        st.title("⚠️ Najpogostejši vzroki prometnih nesreč")

        tipi = sorted(data['TipNesrece'].dropna().unique())
        izbrani_tip = st.selectbox("Filtriraj po tipu nesreče", options=["Vse"] + tipi)
        filtered_vzroki = data if izbrani_tip == "Vse" else data[data['TipNesrece'] == izbrani_tip]

        vzroki_counts = filtered_vzroki['VzrokNesrece'].value_counts().head(10)
        fig2, ax2 = plt.subplots()
        vzroki_counts.plot(kind='barh', ax=ax2, color='steelblue')
        ax2.set_title("10 najpogostejših vzrokov nesreč")
        ax2.set_xlabel("Število nesreč")
        ax2.invert_yaxis()
        st.pyplot(fig2)

    elif page == "👶 Mladi povzročitelji":
        st.title("👶 Analiza mladih povzročiteljev (18–24 let)")

        spoli = sorted(data['Spol'].dropna().unique())
        izbrani_spol = st.radio("Izberi spol", options=["Vsi"] + spoli, horizontal=True)

        povzrocitelji = data[data['Povzrocitelj'] == 'POVZROČITELJ'].copy()
        if izbrani_spol != "Vsi":
            povzrocitelji = povzrocitelji[povzrocitelji['Spol'] == izbrani_spol]

        bins = [18, 24, 34, 44, 54, 64, 74, 100]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']
        povzrocitelji['StarostnaSkupina'] = pd.cut(povzrocitelji['Starost'], bins=bins, labels=labels, right=False)
        nesrece_po_starosti = povzrocitelji['StarostnaSkupina'].value_counts().sort_index()

        fig3, ax3 = plt.subplots()
        nesrece_po_starosti.plot(kind='bar', color='skyblue', ax=ax3)
        ax3.set_title('Število nesreč po starostnih skupinah povzročiteljev')
        ax3.set_xlabel('Starostna skupina')
        ax3.set_ylabel('Število nesreč')
        st.pyplot(fig3)

        mladi = povzrocitelji[povzrocitelji['StarostnaSkupina'] == '18-24']
        vzroki_mladi = mladi['VzrokNesrece'].value_counts().head(10)

        fig4, ax4 = plt.subplots()
        vzroki_mladi.plot(kind='bar', color='lightcoral', ax=ax4)
        ax4.set_title('10 najpogostejših vzrokov nesreč pri mladih (18–24)')
        ax4.set_xlabel('Vzrok nesreče')
        ax4.set_ylabel('Število nesreč')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig4)

        st.markdown(f"**Povprečna starost mladih povzročiteljev:** {mladi['Starost'].mean():.1f} let")
        st.markdown(f"**Delež med vsemi povzročitelji:** {len(mladi)/len(povzrocitelji)*100:.1f}%")
        

    elif page == "🍷 Alkohol":
        st.title("🍷 Analize povezanosti alkohola in povzročiteljev")
        izbor = st.radio(
            "Izberi prikaz:",
            (
                "Delež povzročiteljev po vrednosti alkotesta",
                "Delež hudo poškodovanih glede na alkoholiziranost povzročitelja"
            ),
            horizontal=True
        )

        def parse_alko(val):
            try:
                return float(str(val).replace(",", ".").replace(" ", ""))
            except:
                return 0.0

        df = data.copy()  # če rabiš večkrat
        df['VrednostAlkotesta_float'] = df['VrednostAlkotesta'].apply(parse_alko)

        if izbor == "Delež povzročiteljev po vrednosti alkotesta":
            povzrocitelji = df[df['Povzrocitelj'] == 'POVZROČITELJ'].copy()

            negativni = (povzrocitelji['VrednostAlkotesta_float'] == 0).sum()
            pozitivni_pod_mejo = ((povzrocitelji['VrednostAlkotesta_float'] > 0) & (povzrocitelji['VrednostAlkotesta_float'] <= 0.5)).sum()
            nad_mejo = (povzrocitelji['VrednostAlkotesta_float'] > 0.5).sum()

            labels = ['Negativni (≤ 0)', 'Pozitivni (0–0.5 g/kg)', 'Nad mejo (> 0.5 g/kg)']
            values = [negativni, pozitivni_pod_mejo, nad_mejo]
            total = sum(values)
            percentages = [v / total * 100 for v in values]

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(labels, percentages, color=['#4e79a7', '#f28e2b', '#e15759'])
            ax.set_title('Delež povzročiteljev po vrednosti alkotesta (%)', fontsize=15, fontweight='bold')
            ax.set_ylabel('Delež (%)', fontsize=13)
            ax.set_xlabel('Skupina', fontsize=13)
            ax.set_ylim(0, 100)
            ax.bar_label(bars, fmt='%.1f %%', fontsize=13, fontweight='bold')
            ax.tick_params(axis='both', labelsize=12)
            plt.tight_layout()
            st.pyplot(fig)

        elif izbor == "Delež hudo poškodovanih glede na alkoholiziranost povzročitelja":
            # 1. ID-ji nesreč, kjer je povzročitelj imel alkohol > 0
            nesrece_pijanec = df[(df['Povzrocitelj'] == 'POVZROČITELJ') & (df['VrednostAlkotesta_float'] > 0)]['ZaporednaStevilkaPN'].unique()

            # 2. Udeleženci s hudo poškodbo v teh nesrečah
            hudo_v_pijani = df[(df['ZaporednaStevilkaPN'].isin(nesrece_pijanec)) & (df['PoskodbaUdelezenca'] == 'HUDA TELESNA POŠKODBA')]

            # 3. Vsi udeleženci s hudo poškodbo (ne glede na alkohol)
            vsi_hudo = df[df['PoskodbaUdelezenca'] == 'HUDA TELESNA POŠKODBA']

            # 4. Hudo poškodovani v nesrečah brez alkoholiziranega povzročitelja
            hudo_v_trezni = len(vsi_hudo) - len(hudo_v_pijani)

            labels = ['Povzročil alkoholiziran voznik', 'Povzročil trezen voznik']
            values = [len(hudo_v_pijani), hudo_v_trezni]
            percentages = [v / len(vsi_hudo) * 100 for v in values]

            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(7, 5))
            bars = ax.bar(labels, percentages, color=['#e15759', '#4e79a7'])
            ax.set_ylabel('Delež (%)', fontsize=13)
            ax.set_title('Delež hudo poškodovanih udeležencev\n glede na alkoholiziranost povzročitelja', fontsize=15, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.bar_label(bars, fmt='%.1f %%', fontsize=13, fontweight='bold')
            ax.tick_params(axis='both', labelsize=12)
            plt.tight_layout()
            st.pyplot(fig)


    elif page == "🛡️Varnostni pas":
        st.title("🛡️ Analize uporabe varnostnega pasu")
        izbor = st.radio(
            "Izberi prikaz:",
            (
                "Primerjava smrtnosti glede na uporabo pasu",
                "Izid prometne nesreče glede na uporabo pasu"
            ),
            horizontal=True
        )

        df_pas = data[data['UporabaVarnostnegaPasu'].isin(['DA', 'NE'])].copy()

        # PIVOT tabela za oba grafa
        pivot = pd.pivot_table(
            df_pas,
            index='PoskodbaUdelezenca',
            columns='UporabaVarnostnegaPasu',
            aggfunc='size',
            fill_value=0
        )

        if izbor == "Primerjava smrtnosti glede na uporabo pasu":
            # SMRTNOST: SMRT / skupaj DA oz. NE
            umrli_z_pasu = pivot.loc['SMRT', 'DA'] if 'SMRT' in pivot.index else 0
            umrli_brez_pasu = pivot.loc['SMRT', 'NE'] if 'SMRT' in pivot.index else 0

            skupaj_z_pasu = pivot['DA'].sum()
            skupaj_brez_pasu = pivot['NE'].sum()

            smrtnost_z_pasu = umrli_z_pasu / skupaj_z_pasu * 100 if skupaj_z_pasu > 0 else 0
            smrtnost_brez_pasu = umrli_brez_pasu / skupaj_brez_pasu * 100 if skupaj_brez_pasu > 0 else 0

            labels = ['Z varnostnim pasom', 'Brez varnostnega pasu']
            values = [smrtnost_z_pasu, smrtnost_brez_pasu]

            fig, ax = plt.subplots(figsize=(7, 5))
            bars = ax.bar(labels, values, color=['#4e79a7', '#e15759'])
            ax.set_ylabel('Smrtnost (%)')
            ax.set_title('Primerjava smrtnosti glede na uporabo varnostnega pasu', fontsize=14)
            ax.set_ylim(0, max(values) * 1.4)
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.2f}%', 
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)

            st.markdown(f"**Smrtnost med udeleženci Z varnostnim pasom:** {smrtnost_z_pasu:.3f}%  \n"
                        f"**Smrtnost med udeleženci BREZ varnostnega pasu:** {smrtnost_brez_pasu:.3f}%")

        elif izbor == "Izid prometne nesreče glede na uporabo pasu":
            kategorije = ['SMRT', 'HUDA TELESNA POŠKODBA', 'LAŽJA TELESNA POŠKODBA', 'BREZ POŠKODBE']
            pivot2 = pivot.reindex(kategorije)

            skupaj_z_pasu = pivot2['DA'].sum()
            skupaj_brez_pasu = pivot2['NE'].sum()

            delezi = pd.DataFrame({
                'Z varnostnim pasom': (pivot2['DA'] / skupaj_z_pasu * 100).round(2),
                'Brez varnostnega pasu': (pivot2['NE'] / skupaj_brez_pasu * 100).round(2)
            }, index=kategorije)

            fig2, ax2 = plt.subplots(figsize=(9, 6))
            delezi.plot(kind='bar', ax=ax2, color=['#4e79a7', '#e15759'])
            ax2.set_ylabel('Delež (%)')
            ax2.set_xlabel('Vrsta poškodbe')
            ax2.set_title('Izid prometne nesreče glede na uporabo varnostnega pasu')
            ax2.legend(title='Uporaba varnostnega pasu')
            ax2.set_ylim(0, 100)

            for p in ax2.patches:
                if not pd.isna(p.get_height()):
                    ax2.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width()/2., p.get_height()),
                                ha='center', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig2)


    
    elif page == "👩‍🦰👨‍🦱 Spol povzročiteljev":
        st.title("👩‍🦰👨‍🦱 Analiza po spolu")
        izbor = st.radio(
            "Izberi prikaz:",
            (
                "Vsi udeleženci in povzročitelji (stran ob strani)",
                "Top 10 vzrokov nesreč po spolu povzročitelja"
            ),
            horizontal=True
        )

        if izbor == "Vsi udeleženci in povzročitelji (stran ob strani)":
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))

            # Prvi graf: vsi udeleženci, število
            df1 = data.copy()
            spoli1 = df1['Spol'].dropna()
            spoli1 = spoli1[~spoli1.isin(['NEZNAN', 'NI PODATKA'])]
            counts1 = spoli1.value_counts()
            ax1 = axes[0]
            counts1.plot(kind='bar', color=['lightblue', 'salmon'], ax=ax1)
            ax1.set_title('Vsi udeleženci')
            ax1.set_xlabel('Spol')
            ax1.set_ylabel('Število')
            ax1.set_xticklabels(counts1.index, rotation=0)
            for p in ax1.patches:
                ax1.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=11)

            # Drugi graf: povzročitelji, %
            df2 = data[data['Povzrocitelj'] == 'POVZROČITELJ'].copy()
            spoli2 = df2['Spol'].dropna()
            spoli2 = spoli2[~spoli2.isin(['NEZNAN', 'NI PODATKA'])]
            counts2 = spoli2.value_counts()
            perc2 = counts2 / counts2.sum() * 100
            ax2 = axes[1]
            perc2.plot(kind='bar', color=['lightblue', 'salmon'], ax=ax2)
            ax2.set_title('Samo povzročitelji')
            ax2.set_xlabel('Spol')
            ax2.set_ylabel('Delež (%)')
            ax2.set_xticklabels(perc2.index, rotation=0)
            for p in ax2.patches:
                ax2.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='bottom', fontsize=11)

            plt.tight_layout()
            st.pyplot(fig)

        elif izbor == "Top 10 vzrokov nesreč po spolu povzročitelja":
            povzrocitelji = data[data['Povzrocitelj'] == 'POVZROČITELJ'].copy()
            povzrocitelji = povzrocitelji[povzrocitelji['Spol'].isin(['MOŠKI', 'ŽENSKI'])]

            top_vzroki = povzrocitelji['VzrokNesrece'].value_counts().head(10).index

            tabela = povzrocitelji[povzrocitelji['VzrokNesrece'].isin(top_vzroki)]
            pivot = tabela.pivot_table(
                index='VzrokNesrece',
                columns='Spol',
                values='ZaporednaStevilkaPN',
                aggfunc='count',
                fill_value=0
            )
            pivot = pivot.loc[top_vzroki]

            fig2, ax2 = plt.subplots(figsize=(14, 6))
            pivot.plot(kind='bar', color=['skyblue', 'lightcoral'], ax=ax2)
            ax2.set_title('Top 10 vzrokov prometnih nesreč in spol povzročitelja', fontsize=15, fontweight='bold')
            ax2.set_xlabel('Vzrok nesreče', fontsize=13)
            ax2.set_ylabel('Število povzročiteljev', fontsize=13)
            ax2.tick_params(axis='both', labelsize=12)
            ax2.legend(title='Spol', fontsize=12, title_fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)


    elif page == "🌱 Letni časi":
        st.title("🌱 Pogostost nesreč po letnih časih in vzrokih")
        top_n = st.slider("Število najpogostejših vzrokov", min_value=3, max_value=10, value=5, step=1)

        df = data.copy()
        df['Mesec'] = pd.to_datetime(df['DatumPN'], errors='coerce').dt.month
        sezona_map = {
            12: 'Zima', 1: 'Zima', 2: 'Zima',
            3: 'Pomlad', 4: 'Pomlad', 5: 'Pomlad',
            6: 'Poletje', 7: 'Poletje', 8: 'Poletje',
            9: 'Jesen', 10: 'Jesen', 11: 'Jesen'
        }
        df['LetniCas'] = df['Mesec'].map(sezona_map)

        top_vzroki = df['VzrokNesrece'].value_counts().head(top_n).index
        df_top = df[df['VzrokNesrece'].isin(top_vzroki)]

        tabela = df_top.groupby(['LetniCas', 'VzrokNesrece']).size().unstack().fillna(0)
        season_order = ['Pomlad', 'Poletje', 'Jesen', 'Zima']
        tabela = tabela.reindex(season_order)

        fig, ax = plt.subplots(figsize=(10, 6))
        tabela.plot(ax=ax, marker='o')
        ax.set_title(f'Pogostost {top_n} najpogostejših vzrokov nesreč po letnih časih', fontsize=15, fontweight='bold')
        ax.set_xlabel('Letni čas', fontsize=13)
        ax.set_ylabel('Število nesreč', fontsize=13)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(title='Vzrok nesreče', fontsize=11, title_fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)



else:
    st.warning("Podatki niso na voljo.")

#streamlit run streamlitapp.py

