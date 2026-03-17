from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database 

app = FastAPI(title="ScooterFlow API")

@app.post("/zones/", response_model=schemas.ZoneCreate)
def create_zone(zone: schemas.ZoneCreate, db: Session = Depends(database.get_db)):
    db_zone = models.Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@app.post("/scooters/", response_model=schemas.ScooterResponse)
def create_scooter(scooter: schemas.ScooterCreate, db: Session = Depends(database.get_db)):
    db_scooter = models.Scooter(**scooter.dict())
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter

@app.post("/zonas/{zona_id}/mantenimiento")
def poner_en_mantenimiento(zona_id: int, db: Session = Depends(database.get_db)):
    scooters = db.query(models.Scooter).filter(
        models.Scooter.zona_id == zona_id,
        models.Scooter.bateria < 15
    ).all()
    
    for s in scooters:
        s.estado = models.EstadoPatinete.mantenimiento
    
    db.commit()
    return {"message": f"{len(scooters)} patinetes puestos en mantenimiento"}