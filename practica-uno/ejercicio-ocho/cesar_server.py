from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Message:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.messages = {}
            cls._instance.next_id = 1
        return cls._instance

    def create_message(self, content):
        message_id = self.next_id
        encrypted_content = self.encrypt(content)
        message_data = {
            "id": message_id,
            "contenido": content,
            "contenido_cifrado": encrypted_content
        }
        self.messages[message_id] = message_data
        self.next_id += 1
        return message_data

    def get_all_messages(self):
        return list(self.messages.values())

    def get_message_by_id(self, message_id):
        return self.messages.get(message_id)

    def update_message(self, message_id, new_content):
        if message_id in self.messages:
            encrypted_content = self.encrypt(new_content)
            self.messages[message_id]["contenido"] = new_content
            self.messages[message_id]["contenido_cifrado"] = encrypted_content
            return True
        else:
            return False

    def delete_message(self, message_id):
        if message_id in self.messages:
            del self.messages[message_id]
            return True
        else:
            return False

    @staticmethod
    def encrypt(content):
        encrypted_content = ""
        for char in content:
            if char.isalpha():
                ascii_code = ord(char)
                if char.islower():
                    encrypted_ascii = (ascii_code - ord('a') + 3) % 26 + ord('a')
                else:
                    encrypted_ascii = (ascii_code - ord('A') + 3) % 26 + ord('A')
                encrypted_content += chr(encrypted_ascii)
            else:
                encrypted_content += char
        return encrypted_content

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/mensajes":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            content = json.loads(post_data.decode("utf-8"))["contenido"]
            message_data = message.create_message(content)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(message_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/mensajes":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            messages_data = json.dumps(message.get_all_messages())
            self.wfile.write(messages_data.encode("utf-8"))
        elif self.path.startswith("/mensajes/"):
            message_id = int(self.path.split("/")[-1])
            message_data = message.get_message_by_id(message_id)
            if message_data:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(message_data).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            message_id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            new_content = json.loads(put_data.decode("utf-8"))["contenido"]
            success = message.update_message(message_id, new_content)
            if success:
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            message_id = int(self.path.split("/")[-1])
            success = message.delete_message(message_id)
            if success:
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global message
    message = Message()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, MessageHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
