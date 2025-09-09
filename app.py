import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO

st.set_page_config(page_title="Aggregatzustände – Auswertung", layout="centered")

st.title("🧪 Aggregatzustände: Schmelzen & Verdampfen")
st.markdown("Gib deine Messwerte ein, markiere Übergänge und analysiere den Temperaturverlauf.")

# Eingabe der Messwerttabelle
st.subheader("📋 Messwerttabelle eingeben")
default_csv = """Zeit (s),Temperatur (°C),Beobachtung
0,0,Eis beginnt zu schmelzen
30,0,keine Veränderung
60,0,Wasser sichtbar
90,1,Temperatur steigt
120,2,
150,3,
180,4,Schmelze vollständig
210,10,Wasser kocht leicht
240,20,
270,40,
300,60,Dampf sichtbar"""

csv_input = st.text_area("Messwerte im CSV-Format (mit Kopfzeile)", value=default_csv, height=250)

# Versuch, die Tabelle zu laden
try:
    df = pd.read_csv(StringIO(csv_input))
    if not {"Zeit (s)", "Temperatur (°C)"}.issubset(df.columns):
        st.error("❌ Die Tabelle muss die Spalten 'Zeit (s)' und 'Temperatur (°C)' enthalten.")
        st.stop()
except Exception as e:
    st.error(f"❌ Fehler beim Einlesen der Tabelle: {e}")
    st.stop()

# Slider für markante Punkte
st.subheader("📌 Markante Punkte setzen")
zeit_min, zeit_max = int(df["Zeit (s)"].min()), int(df["Zeit (s)"].max())

schmelzbeginn = st.slider("Schmelzbeginn (s)", zeit_min, zeit_max, 60, step=10)
schmelzende = st.slider("Schmelzende (s)", zeit_min, zeit_max, 180, step=10)
verdampfungsbeginn = st.slider("Verdampfungsbeginn (s)", zeit_min, zeit_max, 300, step=10)

# Diagramm zeichnen
st.subheader("📈 Temperaturverlauf")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Zeit (s)"], df["Temperatur (°C)"], label="Temperaturverlauf", color="blue")

# Markante Punkte einzeichnen
punkte = {
    "Schmelzbeginn": schmelzbeginn,
    "Schmelzende": schmelzende,
    "Verdampfungsbeginn": verdampfungsbeginn
}

for label, zeitpunkt in punkte.items():
    if zeitpunkt in df["Zeit (s)"].values:
        temp = df[df["Zeit (s)"] == zeitpunkt]["Temperatur (°C)"].values[0]
        ax.plot(zeitpunkt, temp, "ro")
        ax.text(zeitpunkt, temp + 1, label, color="red")

ax.set_xlabel("Zeit (s)")
ax.set_ylabel("Temperatur (°C)")
ax.set_title("Temperaturverlauf beim Erhitzen von Eis")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Exportfunktion
buffer = BytesIO()
fig.savefig(buffer, format="png")
st.download_button("📥 Diagramm als PNG herunterladen", buffer.getvalue(), file_name="temperaturverlauf.png")

# Beobachtungen anzeigen
if "Beobachtung" in df.columns:
    st.subheader("📝 Beobachtungen")
    st.dataframe(df[["Zeit (s)", "Temperatur (°C)", "Beobachtung"]])

# Reflexion
st.subheader("🧠 Reflexion")
st.text_area("Was passiert beim Schmelzen und Verdampfen auf Teilchenebene?", height=150)
