from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, List, Schema, Field, Mutation, Boolean

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    planta_por_especie = Field(Planta, especie=String())
    plantas_por_frutos = List(Planta, frutos=Boolean())

    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_por_especie(root, info, especie):
        for planta in plantas:
            if planta.especie == especie:
                return planta
        return None
    
    def resolve_plantas_por_frutos(root, info, frutos):
        return [planta for planta in plantas if planta.frutos == frutos]

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class Mutations(ObjectType):
    delete_planta = DeletePlanta.Field()

plantas = [
    Planta(id=1, nombre="Rosa", especie="Rosa ssp.", edad=24, altura=50, frutos=False),
    Planta(id=2, nombre="Girasol", especie="Helianthus annuus", edad=12, altura=120, frutos=True),
    Planta(id=3, nombre="Manzano", especie="Malus domestica", edad=36, altura=180, frutos=True),
    Planta(id=4, nombre="Cactus", especie="Schlumbergera truncata", edad=48, altura=25, frutos=False),
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
