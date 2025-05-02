import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 28000))
s.listen()
while True:
    new_conn = s.accept()
    print("Connection recieved from IP " + str(new_conn[1][0]))
    new_socket = new_conn[0]
    message = new_socket.recv(4096).decode("ISO-8859-1")
    # locating the request (more like hardcoding)
    request_array = message.split("\r\n")[0].split(" ")
    message_list = message.split('\n')  # checking if end
    if message_list[len(message_list) - 1] == '':
        if request_array[0] == "GET":
            # getting the file name but stripping all slashes
            file_name = request_array[1].split("/")[-1]
            print("Accessed file name is ", file_name)
            if len(file_name) > 0:
                try:
                    with open(file_name, "rb") as fp:
                        file_extension = file_name.split('.')[-1]
                        header1 = "HTTP/1.1 200 OK\r\n"
                        content_type_header = f"Content-Type: text/{file_extension}\r\n"
                        if file_extension == "txt":
                            content_type_header = "Content-Type: text/plain\r\n"
                        if file_extension == "jpg":
                            content_type_header = "Content-Type: image/jpeg\r\n"
                        data = fp.read()
                        content_length_header = f"Content-Length: {len(data)}\r\n"
                        headers = header1 + content_type_header + "\r\n"
                        new_socket.send(headers.encode())
                        new_socket.send(data)
                except:
                    new_socket.send(b"ERROR 404")
        # new_socket.send(b'Hello World')
        new_socket.close()
