from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class PacienteBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.paciente = {}

    def set_CI(self, CI):
        self.paciente['CI'] = CI
        return self

    def set_nombre(self, nombre):
        self.paciente['nombre'] = nombre
        return self

    def set_apellido(self, apellido):
        self.paciente['apellido'] = apellido
        return self

    def set_edad(self, edad):
        self.paciente['edad'] = edad
        return self

    def set_genero(self, genero):
        self.paciente['genero'] = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.paciente['diagnostico'] = diagnostico
        return self

    def set_doctor(self, doctor):
        self.paciente['doctor'] = doctor
        return self

    def build(self):
        paciente = self.paciente
        self.reset()
        return paciente

pacientes = [
    {
        "CI": 111,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 25,
        "genero": "Masculino",
        "diagnostico": "Gripe",
        "doctor": "Dr. Hector",
    },
    {
        "CI": 222,
        "nombre": "María",
        "apellido": "López",
        "edad": 35,
        "genero": "Femenino",
        "diagnostico": "Hipertensión",
        "doctor": "Dra. Martínez",
    },
    {
        "CI": 333,
        "nombre": "Carlos",
        "apellido": "Martínez",
        "edad": 28,
        "genero": "Masculino",
        "diagnostico": "Fractura de pierna",
        "doctor": "Dr. Pérez",
    },
    {
        "CI": 444,
        "nombre": "Ana",
        "apellido": "Rodríguez",
        "edad": 50,
        "genero": "Femenino",
        "diagnostico": "Diabetes",
        "doctor": "Dr. Sánchez",
    },
    {
    "CI": 555,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 40,
    "genero": "Masculino",
    "diagnostico": "Hipertensión",
    "doctor": "Dr. Pedro Pérez",
    },
]


class PacientesService:
    @staticmethod
    def find_paciente(CI):
        return next(
            (paciente for paciente in pacientes if paciente["CI"] == CI),
            None,
        )

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]

    @staticmethod
    def update_paciente(CI, data):
        paciente = PacientesService.find_paciente(CI)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_paciente(CI):
        paciente = PacientesService.find_paciente(CI)
        if paciente:
            pacientes.remove(paciente)
            return pacientes
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
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(
                    diagnostico
                )
                if pacientes_filtrados:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        elif parsed_path.path.startswith("/pacientes/"):
            CI = int(parsed_path.path.split("/")[-1])
            paciente = PacientesService.find_paciente(CI)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_paciente(CI, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            pacientes = PacientesService.delete_paciente(CI)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes.append(data)  # Agregar el nuevo paciente a la lista
            HTTPResponseHandler.handle_response(self, 200, data)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

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
