import subprocess
import sys
import logging
import pickle
import time
import lista
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def para_maquina():
	arg2 = sys.argv[2]
	listaServers = lista.obtener_lista()	
	listaParados = lista.obtener_listaParados()
	listaActivos = lista.obtener_listaActivos()
	logger.info("Para parar todos los servidores, se debera especificar 'parar todo'. Si se quiere parar uno en concreto, se debera indicar 'parar x' siendo x un caracter cualquiera y a continuacion se elegira el nombre del servidor que se quiera parar")
	if arg2 == "todo":
		for i in listaActivos:
			maquinaVirtual=str(i)
			subprocess.call(["lxc","stop", maquinaVirtual])
			logger.info("maquina " + maquinaVirtual + " parada" )
			lista.anadir_listaParados(i, listaParados)
			


		lista.borrar_listaActivos(listaActivos)
		lista.guardar_listaParados(listaParados)
		subprocess.call(["lxc","stop","cl"])
		time.sleep(5)
		logger.info("Lista de servidores creados: ") 
		logger.info(listaServers)
		logger.info("Lista de servidores parados: ")			
		logger.info(listaParados)
	

	else:
		logger.info("La lista de servidores activos es la siguiente: "+str(listaActivos))
		servidor = input("Nombre del servidor a parar: ")

		sv = str(servidor)
		
		if(sv=="lb"):
			logger.warning("El balanceador no se puede parar") 
		elif(sv=="cl"):
			subprocess.call(["lxc", "stop", str(servidor)])
		elif(sv=="db"):
			logger.warning("El contenedor db no se puede parar")

		else:
			if(sv in listaParados):
				logger.warning("Este servidor ya está parado, pruebe con otro")
			else:

				for i in listaServers:
					if (i == sv):
						subprocess.call(["lxc", "stop", sv])
						logger.info("La maquina " +str(servidor)+ " ya esta parada")
						lista.anadir_listaParados(sv,listaParados)
						lista.actualizar_listaActivos(listaActivos, i)
				lista.guardar_listaParados(listaParados)
			time.sleep(5)
			logger.info("Lista de servidores creados: ") 
			logger.info(listaServers)
			logger.info("Lista de servidores parados: ")			
			logger.info(listaParados)
			
		
	subprocess.call(["lxc", "list"])

