from http.server import HTTPServer
import backend.router as router

def run(server_class = HTTPServer, handler_class = router.SimpleHTTPRequestHandler):
    server_address = ("", 8024)
    httpd = server_class(server_address, handler_class)
    print('server is running in 8024....')
    httpd.serve_forever()


if __name__ == '__main__':
    run()