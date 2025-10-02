from src.app import *

if __name__ == "__main__":
    client = TrafficMongoClient()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

