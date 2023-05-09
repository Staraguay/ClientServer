import socket
import threading
from ClientProxy import conection_web


def Proxy_Server(client_Socket, addr):
    client_request = client_Socket.recv(1024)  # se reciben los 1024 bytes del socket

    if client_request:

        request_length = len(client_request)
        message = "El tamaño de la solicitud del cliente con puerto: " + str(addr[1]) + " es " + str(request_length) + " bytes \n"
        print(message)
        message = "Cliente con el puerto: " + str(addr[1]) + " genero una solicitud: " + str(client_request).splitlines()[
            0] + " \n"
        print(message)

        client_request2 = str(client_request)
        resp_part = client_request2.split(' ')[0]

        if resp_part:

            http_part = str(client_request).split(' ')[1]
            double_slash_pos = http_part.find(
                "//")  # se elimina la parte http para obtener solo la URL y eliminar el seguimiento / de la solicitud
            url_connect = ""
            url_slash_check = list()
            url_slash = str()
            if double_slash_pos == -1:  # se verifica si no hay parte http en la url
                url_part = http_part[0:]
                url_connect = url_part.split('/')[0]  # getting the www.abc.com part
            else:

                if http_part.split('//')[1][-1] == "/":  # se elimina "/"
                    url_part = http_part.split('//')[1][:-1]
                    url_connect = url_part.split('/')[0]  # se obtiene solo la URL, ej: www.abc.com
                else:
                    url_part = http_part.split('//')[1]
                    url_connect = url_part.split('/')[0]

            url_slash_check = url_part.split('/')[1:]  # se obtiene la parte después del anfitrión host
            url_slash = ""
            if url_slash_check:
                for path in url_slash_check:
                    url_slash += "/"
                    url_slash += path

            print(url_slash)
            client_request_port_start = str(url_part).find(":")  # se comprueba si se proporciona el número de puerto
            port_number = 80  # puerto dado por defecto en el protocolo HTTP
            url_file_name = url_part.replace('[^0-9a-zA-Z]+',
                                             '_')  # se reemplazan todos los caracteres alfanuméricos por "_"
            url_file_name = url_file_name.replace("/", "_")
            if client_request_port_start == -1:
                pass
            else:
                port_number = int(url_part.split(':')[1])
                url_connect = url_connect.split(':')[0]

            conection_web(url_file_name, url_connect, port_number, client_request, addr, client_Socket)

        else:
            # Comprobacion en caso de que el cliente envíe una solicitud no válida
            message = "El cliente con el puerto: " + str(addr[1]) + " genero una solicitud invalida.: " + str(
                resp_part) + " \n"
            client_Socket.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            client_Socket.close()
            print(message)
            message = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            print(message)
    else:
        client_Socket.send(b"")
        client_Socket.close()
        message = "Cliente con puerto: " + str(addr[1]) + " ha cerrado exitosamente la conexion. \n"
        print(message)


def listen_client():
    while True:
        Cli_Sock, addr = Serv_Sock.accept()  # Se acepta la conexión del cliente

        print('Conexion recibida de: ', addr)

        d = threading.Thread(name=str(addr), target=Proxy_Server, args=(Cli_Sock, addr))
        d.setDaemon(True)
        d.start()

    Serv_Sock.close()


if __name__ == '__main__':
    # Socket de servidor creado, vinculado y listo para recibir conexiones
    Serv_Port = 8080
    Serv_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # se crea el socket.

    print("Arrancando el servidor ....")
    Serv_Sock.bind(('', Serv_Port))
    Serv_Sock.listen(1)
    print("Esperando conexiones...")
    listen_client()
    Serv_Sock.close()
