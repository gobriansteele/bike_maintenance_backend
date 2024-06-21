from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/bike_maintenance")

SessionLocal = sessionmaker(bind=engine)

