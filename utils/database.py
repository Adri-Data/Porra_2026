import streamlit as st
import pandas as pd

class GameDB:
    def __init__(self):
        try:
            self.conn = st.connection("gsheets", type="gsheets")
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")
            self.conn = None

    def get_players(self):
        """Obtiene la lista de jugadores desde la pestaña 'Players'"""
        if self.conn is None: return []
        try:
            df = self.conn.read(worksheet="Players")
            return df['Nombre'].tolist() if not df.empty else []
        except:
            return []

    def save_player(self, name):
        """Guarda un nuevo jugador"""
        if self.conn is None: return
        df = self.conn.read(worksheet="Players")
        if name not in df['Nombre'].tolist():
            new_row = pd.DataFrame([{"Nombre": name}])
            df = pd.concat([df, new_row], ignore_index=True)
            self.conn.update(worksheet="Players", data=df)

    def save_prediction(self, data):
        """Guarda una predicción completa en la pestaña 'Predictions'"""
        if self.conn is None: return
        try:
            df = self.conn.read(worksheet="Predictions")
        except:
            df = pd.DataFrame()
        
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)
        self.conn.update(worksheet="Predictions", data=df)

    def get_all_predictions(self):
        """Obtiene todas las predicciones para el admin"""
        if self.conn is None: return pd.DataFrame()
        try:
            return self.conn.read(worksheet="Predictions")
        except:
            return pd.DataFrame()

