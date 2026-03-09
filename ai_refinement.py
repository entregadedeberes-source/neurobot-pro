from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import sqlite3
import numpy as np

class AIRefinement:
    def __init__(self, db_path='neurobot.db'):
        self.db_path = db_path
        self.model = RandomForestClassifier(n_estimators=100)

    def train_model(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM pronosticos WHERE resultado_real != 'PENDIENTE'", conn)
            if len(df) < 5: return "Necesitas al menos 5 resultados reales."
            
            X = df[['prob_estimada', 'cuota_jugada', 'ev_calculado']]
            y = df['resultado_real'].apply(lambda x: 1 if x == 'GANADA' else 0)
            self.model.fit(X, y)
            return "IA entrenada con éxito."
        except:
            return "Error al entrenar. Registra más partidos."

    def predict_reliability(self, prob, cuota, ev):
        try:
            pred = self.model.predict_proba([[prob, cuota, ev]])
            return round(pred[0][1], 2)
        except:
            return 0.50 # Neutral si no hay entrenamiento