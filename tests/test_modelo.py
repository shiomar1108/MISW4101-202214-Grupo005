import unittest
from unittest import result
from faker import Faker

from src.logica.Logica_real import Logica_real
from src.modelo.conn import Session
from src.modelo.auto import Auto
from src.modelo.accion import Accion
from src.modelo.mantenimiento import Mantenimiento


class ModeloTestEmptySetUp(unittest.TestCase):
    """clase que contiene los test con el setUp vacio"""

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.logica = Logica_real()
        self.session = Session()

    def test_caso01_dar_lista_autos_vacia(self):
        """Test que verifica que la lista de autos este vacia"""
        busqueda = self.logica.dar_autos()
        if len(busqueda) == 0:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)


class ModeloTestTDD(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker()

        self.auto1 = Auto(
            marca="volkswagen",
            modelo=2016,
            placa="XXX001",
            color="gris",
            cilindraje=2.5,
            combustible="GASOLINA",
            kilometraje_compra=0,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )
        self.auto2 = Auto(
            marca="Nissan",
            modelo=2016,
            placa="AAA001",
            color="Rojo",
            cilindraje=2.5,
            combustible="DIESEL",
            kilometraje_compra=25000,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )

        self.manto1 = Mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.manto2 = Mantenimiento(
            nombre="Cambio de Llantas", descripcion="Pago por nuevas llantas"
        )

        self.session.add(self.auto1)
        self.session.add(self.auto2)
        self.session.add(self.manto1)
        self.session.add(self.manto2)
        self.session.commit()

    def tearDown(self):
        self.session = Session()

        """Consulta todos los autos"""
        busqueda = self.session.query(Auto).all()

        """Borra todos los autos"""
        for auto in busqueda:
            self.session.delete(auto)

        """Consulta todos los Mantenimientos"""
        busqueda = self.session.query(Mantenimiento).all()

        """Borra todos los Mantenimientos"""
        for manto in busqueda:
            self.session.delete(manto)

        self.session.commit()
        self.session.close()

    def test_caso02_dar_autos_ordenados(self):
        """Test que verifica que la lista se regrese en orden cronologico"""
        busqueda = self.logica.dar_autos()
        if (
            busqueda[0].get("placa") == self.auto1.placa
            and busqueda[1].get("placa") == self.auto2.placa
        ):
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_caso03_1_agregar_auto_campo_placa_mas_de_6_caracteres(self):
        """test que verifica que el campo placa no tenga mas de 6 caracteres"""
        resultado = self.logica.crear_auto(
            marca="renault",
            modelo=1995,
            placa="XXX0011",
            color="negro",
            cilindraje=1.6,
            combustible="GASOLINA PREMIUM",
            kilometraje=1000,
        )
        self.assertFalse(resultado)

    def test_caso03_2_agregar_auto_campo_placa_letras(self):
        """test que verifica que el campo tenga 3 letras al inicio"""
        resultado = self.logica.crear_auto(
            marca="renault",
            modelo=1995,
            placa="000123",
            color="negro",
            cilindraje=1.6,
            combustible="GASOLINA PREMIUM",
            kilometraje=1000,
        )
        self.assertFalse(resultado)

    def test_caso03_3_agregar_auto_campo_placa_numeros(self):
        """test que verifica que el campo placa tenga tres numero al final"""
        resultado = self.logica.crear_auto(
            marca="renault",
            modelo=1995,
            placa="XXXYYY",
            color="negro",
            cilindraje=1.6,
            combustible="GASOLINA PREMIUM",
            kilometraje=1000,
        )
        self.assertFalse(resultado)

    def test_caso04_crear_auto_ya_creado(self):
        """test que verifica que los datos del auto no esten repetidos"""
        resultado = self.logica.crear_auto(
            marca="volkswagen",
            modelo=2016,
            placa="XXX001",
            color="gris",
            cilindraje=2.5,
            combustible="GASOLINA",
            kilometraje=0,
        )
        self.assertFalse(resultado)

    def test_caso05_crear_auto_placa_y_marca_duplicados(self):
        """test que verifica que el campo placa del auto no este duplicado"""
        resultado = self.logica.crear_auto(
            marca="volkswagen",
            modelo=2019,
            placa="AAA001",
            color="azul",
            cilindraje=1.4,
            combustible="HIBRIDO",
            kilometraje=26000,
        )
        self.assertFalse(resultado)

    def test_caso06_1_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="",
            modelo="",
            placa="",
            color="",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_caso06_2_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="",
            modelo="",
            placa="AAA005",
            color="",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_caso06_3_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="",
            modelo="",
            placa="AAA005",
            color="azul",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_caso06_4_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="volkswagen",
            modelo="",
            placa="AAA005",
            color="",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_caso07_crear_auto_campo_modelo_invalido(self):
        """test que verifica que el campo modelo del auto sean 4 digitos"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=19995,
            placa="ABC001",
            color="azul",
            cilindraje=2500,
            combustible="GASOLINA",
            kilometraje=14000,
        )
        self.assertFalse(resultado)

    def test_caso08_crear_auto_campo_kilometraje_invalido(self):
        """test que verifica que el campo kilometraje del auto sea un numero"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=1995,
            placa="ABC001",
            color="azul",
            cilindraje=2500,
            combustible="GASOLINA",
            kilometraje="14000",
        )
        self.assertFalse(resultado)

    def test_caso09_crear_auto_campo_color_invalido(self):
        """test que verifica que el campo color del auto sea un texto"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=1995,
            placa="ABC001",
            color=123,
            cilindraje=2500,
            combustible="GASOLINA",
            kilometraje=14000,
        )
        self.assertFalse(resultado)

    def test_caso10_crear_auto_campo_clindraje_invalido(self):
        """test que verifica que el campo cilindraje del auto sea un numero"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=1995,
            placa="ABC001",
            color="azul",
            cilindraje="2500",
            combustible="GASOLINA",
            kilometraje=14000,
        )
        self.assertFalse(resultado)

    def test_caso11_crear_auto_campo_combustible_invalido(self):
        """test que verifica que el campo combustible del auto sea un texto"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=1995,
            placa="ABC001",
            color="azul",
            cilindraje=2500,
            combustible=123,
            kilometraje=14000,
        )
        self.assertFalse(resultado)

    def test_caso12_1_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.crear_mantenimiento(nombre="", descripcion="")
        self.assertFalse(resultado)

    def test_caso12_2_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.crear_mantenimiento(
            nombre="Cambio de Llantas", descripcion=""
        )
        self.assertFalse(resultado)

    def test_caso12_3_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.crear_mantenimiento(
            nombre="", descripcion="Pago por nuevas llantas"
        )
        self.assertFalse(resultado)

    def test_caso13_crear_mantenimento_ya_existente(self):
        """test que verifica que no se pueda crear un mantenimiento ya existente"""
        resultado = self.logica.crear_mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.assertFalse(resultado)

    def test_caso14_mantenimiento_creado_debe_ser_visible(self):
        """test que verifica que despues de creado un mantenimiento se vea en la lista"""
        self.logica.crear_mantenimiento(
            nombre="Cambio de Llantas", descripcion="Pago por nuevas llantas"
        )
        lista = self.logica.dar_mantenimientos()
        if lista[len(lista) - 1].get("nombre") == "Cambio de Llantas":
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

class Test_Modelo_Venta(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker()

        self.auto1 = Auto(
            marca="volkswagen",
            modelo=2016,
            placa="XXX001",
            color="gris",
            cilindraje=2.5,
            combustible="GASOLINA",
            kilometraje_compra=0,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )
        self.auto2 = Auto(
            marca="Nissan",
            modelo=2016,
            placa="AAA001",
            color="Rojo",
            cilindraje=2.5,
            combustible="DIESEL",
            kilometraje_compra=25000,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )

        self.manto1 = Mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.manto2 = Mantenimiento(
            nombre="Cambio de Llantas", descripcion="Pago por nuevas llantas"
        )

        self.session.add(self.auto1)
        self.session.add(self.auto2)
        self.session.add(self.manto1)
        self.session.add(self.manto2)
        self.session.commit()

    def tearDown(self):
        self.session = Session()

        """Consulta todos los autos"""
        busqueda = self.session.query(Auto).all()

        """Borra todos los autos"""
        for auto in busqueda:
            self.session.delete(auto)

        """Consulta todos los Mantenimientos"""
        busqueda = self.session.query(Mantenimiento).all()

        """Borra todos los Mantenimientos"""
        for manto in busqueda:
            self.session.delete(manto)

        self.session.commit()
        self.session.close()

    def test_HU005_1_vender_automovil(self):
        """test que verifica que se pueda vender un automovil"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            precio_venta=self.data_factory.random_int(1000000, 1000000000),
            kilometraje_venta=self.data_factory.random_int(0, 300000),
        )
        self.assertTrue(resultado)

    def test_HU005_2_vender_automovil_no_existente(self):
        """test que verifica que no se pueda vender un automovil que no existe"""
        resultado = self.logica.vender_auto(
            placa="AAA002",
            precio_venta=self.data_factory.random_int(1000000, 1000000000),
            kilometraje_venta=self.data_factory.random_int(0, 300000),
        )
        self.assertFalse(resultado)

    def test_HU005_3_vender_automovil_precio_venta_string(self):
        """test que verifica que no se pueda vender un automovil sin precio de venta"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            precio_venta="abc",
            kilometraje_venta=self.data_factory.random_int(0, 300000),
        )
        self.assertFalse(resultado)

    def test_HU005_4_vender_automovil_kilometraje_venta_string(self):
        """test que verifica que no se pueda vender un automovil sin kilometraje de venta"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            precio_venta=self.data_factory.random_int(1000000, 1000000000),
            kilometraje_venta="abc",
        )
        self.assertFalse(resultado)

    def test_HU005_5_vender_automovil_precio_venta_negativo(self):
        """test que verifica que no se pueda vender un automovil con precio de venta negativo"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            precio_venta=-1,
            kilometraje_venta=self.data_factory.random_int(0, 300000),
        )
        self.assertFalse(resultado)

    def test_HU005_6_vender_automovil_kilometraje_venta_negativo(self):
        """test que verifica que no se pueda vender un automovil con kilometraje de venta negativo"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            precio_venta=self.data_factory.random_int(1000000, 1000000000),
            kilometraje_venta=-1,
        )
        self.assertFalse(resultado)


class Test_Modelo_Accion(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()

        self.auto1 = Auto(
            marca="volkswagen",
            modelo=2016,
            placa="XXX001",
            color="gris",
            cilindraje=2.5,
            combustible="GASOLINA",
            kilometraje_compra=0,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )
        self.auto2 = Auto(
            marca="Nissan",
            modelo=2016,
            placa="AAA001",
            color="Rojo",
            cilindraje=2.5,
            combustible="DIESEL",
            kilometraje_compra=25000,
            precio_venta=0,
            kilometraje_venta=0,
            gasto_total=0,
            gasto_anual=0,
            gasto_kilometro=0,
            vendido=False,
        )

        self.manto1 = Mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.manto2 = Mantenimiento(
            nombre="Cambio de Llantas", descripcion="Pago por nuevas llantas"
        )

        self.session.add(self.auto1)
        self.session.add(self.auto2)
        self.session.add(self.manto1)
        self.session.add(self.manto2)

        self.session.commit()

    def tearDown(self):
        self.session = Session()

        """Consulta todos los autos"""
        busqueda = self.session.query(Auto).all()

        """Borra todos los autos"""
        for auto in busqueda:
            self.session.delete(auto)

        """Consulta todos los Mantenimientos"""
        busqueda = self.session.query(Mantenimiento).all()

        """Borra todos los Mantenimientos"""
        for manto in busqueda:
            self.session.delete(manto)

        self.session.commit()
        self.session.close()

    def test_HU012_1_crear_accion(self):
        """test que verifica que se puede agregar una accion a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.0,
            fecha="15-08-2022",
            kilometraje=15000,
        )
        if resultado == True:
            acciones = self.logica.dar_acciones_auto(id_auto=1)
            for accion in acciones:
                if accion.get("costo") == 25000 and accion.get("fecha") == "15-08-2022":
                    resultado = True
                    continue
                else:
                    resultado = False
        self.assertTrue(resultado)

    def test_HU012_2_crear_dos_acciones(self):
        """test que verifica que se puede agregar varias acciones a un auto"""
        found = 0
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.0,
            fecha="15-08-2022",
            kilometraje=15000,
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=95000.0,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=75000.5,
            fecha="25-08-2020",
            kilometraje=3000,
        )
        acciones = self.logica.dar_acciones_auto(id_auto=1)
        if len(acciones) == 3:
            for accion in acciones:
                if accion.get("costo") == 25000 and accion.get("fecha") == "15-08-2022":
                    found += 1
                elif (
                    accion.get("costo") == 95000 and accion.get("fecha") == "25-08-2022"
                ):
                    found += 1
                else:
                    found += 0
        self.assertEqual(found, 2)

    def test_HU012_3_crear_acciones_vacias_1(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto="", mantenimiento="", valor="", fecha="", kilometraje=""
        )
        self.assertFalse(resultado)

    def test_HU012_3_crear_acciones_vacias_2(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1, mantenimiento="", valor="", fecha="", kilometraje=""
        )
        self.assertFalse(resultado)

    def test_HU012_3_crear_acciones_vacias_3(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor="",
            fecha="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_HU012_3_crear_acciones_vacias_4(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.9,
            fecha="",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_HU012_3_crear_acciones_vacias_3(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.2,
            fecha="25-08-2022",
            kilometraje="",
        )
        self.assertFalse(resultado)

    def test_HU012_3_crear_acciones_vacias_4(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.9,
            fecha="",
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_4_crear_accion_costo_invalido(self):
        """test que verifica que no se puede agregar una accion con un costo invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor="25000.3",
            fecha="25-08-2022",
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_5_crear_accion_kilometraje_invalido(self):
        """test que verifica que no se puede agregar una accion con un kilometraje invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.5,
            fecha="25-08-2022",
            kilometraje="150000",
        )
        self.assertFalse(resultado)

    def test_HU012_6_crear_accion_fecha_invalido_1(self):
        """test que verifica que no se puede agregar una accion con una fecha invalida"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.8,
            fecha=189750369,
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_6_crear_accion_fecha_invalido_2(self):
        """test que verifica que no se puede agregar una accion con una fecha invalida"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.7,
            fecha="25-08",
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_7_crear_accion_Mantenimiento_invalido(self):
        """test que verifica que no se puede agregar una accion con un mantenimiento invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Gasolina",
            valor=25000.7,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_8_crear_accion_duplicada_1(self):
        """test que verifica que no se puede agregar una accion duplicada"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.7,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.7,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        self.assertFalse(resultado)

    def test_HU012_8_crear_accion_duplicada_2(self):
        """test que verifica que no se puede agregar una accion duplicada"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=25000.7,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=25000.7,
            fecha="25-08-2022",
            kilometraje=150000,
        )
        self.assertTrue(resultado)
