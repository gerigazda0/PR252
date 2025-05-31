import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

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
    "🛡️Varnostni pas"
])

if data is not None:
    st.success("Podatki uspešno naloženi.")

    if page == "📍 Toplotna karta":
        st.title("📍 Toplotna karta prometnih nesreč")

        # Interaktivni filter po letih
        leto_min = int(data['Leto'].min())
        leto_max = int(data['Leto'].max())
        izbrano_leto = st.slider("Izberi obdobje nesreč", min_value=leto_min, max_value=leto_max, value=(leto_min, leto_max))

        sample = data[(data['Leto'] >= izbrano_leto[0]) & (data['Leto'] <= izbrano_leto[1])]
        sample = sample.dropna(subset=["GeoKoordinataX", "GeoKoordinataY"]).sample(n=3000, random_state=42)
        sample["GeoKoordinataX"] = sample["GeoKoordinataX"].astype(str).str.replace(",", ".").astype(float)
        sample["GeoKoordinataY"] = sample["GeoKoordinataY"].astype(str).str.replace(",", ".").astype(float)
        geometry = [Point(xy) for xy in zip(sample["GeoKoordinataY"], sample["GeoKoordinataX"])]
        gdf = gpd.GeoDataFrame(sample, geometry=geometry, crs="EPSG:3794").to_crs(epsg=4326)
        heat_data = [[point.y, point.x] for point in gdf.geometry]

        m = folium.Map(location=[46.1512, 14.9955], zoom_start=8, tiles="CartoDB positron")
        HeatMap(heat_data, radius=10, blur=15, min_opacity=0.3).add_to(m)
        st_folium(m, width=1000)

    elif page == "🚧 Nevarni odseki":
        st.title("🚧 Top 10 najbolj nevarnih cestnih odsekov")

        # Interaktivni filter po upravni enoti
        ue_options = sorted(data['UpravnaEnotaStoritve'].dropna().unique())
        izbrana_ue = st.selectbox("Izberi upravno enoto", options=["Vse"] + ue_options)

        filtered_data = data if izbrana_ue == "Vse" else data[data['UpravnaEnotaStoritve'] == izbrana_ue]

        top_odseki = (
            filtered_data.groupby(["TekstCesteNaselja", "TekstOdsekaUlice"])
            .size()
            .sort_values(ascending=False)
            .reset_index(name="SteviloNesrec")
            .head(10)
        )
        top_odseki["OpisOdseka"] = top_odseki["TekstCesteNaselja"] + " – " + top_odseki["TekstOdsekaUlice"]

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.barh(top_odseki["OpisOdseka"], top_odseki["SteviloNesrec"], color='orange')
        ax1.set_title("Top 10 najbolj nevarnih cestnih odsekov")
        ax1.set_xlabel("Število prometnih nesreč")
        ax1.invert_yaxis()
        st.pyplot(fig1)

    elif page == "⚠️ Vzroki nesreč":
        st.title("⚠️ Najpogostejši vzroki prometnih nesreč")

        # Filter po tipu nesreče
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

        # Filter po spolu
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

            import matplotlib.pyplot as plt
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
                "Delež uporabe pasu po vrsti poškodbe (%)",
                "Število poškodb glede na uporabo pasu"
            ),
            horizontal=True
        )

        import numpy as np

        df_pas = data[data['UporabaVarnostnegaPasu'].isin(['DA', 'NE'])].copy()
        
        # Pripravimo pivot za oba grafa (da ni podvajanja kode)
        pivot = pd.pivot_table(
            df_pas,
            index='PoskodbaUdelezenca',
            columns='UporabaVarnostnegaPasu',
            aggfunc='size',
            fill_value=0
        )

        # Po želji odstrani nespremembe/odstop:
        pivot = pivot.drop(['BREZ POŠKODBE', 'BREZ POŠKODBE-UZ', 'ODSTOP OD OGLEDA PN'], errors='ignore')

        if izbor == "Delež uporabe pasu po vrsti poškodbe (%)":
            percent_pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
            percent_pivot = percent_pivot.loc[percent_pivot['NE'].sort_values(ascending=False).index]
            fig, ax = plt.subplots(figsize=(10, 6))
            percent_pivot[['DA', 'NE']].plot(
                kind='bar',
                stacked=True,
                color={'DA': '#4e79a7', 'NE': '#e15759'},
                ax=ax
            )
            ax.set_title('Delež uporabe varnostnega pasu glede na vrsto poškodbe (%)', fontsize=15, fontweight='bold')
            ax.set_xlabel('Vrsta poškodbe', fontsize=13)
            ax.set_ylabel('Delež udeležencev (%)', fontsize=13)
            # Premakni legendo NAD graf
            ax.legend(
                title='Uporaba varnostnega pasu',
                loc='lower center',
                bbox_to_anchor=(0.5, 1.2),
                ncol=2,
                fontsize=12,
                title_fontsize=12
            )
            ax.tick_params(axis='both', labelsize=12)
            plt.tight_layout()
            st.pyplot(fig)


        elif izbor == "Število poškodb glede na uporabo pasu":
            # Sortiraj po skupnem številu (najprej manj pogoste poškodbe)
            pivot_sorted = pivot.loc[pivot.sum(axis=1).sort_values().index]
            y = np.arange(len(pivot_sorted.index))
            bar_width = 0.4
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(y - bar_width/2, pivot_sorted['DA'], height=bar_width, label='Z varnostnim pasom', color='#4e79a7')
            ax.barh(y + bar_width/2, pivot_sorted['NE'], height=bar_width, label='Brez varnostnega pasu', color='#e15759')
            ax.set_yticks(y)
            ax.set_yticklabels(pivot_sorted.index)
            ax.set_xlabel('Število udeležencev', fontsize=13)
            ax.set_ylabel('Vrsta poškodbe', fontsize=13)
            ax.set_title('Poškodbe udeležencev glede na uporabo varnostnega pasu', fontsize=15, fontweight='bold')
            ax.legend()
            ax.tick_params(axis='both', labelsize=12)
            plt.tight_layout()
            st.pyplot(fig)


else:
    st.warning("Podatki niso na voljo.")

#streamlit run streamlitapp.py

