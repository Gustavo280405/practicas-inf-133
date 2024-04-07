from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

dispatcher = SoapDispatcher(
    "ejercicio-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

def SumaDosNumeros(a,b):
    return a+b

dispatcher.register_function(
    "SumaDosNumeros",
    SumaDosNumeros,
    returns={"resultado": int},
    args={"a":int, "b":int},
)

def RestaDosNumeros(a,b):
    return a-b

dispatcher.register_function(
    "RestaDosNumeros",
    RestaDosNumeros,
    returns={"resultado": int},
    args={"a":int, "b":int},
)

def MultiplicacionDosNumeros(a,b):
    return a*b

dispatcher.register_function(
    "MultiplicacionDosNumeros",
    MultiplicacionDosNumeros,
    returns={"resultado": int},
    args={"a":int, "b":int},
)

def DivisionDosNumeros(a,b):
    return a/b

dispatcher.register_function(
    "DivisionDosNumeros",
    DivisionDosNumeros,
    returns={"resultado": float},
    args={"a":int, "b":int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciando en http://localhost:8000/")
server.serve_forever()