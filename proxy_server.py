
import socket
from multiprocessing import Process
import threading
import sys

HOST = 'localhost'
PORT = 8001
BUFFER_SIZE = 1024
PROXY_PORT = 80

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', PORT))
        s.listen()


        while True:
             try:
                conn, addr = s.accept()
                data_from_client = conn.recv(BUFFER_SIZE)
                data_from_client = data_from_client.decode()
         
                remote_ip = get_remote_ip(data_from_client.split('\r\n')[1].split(' ')[1])
 
                proxy_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                proxy_s.connect((remote_ip, PROXY_PORT))
                p = threading.Thread(target=send_data, args=(proxy_s, conn, data_from_client), daemon = True)
                
                p.start()

                
                 
             except Exception as e:
                print(e)
                
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()

def send_data(proxy_s, conn, data_from_client):
     proxy_s.sendall(data_from_client.encode())
     proxy_s.shutdown(socket.SHUT_WR)
     data = proxy_s.recv(BUFFER_SIZE)
     conn.send(data)
if __name__ == "__main__":
    main()


