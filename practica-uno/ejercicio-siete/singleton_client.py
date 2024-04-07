import requests

url = "http://localhost:8000/"

# POST /partidas
elemento = input("Elige tu elemento (piedra, papel o tijera): ").lower()
response = requests.request(
    method="POST", url=url + "partidas", json={"elemento": elemento}
)
print(response.text)

# GET /partidas
response = requests.request(method="GET", url=url + "partidas")
print(response.text)

# GET /partidas?resultado={resultado}
resultado = input("Ingresa el resultado (ganó, perdió o empate): ").lower()
response = requests.request(method="GET", url=url + f"partidas?resultado={resultado}")
print(response.text)
