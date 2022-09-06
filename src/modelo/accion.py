import string
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from .conn import Base


class Accion(Base):
    __tablename__ = 'accion'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    kilometraje = Column(Float)
    costo = Column(Float)
    fecha = Column(String)
    mantenimiento = relationship('Mantenimiento')
    auto = Column(Integer, ForeignKey('auto.id'))