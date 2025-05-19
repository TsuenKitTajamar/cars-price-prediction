from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

app = Flask(__name__)

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_KEY = os.getenv("AZURE_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"  # o "x-api-key": API_KEY si aplica
}

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        input_data = [
            request.form["marca"],
            request.form["modelo"],
            request.form["version"],
            int(request.form["startYear"]),
            int(request.form["endYear"]),
            int(request.form["cilindrada"]),
            int(request.form["cv"]),
            request.form["id_carroceria"],
            int(request.form["pf"]),
            int(request.form["puertas"]),
            request.form["id_combustible"],
            int(request.form["matriculacion"]),
            request.form["periodoDescripcion"],
            int(request.form["Anno"])
        ]

        payload = {
            "input_data": {
                "columns": [
                    "marca", "modelo", "version", "startYear", "endYear",
                    "cilindrada", "cv", "id_carroceria", "pf", "puertas",
                    "id_combustible", "matriculacion", "periodoDescripcion", "Anno"
                ],
                "index": [0],
                "data": [input_data]
            }
        }

        try:
            response = requests.post(AZURE_ENDPOINT, headers=HEADERS, json=payload)
            response.raise_for_status()
            prediction = response.json()
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("index.html", prediction=prediction)

# 👇 Esto es lo que faltaba
if __name__ == "__main__":
    app.run(debug=True)
