import socket
import time
import json

def load_drone_json(filepath='drones.json'):
    try:
        with open(filepath,'r') as file:
            return json.load(file)
    except FileNotFoundError or json.JSONDecodeError:
        print(f'Please provide the correct drone json file!')