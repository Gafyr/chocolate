from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import Stock

app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def init_stock():
    db = SessionLocal()
    
   
    cocoa = db.query(Stock).filter(Stock.item == "cocoa").first()
    if not cocoa:
        db.add(Stock(item="cocoa", quantity=1000))
    else:
        cocoa.quantity = max(cocoa.quantity, 1000)
        
    
    sugar = db.query(Stock).filter(Stock.item == "sugar").first()
    if not sugar:
        db.add(Stock(item="sugar", quantity=1000))
    else:
        sugar.quantity = max(sugar.quantity, 1000)
        
    db.commit()
    db.close()