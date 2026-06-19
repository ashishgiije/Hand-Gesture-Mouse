from flask import Flask, render_template, jsonify
import subprocess
import threading
import signal
import os

app = Flask(__name__)

# Global variable to store the process
process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-script', methods=['POST'])
def start_script():
    global process
    if process is None:  # Start the script only if it's not already running
        process = subprocess.Popen(['python', 'gesture_control.py'])
        return jsonify({'message': 'Gesture control started successfully!'})
    return jsonify({'message': 'Gesture control is already running.'})

@app.route('/stop-script', methods=['POST'])
def stop_script():
    global process
    if process:
        os.kill(process.pid, signal.SIGTERM)  # Terminate the process
        process = None
        return jsonify({'message': 'Gesture control stopped successfully!'})
    return jsonify({'message': 'No running process found.'})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
