from flask import Flask, request, jsonify
from mission_database import create_table, insert_telemetry

app = Flask(__name__)

create_table()


@app.route("/telemetry", methods=["POST"])
def receive_telemetry():
    data = request.get_json()

    insert_telemetry(data)

    print("\nStored UAV telemetry:")
    print(data)

    return jsonify({
        "message": "Telemetry stored by ground control"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)