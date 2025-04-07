from flask import Flask, request, jsonify
import os
import cv2
import pymysql
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Kết nối MySQL
db = pymysql.connect(
    host="localhost",
    user="your_username",  # Thay bằng username MySQL của bạn
    password="your_password",  # Thay bằng password MySQL của bạn
    database="image_recognition_db"
)

# API upload và xử lý ảnh
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Xử lý ảnh (ví dụ: nhận diện đơn giản)
        image = cv2.imread(filepath)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Ở đây bạn có thể thêm logic nhận diện phức tạp hơn (sử dụng mô hình AI)

        # Lưu vào MySQL
        cursor = db.cursor()
        sql = "INSERT INTO images (filename, filepath, label) VALUES (%s, %s, %s)"
        cursor.execute(sql, (filename, filepath, "example_label"))  # Thay "example_label" bằng kết quả nhận diện
        db.commit()
        cursor.close()

        return jsonify({'message': f'File {filename} uploaded and processed successfully!'})

if __name__ == '__main__':
    app.run(debug=True)