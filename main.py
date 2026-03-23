from flask import Flask

print("Successfully make docker image")
print(" :-)   we can do anything now hurray!!!!!")

app = Flask(__name__)

@app.route('/')
def hello():
    return "Successfully made Docker image! :-) We can do anything now hurray!!!!!"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)