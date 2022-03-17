from flask import Flask

app = Flask(__name__)

@app.route('/do_2999')
def do_2999():
    return '2999'

@app.route('/do_30003')
def do_30003():
    return '30003'

if __name__ == "__main__":
    app.run()
