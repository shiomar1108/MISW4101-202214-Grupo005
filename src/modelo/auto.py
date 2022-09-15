import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean
from sqlalchemy.orm import relationship

from .conn import Base


class Auto(Base):
    __tablename__ = "auto"

    id = Column(Integer, primary_key=True)
    marca = Column(String)
    placa = Column(String)
    modelo = Column(Integer)
    color = Column(String)
    cilindraje = Column(Float)
    combustible = Column(String)
    precio_venta = Column(Float)
    kilometraje_compra = Column(Integer)
    kilometraje_venta = Column(Integer)
    gasto_total = Column(Float)
    gasto_anual = Column(Float)
    gasto_kilometro = Column(Float)
    vendido = Column(Boolean)
    acciones = relationship("Accion", cascade="all, delete, delete-orphan")
