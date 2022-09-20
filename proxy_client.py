import socket
 
def main():
    try:
        #define address info, payload, and buffer size
        host = 'localhost'
        remote_ip = '127.0.0.1'
        port = 8001
        payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
        buffer_size = 4096

        #make the socket, get the ip, and connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((remote_ip , port))

        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #send the data and shutdown
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        full_data = s.recv(buffer_size)
         
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
if __name__ == "__main__":
    main()

