import pandas as pd
import numpy as np
from src.models.transaccion import Transaccion
from src.models.presupuesto import Presupuesto
from src.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from src.ml.prediccion import predecir_gasto

def verificar_presupuestos(usuario_id, db: Session = Depends(get_db)):
    presupuestos = db.query(Presupuesto).filter(
        Presupuesto.usuario_id == usuario_id
        ).all()
    
    alertas = []
    for p in presupuestos:
        transacciones = db.query(Transaccion).filter(
            Transaccion.usuario_id == usuario_id,
            Transaccion.categoria_id == p.categoria_id,
            Transaccion.tipo == "gasto"
        ).all()
        
        total_gasto = sum([t.monto for t in transacciones])
        
        resultado = predecir_gasto(usuario_id, db)
        prediccion_monto = resultado.get("prediccion") or 0
        
        if total_gasto + prediccion_monto > p.monto_limite:
            alertas.append({
                "categoria_id": str(p.categoria_id),
                "mensaje": f"Vas a pasarte de tu presupuesto — llevas ${total_gasto}"
                f" y se estima que gastaras ${prediccion_monto} mas"
            })
    return alertas