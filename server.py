import socket
import threading
import json
import random
import globalSettings

class GameServer:
    def __init__(self, host=globalSettings.serverIP, port=globalSettings.serverPort):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)  # Allow up to 2 connections
        self.clients = []
        self.game_data = {
            'player1_health': 100,
            'player2_health': 100,
            'turn': 1,
            'harden_active': False,
            'empower_active': False
        }
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        print(f"Client connected: {client_address}")
        self.clients.append(client_socket)

        if len(self.clients) == 2:
            self.start_game()

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                with self.lock:
                    received_data = json.loads(data)
                    self.update_game_state(received_data)
                    self.broadcast_game_state()

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            print(f"Client disconnected: {client_address}")
            self.clients.remove(client_socket)
            client_socket.close()

    def update_game_state(self, received_data):
        if received_data['action'] == "Kick":
            if self.game_data['turn'] == 1:
                self.game_data['player2_health'] -= 25
            elif self.game_data['turn'] == 2:
                self.game_data['player1_health'] -= 25
        elif received_data['action'] == "Heal":
            if self.game_data['turn'] == 1:
                self.game_data['player1_health'] += 20
                if self.game_data['player1_health'] > 100:
                    self.game_data['player1_health'] = 100
            elif self.game_data['turn'] == 2:
                self.game_data['player2_health'] += 20
                if self.game_data['player2_health'] > 100:
                    self.game_data['player2_health'] = 100
        elif received_data['action'] == "Harden":
            self.game_data['harden_active'] = True
        elif received_data['action'] == "Empower":
            self.game_data['empower_active'] = True
        self.end_turn()

    def end_turn(self):
        if self.game_data['player1_health'] <= 0 or self.game_data['player2_health'] <= 0:
            self.game_data['player1_health'] = 100
            self.game_data['player2_health'] = 100
            self.game_data['turn'] = 1
            self.game_data['harden_active'] = False
            self.game_data['empower_active'] = False
        elif self.game_data['turn'] == 1:
            self.game_data['turn'] = 2
        elif self.game_data['turn'] == 2:
            self.game_data['turn'] = 1
            self.game_data['harden_active'] = False
            self.game_data['empower_active'] = False

    def broadcast_game_state(self):
        game_state_json = json.dumps(self.game_data)
        for client in self.clients:
            try:
                client.sendall(game_state_json.encode())
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def start_game(self):
        print("Game started!")
        self.broadcast_game_state()

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.run()
