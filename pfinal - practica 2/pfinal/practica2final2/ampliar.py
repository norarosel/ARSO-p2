import subprocess
import sys
import logging
import pickle
import time
import lista
import os
import crear
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def ampliar():

	subprocess.call(["lxc","network","delete","lxdbr0"])	
	for i in range(2):
		logger.info("creamos redes virtuales")
		bridge = "lxdbr"+str(i)
		red = "10.0."+str(i)+".1/24"
		subprocess.call(["lxc", "network", "create", bridge, "ipv6.address=none", "ipv6.nat=false", "ipv4.address="+red, "ipv4.nat=true"])
		

	while True:
			nser = input("¿cuántos servidores desea crear? ")
			#prueba si es un numero entero
			if(nser == "ninguno"):
				break
			try:
				nser = int(nser)
			except:
				logger.error("El valor introducido no es valido, introduzca un número entero")
				continue
			listaServers = lista.obtener_lista()
			listaParados = lista.obtener_listaParados()
			listaImagen = lista.obtener_lista_imagenes()
			listaActivos = lista.obtener_listaActivos()
			ns_lista = len(listaServers)
			logger.info("Ya hay " + str(ns_lista) + " creados.")
			f = ns_lista+int(nser)
			inicio = int(ns_lista) + int(1)
			final = int(f) + int(1)
			

			if ("imagenbase" in listaImagen): 
				for i in range(inicio, final):
					server = "s"+str(i)
					numser = str(i)
					if (server in listaServers):
						logger.warning("el servidor "+ server+" que quiere crear ya esta creado, prueba otro")
					else:
						crear.crear_server(server,numser)
						lista.anadir_lista(server,listaServers)
						lista.anadir_listaParados(server, listaParados)
			else:
				crear.crearsi()
				crear.crear_db()
				subprocess.call(["lxc","start","si"])	
				time.sleep(3)
				crear.crearNodes1()
				crear.imagen()
				subprocess.call(["lxc","delete","si"])
				lista.anadir_lista_imagenes("imagenbase", listaImagen)
				lista.guardar_lista_imagenes(listaImagen)
				for i in range(inicio, final):
					server = "s"+str(i)
					numser = str(i)
					if (server in listaServers):
						logger.warning("el servidor "+ server+" que quiere crear ya esta creado, prueba otro")	
					else:
						crear.crear_server(server,numser)
						lista.anadir_lista(server,listaServers)
						lista.anadir_listaParados(server, listaParados)

			
			hr = open("haproxybase.cfg","r")
			lineas = hr.readlines()
			hr.close()
			hw = open("haproxy.cfg", "w")
			for i in lineas:
				hw.write(i)
			hw.close()
			ha = open("haproxy.cfg","a")
				
			if i == ("        option httpchk" + "\n"):
				for i in range(0,len(listaServers)):
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
				for i in range(0, len(listaServers)):										
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
			else:
				for i in range(0,len(listaServers)):
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
				for i in range(0, len(listaServers)):										
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
				ha.write("        option httpchk" + "\n")
			ha.close()
			subprocess.call(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
			time.sleep(10)
			subprocess.call(["lxc","restart","lb"])
			logger.info("Se ha metido el fichero")
			time.sleep(3)
			subprocess.call(["lxc","exec","lb", "--","service", "haproxy", "start"])
			time.sleep(2)
			logger.info("Iniciado haproxy")
			subprocess.call(["lxc", "restart", "lb"])

			
			lista.guardar_lista(listaServers)
			lista.guardar_listaActivos(listaActivos)
			lista.guardar_listaParados(listaParados)
			
			logger.info("Lista de servidores creados: ") 
			logger.info(listaServers)
			logger.info("Lista de servidores parados: ")			
			logger.info(listaParados)
			logger.info("Lista de servidores activos: ")
			logger.info(listaActivos)	
