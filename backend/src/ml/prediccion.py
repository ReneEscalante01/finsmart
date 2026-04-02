import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from src.models.transaccion import Transaccion
from src.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


def predecir_gasto(usuario_id, db: Session = Depends(get_db)):
    transacciones = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == "gasto"
    ).all()
    if len(transacciones) < 4:
        return{
            "prediccion": None, 
            "mensaje": "Aun recopilando datos" 
        }
        
    df = pd.DataFrame([{
        "fecha": t.fecha,
        "monto": t.monto
    } for t in transacciones])
    
    df["semana"] = pd.to_datetime(df["fecha"]).dt.isocalendar().week
    gasto_semanal = df.groupby("semana")["monto"].sum().reset_index()
    
    montos = gasto_semanal["monto"].values
    z_scores = np.abs((montos - np.mean(montos)) / np.std(montos))
    gasto_semanal = gasto_semanal[z_scores < 2]

    if len(gasto_semanal) < 4:
        return {
            "prediccion": None,
            "mensaje": "Aun recopilando datos"
        }   
    
    x = gasto_semanal[["semana"]].values
    y = gasto_semanal["monto"].values
    
    modelo = LinearRegression()
    modelo.fit(x, y)
    
    proxima_semana = int(gasto_semanal["semana"].max()) + 1
    prediccion = modelo.predict([[proxima_semana]])[0]
    
    return {
        "prediccion": round(float(prediccion), 2),
        "mensaje": f"Se estima que gastaras ${round(float(prediccion), 2)} la proxima semana"
    }