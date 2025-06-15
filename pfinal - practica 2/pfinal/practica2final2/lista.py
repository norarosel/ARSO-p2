import subprocess
import sys
import logging
import pickle
import time
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#LISTA IMAGENES
def guardar_lista_imagenes(listaImagenes):
	with open("listaImagenes.dat", "wb") as fich:
		pickle.dump(listaImagenes, fich)	

def anadir_lista_imagenes(imagen,listaImagenes):
	listaImagenes.append(imagen)

def obtener_lista_imagenes():
	if os.stat('listaImagenes.dat').st_size == 0:
		print('El archivo esta vacío.')
		listaImagenes = list()
		print(listaImagenes)
	else:
		with open("listaImagenes.dat", "rb") as fich:
			listaImagenes = pickle.load(fich)
		return listaImagenes

def borrar_lista_imagenes(listaImagenes):
	listaImagenes = list()
	with open("listaImagenes.dat", "wb") as fich:
        	pickle.dump(listaImagenes, fich)


#LISTA SERVIDORES

def anadir_lista(servidor,listaServers):
	listaServers.append(servidor)
	
def guardar_lista(lista):	
	#hacer para guardar la lista
	with open("listaServidores.dat", "wb") as fich:
		pickle.dump(lista, fich)

def obtener_lista():
	if os.stat('listaServidores.dat').st_size == 0:
		print('El archivo esta vacío.')
		listaServidores = list()
		print(listaServidores)
	else:
		with open("listaServidores.dat", "rb") as fich:
			lista = pickle.load(fich)
		return lista	

def borrar_lista(listaServers):
	listaServers = list()
	with open("listaServidores.dat", "wb") as fich:
        	pickle.dump(listaServers, fich)
   #creo que esto lo borraria
def actualizar_lista(listaServers, sv):
	listaServers.remove(sv)
	with open("listaServidores.dat", "wb") as fich:
		pickle.dump(listaServers, fich)

#LISTA SERVIDORES PARADOS

def anadir_listaParados(servidor,listaParados):
	listaParados.append(servidor)

def guardar_listaParados(listaParados):
	with open("listaServidoresParados.dat", "wb") as fich:
		pickle.dump(listaParados, fich)

def obtener_listaParados():
	if os.stat('listaServidoresParados.dat').st_size == 0:
		print('El archivo esta vacío.')
		listaParados = list()
		print(listaParados)
	else:
		with open("listaServidoresParados.dat", "rb") as fich:
			listaParados = pickle.load(fich)
		return listaParados

def borrar_listaParados(listaParados):
	listaParados = list()
	with open("listaServidoresParados.dat", "wb") as fich:
        	pickle.dump(listaParados, fich)

def actualizar_listaParados(listaParados, sv):
	listaParados.remove(sv)
	with open("listaServidoresParados.dat", "wb") as fich:
		pickle.dump(listaParados, fich)

#LISTA SERVIDORES ACTIVOS 

def anadir_listaActivos(servidor,listaActivos):
	listaActivos.append(servidor)

def guardar_listaActivos(listaActivos):
	with open("listaServidoresActivos.dat", "wb") as fich:
		pickle.dump(listaActivos,fich)

def obtener_listaActivos():
	if os.stat('listaServidoresActivos.dat').st_size == 0:
		print('El archivo esta vacío.')
		listaActivos = list()
		print(listaActivos)
	else:

		with open("listaServidoresActivos.dat", "rb") as fich:
			listaActivos = pickle.load(fich)
		return listaActivos


def borrar_listaActivos(listaActivos):
	listaActivos = list()
	with open("listaServidoresActivos.dat", "wb") as fich:
        	pickle.dump(listaActivos, fich)

def actualizar_listaActivos(listaActivos, sv):
	listaActivos.remove(sv)
	with open("listaServidoresActivos.dat", "wb") as fich:
		pickle.dump(listaActivos, fich)

