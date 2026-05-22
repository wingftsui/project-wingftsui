import socket
import time
import json

def load_drone_json(filepath='drones.json'):
    try:
        with open(filepath,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'No json file found!')
    except json.JSONDecodeError:
        print(f'Wrong file format. It should be json file')

