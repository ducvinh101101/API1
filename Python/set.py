import requests

url = "http://127.0.0.1:5000/predict"
files = {"image": open("mri_gbm3.jpg", "rb")}  # Đổi key thành "image"
response = requests.post(url, files=files)

print(response.json())  # Kết quả dự đoán
