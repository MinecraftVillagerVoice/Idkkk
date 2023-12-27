from http.server import HTTPServer, BaseHTTPRequestHandler
import os

UPLOAD_FOLDER = 'uploads'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/download/'):
            file_name = self.path.split('/')[-1]
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Page not found')

    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            uploaded_file = self.rfile.read(content_length)
            file_name = self.headers['Content-Disposition'].split('=')[-1]
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            with open(file_path, 'wb') as file:
                file.write(uploaded_file)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Page not found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    run()
