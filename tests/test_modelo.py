import unittest
import random
from faker import Faker
from faker.providers import BaseProvider
from datetime import date

from src.logica.Logica_real import Logica_real
from src.modelo.conn import Session
from src.modelo.auto import Auto
from src.modelo.accion import Accion
from src.modelo.mantenimiento import Mantenimiento


class ProveedorAuto(BaseProvider):
    """clase para generar marcas de autos aleatorias"""

    def marca_auto(self):
        marcas = [
            "Toyota",
            "Renault",
            "Chevrolet",
            "Tesla",
            "BMW",
            "Honda",
            "Hyundai",
            "Kia",
            "Mazda",
            "Suzuki",
            "Audi",
            "Mercedes-Benz",
            "Fiat",
            "Ford",
            "Peugeot",
            "Citroën",
            "Dodge",
            "Chrysler",
            "Jeep",
            "Mitsubishi",
            "Subaru",
            "Volvo",
            "Land Rover",
            "Jaguar",
            "Porsche",
            "Mini",
            "Smart",
            "Lexus",
            "Infiniti",
            "Acura",
            "Isuzu",
            "Daihatsu",
        ]

        return random.choice(marcas)


class ModeloTestEmptySetUp(unittest.TestCase):
    """clase que contiene los test con el setUp vacio"""

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.logica = Logica_real()
        self.session = Session()

        busqueda = self.session.query(Auto).all()
        for auto in busqueda:
            self.session.delete(auto)

        self.session.commit()

    def tearDown(self):
        self.session = Session()

        """Consulta todos los autos"""
        busqueda = self.session.query(Auto).all()

        """Borra todos los autos"""
        for auto in busqueda:
            self.session.delete(auto)

        self.session.commit()
        self.session.close()

    def test_caso01_dar_lista_autos_vacia(self):
        """Test que verifica que la lista de autos este vacia"""
        busqueda = self.logica.dar_autos()
        if len(busqueda) == 0:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_caso02_dar_2_autos_ordenados(self):
        """Test que verifica que la lista de autos este ordenada por placa"""
        self.logica.crear_auto("Toyota", 1995, "ABC123", "Rojo", 1500, "Gasolina", 0)
        self.logica.crear_auto("Toyota", 2015, "XYZ789", "Rojo", 1500, "Gasolina", 0)
        busqueda = self.logica.dar_autos()
        resultado = True
        for i in range(len(busqueda) - 1):
            if busqueda[i]["placa"] > busqueda[i + 1]["placa"]:
                resultado = False
                break
        self.assertTrue(resultado)


class ModeloTestTDD(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker("es_ES")
        self.data_factory.add_provider(ProveedorAuto)

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
        auto1 = {
            "marca": self.data_factory.marca_auto(),
            "modelo": self.data_factory.random_int(1900, date.today().year),
            "placa": "ABB123",
            "color": self.data_factory.color(),
            "cilindraje": self.data_factory.random_int(10, 50) / 10,
            "combustible": self.data_factory.text(8),
            "kilometraje": self.data_factory.random_int(0, 500000),
        }

        auto2 = {
            "marca": self.data_factory.marca_auto(),
            "modelo": self.data_factory.random_int(1900, date.today().year),
            "placa": "AAA123",
            "color": self.data_factory.color(),
            "cilindraje": self.data_factory.random_int(10, 50) / 10,
            "combustible": self.data_factory.text(8),
            "kilometraje": self.data_factory.random_int(0, 500000),
        }

        self.logica.crear_auto(**auto1)
        self.logica.crear_auto(**auto2)

        busqueda = self.logica.dar_autos()
        placas = []
        for auto in busqueda:
            placas.append(auto["placa"])

        self.assertEqual(placas, sorted(placas))

    def test_caso03_1_agregar_auto_campo_placa_mas_de_6_caracteres(self):
        """test que verifica que el campo placa no tenga mas de 6 caracteres"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(1900, date.today().year),
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(1000, 9999)),
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="GASOLINA PREMIUM",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(
            resultado,
            "Error: placa debe ser de 6 caracteres y modelo debe ser menor a 9999",
        )

    def test_caso03_2_agregar_auto_campo_placa_letras(self):
        """test que verifica que el campo tenga 3 letras al inicio"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(1900, date.today().year),
            placa=str(self.data_factory.random_int(100000, 999999)),
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="GASOLINA PREMIUM",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: placa debe ser un String")

    def test_caso03_3_agregar_auto_campo_placa_numeros(self):
        """test que verifica que el campo placa tenga tres numero al final"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(1900, date.today().year),
            placa=self.data_factory.bothify(text="??????").upper(),
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="GASOLINA PREMIUM",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(
            resultado, "Error: placa debe tener 3 letras y 3 numeros (Ej: ABC123)"
        )

    def test_caso04_crear_auto_ya_creado(self):
        """test que verifica que los datos del auto no esten repetidos"""
        resultado = self.logica.crear_auto(
            marca="Ford",
            modelo=2016,
            placa="XXX001",
            color="gris",
            cilindraje=2.5,
            combustible="GASOLINA",
            kilometraje=0,
        )
        self.assertEqual(resultado, "Error: auto con Placa XXX001 ya esta registrado")

    def test_caso05_crear_auto_placa_duplicada_1(self):
        """test que verifica que el campo placa del auto no este duplicada"""
        resultado = self.logica.crear_auto(
            marca="Seat",
            modelo=2019,
            placa="AAA001",
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="HIBRIDO",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: auto con Placa AAA001 ya esta registrado")

    def test_caso05_crear_auto_marca_duplicado_2(self):
        """test que verifica que el campo marca del auto no este duplicado"""
        resultado = self.logica.crear_auto(
            marca="volkswagen",
            modelo=2019,
            placa="AAA005",
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="HIBRIDO",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(
            resultado, "Error: auto de la Marca volkswagen ya esta registrado"
        )

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
        self.assertEqual(resultado, "Error: marca es requerido")

    def test_caso06_2_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="",
            modelo="",
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            color="",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: marca es requerido")

    def test_caso06_3_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca="",
            modelo="",
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            color="azul",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: marca es requerido")

    def test_caso06_4_crear_auto_vacio(self):
        """test que verifica que los campos al crear un auto no esten vacios"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo="",
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            color="",
            cilindraje="",
            combustible="",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: modelo es requerido")

    def test_caso07_crear_auto_campo_modelo_invalido_1(self):
        """test que verifica que el campo modelo del auto sean 4 digitos"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo=19995,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(
            resultado,
            "Error: placa debe ser de 6 caracteres y modelo debe ser menor a 9999",
        )

    def test_caso07_crear_auto_campo_modelo_invalido_2(self):
        """test que verifica que el campo modelo del auto sean digitos"""
        resultado = self.logica.crear_auto(
            marca=self.data_factory.marca_auto(),
            modelo="19995",
            placa="AAA123" + str(self.data_factory.random_int(100, 999)),
            color=self.data_factory.color(),
            cilindraje=self.data_factory.random_int(10, 50) / 10,
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(
            resultado,
            "Error: placa debe ser de 6 caracteres y modelo debe ser menor a 9999",
        )

    def test_caso08_crear_auto_campo_kilometraje_invalido(self):
        """test que verifica que el campo kilometraje del auto sea un numero"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="ABC001",
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje="asd",
        )
        self.assertEqual(resultado, "Error: kilometraje debe ser un número")

    def test_caso09_crear_auto_campo_color_invalido(self):
        """test que verifica que el campo color del auto sea un texto"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="ABC001",
            color=123,
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: color debe ser un String")

    def test_caso10_crear_auto_campo_clindraje_invalido(self):
        """test que verifica que el campo cilindraje del auto sea un numero"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="ABC001",
            color=self.data_factory.color_name(),
            cilindraje="asd",
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: cilindraje debe ser un número o un decimal")

    def test_caso11_crear_auto_campo_combustible_invalido(self):
        """test que verifica que el campo combustible del auto sea un texto"""
        resultado = self.logica.crear_auto(
            marca="nissan",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="ABC001",
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible=123,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: combustible debe ser un String")

    def test_caso12_1_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.aniadir_mantenimiento(nombre="", descripcion="")
        self.assertEqual(resultado, "Error: nombre es requerido")

    def test_caso12_2_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="Cambio de Llantas", descripcion=""
        )
        self.assertEqual(resultado, "Error: descripcion es requerido")

    def test_caso12_3_crear_mantenimento_vacio(self):
        """test que verifica que los campos al crear un manenimiento no esten vacios"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="", descripcion="Pago por nuevas llantas"
        )
        self.assertEqual(resultado, "Error: nombre es requerido")

    def test_caso13_crear_mantenimento_ya_existente(self):
        """test que verifica que no se pueda crear un mantenimiento ya existente"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.assertEqual(
            resultado,
            "Error: mantenimiento con Nombre Cambio de aceite ya esta registrado",
        )

    def test_caso14_mantenimiento_creado_debe_ser_visible(self):
        """test que verifica que despues de creado un mantenimiento se vea en la lista"""
        self.logica.aniadir_mantenimiento(
            nombre="Cambio de Rines", descripcion="Pago por nuevos Rines"
        )
        lista = self.logica.dar_mantenimientos()
        if lista[len(lista) - 1].get("nombre") == "Cambio de Rines":
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_caso15_mantenimiento_mayor_2_letras(self):
        """test que verifica que despues de creado un mantenimiento tenga mas de tres letras"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="CF", descripcion="Pago por nuevas llantas"
        )
        self.assertEqual(resultado, "Error: nombre debe tener más de 3 caracteres")

    def test_caso16_mantenimiento_menor_200_letras(self):
        """test que verifica que despues de creado un mantenimiento tenga menos de 200 letras"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="CFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCF",
            descripcion="Pago por nuevas llantas",
        )
        self.assertEqual(resultado, "Error: nombre debe tener menos de 200 caracteres")

    def test_caso17_crear_mantenimiento_exitoso(self):
        """test que verifica que se pueda crear un mantenimiento"""
        resultado = self.logica.aniadir_mantenimiento(
            nombre="Cambio de Llanta", descripcion="Pago por nuevas llantas"
        )
        self.assertTrue(resultado)

    def test_HU002_caso01_editar_auto_campo_marca_vacio(self):
        """test que verifica que el campo marca del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca="",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: marca es requerido")

    def test_HU002_caso02_editar_auto_campo_modelo_vacio(self):
        """test que verifica que el campo modelo del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca="toyota",
            modelo="",
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: modelo es requerido")

    def test_HU002_caso03_editar_auto_campo_placa_vacio(self):
        """test que verifica que el campo placa del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: placa es requerido")

    def test_HU002_caso04_editar_auto_campo_color_vacio(self):
        """test que verifica que el campo color del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color="",
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: color es requerido")

    def test_HU002_caso05_editar_auto_campo_cilindraje_vacio(self):
        """test que verifica que el campo cilindraje del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje="",
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: cilindraje es requerido")

    def test_HU002_caso06_editar_auto_campo_combustible_vacio(self):
        """test que verifica que el campo combustible del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: combustible es requerido")

    def test_HU002_caso07_editar_auto_campo_kilometraje_vacio(self):
        """test que verifica que el campo kilometraje del auto no este vacio"""
        resultado = self.logica.editar_auto(
            id=1,
            placa=self.data_factory.bothify(text="???").upper()
            + str(self.data_factory.random_int(100, 999)),
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: kilometraje es requerido")

    def test_HU002_caso09_editar_auto_campo_placa_no_existente(self):
        """test que verifica que el campo placa exista en la base de datos"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="ABC123",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.text(10),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: auto con Placa ABC123 no existe")

    def test_HU002_caso10_editar_auto_campo_placa_existente(self):
        """test que verifica que el campo placa no exista en la base de datos"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="AAA001",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: auto con Placa AAA001 ya esta registrado")

    def test_HU002_caso11_editar_auto_exitosamente_campo_modelo(self):
        """test que verifica que se edito el auto exitosamente"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo=2011,
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )

        auto_editado = self.logica.dar_auto(1)
        self.assertTrue(resultado)

    def test_HU002_caso12_editar_auto_exitosamente_campo_color(self):
        """test que verifica que se edito el auto exitosamente"""
        color = self.data_factory.color_name()

        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=color,
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )

        auto_editado = self.logica.dar_auto(1)
        self.assertTrue(resultado)
        self.assertEqual(auto_editado["color"], color)

    def test_HU002_caso13_editar_auto_exitosamente_campo_cilindraje(self):
        """test que verifica que se edito el auto exitosamente"""
        cilindraje = self.data_factory.pyint()

        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=cilindraje,
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )

        auto_editado = self.logica.dar_auto(1)
        self.assertTrue(resultado)
        self.assertEqual(auto_editado["cilindraje"], cilindraje)

    def test_HU002_caso14_editar_auto_exitosamente_campo_combustible(self):
        """test que verifica que se edito el auto exitosamente"""
        combustible = "GASOLINA Premium"

        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible=combustible,
            kilometraje=self.data_factory.random_int(0, 500000),
        )

        auto_editado = self.logica.dar_auto(1)
        self.assertTrue(resultado)
        self.assertEqual(auto_editado["combustible"], combustible)

    def test_HU002_caso15_editar_auto_exitosamente_campo_kilometraje(self):
        """test que verifica que se edito el auto exitosamente"""
        kilometraje = 14346

        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=kilometraje,
        )

        auto_editado = self.logica.dar_auto(1)
        self.assertTrue(resultado)
        self.assertEqual(auto_editado["kilometraje_compra"], kilometraje)

    def test_HU002_caso16_editar_auto_marca_existente(self):
        """test que verifica que el campo marca no exista en la base de datos"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca="Nissan",
            modelo=self.data_factory.random_int(min=1900, max=2025),
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: auto de la Marca Nissan ya esta registrado")

    def test_HU004_eliminar_auto_no_existente(self):
        """test que verifica que el auto no exista en la base de datos"""
        resultado = self.logica.eliminar_auto(100)
        self.assertEqual(resultado, "Error: El auto debe existir")

    def test_HU004_eliminar_auto_existosamente(self):
        """test que verifica que el auto se elimina exitosamente"""
        resultado = self.logica.eliminar_auto(1)
        self.assertTrue(resultado)

        autos = self.logica.dar_autos()
        for auto in autos:
            self.assertNotEqual(auto["id"], 1)

    def test_HU002_caso17_editar_auto_modelo_string(self):
        """test que verifica que el campo marca no exista en la base de datos"""
        resultado = self.logica.editar_auto(
            id=1,
            placa="XXX001",
            marca=self.data_factory.marca_auto(),
            modelo='asd',
            color=self.data_factory.color_name(),
            cilindraje=self.data_factory.pyint(),
            combustible="GASOLINA",
            kilometraje=self.data_factory.random_int(0, 500000),
        )
        self.assertEqual(resultado, "Error: modelo debe ser un número")



class Test_Modelo_Venta(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker("es_ES")

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
            valor=self.data_factory.random_int(1000000, 10000000000) / 100,
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        self.assertTrue(resultado)

    def test_HU005_2_vender_automovil_no_existente(self):
        """test que verifica que no se pueda vender un automovil que no existe"""
        resultado = self.logica.vender_auto(
            placa="AAA002",
            valor=self.data_factory.random_int(1000000, 1000000000) / 100,
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        self.assertEqual(resultado, "Error: auto con Placa AAA002 no existe")

    def test_HU005_3_vender_automovil_precio_venta_string(self):
        """test que verifica que no se pueda vender un automovil sin precio de venta"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            valor="abc",
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        self.assertEqual(resultado, "Error: valor debe ser un decimal")

    def test_HU005_4_vender_automovil_kilometraje_venta_string(self):
        """test que verifica que no se pueda vender un automovil sin kilometraje de venta"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            valor=self.data_factory.random_int(1000000, 1000000000) / 100,
            kilometraje="abc",
        )
        self.assertEqual(resultado, "Error: kilometraje debe ser un número")

    def test_HU005_5_vender_automovil_precio_venta_negativo(self):
        """test que verifica que no se pueda vender un automovil con precio de venta negativo"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            valor=-1,
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        self.assertEqual(resultado, "Error: valor debe ser un numero mayor a 0")

    def test_HU005_6_vender_automovil_kilometraje_venta_negativo(self):
        """test que verifica que no se pueda vender un automovil con kilometraje de venta negativo"""
        resultado = self.logica.vender_auto(
            placa="AAA001",
            valor=self.data_factory.random_int(1000000, 1000000000) / 100,
            kilometraje=-1,
        )
        self.assertEqual(resultado, "Error: kilometraje debe ser un numero mayor a 0")

    def test_HU005_1_vender_automovil_ya_vendido(self):
        """test que verifica que no se pueda vender un automovil ya vendido"""
        self.logica.vender_auto(
            placa="AAA001",
            valor=self.data_factory.random_int(1000000, 10000000000) / 100,
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        resultado = self.logica.vender_auto(
            placa="AAA001",
            valor=self.data_factory.random_int(1000000, 10000000000) / 100,
            kilometraje=self.data_factory.random_int(0, 300000),
        )
        self.assertEqual(resultado, "Error: auto con placa AAA001 ya fue vendido")


class Test_Modelo_Accion(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker()

        self.auto1 = Auto(
            marca="volkswagen",
            modelo=2016,
            placa="XXX001",
            color=self.data_factory.color_name(),
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
            color=self.data_factory.color_name(),
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
        self.manto3 = Mantenimiento(
            nombre="Carga de Diesel", descripcion="Pago por cargar combustible"
        )

        self.session.add(self.auto1)
        self.session.add(self.auto2)
        self.session.add(self.manto1)
        self.session.add(self.manto2)
        self.session.add(self.manto3)

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
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        if resultado == True:
            acciones = self.logica.dar_acciones_auto(id_auto=1)
            for accion in acciones:
                if accion.get("valor") == valor and accion.get("fecha") == fecha:
                    resultado = True
                    break
                else:
                    resultado = False
        self.assertTrue(resultado)

    def test_HU012_2_crear_dos_acciones(self):
        """test que verifica que se puede agregar varias acciones a un auto"""
        found = 0
        fecha1 = self.data_factory.date(pattern="%Y-%m-%d")
        fecha2 = self.data_factory.date(pattern="%Y-%m-%d")
        fecha3 = self.data_factory.date(pattern="%Y-%m-%d")
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor3 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha=fecha1,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=valor2,
            fecha=fecha2,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=valor3,
            fecha=fecha3,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        acciones = self.logica.dar_acciones_auto(id_auto=1)
        if len(acciones) == 3:
            for accion in acciones:
                if accion.get("valor") == valor1 and accion.get("fecha") == fecha1:
                    found += 1
                elif accion.get("valor") == valor2 and accion.get("fecha") == fecha2:
                    found += 1
                else:
                    found += 0
        self.assertEqual(found, 2)

    def test_HU012_3_crear_acciones_vacias_1(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto="", mantenimiento="", valor="", fecha="", kilometraje=""
        )
        self.assertEqual(resultado, "Error: id_auto es requerido")

    def test_HU012_3_crear_acciones_vacias_2(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1, mantenimiento="", valor="", fecha="", kilometraje=""
        )
        self.assertEqual(resultado, "Error: mantenimiento es requerido")

    def test_HU012_3_crear_acciones_vacias_3(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor="",
            fecha="",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: valor es requerido")

    def test_HU012_3_crear_acciones_vacias_4(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha="",
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: fecha es requerido")

    def test_HU012_3_crear_acciones_vacias_3(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: kilometraje es requerido")

    def test_HU012_3_crear_acciones_vacias_4(self):
        """test que verifica que no se puede agregar una accion vacia a un auto"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha="",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: fecha es requerido")

    def test_HU012_4_crear_accion_valor_invalido(self):
        """test que verifica que no se puede agregar una accion con un valor invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor="25000.3",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(
            resultado, "Error: valor debe ser un número con decimal mayor a 0"
        )

    def test_HU012_5_crear_accion_kilometraje_invalido(self):
        """test que verifica que no se puede agregar una accion con un kilometraje invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje="150000",
        )
        self.assertEqual(resultado, "Error: kilometraje debe ser un Entero")

    def test_HU012_6_crear_accion_fecha_invalido_1(self):
        """test que verifica que no se puede agregar una accion con una fecha invalida"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=189750369,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: fecha debe ser un String")

    def test_HU012_6_crear_accion_fecha_invalido_2(self):
        """test que verifica que no se puede agregar una accion con una fecha invalida"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha="25-08",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: La fecha debe ser en formato AAAA-MM-DD")

    def test_HU012_7_crear_accion_Mantenimiento_invalido_1(self):
        """test que verifica que no se puede agregar una accion con un mantenimiento invalido"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Gasolina",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: El Mantenimiento debe existir")

    def test_HU012_7_crear_accion_Mantenimiento_invalido_2(self):
        """test que verifica que no se puede agregar una accion con un mantenimiento de mas de 50 caracteres"""
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="CFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCFCF",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(
            resultado, "Error: mantenimiento debe tener menos de 50 caracteres"
        )

    def test_HU012_8_crear_accion_duplicada_1(self):
        """test que verifica que no se puede agregar una accion duplicada"""
        kilo = self.data_factory.random_int(min=0, max=999999)
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=kilo,
        )
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=kilo,
        )
        self.assertEqual(resultado, "Error: La Accion no debe estar repetidas")

    def test_HU012_8_crear_accion_duplicada_2(self):
        """test que verifica que no se puede agregar una accion duplicada"""
        kilo = self.data_factory.random_int(min=0, max=999999)
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=kilo,
        )
        resultado = self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=valor,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=kilo,
        )
        self.assertTrue(resultado)

    def test_HU012_9_crear_accion_auto_invalido(self):
        """test que verifica que no se puede agregar una accion a un auto que no exista"""
        kilo = self.data_factory.random_int(min=0, max=999999)
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        resultado = self.logica.crear_accion(
            id_auto=3,
            mantenimiento="Cambio de Llantas",
            valor=valor,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=kilo,
        )
        self.assertEqual(resultado, "Error: El Auto debe existir")

    def test_HU010_1_ver_lista_acciones_ordenada(self):
        """test que verifica que la lista de acciones estan ordenadas en descentente por kilometro"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Diesel",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Diesel",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista = self.logica.dar_acciones_auto(id_auto=1)
        if (
            lista[0].get("kilometraje")
            > lista[1].get("kilometraje")
            > lista[2].get("kilometraje")
        ):
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_HU010_2_ver_accion_especifica(self):
        """test que verifica que el retornar una accion especifica de un auto"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Diesel",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        kilo = self.data_factory.random_int(min=0, max=999999)
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Diesel",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=fecha,
            kilometraje=kilo,
        )
        busqueda = self.logica.dar_accion(id_auto=1, id_accion=2)
        if busqueda != None:
            if busqueda.get("kilometraje") == kilo and busqueda.get("fecha") == fecha:
                resultado = True
            else:
                resultado = False
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_HU010_3_ver_accion_invalida(self):
        """test que verifica el error al pedir la lista de acciones de un auto invalido"""
        lista = self.logica.dar_acciones_auto(id_auto=3)
        if len(lista) == 0:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_HU010_4_ver_accion_especifica_invalida(self):
        """test que verifica el error al pedir la una accion invalida de un auto valido"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Carga de Diesel",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista = self.logica.dar_accion(id_auto=1, id_accion=3)
        if lista == None:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)


class Test_Modelo_Gastos(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker("es_ES")
        self.data_factory.add_provider(ProveedorAuto)

        self.auto1 = Auto(
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="XXX001",
            color="gris",
            cilindraje=self.data_factory.pyfloat(
                left_digits=3, right_digits=1, positive=True
            ),
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
            marca=self.data_factory.marca_auto(),
            modelo=self.data_factory.random_int(min=1900, max=2025),
            placa="AAA001",
            color="Rojo",
            cilindraje=self.data_factory.pyfloat(
                left_digits=3, right_digits=1, positive=True
            ),
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
            nombre="Gasolina", descripcion="Pago por carga de Gasolina"
        )
        self.manto3 = Mantenimiento(
            nombre="Seguro", descripcion="Prima anual por coberturas del Seguro"
        )

        self.session.add(self.auto1)
        self.session.add(self.auto2)
        self.session.add(self.manto1)
        self.session.add(self.manto2)
        self.session.add(self.manto3)
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

    def test_HU014_1_gasto_total_0(self):
        """test que valida el campo de valor total del reporte sin acciones"""
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            if gastos[1] == 0:
                resultado = True
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU014_1_gasto_total_1(self):
        """test que valida el campo de valor total del reporte con una accion"""
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            if gastos[1] == valor:
                resultado = True
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU014_1_gasto_total_2(self):
        """test que valida el campo de valor total del reporte con dos acciones"""
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            if gastos[1] == round((valor1 + valor2), 2):
                resultado = True
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU014_1_gasto_total_3(self):
        """test que valida el campo de valor total del reporte sin acciones del carro escogido"""
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=2)
        for gastos in lista_gastos:
            if gastos[1] == 0:
                resultado = True
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU014_2_gasto_total_0(self):
        """Prueba que los gastos sea un numero positivo"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=-10.0,
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)

        for gastos in lista_gastos:
            if gastos[1] >= 0:
                resultado = True
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU015_1_gasto_anual_1(self):
        """Prueba que los gastos por año"""
        found = 0
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor3 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2019-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2020-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor3,
            fecha="2021-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)

        for gastos in lista_gastos:
            # If gasto(2019) == valor1 and gasto(2020) == valor2 and gasto(2021) == valor3
            if gastos[0] == "2019" and gastos[1] == valor1:
                found += 1
            elif gastos[0] == "2020" and gastos[1] == valor2:
                found += 1
            elif gastos[0] == "2021" and gastos[1] == valor3:
                found += 1
            elif gastos[0] == "Total" and gastos[1] == round(
                (valor1 + valor2 + valor3), 2
            ):
                found += 1
            else:
                found += 0
        self.assertEqual(found, 4)

    def test_HU015_1_gasto_anual_2(self):
        """Prueba que los gastos por año"""
        found = 0
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor3 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor4 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2019-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2020-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor3,
            fecha="2021-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor4,
            fecha="2019-03-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            # If gasto(2019) == (valor1+valor4) and gasto(2020) == valor2 and gasto(2021) == valor3
            if gastos[0] == "2019" and gastos[1] == (valor1 + valor4):
                found += 1
            elif gastos[0] == "2020" and gastos[1] == valor2:
                found += 1
            elif gastos[0] == "2021" and gastos[1] == valor3:
                found += 1
            elif gastos[0] == "Total" and gastos[1] == round(
                (valor1 + valor2 + valor3 + valor4), 2
            ):
                found += 1
            else:
                found += 0
        self.assertEqual(found, 4)

    def test_HU015_1_gasto_anual_3(self):
        """Prueba que los gastos por año"""
        found = 0
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor3 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor4 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2019-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2020-03-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor3,
            fecha="2020-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor4,
            fecha="2019-03-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            # If gasto(2019) == (valor1+valor4) and gasto(2020) == valor2 and gasto(2021) == valor3
            if gastos[0] == "2019" and gastos[1] == (valor1 + valor4):
                found += 1
            elif gastos[0] == "2020" and gastos[1] == (valor2 + valor3):
                found += 1
            elif gastos[0] == "Total" and gastos[1] == round(
                (valor1 + valor2 + valor3 + valor4), 2
            ):
                found += 1
            else:
                found += 0
        self.assertEqual(found, 3)

    def test_HU015_2_gasto_anual_invalido(self):
        """Prueba que los gastos por año con valor invalido"""
        found = 0
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor2 = -10000
        valor3 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        valor4 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)

        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2019-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2020-03-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor3,
            fecha="2020-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor4,
            fecha="2019-03-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        for gastos in lista_gastos:
            # If gasto(2019) == (valor1+valor4) and gasto(2020) == valor2 and gasto(2021) == valor3
            if gastos[0] == "2019" and gastos[1] == (valor1 + valor4):
                found += 1
            elif gastos[0] == "2020" and gastos[1] == (valor2 + valor3):
                found += 1
            elif gastos[0] == "Total" and gastos[1] == round(
                (valor1 + valor2 + valor3 + valor4), 2
            ):
                found += 1
            else:
                found += 0
        self.assertNotEqual(found, 3)

    def test_HU016_1_gasto_xKilometro(self):
        """Prueba que los gastos por kilometros se calculen bien"""
        valor1 = 2400.00
        kilo1 = 800
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2022-02-15",
            kilometraje=kilo1,
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        self.assertEqual(valor_kilometro, (valor1 / kilo1))

    def test_HU016_1_gasto_xKilometro_2(self):
        """Prueba que los gastos por kilometros se calculen bien"""
        valor1 = 2400.00
        kilo1 = 800
        valor2 = 2400.00
        kilo2 = 1600
        valor3 = 1200.00
        kilo3 = 0
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2022-02-15",
            kilometraje=kilo1,
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2022-05-15",
            kilometraje=kilo2,
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor3,
            fecha="2021-05-15",
            kilometraje=kilo3,
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        self.assertEqual(valor_kilometro, 3.0)

    def test_HU016_1_gasto_xKilometro_3(self):
        """Prueba que los gastos por kilometros se calculen bien"""
        valor1 = 2400.00
        kilo1 = 800
        valor2 = 2400.00
        kilo2 = 1600
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2022-02-15",
            kilometraje=kilo1,
        )
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor2,
            fecha="2022-05-15",
            kilometraje=kilo2,
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        self.assertEqual(valor_kilometro, 3.0)

    def test_HU016_2_gasto_xKilometro(self):
        """Prueba que los gastos por kilometros usen valores del ultimo año"""
        valor1 = 10021.86
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor1,
            fecha="2021-02-15",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        lista_gastos, valor_kilometro = self.logica.dar_reporte_ganancias(id_auto=1)
        self.assertEqual(valor_kilometro, 0)


class ModeloTestEmptySetUp(unittest.TestCase):
    """clase que contiene los test con el setUp vacio"""

    def setUp(self):
        """Se ejecuta antes de cada prueba"""
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker("es_ES")

    def test_caso01_dar_lista_autos_vacia(self):
        """Test que verifica que la lista de autos este vacia"""
        busqueda = self.logica.dar_autos()
        if len(busqueda) == 0:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_caso01_dar_lista_auto_vacio(self):
        """Test que verifica que no se regrese nada cuando el auto no exista"""
        busqueda = self.logica.dar_auto(id_auto=1)
        if busqueda == None:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)

    def test_caso_marca_muy_larga(self):
        """Test que verifica que no se cree un auto con marca de mas de 50 caracteres"""
        resultado = self.logica.crear_auto(
            "ToyotaGrisCorollaSuperEquipadoTurboHibridoLEDCajuela",
            "ABC123",
            self.data_factory.random_int(1900, date.today().year),
            0,
            "Rojo",
            1500,
            "Gasolina",
        )
        self.assertEqual(resultado, "Error: marca debe tener menos de 50 caracteres")

    def test_caso_marca_muy_corta(self):
        """Test que verifica que no se cree un auto con menos de mas de 2 caracteres"""
        resultado = self.logica.crear_auto(
            "VW",
            "ABC123",
            self.data_factory.random_int(1900, date.today().year),
            0,
            "Rojo",
            1500,
            "Gasolina",
        )
        self.assertEqual(resultado, "Error: marca debe tener más de 2 caracteres")

    def test_caso_vender_sin_placa(self):
        """Test que verifica que no se pueda vender un carro con placa vacia"""
        kilometraje = self.data_factory.random_int(0, 500000)
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        resultado = self.logica.vender_auto("", valor, kilometraje)

        self.assertEqual(resultado, "Error: placa es requerida")

    def test_HU006_ver_mantenimientos_vacios(self):
        """Test que verifica que dr purda devolver la lista de Mantenimientos vacia"""
        busqueda = self.logica.dar_mantenimientos()
        if len(busqueda) == 0:
            resultado = True
        else:
            resultado = False
        self.assertTrue(resultado)


class ModeloTestEditarAccion(unittest.TestCase):
    """Clase que contiene los test de la logica"""

    def setUp(self):
        self.logica = Logica_real()
        self.session = Session()
        self.data_factory = Faker("es_ES")

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

        self.manto1 = Mantenimiento(
            nombre="Cambio de aceite", descripcion="Cambio de aceite"
        )
        self.manto2 = Mantenimiento(
            nombre="Cambio de Llantas", descripcion="Pago por nuevas llantas"
        )

        self.session.add(self.auto1)
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

    def test_HU011_01_editar_accion_exitosa(self):
        """Test que verifica que se pueda editar una accion"""
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        fecha2 = self.data_factory.date(pattern="%Y-%m-%d")
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.editar_accion(
            id_accion=1,
            mantenimiento="Cambio de aceite",
            id_auto=1,
            valor=valor2,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
            fecha=fecha2,
        )
        busqueda = self.logica.dar_acciones_auto(id_auto=1)
        for accion in busqueda:
            if accion.get("valor") == valor2 and accion.get("fecha") == fecha2:
                resultado = True
                break
            else:
                resultado = False
        self.assertTrue(resultado)

    def test_HU011_02_editar_accion_mantenimiento_vacio(self):
        """Test que verifica que no se pueda editar una accion con mantenimiento vacio"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: mantenimiento es requerido")

    def test_HU011_03_editar_accion_mantenimiento_muy_largo(self):
        """Test que verifica que no se pueda editar una accion con mantenimiento vacio"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(
            resultado, "Error: mantenimiento no puede tener mas de 50 caracteres"
        )

    def test_HU011_04_editar_accion_valor_text(self):
        """Test que verifica que no se pueda editar una accion con valor como texto"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor="",
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: valor es requerido")

    def test_HU011_05_editar_accion_valor_0(self):
        """Test que verifica que no se pueda editar una accion con valor de 0"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=0,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(
            resultado, "Error: valor debe ser un número con decimal mayor a 0"
        )

    def test_HU011_06_editar_accion_valor_negativo(self):
        """Test que verifica que no se pueda editar una accion con valor de 0"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=-25000,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(
            resultado, "Error: valor debe ser un número con decimal mayor a 0"
        )

    def test_HU011_07_editar_accion_fecha_vacia(self):
        """Test que verifica que no se pueda editar una accion con fecha de vacia"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha="",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: fecha es requerido")

    def test_HU011_08_editar_accion_fecha_incompleta(self):
        """Test que verifica que no se pueda editar una accion con fecha incompleta"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha="2020-08",
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: La fecha debe ser en formato AAAA-MM-DD")

    def test_HU011_09_editar_accion_fecha_numerica(self):
        """Test que verifica que no se pueda editar una accion con fecha numerica"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=123654987,
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: La fecha debe ser un string")

    def test_HU011_10_editar_accion_auto_errado(self):
        """Test que verifica que no se pueda editar una accion de un auto equivocado"""
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=3,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: El auto debe existir")

    def test_HU011_11_editar_accion_errado(self):
        """Test que verifica que no se pueda editar una accion equivocada"""
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: La accion debe existir")

    def test_HU011_12_editar_accion_kilometraje_decimal(self):
        """Test que verifica que no se pueda editar una accion con fecha numerica"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
        )
        self.assertEqual(resultado, "Error: El kilometraje debe ser entero")

    def test_HU011_13_editar_accion_kilometraje_vacio(self):
        """Test que verifica que no se pueda editar una accion con fecha numerica"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje="",
        )
        self.assertEqual(resultado, "Error: kilometraje es requerido")

    def test_HU011_14_editar_accion_repetida(self):
        """Test que verifica que al editar una accion no quede repetida"""
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        kilo = self.data_factory.random_int(min=0, max=999999)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=kilo,
        )
        fecha2 = self.data_factory.date(pattern="%Y-%m-%d")
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        kilo2 = self.data_factory.random_int(min=0, max=999999)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=valor2,
            fecha=fecha2,
            kilometraje=kilo2,
        )
        resultado = self.logica.editar_accion(
            id_accion=2,
            mantenimiento="Cambio de aceite",
            id_auto=1,
            valor=valor,
            kilometraje=kilo,
            fecha=fecha,
        )
        self.assertEqual(
            resultado, "Error: La accion modificada no puede estar duplicada"
        )

    def test_HU011_15_editar_accion_mantenimiento_erroneo(self):
        """Test que verifica que no se pueda editar una accion con mantenimiento inexistente"""
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        resultado = self.logica.editar_accion(
            id_accion=1,
            id_auto=1,
            mantenimiento="Impuestos",
            fecha=self.data_factory.date(pattern="%Y-%m-%d"),
            valor=self.data_factory.pyfloat(
                left_digits=5, right_digits=2, positive=True
            ),
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        self.assertEqual(resultado, "Error: El Mantenimiento debe existir")

    def test_HU011_16_editar_accion_exitosa_2(self):
        """Test que verifica que se pueda editar una accion"""
        fecha1 = self.data_factory.date(pattern="%Y-%m-%d")
        valor1 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de Llantas",
            valor=valor1,
            fecha=fecha1,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        fecha = self.data_factory.date(pattern="%Y-%m-%d")
        valor = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.crear_accion(
            id_auto=1,
            mantenimiento="Cambio de aceite",
            valor=valor,
            fecha=fecha,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
        )
        fecha2 = self.data_factory.date(pattern="%Y-%m-%d")
        valor2 = self.data_factory.pyfloat(left_digits=5, right_digits=2, positive=True)
        self.logica.editar_accion(
            id_accion=2,
            mantenimiento="Cambio de aceite",
            id_auto=1,
            valor=valor2,
            kilometraje=self.data_factory.random_int(min=0, max=999999),
            fecha=fecha2,
        )
        busqueda = self.logica.dar_acciones_auto(id_auto=1)
        for accion in busqueda:
            if accion.get("valor") == valor2 and accion.get("fecha") == fecha2:
                resultado = True
                break
            else:
                resultado = False
        self.assertTrue(resultado)
