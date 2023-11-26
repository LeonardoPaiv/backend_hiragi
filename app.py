from flask import Flask, request, jsonify, redirect
from model.dao import DAO

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/api/v0/login")

@app.route("/api/v0/login", methods=['GET'])
def login():
    email = request.args.get('email')
    senha = request.args.get('senha')
    return jsonify(email, senha)

app.run(debug=True)

