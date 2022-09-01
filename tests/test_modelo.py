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

		self.auto1 = Auto(marca = 'volkswagen', modelo = 2016, placa = 'XXX001', color = 'gris', cilindraje = 2.5, combustible= 'GASOLINA' )
		self.manto1 = Mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')

		self.session.add(self.auto1)
		self.session.add(self.manto1)

		self.session.commit()
		self.session.close()


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


	def test_crear_auto(self):
		resultado = self.logica.crear_auto(marca='renault', modelo=1995, placa='XXX003', color='negro', cilindraje=1.6, combustible= 'GASOL')
		self.assertTrue(resultado)

	def test_crear_auto_ya_creado(self):
		resultado = self.logica.crear_auto(marca='volkswagen', modelo=2016, placa='XXX001', color='gris', cilindraje=2.5, combustible= 'GASOLINA')
		self.assertFalse(resultado)

	def test_crear_mantenimiento(self):
		resultado = self.logica.crear_mantenimiento(nombre='Polarizado', descripcion='Pago por colocacion de Polarizado en Ventana')
		self.assertTrue(resultado)

	def test_crear_mantenimiento_ya_creado(self):
		resultado = self.logica.crear_mantenimiento(nombre='Cambio de Filtro', descripcion='Pago por nuevo filtro de gasolina')
		self.assertFalse(resultado)
