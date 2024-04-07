import requests

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

url = "http://localhost:8000/pacientes"

get_response = requests.get(url)
print("Listar todos los pacientes:")
print(get_response.json())

paciente_builder = PacienteBuilder()
nuevo_paciente = (
    paciente_builder
    .set_CI(555)
    .set_nombre("Juan")
    .set_apellido("Pérez")
    .set_edad(40)
    .set_genero("Masculino")
    .set_diagnostico("Hipertensión")
    .set_doctor("Dr. Pedro Pérez")
    .build()
)

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
