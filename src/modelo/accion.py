import string
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from .conn import Base


class Accion(Base):
    __tablename__ = "accion"

    id = Column(Integer, primary_key=True)
    kilometraje = Column(Integer)
    valor = Column(Float)
    fecha = Column(String)
    mantenimiento = Column(Integer, ForeignKey("mantenimiento.nombre"))
    auto = Column(String, ForeignKey("auto.id"))
