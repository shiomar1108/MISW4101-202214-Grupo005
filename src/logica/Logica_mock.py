from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion
from datetime import datetime
import operator

from src.modelo.conn import engine, Base, session


class Logica_mock:
    def __init__(self):
        Base.metadata.create_all(engine)

        # Este constructor contiene los datos falsos para probar la interfaz
        self.autos = [
            {
                "Marca": "Volkswagen",
                "Placa": "KBL000",
                "Modelo": "2010",
                "Kilometraje": 150000.0,
                "Color": "Rojo",
                "Cilindraje": "2000",
                "TipoCombustible": "Gasolina",
                "Vendido": False,
                "ValorVenta": 0,
                "KilometrajeVenta": 0,
            },
            {
                "Marca": "Renault",
                "Placa": "BSQ782",
                "Modelo": "2015",
                "Kilometraje": 182000.0,
                "Color": "Plateado",
                "Cilindraje": "1600",
                "TipoCombustible": "Gasolina",
                "Vendido": True,
                "ValorVenta": 18000000,
                "KilometrajeVenta": 195000,
            },
        ]
        self.mantenimientos = [
            {"Nombre": "Seguros", "Descripcion": "Compra de seguros para automóviles"},
            {"Nombre": "Impuestos", "Descripcion": "Impuestos que se deben pagar"},
            {"Nombre": "Gasolina", "Descripcion": "Abastecimiento de combustible"},
        ]
        self.acciones = [
            {
                "Mantenimiento": "Seguros",
                "Auto": "Volkswagen",
                "Kilometraje": 151000.0,
                "Valor": 120000.0,
                "Fecha": "2022-01-01",
            },
            {
                "Mantenimiento": "Impuestos",
                "Auto": "Volkswagen",
                "Kilometraje": 152000.0,
                "Valor": 600000.0,
                "Fecha": "2022-02-01",
            },
            {
                "Mantenimiento": "Gasolina",
                "Auto": "Volkswagen",
                "Kilometraje": 150600.0,
                "Valor": 120000.0,
                "Fecha": "2022-01-05",
            },
            {
                "Mantenimiento": "Gasolina",
                "Auto": "Volkswagen",
                "Kilometraje": 151200.0,
                "Valor": 120000.0,
                "Fecha": "2022-01-28",
            },
        ]
        self.gastos = [
            {
                "Marca": "Volkswagen",
                "Gastos": [
                    ("2019", 1200000),
                    ("2020", 1300000),
                    ("2021", 2000000),
                    ("2022", 2500000),
                    ("Total", 7000000),
                ],
                "ValorKilometro": 175,
            },
            {
                "Marca": "Renault",
                "Gastos": [
                    ("2020", 900000),
                    ("2021", 1100000),
                    ("2022", 1300000),
                    ("Total", 3300000),
                ],
                "ValorKilometro": 128,
            },
        ]

    def dar_autos(self):
        # return self.autos.copy()
        lista = []
        autos = session.query(Auto).order_by(Auto.placa).all()
        for auto in autos:
            lista.append(auto.__dict__)
        return lista

    def dar_auto(self, id_auto):
        # return self.autos[id_auto].copy()
        # return session.query(Auto).filter(Auto.id==id_auto).first()
        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        if auto != None:
            return auto.__dict__
        else:
            return None

    def crear_auto(
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

        if type(modelo) != int:
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

        busqueda = session.query(Auto).filter(Auto.marca == marca).all()
        if len(busqueda) != 0:
            return "Error: auto de la Marca " + marca + " ya esta registrado"

        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) == 0:
            auto = Auto(
                marca=marca,
                modelo=modelo,
                placa=placa,
                color=color,
                cilindraje=cilindraje,
                combustible=combustible,
                kilometraje_compra=kilometraje,
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
        self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible
    ):
        self.autos[id]["Marca"] = marca
        self.autos[id]["Placa"] = placa
        self.autos[id]["Modelo"] = modelo
        self.autos[id]["Kilometraje"] = float(kilometraje)
        self.autos[id]["Color"] = color
        self.autos[id]["Cilindraje"] = cilindraje
        self.autos[id]["TipoCombustible"] = tipo_combustible

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

    def eliminar_auto(self, id):
        # del self.autos[id]
        auto = session.query(Auto).filter(Auto.id == id).first()
        session.delete(auto)
        session.commit()

    def validar_crear_editar_auto(
        self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible
    ):
        validacion = False
        try:
            float(kilometraje)
            validacion = True
        except ValueError:
            return False

    def validar_vender_auto(self, id, kilometraje_venta, valor_venta):
        validacion = False
        try:
            float(kilometraje_venta)
            float(valor_venta)
            validacion = True
        except ValueError:
            validacion = False

        return validacion

    def dar_mantenimientos(self):
        # return self.mantenimientos.copy()
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

    def editar_mantenimiento(self, id, nombre, descripcion):
        self.mantenimientos[id]["Nombre"] = nombre
        self.mantenimientos[id]["Descripcion"] = descripcion

    def eliminar_mantenimiento(self, id):
        # del self.mantenimientos[id]
        mantenimiento = (
            session.query(Mantenimiento).filter(Mantenimiento.id == id).first()
        )
        session.delete(mantenimiento)
        session.commit()

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        validacion = False
        if nombre != None and descripcion != None:
            validacion = True
        return validacion

    def dar_acciones_auto(self, id_auto):
        # marca_auto = self.autos[id_auto]['Marca']
        # return list(filter(lambda x: x['Auto']==marca_auto, self.acciones))
        lista = []
        auto = session.query(Auto).filter(Auto.id == id_auto).first()
        if auto is None:
            return lista

        for accion in auto.acciones:
            lista.append(accion.__dict__)
        newlist = sorted(lista, key=operator.itemgetter("kilometraje"), reverse=True)
        return newlist

    def dar_accion(self, id_auto, id_accion):
        # return self.dar_acciones_auto(id_auto)[id_accion].copy()
        acciones = self.dar_acciones_auto(id_auto)
        for accion in acciones:
            if accion.get("id") == id_accion:
                return accion
        return None

    def crear_accion(self, mantenimiento, id_auto, valor, kilometraje, fecha):
        # n_accion = {}
        # n_accion['Mantenimiento'] = mantenimiento
        # n_accion['Auto'] = self.autos[id_auto]['Marca']
        # n_accion['Valor'] = valor
        # n_accion['Kilometraje'] = kilometraje
        # n_accion['Fecha'] = fecha
        # self.acciones.append(n_accion)
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
        self.acciones[id_accion]["Mantenimiento"] = mantenimiento
        self.acciones[id_accion]["Auto"] = self.autos[id_auto]["Marca"]
        self.acciones[id_accion]["Valor"] = valor
        self.acciones[id_accion]["Kilometraje"] = kilometraje
        self.acciones[id_accion]["Fecha"] = fecha

    def eliminar_accion(self, id_auto, id_accion):
        marca_auto = self.autos[id_auto]["Marca"]
        i = 0
        id = 0
        while i < len(self.acciones):
            if self.acciones[i]["Auto"] == marca_auto:
                if id == id_accion:
                    self.acciones.pop(i)
                    return True
                else:
                    id += 1
            i += 1

        return False

        del self.accion[id_accion]

    def validar_crear_editar_accion(
        self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha
    ):
        validacion = False
        try:
            int(kilometraje)
            float(valor)
            validacion = True
        except ValueError:
            validacion = False

        return validacion

    def dar_reporte_ganancias(self, id_auto):
        # n_auto = self.autos[id_auto]['Marca']

        # for gasto in self.gastos:
        #     if gasto['Marca'] == n_auto:
        #         return gasto['Gastos'], gasto['ValorKilometro']

        # return [('Total',0)], 0
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
