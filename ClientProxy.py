import datetime
import socket


def conection_web(url_file_name, url_connect, port_number, data, addr, client_Socket):
    try:
        cached_file = open("cache/" + url_file_name, "r")  # se obtiene el archivo en caché para la url si existe
        time_control = cached_file.readline()
        day_control = time_control.split(" ")[0]
        hour_control = time_control.split(" ")[1]

        day_expired = 1  # límite de días para usar la cache
        hour_expired = 2  # límite de horas para usar la cache
        minute_expired = 5  # límite de minutos para usar la cache

        time_control = time_control.replace("\n", "")
        hora = datetime.datetime.strptime(time_control, '%Y-%m-%d %H:%M:%S')

        if hora + datetime.timedelta(minutes=minute_expired) < datetime.datetime.now():
            c = open("imaginario.txt", "r")
            # línea para producir excepción y saltar a excepto bloquear e ignorar el archivo de caché para hacer un
            # hit al servidor web

        else:

            # aqui se lee  el contenido de los archivos guardados en cache
            message = "El cliente con el puerto: " + str(addr[0]) + ": Cache hit" \
                                                                    "  Recuperando informacion desde la caché. \n"
            print(message)

            # se lee los datos línea por línea y se los agrega
            f = open("cache/" + url_file_name, "r")
            l = f.read()
            l = l.split("\n")[1]



            cached_file.close()  # se cierra el file handler
            sendMessage = l.encode('ASCII')  # Se envia los datos en caché
            client_Socket.send(sendMessage)
            print('Datos cargados con éxito.')
            print("--------------------------------------------------------------------------------------------------")
            print("")


    except:

        message = "El cliente con el puerto: " + str(addr[0]) + " Cache miss" \
                                                                " No existe caché para la página solicitada, regresando al servidor web orignal \n"
        print(message)

        try:
            # creacion del socket para el servidor proxy
            proxy_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except Exception as e:
            print('No se pudo crear el socket. Error: %s' % e)

        try:
            # conexión a la url especificada por el cliente
            print(url_connect, port_number)
            proxy_connection_socket.connect((url_connect, port_number))

            print("Conectando con el servidor ")
            proxy_connection_socket.send(data)
            message = "El cliente con el puerto: " + str(
                addr) + " Solicita el tamaño " + "al web server de " + str(len(data)) + " bytes \n"
            print(message)
            message = "El cliente con el puerto: " + str(
                addr) + " generó una solicitud " + " al servidor web como: " + str(
                data) + " \n"
            print(message)

            R = '\033[31m'  # red
            G = '\033[32m'  # green
            C = '\033[36m'  # cyan
            W = '\033[0m'  # white
            M = '\033[34m'  # morado

            web_server_response_append = ""
            while True:
                reply = proxy_connection_socket.recv(1024000)

                if len(reply) > 0:
                    client_Socket.send(reply)
                    web_server_response_append += str(reply)
                    print(M + "Respuesta del servidor web: ")
                    print()
                    print(R + str(reply))  # se especifica la hora y fecha de conexion
                    print(G + web_server_response_append)
                    print()
                    dar = float(len(reply))
                    dar = float(dar / 1024)
                    dar = "{}.3s".format(dar)
                    print("[*] Solicitud aceptada: {} => {} => {}".format(addr, dar, url_connect))

                else:
                    print("No se recibieron datos.")

                    break

            # se almacena la respuesta en el servidor proxy
            proxy_temp_file = open("cache/" + url_file_name, "w")

            # se escribern todas la respuestas al archivo
            web_server_response_appendSTR = str(web_server_response_append)
            web_server_response_appendSTR = web_server_response_appendSTR.replace("'", "")
            web_server_response_appendSTR = web_server_response_appendSTR[1:]
            x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            proxy_temp_file.write(str(x))
            proxy_temp_file.write("\n")

            for line in web_server_response_appendSTR:
                proxy_temp_file.write(line)

            proxy_temp_file.close()
            proxy_connection_socket.close()
            client_Socket.close()

        except Exception as e:
            print(e)
            proxy_connection_socket.close()
            client_Socket.close()
