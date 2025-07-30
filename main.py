
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

VIATOR_API_KEY = os.getenv("VIATOR_API_KEY")
VIATOR_BASE_URL = "https://api.sandbox.viator.com/partner/products/search"

@app.route("/")
def home():
    return "Viator proxy is running."

@app.route("/viator")
def viator():
    location = request.args.get("location", "Sarasota")
    topX = request.args.get("topX", "10")
    categoryId = request.args.get("categoryId")

    headers = {
        "Accept": "application/json",
        "exp-api-key": VIATOR_API_KEY
    }

    params = {
        "location": location,
        "topX": topX
    }

    if categoryId:
        params["categoryId"] = categoryId

    try:
        response = requests.get(VIATOR_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
