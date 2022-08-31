import unittest

from src.logica.Logica_real import Logica_real
from src.modelo.conn import Session
from src.modelo.auto import Auto, Combustible

#Clase de ejemplo, debe tener un nombre que termina con el sufijo TestCase, y conservar la herencia
class ModeloTestCase(unittest.TestCase):

	#Instancia el atributo logica para cada prueba
	def setUp(self):
		self.logica = Logica_real()
		self.session = Session()

		self.auto1 = Auto(marca = 'volkswagen', modelo = 2016, placa = 'XXX001', color = 'gris', cilindraje = 2.5, combustible=Combustible.GASOLINA)

		self.session.add(self.auto1)

		self.session.commit()
		self.session.close()


	def tearDown(self):
		'''Abre la sesión'''
		self.session = Session()

		'''Consulta todos los álbumes'''
		busqueda = self.session.query(Auto).all()

		'''Borra todos los álbumes'''
		for auto in busqueda:
			self.session.delete(auto)

		self.session.commit()
		self.session.close()


	def test_crear_auto(self):
		resultado = self.logica.crear_auto(marca='renault', modelo=1995, placa='XXX003', color='negro', cilindraje=1.6, combustible=Combustible.GASOLINA)
		self.assertTrue(resultado)

	def test_crear_auto_ya_creado(self):
		resultado = self.logica.crear_auto(marca='volkswagen', modelo=2016, placa='XXX001', color='gris', cilindraje=2.5, combustible=Combustible.GASOLINA)
		self.assertFalse(resultado)