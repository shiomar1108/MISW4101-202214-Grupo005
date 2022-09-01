from pickle import TRUE
from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion

from src.modelo.conn import engine, Base, session


class Logica_real():
    def __init__(self):
        Base.metadata.create_all(engine)

    def crear_auto(self, marca, modelo, placa, color, cilindraje, combustible, kilomentraje):
        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            auto = Auto(
                marca=marca, 
                modelo=modelo, 
                placa=placa, 
                color=color, 
                cilindraje=cilindraje, 
                combustible=combustible,
                kilometraje_compra = kilomentraje,
                precio_venta = 0,
                kilometraje_venta = 0,
                gasto_total = 0,
                gasto_anual = 0,
                gasto_kilometro = 0,
                vendido = False,
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

    def crear_accion(self, kilometraje, costo,fecha, nombre):
        busqueda = session.query(Accion).filter(Accion.kilometraje == kilometraje, Mantenimiento.nombre == nombre).all()
        print(len(busqueda))
        if len(busqueda) == 0:
            accion = Accion(
                kilometraje= kilometraje,
                costo = costo,
                fecha = fecha,
                mantenimiento = [self.dar_mantenimiento(nombre=nombre)],
            )
            session.add(accion)
            session.commit()
            return True
        else:
            print('Accion con Kilometraje ' + str(kilometraje) + ' y mantenimiento llamado ' + nombre +' ya esta registrado')
            return False

    # Funciones relacionadas a Autos
    def dar_auto(self, placa):
        return session.query(Auto).filter(Auto.placa == placa).first()

    def dar_autos(self):
        return session.query(Auto).all()

    def editar_auto(self, auto_id, marca, modelo, placa, color, cilindraje, combustible, kilometraje):
        busqueda = session.query(Auto).filter(Auto.id == auto_id).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).get(auto_id).__dict__
            temp.marca = marca
            temp.modelo=modelo
            temp.temp.placa=placa
            temp.color=color
            temp.cilindraje=cilindraje
            temp.combustible=combustible
            temp.kilometraje_compra = kilometraje
            session.commit()
            return True
        else:
            return False

    def vender_auto(self, placa, precio_venta, kilometraje_venta):
        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).filter(Auto.placa == placa).first()
            temp.vendido = True
            temp.precio_venta = precio_venta
            temp.kilometraje_venta = kilometraje_venta
            session.commit()
            return True
        else:
            return False
        

    # Funciones relacionadas a Mantenimientos
    def dar_mantenimientos(self):
        return session.query(Mantenimiento).all()

    def aniadir_mantenimiento(self, nombre, descripcion):
        return Logica_real.crear_mantenimiento(self,nombre,descripcion)

    def dar_mantenimiento(self, nombre):
        return session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()

    #Funciones relacionadas a Acciones
