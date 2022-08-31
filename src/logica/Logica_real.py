from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento

from src.modelo.conn import engine, Base, session


class Logica_real():
    def __init__(self):
        Base.metadata.create_all(engine)

    def crear_auto(self, marca, modelo, placa, color, cilindraje, combustible):
        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            auto = Auto(
                marca=marca, 
                modelo=modelo, 
                placa=placa, 
                color=color, 
                cilindraje=cilindraje, 
                combustible=combustible, 
                vendido=False,
            )
            session.add(auto)
            session.commit()
            return True
        else:
            #print('Auto con Placa ' + placa + ' ya esta registrado')
            return False

    def crear_mantenimiento(self, nombre, descripcion):
        busqueda = session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).all()
        if len(busqueda) == 0:
            mantenimiento = Mantenimiento(
                nombre=nombre, 
                descripcion=descripcion, 
            )
            session.add(mantenimiento)
            session.commit()
            return True
        else:
            #print('Mantenimiento con Nombre ' + nombre + ' ya esta registrado')
            return False


    def dar_auto(self, auto_id):
        return session.query(Auto).get(auto_id).__dict__

    def dar_autos(self):
        return session.query(Auto).all()

    def dar_mantenimientos(self):
        return session.query(Mantenimiento).all()

    def aniadir_mantenimiento(self, nombre, descripcion):
        return Logica_real.crear_mantenimiento(self,nombre,descripcion)
