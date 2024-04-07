from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Game:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = []
        return cls._instance

    def create_game(self, element):
        game_id = len(self.games) + 1
        server_element = random.choice(["piedra", "papel", "tijera"])
        result = Game.calculate_result(element, server_element)
        game_data = {
            "id": game_id,
            "elemento_jugador": element,
            "elemento_servidor": server_element,
            "resultado": result
        }
        self.games.append(game_data)
        return game_data

    def get_all_games(self):
        return self.games

    def get_games_by_result(self, result):
        return [game for game in self.games if game["resultado"] == result]

    @staticmethod
    def calculate_result(player_element, server_element):
        if player_element == server_element:
            return "empate"
        elif (player_element == "piedra" and server_element == "tijera") or \
             (player_element == "tijera" and server_element == "papel") or \
             (player_element == "papel" and server_element == "piedra"):
            return "ganó"
        else:
            return "perdió"

class GameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            player_element = json.loads(post_data.decode("utf-8"))["elemento"]
            game_data = game.create_game(player_element)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == "/partidas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            games_data = json.dumps(game.get_all_games())
            self.wfile.write(games_data.encode("utf-8"))
        elif self.path.startswith("/partidas?resultado="):
            result = self.path.split("=")[-1]
            if result in ["ganó", "perdió", "empate"]:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                games_data = json.dumps(game.get_games_by_result(result))
                self.wfile.write(games_data.encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global game
    game = Game()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, GameHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
