import http.server # Parametrages : localisation, handler
import socketserver # Ecoute

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
       print("hello")
       self.send_response(200)
       self.send_header('content-type','text/plain')
       self.end_headers()
       self.wfile.write("hello".encode('utf-8'))

MyAPIHandler = APIHandler

# socketserver
try:   
    with socketserver.TCPServer(("",8082), MyAPIHandler) as httpd:
     print("Server working")
     httpd.allow_reuse_address = True
     httpd.serve_forever()

except KeyboardInterrupt:
     print("Stopping server")
     httpd.server_close()