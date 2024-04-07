import requests
import json

url = "http://localhost:8000/"

def create_message(content):
    response = requests.post(url + "mensajes", json={"contenido": content})
    return response.json()

def get_all_messages():
    response = requests.get(url + "mensajes")
    return response.json()

def get_message_by_id(message_id):
    response = requests.get(url + f"mensajes/{message_id}")
    return response.json()

def update_message(message_id, new_content):
    response = requests.put(url + f"mensajes/{message_id}", json={"contenido": new_content})
    return response.status_code

def delete_message(message_id):
    response = requests.delete(url + f"mensajes/{message_id}")
    return response.status_code

# Ejemplo de uso
print("Creando mensaje...")
new_message = create_message("Hola mundo")
print("Mensaje creado:", new_message)

print("\nObteniendo todos los mensajes...")
all_messages = get_all_messages()
print("Todos los mensajes:", all_messages)

message_id = new_message["id"]
print(f"\nObteniendo mensaje con ID {message_id}...")
specific_message = get_message_by_id(message_id)
print("Mensaje encontrado:", specific_message)

print("\nActualizando mensaje...")
update_status = update_message(message_id, "¡Hola de nuevo!")
if update_status == 200:
    print("Mensaje actualizado con éxito.")
else:
    print("No se pudo actualizar el mensaje.")

print("\nEliminando mensaje...")
delete_status = delete_message(message_id)
if delete_status == 200:
    print("Mensaje eliminado con éxito.")
else:
    print("No se pudo eliminar el mensaje.")
