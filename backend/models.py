from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    routes = relationship("Route", back_populates="user")
    emissions = relationship("EmissionHistory", back_populates="user")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    mode = Column(String, nullable=False)

    distance_km = Column(Float, nullable=False)
    duration_min = Column(Float, nullable=False)
    duration_in_traffic_min = Column(Float, nullable=True)

    eco_score = Column(Float, nullable=True)
    co2_kg = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="routes")
    emissions = relationship("EmissionHistory", back_populates="route")


class EmissionHistory(Base):
    __tablename__ = "emission_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    mode = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    duration_min = Column(Float, nullable=False)
    traffic_delay_min = Column(Float, nullable=True)
    co2_kg = Column(Float, nullable=False)
    eco_score = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emissions")
    route = relationship("Route", back_populates="emissions")

