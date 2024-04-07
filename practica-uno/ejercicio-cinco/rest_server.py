from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "Leon",
        "especie": "Panthera leo",
        "genero": "Macho",
        "edad": 5,
        "peso": 180,
    }
]

class ZooService:
    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )

    @staticmethod
    def filter_animals_by_species(especie):
        return [
            animal for animal in animales if animal["especie"] == especie
        ]

    @staticmethod
    def filter_animals_by_gender(genero):
        return [
            animal for animal in animales if animal["genero"] == genero
        ]

    @staticmethod
    def update_animal(id, data):
        animal = ZooService.find_animal(id)
        if animal:
            animal.update(data)
            return animales
        else:
            return None

    @staticmethod
    def delete_animal(id):
        animal = ZooService.find_animal(id)
        if animal:
            animales.remove(animal)
            return animales
        else:
            return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def handle_error_response(self):
        HTTPResponseHandler.handle_response(
            self, 404, {"Error": "Ruta no existente"}
        )

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = ZooService.filter_animals_by_species(
                    especie
                )
                if animales_filtrados:
                    HTTPResponseHandler.handle_response(
                        self, 200, animales_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = ZooService.filter_animals_by_gender(
                    genero
                )
                if animales_filtrados:
                    HTTPResponseHandler.handle_response(
                        self, 200, animales_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, animales)
        elif parsed_path.path.startswith("/animales/"):
            id = int(parsed_path.path.split("/")[-1])
            animal = ZooService.find_animal(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, [animal])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            self.handle_error_response()

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            nuevo_animal = {
                "id": len(animales) + 1,
                **data
            }
            animales.append(nuevo_animal)
            HTTPResponseHandler.handle_response(self, 201, nuevo_animal)
        else:
            self.handle_error_response()

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animales = ZooService.update_animal(id, data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                self.handle_error_response()
        else:
            self.handle_error_response()

    def do_DELETE(self):
        if self.path.startswith("/animales/") and len(self.path.split("/")) == 3:
            id = int(self.path.split("/")[-1])
            animales = ZooService.delete_animal(id)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                self.handle_error_response()
        else:
            self.handle_error_response()

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
