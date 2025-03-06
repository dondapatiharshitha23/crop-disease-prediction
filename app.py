import base64
import os
import uuid
from flask import Flask, jsonify,render_template, request
from flask_cors import CORS
import numpy as np
import tensorflow as tf

app = Flask(__name__)

tomato_model = tf.keras.models.load_model('model.h5')
chilli_model = tf.keras.models.load_model('model.h5')

image_size = 256

tomato_class_names = ['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___healthy']

tomato_remedies = {
    'Tomato___Early_blight': "Remove infected leaves and apply fungicides containing copper or mancozeb.",
    'Tomato___Late_blight': "Use fungicides like chlorothalonil or copper-based sprays. Ensure proper drainage.",
    'Tomato___Leaf_Mold': "Improve air circulation. Use fungicides such as chlorothalonil or mancozeb.",
    'Tomato___healthy': "No action needed. Continue maintaining good practices."
}

chilli_class_names = ['healthy', 'leaf curl', 'leaf spot', 'whitefly', 'yellowish']

chilli_remedies = {
    'healthy': "No action needed. Keep maintaining good crop health.",
    'leaf curl': "Use insecticides to control whiteflies and aphids. Apply neem oil.",
    'leaf spot': "Remove infected leaves. Apply fungicides containing copper or chlorothalonil.",
    'whitefly': "Use yellow sticky traps. Apply insecticidal soaps or neem oil.",
    'yellowish': "Provide balanced nutrients. Avoid waterlogging. Use pest management strategies."
}


@app.route('/predicttomatodisesase', methods=['POST'])
def predict_tomato_disease():
    data = request.get_json()
    image_data = data['image'].split(",")[1]  # Remove the header
    image_bytes = base64.b64decode(image_data)
    random_guid = uuid.uuid4()
    guid_str = str(random_guid)
    image_name = "photo"+guid_str+".png"
    # Save the image
    image_path = os.path.join("uploads", image_name)
    os.makedirs("uploads", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    # Load and preprocess the image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(image_size, image_size))
    img_array = tf.keras.preprocessing.image.img_to_array(img)  # Convert image to array
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize pixel values

     # Predict the class
    predictions = tomato_model.predict(img_array)
    predicted_class = tomato_class_names[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)


    if confidence < 95:
        message = "This is not a tomato leaf."
        return jsonify({"message": message, "path": image_path})

    remedy = tomato_remedies.get(predicted_class, "No remedy available for this class.")
    message = "PredictedClass:"+str(predicted_class)+"  Confidence:"+str(confidence)+" Remedy: "+str(remedy)
    return jsonify({"message": message, "path": image_path})


@app.route('/predictchillidisesase', methods=['POST'])
def predict_chilli_disease():
    data = request.get_json()
    image_data = data['image'].split(",")[1]  # Remove the header
    image_bytes = base64.b64decode(image_data)
    random_guid = uuid.uuid4()
    guid_str = str(random_guid)
    image_name = "photo"+guid_str+".png"
    # Save the image
    image_path = os.path.join("uploads", image_name)
    os.makedirs("uploads", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(image_bytes)

    # Load and preprocess the image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(image_size, image_size))
    img_array = tf.keras.preprocessing.image.img_to_array(img)  # Convert image to array
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize pixel values

     # Predict the class
    predictions = chilli_model.predict(img_array)
    predicted_class = chilli_class_names[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)

    if confidence < 95:
         message = "This is not a chili leaf."
         return jsonify({"message": message, "path": image_path})


    remedy = chilli_remedies.get(predicted_class, "No remedy available for this class.")
    message = "PredictedClass:"+str(predicted_class)+"  Confidence:"+str(confidence)+" Remedy: "+str(remedy)
    return jsonify({"message": message, "path": image_path})



@app.route('/')
def home():
    return render_template('index.html')






if __name__ == '__main__':
    app.run(debug=True)