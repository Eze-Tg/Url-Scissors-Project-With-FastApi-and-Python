from database import SessionLocal

db = SessionLocal()

from models import URL
db.query(URL).all()
[]