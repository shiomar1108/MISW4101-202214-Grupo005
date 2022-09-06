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
		resultado = self.logica.crear_auto(marca='renault', modelo=1995, placa='XXX003', color='negro', cilindraje=1.6, combustible= 'GASOLINA PREMIUM', kilomentraje= 1000 )
		self.assertTrue(resultado)

	def test_crear_auto_ya_creado(self):
		resultado = self.logica.crear_auto(marca='volkswagen', modelo=2016, placa='XXX001', color='gris', cilindraje=2.5, combustible= 'GASOLINA', kilomentraje= 0)
		self.assertFalse(resultado)

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
			if(temp.get('modelo') == '2019' and temp.get('color') == "Negro"):
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

	def test_aniadir_accion(self):
		descripcion = 'se agrego el filtro X de mejor marca' 
		resultado = self.logica.aniadir_accion(
			placa= 'XXX001', 
			descripcion=descripcion,
			kilometraje= 25000, 
			costo= 5820, 
			fecha= '11-01-2021'
		)

		self.assertEqual(resultado.descripcion, descripcion)