from src.modelo.auto import Auto
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion import Accion

from src.modelo.conn import engine, Base, session



class Logica_mock():

    def __init__(self):
        Base.metadata.create_all(engine)

        #Este constructor contiene los datos falsos para probar la interfaz
        self.autos = [{'Marca':'Volkswagen', 'Placa':'KBL000', 'Modelo': '2010', 'Kilometraje': 150000.0, \
                        'Color':'Rojo', 'Cilindraje': '2000', 'TipoCombustible':'Gasolina', 'Vendido': False, \
                        'ValorVenta': 0, 'KilometrajeVenta':0 },
                    {'Marca':'Renault', 'Placa':'BSQ782', 'Modelo': '2015', 'Kilometraje': 182000.0, \
                        'Color':'Plateado', 'Cilindraje': '1600', 'TipoCombustible':'Gasolina', 'Vendido': True, \
                        'ValorVenta': 18000000, 'KilometrajeVenta':195000 }]
        self.mantenimientos = [{'Nombre':'Seguros', 'Descripcion': 'Compra de seguros para automóviles'}, \
                               {'Nombre':"Impuestos", 'Descripcion': 'Impuestos que se deben pagar'}, \
                               {'Nombre':"Gasolina", 'Descripcion': 'Abastecimiento de combustible'}]
        self.acciones = [{'Mantenimiento':'Seguros', 'Auto':'Volkswagen', 'Kilometraje':151000.0, 'Valor':120000.0, 'Fecha':'2022-01-01'},\
                        {'Mantenimiento':'Impuestos', 'Auto':'Volkswagen', 'Kilometraje':152000.0, 'Valor':600000.0, 'Fecha':'2022-02-01'},\
                        {'Mantenimiento':'Gasolina', 'Auto':'Volkswagen', 'Kilometraje':150600.0, 'Valor':120000.0, 'Fecha':'2022-01-05'},\
                        {'Mantenimiento':'Gasolina', 'Auto':'Volkswagen', 'Kilometraje':151200.0, 'Valor':120000.0, 'Fecha':'2022-01-28'}]
        self.gastos = [{'Marca':'Volkswagen', 'Gastos':[('2019',1200000),('2020',1300000), ('2021',2000000), ('2022',2500000), \
                        ('Total',7000000)], 'ValorKilometro': 175},\
                       {'Marca':'Renault', 'Gastos':[('2020',900000), ('2021',1100000), ('2022',1300000), \
                        ('Total',3300000)], 'ValorKilometro': 128},]

    def dar_autos(self):
        # return self.autos.copy()
        lista = []
        autos = session.query(Auto).all()
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
    
    def crear_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        # self.autos.append({'Marca':marca, 'Placa':placa, 'Modelo': modelo, 'Kilometraje': float(kilometraje), \
        #                    'Color':color, 'Cilindraje': cilindraje, 'TipoCombustible':tipo_combustible, 'Vendido': False})
        busqueda = session.query(Auto).filter(Auto.placa == placa).all()
        if len(busqueda) > 0:
            return False
      
        auto = Auto(
            marca=marca, 
            modelo=modelo, 
            placa=placa, 
            color=color, 
            cilindraje=cilindraje, 
            combustible=tipo_combustible,
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

        return auto




    def editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        self.autos[id]['Marca'] = marca
        self.autos[id]['Placa'] = placa
        self.autos[id]['Modelo'] = modelo
        self.autos[id]['Kilometraje'] = float(kilometraje)
        self.autos[id]['Color'] = color
        self.autos[id]['Cilindraje'] = cilindraje
        self.autos[id]['TipoCombustible'] = tipo_combustible

    def vender_auto(self, id, kilometraje_venta, valor_venta):
        self.autos[id]['ValorVenta'] = valor_venta
        self.autos[id]['KilometrajeVenta'] = kilometraje_venta
        self.autos[id]['Vendido'] = True

    def eliminar_auto(self, id):
        # del self.autos[id]
        auto = session.query(Auto).filter(Auto.id==id).first()
        session.delete(auto)
        session.commit()

        


        
    def validar_crear_editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        validacion = False
        try:
            float(kilometraje)
            validacion = True
        except ValueError:
            return False
        return validacion
        
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
        return self.mantenimientos.copy()

    def aniadir_mantenimiento(self, nombre, descripcion):
        self.mantenimientos.append({'Nombre': nombre, 'Descripcion': descripcion})
    
    def editar_mantenimiento(self, id, nombre, descripcion):
        self.mantenimientos[id]['Nombre'] = nombre
        self.mantenimientos[id]['Descripcion'] = descripcion
    
    def eliminar_mantenimiento(self, id):
        del self.mantenimientos[id]

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        validacion = False
        if nombre!=None and descripcion!=None:
            validacion = True
        return validacion
        
    def dar_acciones_auto(self, id_auto):
        marca_auto = self.autos[id_auto]['Marca']
        return list(filter(lambda x: x['Auto']==marca_auto, self.acciones))

    def dar_accion(self, id_auto, id_accion):
        return self.dar_acciones_auto(id_auto)[id_accion].copy()

    def crear_accion(self, mantenimiento, id_auto, valor, kilometraje, fecha):
        n_accion = {}
        n_accion['Mantenimiento'] = mantenimiento
        n_accion['Auto'] = self.autos[id_auto]['Marca']
        n_accion['Valor'] = valor
        n_accion['Kilometraje'] = kilometraje
        n_accion['Fecha'] = fecha
        self.acciones.append(n_accion)

    def editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        self.acciones[id_accion]['Mantenimiento'] = mantenimiento
        self.acciones[id_accion]['Auto'] = self.autos[id_auto]['Marca']
        self.acciones[id_accion]['Valor'] = valor
        self.acciones[id_accion]['Kilometraje'] = kilometraje
        self.acciones[id_accion]['Fecha'] = fecha

    def eliminar_accion(self, id_auto, id_accion):
        marca_auto =self.autos[id_auto]['Marca']
        i = 0
        id = 0
        while i < len(self.acciones):
            if self.acciones[i]['Auto'] == marca_auto:
                if id == id_accion:
                    self.acciones.pop(i)
                    return True
                else:
                    id+=1
            i+=1
        
        return False
                

        del self.accion[id_accion]
        
    def validar_crear_editar_accion(self, id_accion, mantenimiento, id_auto, valor, kilometraje, fecha):
        validacion = False
        try:
            float(kilometraje)
            float(valor)
            validacion = True
        except ValueError:
            validacion = False

        return validacion

    def dar_reporte_ganancias(self, id_auto):
        n_auto = self.autos[id_auto]['Marca']
        
        for gasto in self.gastos:
            if gasto['Marca'] == n_auto:
                return gasto['Gastos'], gasto['ValorKilometro']

        return [('Total',0)], 0