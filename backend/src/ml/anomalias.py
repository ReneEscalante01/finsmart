import pandas as pd
import numpy as np
from src.models.transaccion import Transaccion
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi import Depends

def detectar_anomalia(usuario_id, categoria_id, db: Session = Depends(get_db)):
    transacciones = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.categoria_id == categoria_id,
        Transaccion.tipo == "gasto"
        ).all()
    if len(transacciones) < 4:
        return {
            "mensaje": "No hay datos suficientes"
        }
    
    montos = [t.monto for t in transacciones]
    promedio = np.mean(montos)
    desviacion = np.std(montos)
    
    ultimo_gasto = montos[-1]
    z_score = (ultimo_gasto - promedio) / desviacion if desviacion > 0 else 0
    if z_score > 2:
        return {
            "anomalia": True,
            "mensaje": f"Gasto inusual detectado ${ultimo_gasto} cuando normalmente gastas ${round(promedio, 2)}"
        }

    return {
        "anomalia": False,
        "mensaje": "Gasto dentro de tu rango normal"
    }