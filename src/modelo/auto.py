import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean
from sqlalchemy.orm import relationship

from .conn import Base


class Combustible(enum.Enum):
    DIESEL = 1
    GASOLINA = 2
    HIBRIDO = 3
    ELECTRICO = 4


class Auto(Base):
    __tablename__ = 'auto'

    id = Column(Integer, primary_key=True)
    marca = Column(String)
    placa = Column(String)
    modelo = Column(String)
    kilometraje = Column(Float)
    color = Column(String)
    cilindraje = Column(Float)
    combustible = Column(Enum(Combustible))
    vendido = Column(Boolean)
    valor_venta = Column(Float)
    kilometraje_venta = Column(Float)
    mantenimientos = relationship('Mantenimiento', cascade='all, delete, delete-orphan')




# class Auto(Base):
#     __tablename__ = 'auto'

#     id = Column(Integer, primary_key=True)
#     marca = Column(String)
#     placa = Column(String)
#     modelo = Column(String)
#     kilometraje = Column(Float)
#     color = Column(String)
#     cilindraje = Column(Float)
#     combustible = Column(Enum(Combustible))
#     precio_venta = Column(Float)
#     kilometraje_compra = Column(Float)
#     kilometraje_venta = Column(Float)
#     gasto_total = Column(Float)
#     gasto_anual = Column(Float)
#     gasto_kilometro = Column(Float)
#     acciones = relationship('Accion', cascade='all, delete, delete-orphan')
#     usuario = Column(Integer, ForeignKey('usuario.id'))