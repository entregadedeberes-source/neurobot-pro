import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path='neurobot.db'):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pronosticos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    liga TEXT, local TEXT, visitante TEXT,
                    prob_estimada REAL, cuota_jugada REAL, ev_calculado REAL,
                    mercado TEXT, resultado_real TEXT DEFAULT 'PENDIENTE',
                    ganancia_neta REAL DEFAULT 0
                )
            """)

    def save_prediction(self, data):
        query = "INSERT INTO pronosticos (liga, local, visitante, prob_estimada, cuota_jugada, ev_calculado, mercado) VALUES (?,?,?,?,?,?,?)"
        with self._connect() as conn:
            conn.execute(query, (data['liga'], data['local'], data['visitante'], data['prob'], data['cuota'], data['ev'], data['mercado']))

    def update_result(self, p_id, status):
        with self._connect() as conn:
            p = conn.execute("SELECT cuota_jugada FROM pronosticos WHERE id = ?", (p_id,)).fetchone()
            ganancia = (p['cuota_jugada'] - 1) if status == 'GANADA' else -1
            conn.execute("UPDATE pronosticos SET resultado_real = ?, ganancia_neta = ? WHERE id = ?", (status, ganancia, p_id))