from flask import Flask, jsonify, request
import chatbot
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/chat", methods=["POST"])
@cross_origin()
def home():
    data = request.json
    msg = data.get("msg")
    # return msg
    return chatbot.start_bot(msg)


if __name__ == "__main__":
    app.run(debug=True)
