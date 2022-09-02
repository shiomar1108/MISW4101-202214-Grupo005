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
		self.manto1 = Mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')
		self.accion1 = Accion(
			kilometraje=15000, 
			costo=9600, 
			fecha='01/09/2022',
			mantenimiento = [self.manto1] ,
		)

		self.session.add(self.auto1)
		self.session.add(self.manto1)
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
		if(temp.placa == 'XXX001'):
			resultado = True
		else:
			resultado = False
		self.assertTrue(resultado)

	def test_crear_mantenimiento(self):
		resultado = self.logica.crear_mantenimiento(nombre='Polarizado', descripcion='Pago por colocacion de Polarizado en Ventana')
		self.assertTrue(resultado)

	def test_crear_mantenimiento_ya_creado(self):
		resultado = self.logica.crear_mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')
		self.assertFalse(resultado)

	def test_dar_mantenimiento(self):
		temp = self.logica.dar_mantenimiento(nombre= self.manto1.nombre)
		if(temp.nombre == self.manto1.nombre and temp.descripcion == self.manto1.descripcion):
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