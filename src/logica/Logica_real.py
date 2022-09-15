from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion
from datetime import datetime
import operator

from src.modelo.conn import engine, Base, session


class Logica_real:
    def __init__(self):
        Base.metadata.create_all(engine)

    def crear_auto(
        self, marca, modelo, placa, color, cilindraje, combustible, kilometraje
    ):
        required_fields = ['marca', 'modelo', 'placa', 'color', 'cilindraje', 'combustible', 'kilometraje']
        for field in required_fields:
            if field not in locals() or locals()[field] == '':
                return "Error: {} es requerido".format(field)

        int_fields = ['kilometraje', 'modelo']
        for field in int_fields:
            if not isinstance(locals()[field], int):
                return "Error: {} debe ser un numero".format(field)

        str_fields = ['marca', 'placa', 'color', 'combustible']
        for field in str_fields:
            if not isinstance(locals()[field], str):
                return "Error: {} debe ser un String".format(field)

        if not isinstance(cilindraje, (int, float)):
            return "Error: cilindraje debe ser un numero o un decimal"

        if(len(placa) != 6 or modelo > 9999):
            return "Error: placa debe ser de 6 caracteres y modelo debe ser menor a 9999"
        else:
            chunks = [placa[i:i+3] for i in range(0, len(placa), 3)]
            if(chunks[1].isalpha() or chunks[0].isnumeric() ):
                return "Error: placa debe tener 3 letras y 3 numeros (Ej: ABC123)"

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
            return 'Error: auto con Placa ' + placa + ' ya esta registrado'

    def crear_mantenimiento(self, nombre, descripcion):
        required_fields = ["nombre", "descripcion"]
        for field in required_fields:
            if len(locals()[field]) == 0:
                return False

        busqueda = (
            session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).all()
        )
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

    def editar_auto(
        self,
        placa_og,
        marca_n,
        modelo_n,
        placa_n,
        color_n,
        cilindraje_n,
        combustible_n,
        kilometraje_n,
    ):
        busqueda = session.query(Auto).filter(Auto.placa == placa_og).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).filter(Auto.placa == placa_og).first()
            temp.marca = marca_n
            temp.modelo = modelo_n
            temp.placa = placa_n
            temp.color = color_n
            temp.cilindraje = cilindraje_n
            temp.combustible = combustible_n
            temp.kilometraje_compra = kilometraje_n
            session.commit()
            return True
        else:
            return False

    def vender_auto(self, placa, precio_venta, kilometraje_venta):
        if placa is None or len(placa) == 0:
            return "Error: placa es requerida"

        required_numeric_fields = ['precio_venta', 'kilometraje_venta']
        for field in required_numeric_fields:
            if field not in locals() or locals()[field] == '':
                return "Error: {} es requerido".format(field)

            if not isinstance(locals()[field], (int, float)) or locals()[field] < 0:
                return "Error: {} debe ser un numero mayor a 0".format(field)

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
                return "Error: auto con placa " + placa + " ya fue vendido"
        else:
            return "Error: auto con Placa " + placa + " no existe"

    # Funciones relacionadas a Mantenimientos
    def agregar_mantenimiento(self, nombre):
        return (
            session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
        )

    def dar_mantenimientos(self):
        lista = []
        mantos = session.query(Mantenimiento).all()
        for manto in mantos:
            lista.append(manto.__dict__)
        return lista

    def dar_mantenimiento(self, nombre):
        manto = (
            session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
        )
        if manto != None:
            return manto.__dict__
        else:
            return None

    # Funciones relacionadas a Acciones
    def crear_accion(self, id_auto, kilometraje, valor, fecha, mantenimiento):

        required_fields = ["id_auto", "kilometraje", "valor", "fecha", "mantenimiento"]
        for field in required_fields:
            if field not in locals():
                return False

        str_fields = ["fecha", "mantenimiento"]
        for field in str_fields:
            if not isinstance(locals()[field], str):
                return False

        if not isinstance(valor, (float)):
            return False

        int_fields = ["id_auto", "kilometraje"]
        for field in int_fields:
            if not isinstance(locals()[field], int):
                return False

        busqueda = session.query(Auto).filter(Auto.id == id_auto).all()
        if len(busqueda) != 1:
            return False

        manto_tempo = self.agregar_mantenimiento(nombre=mantenimiento)
        if manto_tempo == None:
            return False

        try:
            datetime_object = datetime.strptime(fecha, "%d-%m-%Y")
        except ValueError as ve:
            return False

        acciones = self.dar_acciones_auto(id_auto)
        for dato in acciones:
            if (
                dato.get("costo") == valor
                and dato.get("kilometraje") == kilometraje
                and dato.get("fecha") == fecha
                and dato.get("mantenimiento") == manto_tempo.id
            ):
                return False

        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        accion = Accion(
            kilometraje=kilometraje,
            costo=valor,
            fecha=fecha,
            auto=id_auto,
            mantenimiento=manto_tempo.id,
        )
        auto.acciones.append(accion)
        session.commit()

        return True

    def dar_acciones_auto(self, id_auto):
        lista = []
        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        if auto is None:
            return None

        for accion in auto.acciones:
            lista.append(accion.__dict__)
        newlist = sorted(lista, key=operator.itemgetter('kilometraje'), reverse=True) 
        return newlist

    def dar_accion(self, id_auto, id_accion):
        acciones = self.dar_acciones_auto(id_auto)
        for accion in acciones:
            if(accion.get('id') == id_accion):
                return accion
        return None