import subprocess
import sys
import logging
import pickle
import time
import lista
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




def arranca_maquina():
	logger.info("No especificar el numero de servidores que se quiere arrancar, únicamente se debe mandar la orden 'arrancar'. A continuacion se podra decidir si se desea arrancar un servidor determinado. En caso contrario, se arrancaran los servidores que estaban creados.")
	listaParados = lista.obtener_listaParados()
	listaActivos = lista.obtener_listaActivos()
	listaServers = lista.obtener_lista()
	orden = input("¿Desea arrancar un servidor en especifico? Y/N: ")
	logger.info("La lista de servidores parados es la siguiente: "+str(listaParados))
	if (orden == "N"):
		
		subprocess.call(["lxc","start","cl"])
		logger.info("No se desea arrancar un servidor especifico, asi que se arrancaran los ya creados")
		for i in listaParados:
			maquinaVirtual=str(i)
			subprocess.call(["lxc", "start", maquinaVirtual])
			subprocess.call(["lxc", "exec", maquinaVirtual, "--", "forever", "start", "app/rest_server.js"])
			time.sleep(5)
			orden = "lxc exec " +maquinaVirtual+ " bash"
			subprocess.Popen(["xterm","-fa","monaco","-fs","13","-bg","black","-fg","green","-e", orden])
			logger.info("La maquina " +maquinaVirtual+ " se ha arrancado")
			lista.anadir_listaActivos(maquinaVirtual, listaActivos)

		subprocess.call(["lxc","restart","lb"])
		time.sleep(3)
		subprocess.call(["lxc","exec","lb", "--","service", "haproxy", "start"])
		time.sleep(2)
		logger.info("Iniciado haproxy")
		subprocess.call(["lxc", "restart", "lb"])	
		lista.guardar_listaActivos(listaActivos)
		lista.borrar_listaParados(listaParados)
		time.sleep(5)	
		logger.info("Todas las maquinas se han arrancado")
		logger.info("Lista de servidores creados: ") 
		logger.info(listaServers)
		logger.info("Lista de servidores activos: ")
		logger.info(listaActivos)

	elif(orden == "Y"):
		logger.info("Se desea arrancar un servidor en concreto, a continuacion se indica cual")
		servidor = input("Seleccione el servidor que desea arrancar, junto con el lb y el cl: ")
		
		subprocess.call(["lxc","start","cl"])
		sv = str(servidor)
		if (sv in listaActivos):
			logger.warning("El servidor ya se encuentra activo, pruebe con otro")
		else: 
			subprocess.call(["lxc", "start", servidor])
			subprocess.call(["lxc", "exec", servidor, "--", "forever", "start", "app/rest_server.js"])
			time.sleep(5)
			orden = "lxc exec " + servidor + " bash"
			subprocess.Popen(["xterm", "-fa","monaco","-fs", "13", "-bg", "black", "-fg", "green", "-e", orden])
			logger.info(listaActivos)
			logger.info("La maquina " + servidor + " se ha arrancado")
			lista.anadir_listaActivos(servidor, listaActivos)
			lista.actualizar_listaParados(listaParados, servidor)
		subprocess.call(["lxc","restart","lb"])
		time.sleep(3)
		subprocess.call(["lxc","exec","lb", "--","service", "haproxy", "start"])
		time.sleep(2)
		logger.info("Iniciado haproxy")
		subprocess.call(["lxc", "restart", "lb"])
		lista.guardar_listaActivos(listaActivos)
		time.sleep(5)	
		logger.info("Todas las maquinas indicadas se han arrancado")
		logger.info("Lista de servidores creados: ") 
		logger.info(listaServers)
		logger.info("Lista de servidores activos: ")
		logger.info(listaActivos)


