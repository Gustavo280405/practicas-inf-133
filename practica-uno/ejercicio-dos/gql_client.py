import requests

url = 'http://localhost:8000/graphql'

query_lista = """
{
    plantas {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': query_lista})
print(response.json())

query = """
{
    planta_por_especie(especie: 'Helianthus annuus') {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': query})
print(response.json())

query = """
{
    planta_por_frutos(frutos: True) {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

response = requests.post(url, json={'query': query})
print(response.json())

query_crear = """
mutation {
    crearPlanta(nombre: "Lavanda", especie: "Lavandula angustifolia", edad: 18, altura: 30, frutos: False) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.json())

response = requests.post(url, json={'query': query_lista})
print(response.json())

query_eliminar = """
mutation {
    deletePlanta(id: 3) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.json())

response = requests.post(url, json={'query': query_lista})
print(response.json())
