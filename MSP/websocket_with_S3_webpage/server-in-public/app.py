from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS
import subprocess
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    # Serve a placeholder or a redirection to the S3-hosted page
    return "Please access your HTML page from the S3 bucket URL."

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('run_terraform')
def run_terraform():
    print('Running Terraform...')
    current_directory = os.path.dirname(os.path.abspath(__file__))

    print("Current working directory:", os.getcwd())
    os.chdir(current_directory)
    try:
        subprocess.run(["terraform", "init"], check=True)
        process = subprocess.Popen(
            ['terraform', 'apply', '-auto-approve'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except:
        print("Error running terraform")
       
    

    print('Output from Terraform:')
    # Send real-time output from Terraform to the client
    for line in iter(process.stdout.readline, ''):
        emit('terraform_output', {'data': line})

    process.stdout.close()
    process.wait()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)