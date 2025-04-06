import socket
import threading
import json
import random
from game import Game

class GameServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)  # Allow up to 2 connections
        self.clients = []
        self.client_ids = {}  # Store client IDs
        self.next_client_id = 1
        self.game = Game()
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        client_id = self.assign_client_id(client_socket)
        print(f"Client {client_id} connected: {client_address}")
        self.clients.append(client_socket)

        # Send the client their ID
        self.send_client_id(client_socket, client_id)

        if len(self.clients) == 2:
            self.start_game()

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                with self.lock:
                    try:
                        received_data = json.loads(data)
                        # Validate received data
                        if not isinstance(received_data, dict) or 'action' not in received_data:
                            print(f"Invalid data received from client {client_id}: {received_data}")
                            continue
                        self.update_game_state(received_data)
                        self.broadcast_game_state()
                    except json.JSONDecodeError:
                        print(f"Invalid JSON received from client {client_id}: {data}")

        except (socket.error, ConnectionResetError) as e:
            print(f"Client {client_id} disconnected unexpectedly: {e}")
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
        finally:
            print(f"Client {client_id} disconnected: {client_address}")
            self.remove_client(client_socket)
            client_socket.close()

    def assign_client_id(self, client_socket):
        client_id = self.next_client_id
        self.next_client_id += 1
        self.client_ids[client_socket] = client_id
        return client_id

    def send_client_id(self, client_socket, client_id):
        try:
            client_socket.sendall(json.dumps({"client_id": client_id}).encode())
        except Exception as e:
            print(f"Error sending client ID: {e}")

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        if client_socket in self.client_ids:
            del self.client_ids[client_socket]
        # Consider resetting the game if a client disconnects mid-game
        if len(self.clients) < 2:
            print("Not enough players, resetting game")
            self.reset_game()

    def reset_game(self):
        self.game = Game()
        self.broadcast_game_state()

    def update_game_state(self, received_data):
        """Updates the game state based on received data."""
        action = received_data['action']
        if action == "Kick":
            self.game.player_kick()
        elif action == "Heal":
            self.game.player_heal()
        elif action == "Harden":
            self.game.player_harden()
        elif action == "Empower":
            self.game.player_empower()
        else:
            print(f"Unknown action: {action}")

    def broadcast_game_state(self):
        """Broadcasts the current game state to all connected clients."""
        game_state = {
            'player1_health': self.game.health,
            'player2_health': self.game.health2,
            'turn': self.game.turn,
            'harden_active': self.game.harden_active,
            'empower_active': self.game.empower_active
        }
        for client in self.clients:
            try:
                client.sendall(json.dumps(game_state).encode())
            except Exception as e:
                print(f"Error broadcasting game state: {e}")

    def start_game(self):
        """Starts the game."""
        print("Starting game...")
        self.broadcast_game_state()

def main():
    server = GameServer()
    print(f"Server listening on {server.host}:{server.port}")
    while True:
        client_socket, client_address = server.server_socket.accept()
        client_thread = threading.Thread(target=server.handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
