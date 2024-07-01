from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, ForeignKey, Integer, String, DateTime, FetchedValue
from sqlalchemy.orm import relationship

Base = declarative_base()

class Bike(Base):
    __tablename__ = "bike"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    nickname = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="bikes")
    purchase_date = Column(DateTime(timezone=True))
    type = Column(String)
    notes = Column(String)
    year = Column(String)
    maintenance_records = relationship("MaintenanceRecord", back_populates="bike")
    created_on = Column(DateTime(timezone=True), server_default=FetchedValue())
    modified_on = Column(DateTime(timezone=True), server_default=FetchedValue())

    __mapper_args__ = {"eager_defaults": True}



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    created_on = Column(DateTime(timezone=True), server_default=FetchedValue())
    modified_on = Column(DateTime(timezone=True), server_default=FetchedValue())
    bikes = relationship("Bike", back_populates="owner")
    password = Column(String)


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_record"

    id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(Integer, ForeignKey("bike.id"))
    bike = relationship("Bike", back_populates="maintenance_records")
    description = Column(String)
    date = Column(String)
    notes = Column(String)
    created_on = Column(String)
    modified_on = Column(String)