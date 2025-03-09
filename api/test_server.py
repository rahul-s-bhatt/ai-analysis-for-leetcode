from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Flask server is running!'

if __name__ == '__main__':
    print("Starting test server...")
    app.run(host='0.0.0.0', port=8080, debug=True)