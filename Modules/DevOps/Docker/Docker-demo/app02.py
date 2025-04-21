from flask import Flask, redirect, render_template, request
import platform
import os


app = Flask(__name__)

@app.route('/')
def hello():
    return "Docker Demo"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)