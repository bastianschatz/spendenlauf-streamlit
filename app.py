import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Globale Konstante für Speicherort auf Render (Persistent Disk)
DATA_PATH = "/data"
if not os.path.exists(DATA_PATH):
    st.error("Datenverzeichnis '/data' nicht gefunden. Ist die Persistent Disk korrekt eingerichtet?")
    st.stop()
    
# Authentifizierung
def load_users():
    with open(f"{DATA_PATH}/users.json", "r") as f:
        return json.load(f)

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Benutzername")
    password = st.sidebar.text_input("Passwort", type="password")
    if st.sidebar.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state["user"] = username
            st.success(f"Eingeloggt als {username}")
        else:
            st.error("Ungültige Zugangsdaten")

if "user" not in st.session_state:
    login()
    st.stop()

# Lade Schülerliste
csv_file = f"{DATA_PATH}/schuelerliste.csv"
df = pd.read_csv(csv_file)

st.title("🏃 Spendenlauf – Runden erfassen")
st.write(f"Eingeloggt als **{st.session_state['user']}**")

name = st.selectbox("Schüler auswählen", df["Name"].tolist())
runden = st.number_input("Anzahl gelaufener Runden", min_value=0, step=1)

if st.button("✅ Runden speichern"):
    df.loc[df["Name"] == name, "Rundenanzahl"] = runden
    df.to_csv(csv_file, index=False)
    st.success(f"Runden für {name} aktualisiert: {runden} Runden gespeichert.")

# Optional: Log speichern
log_dir = f"{DATA_PATH}/logs"
os.makedirs(log_dir, exist_ok=True)
with open(os.path.join(log_dir, "log.csv"), "a") as log_file:
    log_file.write(f"{datetime.now()},{st.session_state['user']},{name},{runden}\n")
