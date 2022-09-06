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
        if len(busqueda) == 0:
            accion = Accion(
                kilometraje= kilometraje,
                costo = costo,
                fecha = fecha,
                mantenimiento = [self.agregar_mantenimiento(nombre=nombre)],
            )
            session.add(accion)
            session.commit()
            return True
        else:
            #print('Accion con Kilometraje ' + str(kilometraje) + ' y mantenimiento llamado ' + nombre +' ya esta registrado')
            return False

    # Funciones relacionadas a Autos
    def dar_auto(self, placa):
        auto = session.query(Auto).filter(Auto.placa == placa).first()
        if auto != None:
            return auto.__dict__
        else:
            return None

    def dar_autos(self):
        lista = []
        autos = session.query(Auto).all()
        for auto in autos:
            lista.append(auto.__dict__)
        return lista

    def editar_auto(self, placa_og, marca_n, modelo_n, placa_n, color_n, cilindraje_n, combustible_n, kilometraje_n):
        busqueda = session.query(Auto).filter(Auto.placa == placa_og).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).filter(Auto.placa == placa_og).first()
            temp.marca = marca_n
            temp.modelo=modelo_n
            temp.placa=placa_n
            temp.color=color_n
            temp.cilindraje=cilindraje_n
            temp.combustible=combustible_n
            temp.kilometraje_compra = kilometraje_n
            session.commit()
            return True
        else:
            return False

    def vender_auto(self, placa, precio_venta, kilometraje_venta):
        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).filter(Auto.placa == placa).first()
            if temp.vendido == False:
                temp.vendido = True
                temp.precio_venta = precio_venta
                temp.kilometraje_venta = kilometraje_venta
                session.commit()
                return True
            else:
                return False
        else:
            return False
        
    # Funciones relacionadas a Mantenimientos
    def agregar_mantenimiento(self, nombre):
        return session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()

    def dar_mantenimientos(self):
        lista = []
        mantos = session.query(Mantenimiento).all()
        for manto in mantos:
            lista.append(manto.__dict__)
        return lista

    def dar_mantenimiento(self, nombre):
        manto = session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
        if manto != None:
            return manto.__dict__
        else:
            return None

    # Funciones relacionadas a Acciones
    def aniadir_accion(self, placa, descripcion, kilometraje, costo, fecha):
        auto = session.query(Auto).filter(Auto.placa == placa).one()
        if auto is None:
            return False

        busqueda = session.query(Accion).filter(Accion.auto==auto.id).all()
        if len(busqueda) > 0:
            return False

        accion = Accion(
                kilometraje=kilometraje,
                descripcion=descripcion,
                costo=costo,
                fecha=fecha,
                auto=auto.id
        )
        session.add(accion)
        session.commit()

        return True

        

