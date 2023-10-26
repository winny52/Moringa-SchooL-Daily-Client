from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    data = {
        'message': 'Welcome to Moringa Daily',
        
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
