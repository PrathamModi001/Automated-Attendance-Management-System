from flask import Flask, render_template, request, jsonify,redirect, send_file, url_for
import os

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    names = os.listdir('uploads')
    for i in names :
        files = os.remove(f'./uploads/{i}')
    if 'image' not in request.files:    
        return jsonify(success=False,message='No file part')
    
    image = request.files['image']
    if image.filename == '':
        return jsonify(success=False, message='No selected file')

    if image:   
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)
        return redirect(url_for('attend'))
    else:
        return jsonify(success=False, message='Image upload failed')
    
@app.route("/attendance",methods = ['GET','POST'])
def attend() :
    import face_recognition as fr
    import os
    import cv2
    import face_recognition
    import numpy as np
    import pandas as pd
    from time import sleep
    import openpyxl

    def get_encoded_faces():

        encoded = {}

        for dirpath, dnames, fnames in os.walk("./face_repository"):
            for f in fnames:
                if f.endswith(".jpeg") or f.endswith(".png"):
                    face = fr.load_image_file("face_repository/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding

        return encoded


    def unknown_image_encoded(img):

        face = fr.load_image_file("face_repository/" + img)
        encoding = fr.face_encodings(face)[0]

        return encoding


    def classify_face(im):
    
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        img = cv2.imread(im, 1)
    
        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
        
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"


            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):

                cv2.rectangle(img, (left-20, top-10), (right+20, bottom+15), (300, 0, 0), 2)


                cv2.rectangle(img, (left-20, bottom -10), (right+20, bottom+15), (500, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left -10, bottom + 10), font, 0.5, (300, 300, 300), 1)


    
        while True:

            cv2.imshow('Faces Detected', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return face_names 

    name = os.listdir('uploads')
    print(name)
    print(type(name))
    students = classify_face(name[0])
    df = pd.read_csv('Attendance.csv')
    for i in students :
        if i == 'unknown' :
            pass
        else :
            df.loc[df['Rollcall'] == i, '09-11-2023'] = 'P'
    # df.to_csv('Attendance1.csv')
    df.to_excel('./static/Attendance1.xlsx')
    print('done')
    return render_template('test.html')

@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('download')
    if filename == 'attendance':
        return send_file('static/Attendance1.xlsx', as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
