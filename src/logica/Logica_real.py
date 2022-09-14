from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion
from datetime import datetime

from src.modelo.conn import engine, Base, session


class Logica_real():
    def __init__(self):
        Base.metadata.create_all(engine)

    def crear_auto(self, marca, modelo, placa, color, cilindraje, combustible, kilometraje):
        required_fields = ['marca', 'modelo', 'placa', 'color', 'cilindraje', 'combustible', 'kilometraje']
        for field in required_fields:
            if field not in locals():
                return False

        int_fields = ['kilometraje', 'modelo']
        for field in int_fields:
            if not isinstance(locals()[field], int):
                return False

        str_fields = ['marca', 'placa', 'color', 'combustible']
        for field in str_fields:
            if not isinstance(locals()[field], str):
                return False

        if not isinstance(cilindraje, (int, float)):
            return False

        if(len(placa) != 6 or modelo > 9999):
            return False
        else:
            chunks = [placa[i:i+3] for i in range(0, len(placa), 3)]
            if(chunks[1].isalpha() or chunks[0].isnumeric() ):
                return False

        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            auto = Auto(
                marca=marca, 
                modelo=modelo, 
                placa=placa, 
                color=color, 
                cilindraje=cilindraje, 
                combustible=combustible,
                kilometraje_compra = kilometraje,
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
            return False

    def crear_mantenimiento(self, nombre, descripcion):
        required_fields = ['nombre', 'descripcion']
        for field in required_fields:
            if len(locals()[field]) == 0:
                return False

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
    def aniadir_accion(self, placa,  kilometraje, costo, fecha, nombre):

        required_fields = ['placa', 'kilometraje', 'costo', 'fecha', 'nombre']
        for field in required_fields:
            if field not in locals():
                return False

        str_fields = ['fecha', 'placa', 'nombre']
        for field in str_fields:
            if not isinstance(locals()[field], str):
                return False

        if not isinstance(costo, (float)):
            return False

        if not isinstance(kilometraje, (int)):
            return False

        busqueda = session.query(Auto).filter(Auto.placa==placa).all()
        if len(busqueda) != 1:
            return False

        manto_tempo = self.agregar_mantenimiento(nombre=nombre)
        if(manto_tempo == None):   
            return False

        try:
            datetime_object = datetime.strptime(fecha, '%d-%m-%Y')
        except ValueError as ve:
            return False

        acciones = self.dar_accion_auto(placa)
        for dato in acciones:
            if(dato.get('costo') == costo and dato.get('kilometraje') == kilometraje and dato.get('fecha') == fecha and dato.get('mantenimiento') == manto_tempo.id):
                return False
        
        auto = session.query(Auto).filter(Auto.placa==placa).first()
        accion = Accion(
                kilometraje=kilometraje,
                costo=costo,
                fecha=fecha,
                auto=auto.id,
                mantenimiento = manto_tempo.id
        )
        auto.acciones.append(accion)
        session.commit()

        return True

    def dar_accion_auto(self, placa):
        lista = []
        auto = session.query(Auto).filter(Auto.placa == placa).first()
        if auto is None:
            return False

        for accion in auto.acciones:
             lista.append(accion.__dict__)
        return lista
        

