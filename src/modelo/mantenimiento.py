from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from .conn import Base


class Mantenimiento(Base):
    __tablename__ = 'mantenimiento'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    accion = Column(Integer, ForeignKey('accion.id'))