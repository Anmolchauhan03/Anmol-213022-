from flask import Flask, jsonify
import requests
from threading import Lock
import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
API_TIMEOUT = 0.5  # 500 milliseconds
VALID_IDS = {'p', 'f', 'e', 'r'}
THIRD_PARTY_API_URLS = {
    'p': "http://20.244.56.144/test/register",
    'f': "http://20.244.56.144/test/auth",
    
}

# Data storage
window = []
lock = Lock()

def fetch_numbers(numberid):
    try:
        url = THIRD_PARTY_API_URLS[numberid]
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except (requests.exceptions.RequestException, KeyError):
        return []

def update_window(new_numbers):
    global window
    with lock:
        windowPrevState = window.copy()
        for number in new_numbers:
            if number not in window:
                if len(window) >= WINDOW_SIZE:
                    window.pop(0)                
                window.append(number)
        return windowPrevState, window

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0.0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in VALID_IDS:
        return jsonify({"error": "Invalid number ID"}), 400

    start_time = time.time()

    new_numbers = fetch_numbers(numberid)
    windowPrevState, windowCurrState = update_window(new_numbers)

    avg = calculate_average(windowCurrState[:WINDOW_SIZE])

    response_time = time.time() - start_time
    if response_time > API_TIMEOUT:
        return jsonify({"error": "Request took too long"}), 500

    response = {
        "windowPrevState": windowPrevState,
        "windowCurrState": windowCurrState,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
