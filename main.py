import face_recognition
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data for demo purposes
users = [
    {'username': 'Nitit', 'image_path': 'D:/.Mahidol University/year 3/Security/Project/Data/Nitit_data.png'},
    {'username': 'Siranut', 'image_path': 'D:/.Mahidol University/year 3/Security/Project/Data/Siranut_data.png'},
    {'username': 'Tawan', 'image_path': 'D:/.Mahidol University/year 3/Security/Project/Data/Tawan_data.png'}
]

# Homepage
@app.route('/')
def index():
    message = ''
    return render_template('index.html', error=message)

# Login form submission
@app.route('/login', methods=['POST'])
def login():
    # Get form data

    image_file = request.files['fileInput']

    # Authenticate user using face recognition
    for user in users:
        try:
            known_image = face_recognition.load_image_file(user['image_path'])
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_image = face_recognition.load_image_file(image_file)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            face_distances = face_recognition.face_distance([known_encoding], unknown_encoding)
        except:
          message = 'We were unable to verify your identity based on the uploaded image. Please try again.'
          return render_template('index.html', error=message)
        
        print(face_distances[0])

        if face_distances[0] < 0.6:
            # Successful login
            return redirect(url_for('dashboard'))

    # Failed login
    message = 'We were unable to verify your identity based on the uploaded image. Please try again.'
    return render_template('index.html', error=message)

# Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
