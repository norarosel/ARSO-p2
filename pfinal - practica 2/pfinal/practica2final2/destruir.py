import subprocess
import sys
import logging
import pickle
import time
import lista
import os
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def destruir():
	listaServers = lista.obtener_lista()	
	listaParados = lista.obtener_listaParados()
	listaActivos = lista.obtener_listaActivos()
	arg2 = sys.argv[2]
	logger.info("Para destruir todos los servidores, se debera especificar 'destruir todo'. Si se quiere destruir uno en concreto, indicar 'destruir x', siendo x un caracter cualquiera y a continuacion se elegira el nombre del servidor que se quiera destruir")
	if arg2 == "todo":

		for i in listaServers:
			maquinaVirtual=str(i)
			subprocess.call(["lxc","stop",maquinaVirtual])
			subprocess.call(["lxc","delete",maquinaVirtual])
			logger.info("La máquina "+maquinaVirtual+" virtual se han borrado")
		subprocess.call(["lxc","stop","lb"])
		subprocess.call(["lxc","stop","db"])
		subprocess.call(["lxc","stop","cl"])		
		subprocess.call(["lxc","delete","lb"])
		subprocess.call(["lxc","delete","db"])
		subprocess.call(["lxc","delete","cl"])
		subprocess.call(["lxc","network","delete","lxdbr0"])
		subprocess.call(["lxc","network","delete","lxdbr1"])
		lista.borrar_lista(listaServers)
		lista.borrar_listaParados(listaParados)
		lista.borrar_listaActivos(listaActivos)
		for i in range(2):		
			time.sleep(10)
			hr = open("haproxybase.cfg","r")
			lineas = hr.readlines()
			hr.close()
			hw = open("haproxy.cfg", "w")
			for i in lineas:
				hw.write(i)
			hw.close()
			ha = open("haproxy.cfg","a")
			for i in range(0,len(listaServers)):
				ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
				time.sleep(5)
			for i in range(0, len(listaServers)):										
				ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
				time.sleep(5)
			ha.write("        option httpchk" + "\n")
			time.sleep(5)
			ha.close()
			time.sleep(5)

		pregunta = input("¿Desea eliminar la imagen de los servidores? si o no: ")
		if pregunta == "si":
			
			subprocess.call(["lxc", "image", "delete", "imagenbase"])
			lista.borrar_lista_imagenes(lista.obtener_lista_imagenes())
		elif pregunta == "no":
			logger.info("no se ha eliminado")

		logger.info("Todos los elementos se han destruido")
		
	else:
		logger.info("La lista de servidores es la siguiente: "+str(listaServers))
		servidor = input("Nombre del elemento a borrar: ")

		if(str(servidor) in listaServers):

			subprocess.call(["lxc","stop",servidor])
			subprocess.call(["lxc","delete",servidor])
			logger.info("Máquina " + str(servidor) + " destruida" )
			lista.actualizar_lista(listaServers, servidor)
			for i in range(2):			
				time.sleep(5)
				hr = open("haproxybase.cfg","r")
				lineas = hr.readlines()
				hr.close()
				hw = open("haproxy.cfg", "w")
				for i in lineas:
					hw.write(i)
				hw.close()
				ha = open("haproxy.cfg","a")
				for i in range(0,len(listaServers)):
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001" + "\n")
					time.sleep(5)
				for i in range(0, len(listaServers)):										
					ha.write("        server webserver" + str(i+1) + " " + listaServers[i] + ":8001 " + "check" + "\n")
					time.sleep(5)
				ha.write("        option httpchk" + "\n")
				time.sleep(5)
				ha.close()	  
			for i in listaParados:
				if i == servidor:
					lista.actualizar_listaParados(listaParados, i)
				else:
					logger.info("-")
			for i in listaActivos:
				if i == servidor:
					lista.actualizar_listaActivos(listaActivos, i)
				else:
					logger.info("-")
			
			
		elif(str(servidor)=="lb"):
			subprocess.call(["lxc", "stop", str(servidor)])
			subprocess.call(["lxc", "delete", str(servidor)])
			logger.info("Balanceador de carga destruido" )
		elif(str(servidor)=="db"):
			subprocess.call(["lxc", "stop", str(servidor)])
			subprocess.call(["lxc", "delete", str(servidor)])
			logger.info("Contenedor db destruido" )
		elif(str(servidor)=="cl"):
			subprocess.call(["lxc", "stop", str(servidor)])
			subprocess.call(["lxc", "delete", str(servidor)])
			logger.info("Cliente destruido")
		elif(str(servidor)=="lxdbr0"):
			subprocess.call(["lxc", "stop", str(servidor)])
			subprocess.call(["lxc", "delete", str(servidor)])
			logger.info("lxdbr0 destruido")
		elif(str(servidor)=="lxdbr1"):
			subprocess.call(["lxc", "stop", str(servidor)])
			subprocess.call(["lxc", "delete", str(servidor)])
			logger.info("lxdbr1 destruido")
		time.sleep(5)
		
		pregunta = input("¿Desea eliminar la imagen de los servidores? si o no: ")
		if pregunta == "si":
			
			subprocess.call(["lxc", "image", "delete", "imagenbase"])
			lista.borrar_lista_imagenes(lista.obtener_lista_imagenes())
			subprocess.call(["lxc","image", "list"])
		elif pregunta == "no":
			logger.info("no se ha eliminado")
			subprocess.call(["lxc","image", "list"])
		pregunta2 = input("¿Desea eliminar la imagen del db remoto? si o no: ")
		if pregunta2 == "si":
			
			subprocess.call(["lxc", "image", "delete", "imagendbrem"])
			subprocess.call(["lxc","image", "list"])
		elif pregunta2 == "no":
			logger.info("no se ha eliminado")
			subprocess.call(["lxc","image", "list"])

		logger.info("Todos los elementos se han destruido")
	subprocess.call(["lxc", "list"])
	
