from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import datetime

from database import engine, Base, get_db, SessionLocal
import models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Chocolate Factory - Mini-MRP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db():
    db = SessionLocal()
    try:
        if not db.query(models.Material).filter_by(name="Kakao").first():
            db.add(models.Material(name="Kakao", quantity=500))
        if not db.query(models.Material).filter_by(name="Shakar").first():
            db.add(models.Material(name="Shakar", quantity=200))
        if not db.query(models.Product).filter_by(name="Qora shokolad").first():
            db.add(models.Product(name="Qora shokolad", quantity=0))
        db.commit()
    finally:
        db.close()

init_db()

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html topilmadi!</h1>"

@app.get("/api/stock")
def get_stock(db: Session = Depends(get_db)):
    cocoa = db.query(models.Material).filter_by(name="Kakao").first()
    sugar = db.query(models.Material).filter_by(name="Shakar").first()
    chocolate = db.query(models.Product).filter_by(name="Qora shokolad").first()
    
    return {
        "cocoa": cocoa.quantity if cocoa else 0,
        "sugar": sugar.quantity if sugar else 0,
        "chocolate": chocolate.quantity if chocolate else 0
    }

@app.get("/api/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.ProductionLog).order_by(models.ProductionLog.id.desc()).all()
    return [{
        "time": log.timestamp.strftime("%H:%M:%S"),
        "action": log.action,
        "status": log.status
    } for log in logs]


@app.post("/api/produce")
def produce_chocolate(db: Session = Depends(get_db)):
    try:
        
        cocoa = db.query(models.Material).filter_by(name="Kakao").first()
        sugar = db.query(models.Material).filter_by(name="Shakar").first()
        chocolate = db.query(models.Product).filter_by(name="Qora shokolad").first()

        
        if cocoa.quantity < 50 or sugar.quantity < 20:
            
            fail_log = models.ProductionLog(
                action="Ishlab chiqarish rad etildi: Xom ashyo yetarli emas",
                status="FAILED"
            )
            db.add(fail_log)
            db.commit()
            raise HTTPException(status_code=400, detail="Xatolik: Kakao (50g) yoki Shakar (20g) yetarli emas!")

        
        cocoa.quantity -= 50
        sugar.quantity -= 20
        chocolate.quantity += 1

        
        success_log = models.ProductionLog(
            action="1 dona Qora shokolad ishlab chiqarildi (-50g Kakao, -20g Shakar)",
            status="SUCCESS"
        )
        db.add(success_log)

        
        db.commit()
        return {"message": "Muvaffaqiyatli! 1 dona Qora shokolad ishlab chiqarildi."}

    except HTTPException as e:
        raise e
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Tranzaksiya xatosi: {str(e)}")