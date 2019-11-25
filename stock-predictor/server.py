from flask import Flask
from keras.models import Sequential

app = Flask(__name__)

def loadModel():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('./modelBin/model.h5')
    loaded_model.compile(close='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, port=3000)
