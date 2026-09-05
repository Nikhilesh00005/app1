from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Docker Jenkins CI Pipeline Application is ruunning!"

@app.route("/health")
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
