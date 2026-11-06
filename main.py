import datetime
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./chocolate_factory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class StockModel(Base):
  __tablename__ = "stocks"
  id = Column(Integer, primary_key=True, index=True)
  item = Column(String, unique=True, index=True)
  quantity = Column(Integer, default=0)


class LogModel(Base):
  __tablename__ = "logs"
  id = Column(Integer, primary_key=True, index=True)
  time = Column(String)
  action = Column(String)
  status = Column(String)


# Создаем таблицы сразу при запуске файла (вне lifespan/startup, чтобы не вешать сервер)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def serve_frontend():
  if os.path.exists("index.html"):
    return FileResponse("index.html")
  return {"detail": "index.html topilmadi"}


# Bazani yaratish va boshlang'ich ma'lumotlarni qo'shish
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
  for item_name, qty in [
      ("cocoa", 1000),
      ("sugar", 1000),
      ("chocolate", 0),
  ]:
    exists = db.query(StockModel).filter(StockModel.item == item_name).first()
    if not exists:
      db.add(StockModel(item=item_name, quantity=qty))
  db.commit()
except Exception as e:
  db.rollback()
finally:
  db.close()


@app.get("/api/stock")
def get_stock():
  db = SessionLocal()
  try:
    cocoa = db.query(StockModel).filter(StockModel.item == "cocoa").first()
    sugar = db.query(StockModel).filter(StockModel.item == "sugar").first()
    chocolate = (
        db.query(StockModel).filter(StockModel.item == "chocolate").first()
    )

    return {
        "cocoa": cocoa.quantity if cocoa else 1000,
        "sugar": sugar.quantity if sugar else 1000,
        "chocolate": chocolate.quantity if chocolate else 0,
    }
  finally:
    db.close()
  db = SessionLocal()
  try:
    cocoa = (
        db.query(StockModel).filter(StockModel.item == "cocoa").first()
    )
    sugar = (
        db.query(StockModel).filter(StockModel.item == "sugar").first()
    )
    chocolate = (
        db.query(StockModel).filter(StockModel.item == "chocolate").first()
    )

    # Если в базе пусто, автоматически заполним начальными данными
    if not cocoa or not sugar:
      if not cocoa:
        db.add(StockModel(item="cocoa", quantity=1000))
      if not sugar:
        db.add(StockModel(item="sugar", quantity=1000))
      if not chocolate:
        db.add(StockModel(item="chocolate", quantity=0))
      db.commit()
      return {"cocoa": 1000, "sugar": 1000, "chocolate": 0}

    return {
        "cocoa": cocoa.quantity,
        "sugar": sugar.quantity,
        "chocolate": chocolate.quantity if chocolate else 0,
    }
  finally:
    db.close()


@app.post("/api/produce")
def produce_chocolate():
  db = SessionLocal()
  now_str = datetime.datetime.now().strftime("%H:%M:%S")
  try:
    cocoa = (
        db.query(StockModel).filter(StockModel.item == "cocoa").first()
    )
    sugar = (
        db.query(StockModel).filter(StockModel.item == "sugar").first()
    )
    chocolate = (
        db.query(StockModel).filter(StockModel.item == "chocolate").first()
    )

    if not cocoa or not sugar or not chocolate:
      raise HTTPException(status_code=400, detail="Omborxona topilmadi")

    if cocoa.quantity < 50 or sugar.quantity < 20:
      db.add(
          LogModel(
              time=now_str,
              action="Rad etildi: Xom ashyo yetarli emas",
              status="FAILED",
          )
      )
      db.commit()
      raise HTTPException(status_code=400, detail="Xom ashyo yetarli emas!")

    cocoa.quantity -= 50
    sugar.quantity -= 20
    chocolate.quantity += 1

    db.add(
        LogModel(
            time=now_str,
            action="1 dona Qora shokolad ishlab chiqarildi",
            status="SUCCESS",
        )
    )
    db.commit()
    return {"message": "Muvaffaqiyatli ishlab chiqarildi!"}
  finally:
    db.close()


@app.get("/api/logs")
def get_logs():
  db = SessionLocal()
  try:
    logs = db.query(LogModel).order_by(LogModel.id.desc()).all()
    return [
        {"time": l.time, "action": l.action, "status": l.status} for l in logs
    ]
  finally:
    db.close()