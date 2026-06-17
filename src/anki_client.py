import requests

class AnkiClient:
    def __init__(self, url="http://10.255.255.254:8765"):
        self.url = url

    def test_connection(self):
        try:
            response = requests.post(self.url, json={"action": "version", "version": 6})
            return response.json()
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    client = AnkiClient()
    print(f"Connection Status: {client.test_connection()}")
