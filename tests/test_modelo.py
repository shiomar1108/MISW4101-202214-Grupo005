from pickle import FALSE
import unittest
from unittest import result

from src.logica.Logica_real import Logica_real
from src.modelo.conn import Session
from src.modelo.auto import Auto
from src.modelo.accion import Accion
from src.modelo.mantenimiento import Mantenimiento

#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class ModeloTestCase(unittest.TestCase):

	#Instancia el atributo logica para cada prueba
	def setUp(self):
		self.logica = Logica_real()
		self.session = Session()
		
		self.auto1 = Auto(
			marca = 'volkswagen',
		 	modelo = 2016, 
			placa = 'XXX001', 
			color = 'gris', 
			cilindraje = 2.5, 
			combustible= 'GASOLINA', 
			kilometraje_compra = 0, 
			precio_venta=0,
			kilometraje_venta = 0,
			gasto_total = 0,
			gasto_anual = 0,
			gasto_kilometro = 0,
			vendido = False,
		)
		self.auto2 = Auto(
			marca = 'Nissan',
		 	modelo = 2016, 
			placa = 'AAA001', 
			color = 'Rojo', 
			cilindraje = 2.5, 
			combustible= 'DIESEL', 
			kilometraje_compra = 25000, 
			precio_venta=0,
			kilometraje_venta = 0,
			gasto_total = 0,
			gasto_anual = 0,
			gasto_kilometro = 0,
			vendido = False,
		)
		self.manto1 = Mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')
		self.manto2 = Mantenimiento(nombre='Cambio de Llantas', descripcion='Pago por nuevas llantas')
		self.accion1 = Accion(
			kilometraje=15000, 
			costo=9600, 
			fecha='01/09/2022',
			mantenimiento = [self.manto1] ,
		)

		self.session.add(self.auto1)
		self.session.add(self.auto2)
		self.session.add(self.manto1)
		self.session.add(self.manto2)
		self.session.add(self.accion1)
		self.session.commit()


	def tearDown(self):
		self.session = Session()

		'''Consulta todos los autos'''
		busqueda = self.session.query(Auto).all()

		'''Borra todos los autos'''
		for auto in busqueda:
			self.session.delete(auto)

		'''Consulta todos los Mantenimientos'''
		busqueda = self.session.query(Mantenimiento).all()

		'''Borra todos los Mantenimientos'''
		for manto in busqueda:
			self.session.delete(manto)

		'''Consulta todos las Acciones'''
		busqueda = self.session.query(Accion).all()

		'''Borra todos los Mantenimientos'''
		for accion in busqueda:
			self.session.delete(accion)
			
		self.session.commit()
		self.session.close()


	def test_crear_auto(self):
		resultado = self.logica.crear_auto(
			marca='renault', 
			modelo=1995, 
			placa='XXX003', 
			color='negro', 
			cilindraje=1.6, 
			combustible= 'GASOLINA PREMIUM', 
			kilometraje= 1000
		)
		self.assertTrue(resultado)

	def test_dar_auto(self):
		temp = self.logica.dar_auto(placa='XXX001')
		if(temp.get('placa') == 'XXX001'):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_dar_auto_negativo(self):
		temp = self.logica.dar_auto(placa='XXX002')
		if(temp == None ):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_dar_autos(self):
		busqueda = self.logica.dar_autos()
		if len(busqueda) == 2:
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_editar_auto(self):
		resultado1 = self.logica.editar_auto(placa_og='XXX001', marca_n = 'volkswagen', modelo_n = 2019, placa_n = 'XXX001', color_n = 'Negro', cilindraje_n = 2.5, combustible_n= 'GASOLINA', kilometraje_n = 0,  ) 
		if(resultado1):
			temp = self.logica.dar_auto(placa='XXX001')
			if(temp.get('modelo') == 2019 and temp.get('color') == "Negro"):
				resultadoT = True
			else:
				resultadoT = False
		else:
			resultadoT = False
		self.assertTrue(resultadoT)

	def test_editar_auto_negativo(self):
		resultado1 = self.logica.editar_auto(placa_og='XXX005', marca_n = 'volkswagen', modelo_n = 2019, placa_n = 'XXX001', color_n = 'Negro', cilindraje_n = 2.5, combustible_n= 'GASOLINA', kilometraje_n = 0,  ) 
		if(resultado1):
			temp = self.logica.dar_auto(placa='XXX001')
			if(temp.modelo == '2019' and temp.color == "Negro"):
				resultadoT = True
			else:
				resultadoT = False
		else:
			resultadoT = False
		self.assertFalse(resultadoT)

	def test_crear_mantenimiento(self):
		resultado = self.logica.crear_mantenimiento(nombre='Polarizado', descripcion='Pago por colocacion de Polarizado en Ventana')
		self.assertTrue(resultado)

	def test_crear_mantenimiento_ya_creado(self):
		resultado = self.logica.crear_mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')
		self.assertFalse(resultado)

	def test_dar_mantenimiento(self):
		temp = self.logica.dar_mantenimiento(nombre= self.manto1.nombre)
		if(temp.get('nombre') == self.manto1.nombre and temp.get('descripcion') == self.manto1.descripcion):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_dar_mantenimiento_negativo(self):
		temp = self.logica.dar_mantenimiento(nombre= "Rines")
		if(temp == None):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_dar_mantenimentos(self):
		busqueda = self.logica.dar_mantenimientos()
		if len(busqueda) == 2:
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_crear_accion(self):
		resultado = self.logica.crear_accion(kilometraje= 1500,costo=850,fecha='15-08-2022', nombre='Cambio de Filtro')
		self.assertTrue(resultado)

	def test_crear_accion_ya_creado(self):
		resultado = self.logica.crear_accion(kilometraje= 15000,costo=9600,fecha='01/09/2022', nombre='Cambio de Filtro')
		self.assertFalse(resultado)

	def test_vender_auto(self):
		resultado = self.logica.vender_auto(placa='XXX001', precio_venta=15000000, kilometraje_venta= 352000)
		self.assertTrue(resultado)

	def test_vender_auto_ya_vendido(self):
		self.logica.vender_auto(placa='XXX001', precio_venta=15000000, kilometraje_venta= 352000)
		resultado = self.logica.vender_auto(placa='XXX001', precio_venta=15000000, kilometraje_venta= 352000)
		self.assertFalse(resultado)

class ModeloTestEmptySetUp(unittest.TestCase):
	"""clase que contiene los test con el setUp vacio"""
	def setUp(self):
		"""Se ejecuta antes de cada prueba"""
		self.logica = Logica_real()
		self.session = Session()

	def test_caso1_dar_lista_autos_vacia(self):
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
		
		self.auto1 = Auto(
			marca = 'volkswagen',
		 	modelo = 2016, 
			placa = 'XXX001', 
			color = 'gris', 
			cilindraje = 2.5, 
			combustible= 'GASOLINA', 
			kilometraje_compra = 0, 
			precio_venta=0,
			kilometraje_venta = 0,
			gasto_total = 0,
			gasto_anual = 0,
			gasto_kilometro = 0,
			vendido = False,
		)
		self.auto2 = Auto(
			marca = 'Nissan',
		 	modelo = 2016, 
			placa = 'AAA001', 
			color = 'Rojo', 
			cilindraje = 2.5, 
			combustible= 'DIESEL', 
			kilometraje_compra = 25000, 
			precio_venta=0,
			kilometraje_venta = 0,
			gasto_total = 0,
			gasto_anual = 0,
			gasto_kilometro = 0,
			vendido = False,
		)

		self.manto1 = Mantenimiento(nombre='Cambio de aceite', descripcion='Cambio de aceite' )
		self.manto2 = Mantenimiento(nombre='Cambio de Llantas', descripcion='Pago por nuevas llantas')

		self.session.add(self.auto1)
		self.session.add(self.auto2)
		self.session.add(self.manto1)
		self.session.add(self.manto2)
		self.session.commit()


	def tearDown(self):
		self.session = Session()

		'''Consulta todos los autos'''
		busqueda = self.session.query(Auto).all()

		'''Borra todos los autos'''
		for auto in busqueda:
			self.session.delete(auto)

		'''Consulta todos los Mantenimientos'''
		busqueda = self.session.query(Mantenimiento).all()

		'''Borra todos los Mantenimientos'''
		for manto in busqueda:
			self.session.delete(manto)
			
		self.session.commit()
		self.session.close()

	def test_caso2_dar_autos_ordenados(self):
		"""Test que verifica que la lista se regrese en orden cronologico"""
		busqueda = self.logica.dar_autos()
		if (busqueda[0].get('placa') == self.auto1.placa and busqueda[1].get('placa') == self.auto2.placa):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)	


	def test_caso3_1_agregar_auto_campo_placa_mas_de_6_caracteres(self):
		"""test que verifica que el campo placa no tenga mas de 6 caracteres"""
		resultado = self.logica.crear_auto(
			marca='renault', 
			modelo=1995, 
			placa='XXX0011', 
			color='negro', 
			cilindraje=1.6, 
			combustible= 'GASOLINA PREMIUM', 
			kilometraje= 1000 
		)
		self.assertFalse(resultado)

	def test_caso3_2_agregar_auto_campo_placa_letras(self):
		"""test que verifica que el campo tenga 3 letras al inicio"""
		resultado = self.logica.crear_auto(
			marca='renault', 
			modelo=1995, 
			placa='000123', 
			color='negro', 
			cilindraje=1.6, 
			combustible= 'GASOLINA PREMIUM', 
			kilometraje= 1000 
		)
		self.assertFalse(resultado)

	def test_caso3_3_agregar_auto_campo_placa_numeros(self):
		"""test que verifica que el campo placa tenga tres numero al final"""
		resultado = self.logica.crear_auto(
			marca='renault', 
			modelo=1995, 
			placa='XXXYYY', 
			color='negro', 
			cilindraje=1.6, 
			combustible= 'GASOLINA PREMIUM', 
			kilometraje= 1000 
		)
		self.assertFalse(resultado)

	def test_caso4_crear_auto_ya_creado(self):
		"""test que verifica que los datos del auto no esten repetidos"""
		resultado = self.logica.crear_auto(marca='volkswagen', modelo=2016, placa='XXX001', color='gris', cilindraje=2.5, combustible= 'GASOLINA', kilometraje= 0)
		self.assertFalse(resultado)

	def test_caso5_crear_auto_placa_y_marca_duplicados(self):
		"""test que verifica que el campo placa del auto no este duplicado"""
		resultado = self.logica.crear_auto(
			marca='volkswagen', 
			modelo=2019, 
			placa='AAA001', 
			color='azul', 
			cilindraje=1.4, 
			combustible= 'HIBRIDO', 
			kilometraje= 26000
		)
		self.assertFalse(resultado)

	def test_caso6_1_crear_auto_vacio(self):
		"""test que verifica que los campos al crear un auto no esten vacios"""
		resultado = self.logica.crear_auto(
			marca='', 
			modelo='', 
			placa='', 
			color='', 
			cilindraje='', 
			combustible= '', 
			kilometraje= ''
		)
		self.assertFalse(resultado)

	def test_caso6_2_crear_auto_vacio(self):
		"""test que verifica que los campos al crear un auto no esten vacios"""
		resultado = self.logica.crear_auto(
			marca='', 
			modelo='', 
			placa='AAA005', 
			color='', 
			cilindraje='', 
			combustible= '', 
			kilometraje= ''
		)
		self.assertFalse(resultado)

	def test_caso6_3_crear_auto_vacio(self):
		"""test que verifica que los campos al crear un auto no esten vacios"""
		resultado = self.logica.crear_auto(
			marca='', 
			modelo='', 
			placa='AAA005', 
			color='azul', 
			cilindraje='', 
			combustible= '', 
			kilometraje= ''
		)
		self.assertFalse(resultado)

	def test_caso6_4_crear_auto_vacio(self):
		"""test que verifica que los campos al crear un auto no esten vacios"""
		resultado = self.logica.crear_auto(
			marca='volkswagen', 
			modelo='', 
			placa='AAA005', 
			color='', 
			cilindraje='', 
			combustible= '', 
			kilometraje= ''
		)
		self.assertFalse(resultado)

	def test_caso7_crear_auto_campo_modelo_invalido(self):
		"""test que verifica que el campo modelo del auto sean 4 digitos"""
		resultado = self.logica.crear_auto(
			marca='nissan', 
			modelo=19995,
			placa='ABC001', 
			color='azul', 
			cilindraje=2500, 
			combustible= 'GASOLINA', 
			kilometraje= 14000
		)
		self.assertFalse(resultado)

	def test_caso8_crear_auto_campo_kilometraje_invalido(self):
		"""test que verifica que el campo kilometraje del auto sea un numero"""
		resultado = self.logica.crear_auto(
			marca='nissan', 
			modelo=1995,
			placa='ABC001', 
			color='azul', 
			cilindraje=2500, 
			combustible= 'GASOLINA', 
			kilometraje= '14000'
		)
		self.assertFalse(resultado)

	def test_caso9_crear_auto_campo_color_invalido(self):
		"""test que verifica que el campo color del auto sea un texto"""
		resultado = self.logica.crear_auto(
			marca='nissan', 
			modelo=1995,
			placa='ABC001', 
			color=123, 
			cilindraje=2500,
			combustible= 'GASOLINA', 
			kilometraje= 14000
		)
		self.assertFalse(resultado)

	def test_caso10_crear_auto_campo_clindraje_invalido(self):
		"""test que verifica que el campo cilindraje del auto sea un numero"""
		resultado = self.logica.crear_auto(
			marca='nissan', 
			modelo=1995,
			placa='ABC001', 
			color='azul', 
			cilindraje="2500",
			combustible= 'GASOLINA', 
			kilometraje= 14000
		)
		self.assertFalse(resultado)

	def test_caso11_crear_auto_campo_combustible_invalido(self):
		"""test que verifica que el campo combustible del auto sea un texto"""
		resultado = self.logica.crear_auto(
			marca='nissan', 
			modelo=1995,
			placa='ABC001', 
			color='azul', 
			cilindraje=2500,
			combustible= 123, 
			kilometraje= 14000
		)
		self.assertFalse(resultado)

	def test_caso12_1_crear_mantenimento_vacio(self):
		"""test que verifica que los campos al crear un manenimiento no esten vacios"""
		resultado = self.logica.crear_mantenimiento(
			nombre='', 
			descripcion=''
		)
		self.assertFalse(resultado)

	def test_caso12_2_crear_mantenimento_vacio(self):
		"""test que verifica que los campos al crear un manenimiento no esten vacios"""
		resultado = self.logica.crear_mantenimiento(
			nombre='Cambio de Llantas', 
			descripcion=''
		)
		self.assertFalse(resultado)

	def test_caso12_3_crear_mantenimento_vacio(self):
		"""test que verifica que los campos al crear un manenimiento no esten vacios"""
		resultado = self.logica.crear_mantenimiento(
			nombre='', 
			descripcion='Pago por nuevas llantas'
		)
		self.assertFalse(resultado)

	def test_caso13_crear_mantenimento_ya_existente(self):
		"""test que verifica que no se pueda crear un mantenimiento ya existente"""
		resultado = self.logica.crear_mantenimiento(
			nombre='Cambio de aceite', 
			descripcion='Cambio de aceite'
		)
		self.assertFalse(resultado)

	def test_caso14_mantenimiento_creado_debe_ser_visible(self):
		"""test que verifica que despues de creado un mantenimiento se vea en la lista"""
		self.logica.crear_mantenimiento(
			nombre='Cambio de Llantas', 
			descripcion='Pago por nuevas llantas'
		)
		lista = self.logica.dar_mantenimientos()
		if (lista[len(lista)-1].get('nombre') == 'Cambio de Llantas'):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_HU012_1_crear_accion(self):
		"""test que verifica que se puede agregar una accion a un auto"""
		self.logica.aniadir_accion(placa='AAA001' ,nombre= "Cambio de aceite", costo= 25000.0,fecha= "15-08-2022", kilometraje=15000)
		acciones = self.logica.dar_accion_auto(placa='AAA001')
		for accion in acciones:
			if (accion.get("costo") == 25000 and accion.get("fecha") == "15-08-2022"):
				resultado = True
				continue
			else:
				resultado = False
		self.assertTrue(resultado)

	def test_HU012_2_crear_dos_acciones(self):
		"""test que verifica que se puede agregar varias acciones a un auto"""
		found = 0
		self.logica.aniadir_accion(placa='AAA001' ,nombre= "Cambio de aceite", costo= 25000.0,fecha= "15-08-2022", kilometraje=15000)
		self.logica.aniadir_accion(placa='AAA001' ,nombre= "Cambio de Llantas", costo= 95000.0,fecha= "25-08-2022", kilometraje=150000)
		self.logica.aniadir_accion(placa='AAA001' ,nombre= "Cambio de Llantas", costo= 75000.5,fecha= "25-08-2020", kilometraje=3000)
		acciones = self.logica.dar_accion_auto(placa='AAA001')
		if(len(acciones) == 3):
			for accion in acciones:
				if (accion.get("costo") == 25000 and accion.get("fecha") == "15-08-2022"):
					found += 1
				elif (accion.get("costo") == 95000 and accion.get("fecha") == "25-08-2022"):
					found += 1
				else:
					found += 0
		self.assertEqual(found,2)

	def test_HU012_3_crear_acciones_vacias_1(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='' ,nombre='', costo= '',fecha= '', kilometraje='')
		self.assertFalse(resultado)

	def test_HU012_3_crear_acciones_vacias_2(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='', costo= '',fecha= '', kilometraje='')
		self.assertFalse(resultado)

	def test_HU012_3_crear_acciones_vacias_3(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo= '',fecha= '', kilometraje='')
		self.assertFalse(resultado)

	def test_HU012_3_crear_acciones_vacias_4(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo= 25000.9,fecha= '', kilometraje='')
		self.assertFalse(resultado)

	def test_HU012_3_crear_acciones_vacias_3(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo=25000.2 ,fecha= '25-08-2022', kilometraje='')
		self.assertFalse(resultado)

	def test_HU012_3_crear_acciones_vacias_4(self):
		"""test que verifica que no se puede agregar una accion vacia a un auto"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo=25000.9,fecha= '', kilometraje=150000)
		self.assertFalse(resultado)

	def test_HU012_4_crear_accion_costo_invalido(self):
		"""test que verifica que no se puede agregar una accion con un costo invalido"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo='25000.3',fecha='25-08-2022', kilometraje=150000)
		self.assertFalse(resultado)

	def test_HU012_5_crear_accion_kilometraje_invalido(self):
		"""test que verifica que no se puede agregar una accion con un kilometraje invalido"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo=25000.5,fecha='25-08-2022', kilometraje='150000')
		self.assertFalse(resultado)

	def test_HU012_6_crear_accion_fecha_invalido_1(self):
		"""test que verifica que no se puede agregar una accion con una fecha invalida"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo=25000.8,fecha=189750369, kilometraje=150000)
		self.assertFalse(resultado)

	def test_HU012_6_crear_accion_fecha_invalido_2(self):
		"""test que verifica que no se puede agregar una accion con una fecha invalida"""
		resultado = self.logica.aniadir_accion(placa='AAA001' ,nombre='Cambio de aceite', costo=25000.7,fecha='25-08', kilometraje=150000)
		self.assertFalse(resultado)
