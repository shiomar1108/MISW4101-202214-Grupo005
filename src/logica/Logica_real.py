from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion
from datetime import datetime
import operator

from src.modelo.conn import engine, Base, session


class Logica_real:
    def __init__(self):
        Base.metadata.create_all(engine)

    def dar_autos(self):
        lista = []
        autos = session.query(Auto).order_by(Auto.placa).all()
        for auto in autos:
            lista.append(auto.__dict__)
        return lista

    def dar_auto(self, id_auto):
        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        if auto != None:
            return auto.__dict__
        else:
            return None

    def crear_auto(
        self, marca, placa, modelo, kilometraje, color, cilindraje, combustible
    ):
        response = self.validar_crear_editar_auto(
            marca=marca,
            placa=placa,
            modelo=modelo,
            kilometraje=kilometraje,
            color=color,
            cilindraje=cilindraje,
            combustible=combustible,
        )
        if not isinstance(response, dict):
            return response

        busqueda = session.query(Auto).filter(Auto.marca == marca).all()
        if len(busqueda) != 0:
            return "Error: auto de la Marca " + marca + " ya esta registrado"

        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            auto = Auto(
                marca=response["marca"],
                placa=response["placa"],
                modelo=response["modelo"],
                kilometraje_compra=response["kilometraje"],
                color=response["color"],
                cilindraje=response["cilindraje"],
                combustible=response["combustible"],
                precio_venta=0,
                kilometraje_venta=0,
                gasto_total=0,
                gasto_anual=0,
                gasto_kilometro=0,
                vendido=False,
            )
            session.add(auto)
            session.commit()
            return True
        else:
            return "Error: auto con Placa " + placa + " ya esta registrado"

    def editar_auto(
        self, id, marca, placa, modelo, kilometraje, color, cilindraje, combustible
    ):

        busqueda_inicial = session.query(Auto).filter(Auto.id == id).first()
        if busqueda_inicial.placa != placa:
            busqueda = session.query(Auto).filter(Auto.placa == placa).all()
            if len(busqueda) != 0:
                return "Error: auto con Placa " + placa + " ya esta registrado"

        if busqueda_inicial.marca != marca:
            busqueda = session.query(Auto).filter(Auto.marca == marca).all()
            if len(busqueda) != 0:
                return "Error: auto de la Marca " + marca + " ya esta registrado"

        response = self.validar_crear_editar_auto(
            marca=marca,
            placa=placa,
            modelo=modelo,
            kilometraje=kilometraje,
            color=color,
            cilindraje=cilindraje,
            combustible=combustible,
        )
        if not isinstance(response, dict):
            return response

        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            return "Error: auto con Placa " + placa + " no existe"

        session.query(Auto).filter(Auto.id == id).update(
            {
                "marca": response["marca"],
                "placa": response["placa"],
                "modelo": response["modelo"],
                "modelo": response["modelo"],
                "kilometraje_compra": response["kilometraje"],
                "color": response["color"],
                "cilindraje": response["cilindraje"],
                "combustible": response["combustible"],
            }
        )
        session.commit()
        return True

    def vender_auto(self, placa, valor, kilometraje):
        if placa is None or len(placa) == 0:
            return "Error: placa es requerida"

        try:
            kilometraje = int(kilometraje)
        except:
            return "Error: kilometraje debe ser un número"

        try:
            valor = float(valor)
        except:
            return "Error: valor debe ser un decimal"

        required_numeric_fields = ["valor", "kilometraje"]
        for field in required_numeric_fields:
            if locals()[field] < 0:
                return "Error: {} debe ser un numero mayor a 0".format(field)

        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 1:
            temp = session.query(Auto).filter(Auto.placa == placa).first()
            if temp.vendido == False:
                temp.vendido = True
                temp.precio_venta = valor
                temp.kilometraje_venta = kilometraje
                session.commit()
                return True
            else:
                return "Error: auto con placa " + placa + " ya fue vendido"
        else:
            return "Error: auto con Placa " + placa + " no existe"

    def validar_crear_editar_auto(
        self, marca, placa, modelo, kilometraje, color, cilindraje, combustible
    ):
        required_fields = [
            "marca",
            "modelo",
            "placa",
            "color",
            "cilindraje",
            "combustible",
            "kilometraje",
        ]
        for field in required_fields:
            if field not in locals() or locals()[field] == "":
                return "Error: {} es requerido".format(field)

        try:
            modelo = int(modelo)
        except:
            return "Error: modelo debe ser un número"

        try:
            kilometraje = int(kilometraje)
        except:
            return "Error: kilometraje debe ser un número"

        str_fields = ["marca", "placa", "color", "combustible"]
        for field in str_fields:
            try:
                int(locals()[field])
                return "Error: {} debe ser un String".format(field)
            except:
                if len(locals()[field]) > 50:
                    return "Error: {} debe tener menos de 50 caracteres".format(field)
                treeshold = 3
                if field == "marca":
                    treeshold = 2

                if len(locals()[field]) <= treeshold:
                    return f"Error: {field} debe tener más de {treeshold} caracteres"

        try:
            cilindraje = int(cilindraje)
        except:
            mensaje = "Error: cilindraje debe ser un número o un decimal"
            try:
                cilindraje = float(cilindraje)
            except:
                return mensaje

        if len(placa) != 6 or modelo > 9999:
            return (
                "Error: placa debe ser de 6 caracteres y modelo debe ser menor a 9999"
            )
        else:
            chunks = [placa[i : i + 3] for i in range(0, len(placa), 3)]
            if chunks[1].isalpha() or chunks[0].isnumeric():
                return "Error: placa debe tener 3 letras y 3 numeros (Ej: ABC123)"

        output = {
            "marca": marca,
            "modelo": modelo,
            "placa": placa,
            "color": color,
            "cilindraje": cilindraje,
            "combustible": combustible,
            "kilometraje": kilometraje,
        }
        return output

    def dar_mantenimientos(self):
        lista = []
        mantos = session.query(Mantenimiento).all()
        for manto in mantos:
            lista.append(manto.__dict__)
        return lista

    def aniadir_mantenimiento(self, nombre, descripcion):
        required_fields = ["nombre", "descripcion"]
        for field in required_fields:
            if len(locals()[field]) == 0:
                return f"Error: {field} es requerido"

            if field == "nombre":
                if len(locals()[field]) < 3:
                    return f"Error: {field} debe tener más de 3 caracteres"
                if len(locals()[field]) > 200:
                    return f"Error: {field} debe tener menos de 200 caracteres"

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
            return "Error: mantenimiento con Nombre " + nombre + " ya esta registrado"

    def dar_acciones_auto(self, id_auto):
        lista = []
        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        if auto is None:
            return lista

        for accion in auto.acciones:
            lista.append(accion.__dict__)
        newlist = sorted(lista, key=operator.itemgetter("kilometraje"), reverse=True)
        return newlist

    def dar_accion(self, id_auto, id_accion):
        acciones = self.dar_acciones_auto(id_auto)
        for accion in acciones:
            if accion.get("id") == id_accion:
                return accion
        return None

    def crear_accion(self, mantenimiento, id_auto, valor, kilometraje, fecha):
        required_fields = ["id_auto", "mantenimiento", "valor", "fecha", "kilometraje"]
        for field in required_fields:
            if field not in locals() or locals()[field] == "":
                return "Error: {} es requerido".format(field)

        str_fields = ["fecha", "mantenimiento"]
        for field in str_fields:
            try:
                int(locals()[field])
                return "Error: {} debe ser un String".format(field)
            except:
                if len(locals()[field]) > 50:
                    return "Error: {} debe tener menos de 50 caracteres".format(field)

        if not isinstance(valor, (float)) or valor <= 0:
            return "Error: valor debe ser un número con decimal mayor a 0"

        int_fields = ["id_auto", "kilometraje"]
        for field in int_fields:
            if not isinstance(locals()[field], int):
                return "Error: {} debe ser un Entero".format(field)

        busqueda = session.query(Auto).filter(Auto.id == id_auto).all()
        if len(busqueda) != 1:
            return "Error: El Auto debe existir"

        manto_tempo = self.agregar_mantenimiento(nombre=mantenimiento)
        if manto_tempo == None:
            return "Error: El Mantenimiento debe existir"

        try:
            datetime_object = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as ve:
            return "Error: La fecha debe ser en formato AAAA-MM-DD"

        acciones = self.dar_acciones_auto(id_auto)
        for dato in acciones:
            if (
                dato.get("valor") == valor
                and dato.get("kilometraje") == kilometraje
                and dato.get("fecha") == fecha
                and dato.get("mantenimiento") == manto_tempo.nombre
            ):
                return "Error: La Accion no debe estar repetidas"

        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        accion = Accion(
            kilometraje=kilometraje,
            valor=valor,
            fecha=fecha,
            auto=id_auto,
            mantenimiento=manto_tempo.nombre,
        )
        auto.acciones.append(accion)
        session.commit()
        return True

    def editar_accion(
        self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha
    ):
        required_fields = ["id_auto", "mantenimiento", "valor", "fecha", "kilometraje", "id_accion"]
        for field in required_fields:
            if field not in locals() or locals()[field] == "":
                return "Error: {} es requerido".format(field)

        str_fields = ["fecha", "mantenimiento"]
        for field in str_fields:
            try:
                int(locals()[field])
                return "Error: La {} debe ser un string".format(field)
            except:
                if len(locals()[field]) > 50:
                    return "Error: {} no puede tener mas de 50 caracteres".format(field)

        if not isinstance(valor, (float)) or valor <= 0:
            return "Error: valor debe ser un número con decimal mayor a 0"

        int_fields = ["id_auto", "kilometraje", "id_accion"]
        for field in int_fields:
            if not isinstance(locals()[field], int):
                return "Error: El {} debe ser entero".format(field)

        busqueda = session.query(Auto).filter(Auto.id == id_auto).all()
        if len(busqueda) != 1:
            return "Error: El auto debe existir"

        manto_tempo = self.agregar_mantenimiento(nombre=mantenimiento)
        if manto_tempo == None:
            return "Error: El Mantenimiento debe existir"

        try:
            datetime_object = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as ve:
            return "Error: La fecha debe ser en formato AAAA-MM-DD"

        acciones = self.dar_acciones_auto(id_auto)
        for dato in acciones:
            if (
                dato.get("valor") == valor
                and dato.get("kilometraje") == kilometraje
                and dato.get("fecha") == fecha
                and dato.get("mantenimiento") == manto_tempo.nombre
            ):
                return "Error: La accion modificada no puede estar duplicada"

        for dato in acciones:
            if ( dato.get("id") == id_accion ):
                session.query(Accion).filter(Accion.id == id_auto).update(
                    {
                        "kilometraje": kilometraje,
                        "valor": valor,
                        "fecha": fecha,
                        "mantenimiento": mantenimiento,                                             
                    }
                )
                session.commit()
                return True
        return "Error: La accion debe existir"

    def dar_reporte_ganancias(self, id_auto):
        acciones = self.dar_acciones_auto(id_auto)
        if len(acciones) == 0:
            return [("Total", 0)], 0

        ganancias = 0
        lista_year = []
        lista_valor = []
        lista_calculo = []
        for i in range(0, len(acciones), 1):
            accion = acciones[i]
            # calculo gasto total
            ganancias += accion.get("valor")
            # calculo gasto por año
            year = accion.get("fecha")[:4]
            try:
                index = lista_year.index(year)
                lista_valor[index] += accion.get("valor")
            except:
                lista_year.append(year)
                lista_valor.append(accion.get("valor"))
            # gasto x kilometro ultimo año
            if (
                datetime.today() - datetime.strptime(accion.get("fecha"), "%Y-%m-%d")
            ).days < 365:
                if (i + 1) == len(acciones):
                    calculo_Accion = (accion.get("valor")) / (
                        accion.get("kilometraje")
                        - self.dar_auto(id_auto=id_auto).get("kilometraje_compra")
                    )
                    lista_calculo.append(calculo_Accion)
                else:
                    calculo_Accion = (accion.get("valor")) / (
                        accion.get("kilometraje") - acciones[i + 1].get("kilometraje")
                    )
                    lista_calculo.append(calculo_Accion)

        lista = list(map(lambda x, y: (x, y), lista_year, lista_valor))
        lista_ordenada = sorted(lista, key=lambda tup: tup[0])
        lista_ordenada.append(("Total", round(ganancias, 2)))
        if len(lista_calculo) == 0:
            calculo_Accion = 0
        else:
            calculo_Accion = (sum(lista_calculo)) / (len(lista_calculo))

        return lista_ordenada, calculo_Accion

    def agregar_mantenimiento(self, nombre):
        return (
            session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
        )
