import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Aggregatzustände – Schmelzen & Verdampfen", layout="centered")

st.title("🧪 Aggregatzustände: Schmelzen & Verdampfen")
st.markdown("Gib deine Messwerte ein, markiere Übergänge und analysiere den Temperaturverlauf.")

# 📋 Interaktive Tabelle zur Eingabe
st.subheader("Messwerte eingeben")

# Dynamisch erweiterbare Tabelle mit 10 leeren Zeilen
initial_data = pd.DataFrame({
    "Zeit (s)": [None]*10,
    "Temperatur (°C)": [None]*10,
    "Beobachtung": ["" for _ in range(10)]
})

edited_df = st.data_editor(
    initial_data,
    num_rows="dynamic",
    use_container_width=True,
    disabled=[],
    key="messwerte"
)

# 📌 Slider für markante Punkte
st.subheader("Markante Punkte setzen")
try:
    zeit_min = int(pd.to_numeric(edited_df["Zeit (s)"], errors="coerce").min(skipna=True))
    zeit_max = int(pd.to_numeric(edited_df["Zeit (s)"], errors="coerce").max(skipna=True))
except:
    zeit_min, zeit_max = 0, 300

schmelzbeginn = st.slider("Schmelzbeginn (s)", zeit_min, zeit_max, value=60, step=10)
schmelzende = st.slider("Schmelzende (s)", zeit_min, zeit_max, value=180, step=10)
verdampfungsbeginn = st.slider("Verdampfungsbeginn (s)", zeit_min, zeit_max, value=300, step=10)

# 📈 Diagramm anzeigen
if st.button("Diagramm anzeigen"):
    try:
        # Bereinigung und Typkonvertierung
        df_clean = edited_df.dropna(subset=["Zeit (s)", "Temperatur (°C)"])
        df_clean["Beobachtung"] = df_clean["Beobachtung"].fillna("")
        df_clean["Zeit (s)"] = pd.to_numeric(df_clean["Zeit (s)"], errors="coerce")
        df_clean["Temperatur (°C)"] = pd.to_numeric(df_clean["Temperatur (°C)"], errors="coerce")

        # Diagramm erstellen
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_clean["Zeit (s)"], df_clean["Temperatur (°C)"], label="Temperaturverlauf", color="blue")

        # Markante Punkte einzeichnen
        punkte = {
            "Schmelzbeginn": schmelzbeginn,
            "Schmelzende": schmelzende,
            "Verdampfungsbeginn": verdampfungsbeginn
        }

        for label, zeitpunkt in punkte.items():
            if zeitpunkt in df_clean["Zeit (s)"].values:
                temp = df_clean[df_clean["Zeit (s)"] == zeitpunkt]["Temperatur (°C)"].values[0]
                ax.plot(zeitpunkt, temp, "ro")
                ax.text(zeitpunkt, temp + 1, label, color="red")

        ax.set_xlabel("Zeit (s)")
        ax.set_ylabel("Temperatur (°C)")
        ax.set_title("Temperaturverlauf beim Erhitzen von Eis")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # 📥 Export als PNG
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        st.download_button("📥 Diagramm als PNG herunterladen", buffer.getvalue(), file_name="temperaturverlauf.png")

        # 📋 Beobachtungen anzeigen
        st.subheader("Beobachtungen")
        st.dataframe(df_clean.style.format(na_rep=""))

        # 🧠 Analysefeld
        st.subheader("Analyse des Diagramms")
        analyse_text = st.text_area("Was zeigt dir das Temperaturverlauf-Diagramm?", height=150)

        # 📥 Export als Textdatei
        if st.button("📥 Analyse & Daten als Textdatei herunterladen"):
            export_text = f"Analyse:\n{analyse_text}\n\nMesswerte:\n{df_clean.to_csv(index=False)}"
            st.download_button("Download starten", export_text.encode(), file_name="auswertung.txt")

    except Exception as e:
        st.error(f"Fehler beim Zeichnen des Diagramms: {e}")
