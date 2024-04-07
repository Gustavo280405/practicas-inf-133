from zeep import Client

client = Client('http://localhost:8000')

response = client.service.SumaDosNumeros(a=4, b=5)
print(response)

response = client.service.RestaDosNumeros(a=6, b=3)
print(response)

response = client.service.MultiplicacionDosNumeros(a=2, b=5)
print(response)

response = client.service.DivisionDosNumeros(a=10, b=2)
print(response)
