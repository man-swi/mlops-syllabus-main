from flask import Flask, redirect, render_template, request
import platform
import os


app = Flask(__name__)

@app.route('/')
def hello():
    container_details = get_container_details()
    return render_template('index.html', container=container_details)

def get_container_details():
    details = {
        'ip_address': platform.node(),
        'hostname': platform.node(),
        'os': platform.system(),
        'architecture': platform.machine(),
        'Python Version': platform.python_version(),
        'System_Info': platform.system(),
        'platform': platform.platform()
    }
    return details
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)