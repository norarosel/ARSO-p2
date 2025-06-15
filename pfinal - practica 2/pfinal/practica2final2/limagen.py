import subprocess
import sys
import logging
import pickle
import time
import lista
import crear
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


listaImagen = lista.obtener_lista_imagenes()




if ("imagenbase" in listaImagen): 
	crear.crear_server("s1","1")
	logger.info("como ya tenemos la imagen creada, creamos un servidor a partir de ella")
else:
	crear.crearsi()
	crear.imagen()
	subprocess.call(["lxc","delete","si"])
	lista.anadir_lista_imagenes("imagenbase", listaImagen)
	lista.guardar_lista_imagenes(listaImagen)

pregunta = input("eliminar las imagenes? si o no: ")
if pregunta == "si":
	subprocess.call(["lxc", "image", "delete", "imagenbase"])
	subprocess.call(["lxc", "image", "delete", "ubuntu1804"])
	lista.borrar_lista_imagenes(listaImagen)
