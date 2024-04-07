import requests

url = "http://localhost:8000/pacientes"

get_response = requests.get(url)
print("Listar todos los pacientes:")
print(get_response.json())

nuevo_paciente = {
    "CI": 555,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 40,
    "genero": "Masculino",
    "diagnostico": "Hipertensión",
    "doctor": "Dr. Pedro Pérez",
}

post_response = requests.post(url, json=nuevo_paciente)
print("\nCrear un paciente:")
print(post_response.json())

ruta_get_ci = url + "?CI=222"  # Cambiado para buscar pacientes con CI igual a 222
get_response_ci = requests.get(ruta_get_ci)
print("\nBuscar pacientes por CI:")
print(get_response_ci.json())

ruta_get_diabetes = url + "?diagnostico=Diabetes"
get_response_diabetes = requests.get(ruta_get_diabetes)
print("\nListar pacientes con diagnóstico de Diabetes:")
print(get_response_diabetes.json())

ruta_get_doctor = url + "?doctor=Dr. Pedro Pérez"
get_response_doctor = requests.get(ruta_get_doctor)
print("\nListar pacientes atendidos por el doctor Pedro Pérez:")
print(get_response_doctor.json())

datos_actualizados = {
    "diagnostico": "Asma",
    "doctor": "Dra. Martínez",
}

id_paciente_actualizar = 555
ruta_put = f"{url}/{id_paciente_actualizar}"
put_response = requests.put(ruta_put, json=datos_actualizados)
print("\nActualizar la información de un paciente:")
print(put_response.json())

ruta_delete = f"{url}/{id_paciente_actualizar}"
delete_response = requests.delete(ruta_delete)
print("\nEliminar un paciente:")
print(delete_response.json())
