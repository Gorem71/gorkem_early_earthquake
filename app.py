import streamlit as st
import requests
import pandas as pd
import time
from streamlit_folium import folium_static
import folium

st.title("Görkem Deprem Ağı - Kandilli Verileri (Tüm Türkiye)")

placeholder = st.empty()

while True:
    try:
        # Kandilli verileri al
        response = requests.get("https://kandilli.deno.dev/")
        quakes = response.json()
        
        data = []
        for quake in quakes:
            mag = float(quake.get('ml', 0))
            if mag >= 4.0:
                data.append({
                    "Zaman": f"{quake['date']} {quake['time']}",
                    "Yer": quake['location'],
                    "Büyüklük": mag,
                    "Derinlik": quake['depth'],
                    "Enlem": quake['latitude'],
                    "Boylam": quake['longitude']
                })
        
        df = pd.DataFrame(data)
        
        # Tablo göster
        with placeholder.container():
            st.subheader("Son 4.0+ Depremler")
            st.dataframe(df)
            
            # Harita oluştur
            m = folium.Map(location=[39, 35], zoom_start=6)
            for idx, row in df.iterrows():
                folium.Marker([row['Enlem'], row['Boylam']], popup=f"{row['Yer']} - {row['Büyüklük']}").add_to(m)
            folium_static(m)
        
    except:
        st.error("Veri hatası, tekrar deneniyor...")
    
    time.sleep(15)  # 15 sn yenile
