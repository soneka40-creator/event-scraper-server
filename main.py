from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor ativo — pronto para buscar!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get("url")
    keywords = data.get("keywords", [])

    if not url:
        return jsonify({"error": "URL não enviada"}), 400

    try:
        response = requests.get(url, timeout=15)
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")

        found = [kw for kw in keywords if kw in text]

        return jsonify({
            "url": url,
            "found": found,
            "count": len(found)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
