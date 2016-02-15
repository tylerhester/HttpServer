from socket import *
import os
import time

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


class Server:

    # Used to store the request headers and response information
    request_headers = []

    # Initalization method
    def __init__(self):
        pass

    # Method to retreive the contents of an image file and pass it along to the caller
    def retreive_file(self, filename):
        file = open(filename, 'rb')
        contents = file.read()
        file.close()
        return contents

    def check_malformations(self, request):
        pass

    def generate_response_headers(self, code, status, file_name, file_type):
        response_headers = 'HTTP/1.1 ' + str(code) + ' ' + status + '\r\n'
        response_headers += 'Date: ' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.gmtime()) + '\r\n'
        response_headers += 'Server: GiveMeAnAPlease\r\n'
        response_headers += 'Accept-Ranges: bytes\r\n'

        if not (code == 404):
            response_headers += 'Content-Length: ' + str(os.path.getsize(os.getcwd()+'\\'+file_name+'.'+file_type)) + ' \r\n'

        if file_type == 'html' or file_type == 'htm':
            response_headers += 'Content-Type: text/html\r\n'
        elif file_type == 'txt':
            response_headers += 'Content-Type: text/plain\r\n'
        elif file_type == 'jpeg' or file_type == 'jpg':
            response_headers += 'Content-Type: image/jpeg\r\n'

        response_headers += '\r\n'
        return response_headers.encode()

    # Method to parse the information from the broswer or client programs request
    def decode_request(self, request):
        # Temp. store the data
        data = None

        self.check_malformations(request)

        # Break up the request_headers
        self.request_headers = request.split('\r\n')

        # Check the first line of the headers
        request_type = self.request_headers[0].split(' ')

        # Ensure that the request type is supported (hence only GETs)
        if not (request_type[0] == 'GET'):
            return self.generate_response_headers(500, 'Unsupported functionality', '', '')

        # Parse out the file name and type
        if request_type[1].startswith('/'):
            file_name, file_type = (request_type[1])[1:].split('.')
        else:
            file_name, file_type = request_type[1].split('.')

        # Catch supported file types
        if str(file_type).lower() == 'html' or str(file_type).lower() == 'htm':
            data = self.retreive_file(file_name + '.' + file_type)

        elif str(file_type).lower() == 'txt':
            data = self.retreive_file(file_name + '.' + file_type)

        elif str(file_type).lower() == 'jpg' or str(file_type).lower() == 'jpeg':
            data = self.retreive_file(file_name + '.' + file_type)

        else:
            print('File type not supported / File not found')
            return self.generate_response_headers(404, 'File Not Found', file_name, file_type)


        data = self.generate_response_headers(200, 'OK', file_name, file_type) + data
        return data

    # Main method contains busy wait loop
    def main(self):
        while 1:
            client_socket, address = serverSocket.accept()
            request = client_socket.recv(8192)
            request = bytes.decode(request)

            data = self.decode_request(request)

            client_socket.send(data)
            client_socket.close()

if __name__ == '__main__':
    server = Server()
    server.main()
