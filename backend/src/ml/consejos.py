import pandas as pd
from src.models.transaccion import Transaccion
from src.models.presupuesto import Presupuesto
from src.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def generar_consejo(usuario_id, db: Session = Depends(get_db)):
    presupuestos = db.query(Presupuesto).filter(Presupuesto.usuario_id == usuario_id).all()
    if not presupuestos:
        return {
            "mensaje": "No hay presupuestos"
        }
        
    datos = []
    for p in presupuestos:
        gasto_real = db.query(Transaccion).filter(
            Transaccion.usuario_id == usuario_id,
            Transaccion.categoria_id == p.categoria_id,
            Transaccion.tipo == "gasto"
        ).all()
        
        total_gasto = sum([t.monto for t in gasto_real])
        
        datos.append({
            "categoria_id": str(p.categoria_id),
            "limite": p.monto_limite,
            "gastado": total_gasto,
            "exceso": total_gasto - p.monto_limite
        })
    
    df = pd.DataFrame(datos)
    df = df.sort_values("exceso", ascending=False)
    
    peor = df.iloc[0]
    if peor["exceso"] <= 0:
        return {
            "consejo": "Vas muy bien, estas dentro de todos tus presupuestos"
        }
        
    ahorro_semanal = round(peor["exceso"] / 4, 2)
    ahorro_mensual = round(peor["exceso"], 2)
    
    return {
    "consejo": f"Llevas ${round(peor['gastado'], 2)} gastados en tu categoría con mayor exceso" 
    f" cuando tu límite es ${peor['limite']}. Si reduces ${ahorro_semanal} semanales ahorrarías ${ahorro_mensual} al mes"
}