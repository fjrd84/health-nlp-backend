from flask import Flask

app = Flask(__name__)

app.debug = True

@app.route('/')
def base_route():
    return 'health-nlp-backend'

if __name__ == '__main__':
    app.run()
