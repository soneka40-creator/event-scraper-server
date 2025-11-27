from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Lista de palavras-chave (japonês e outros)
KEYWORDS = ["出店", "出店募集", "マルシェ出店", "イベント", "募集", "祭り", "マーケット","プロモーション"]

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    try:
        # Requisição básica HTTP
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = r.apparent_encoding  # tenta detectar encoding
        soup = BeautifulSoup(r.text, "html.parser")

        # Pega todo o texto da página
        text = soup.get_text(separator="\n").strip()

        # Filtra pelas palavras-chave
        found = [kw for kw in KEYWORDS if kw in text]

        return jsonify({
            "url": url,
            "found": found,
            "full_text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
