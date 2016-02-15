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

    # Method to retreive the contents of an html file and pass it along to the caller
    def send_html_file(self, filename):
        contents = ''
        with open(filename, 'r') as f:
            line = f.read()
            contents += line
        f.close()
        return contents

    # Method to retreive the contents of an image file and pass it along to the caller
    def send_image_file(self, filename):
        contents = ''
        with open(filename, 'rb') as f:
            line = f.read()
        f.close()
        return contents

    # Method to retrieve the contents of a text file and pass it along to the caller
    def send_text_file(self, filename):
        contents = ''
        with open(filename, 'r') as f:
            line = f.read()
            contents += line
        f.close()
        return contents

    def generate_response_headers(self, code):
        response_headers = 'HTTP/1.1 200 OK\r\n'
        response_headers += 'Date: ' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.gmtime()) + '\r\n'
        response_headers += 'Server: GiveMeAnAPlease\r\n'
        response_headers += 'Accept-Ranges: bytes\r\n'
        response_headers += 'Content-Length:' + str(os.path.getsize(os.getcwd()+'/test.html')) + ' \r\n'
        response_headers += 'Content-Type: text/html\r\n'
        response_headers += '\r\n'
        return response_headers

    # Method to parse the information from the broswer or client programs request
    def decode_request(self, request):
        # Temp. store the data
        data = ''

        # Break up the request_headers
        self.request_headers = request.split('\r\n')

        # Check the first line of the headers
        request_type = self.request_headers[0].split(' ')

        # Ensure that the request type is supported (hence only GETs)
        if not (request_type[0] == 'GET'):
            print('Request Type Unsupported', request_type[0])
            return None

        # Parse out the file name and type
        file_name, file_type = (request_type[1])[1:].split('.')

        # Catch supported file types
        if str(file_type).lower() == 'html' or str(file_type).lower() == 'htm':
            data += self.send_html_file(file_name + '.' + file_type)

        elif str(file_type).lower() == 'txt':
            data += self.send_text_file(file_name + '.' + file_type)

        elif str(file_type).lower() == 'jpg' or str(file_type).lower() == 'jpeg':
            data += self.send_image_file(file_name + '.' + file_type)

        else:
            print('File type not supported / File not found')

        # Retrieve other information from the headers, may need to be relocated
        for headerline in self.request_headers[1:]:
            pass

        return data

    # Main method contains busy wait loop
    def main(self):
        while 1:
            client_socket, address = serverSocket.accept()
            request = client_socket.recv(8192)
            request = bytes.decode(request)

            data = self.decode_request(request)

            client_socket.send(self.generate_response_headers(200).encode() + data.encode())
            client_socket.close()

if __name__ == '__main__':
    server = Server()
    server.main()
