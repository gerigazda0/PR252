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
    "👶 Mladi povzročitelji"
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
else:
    st.warning("Podatki niso na voljo.")
