## Auth User with JWT
### Mô tả
 * Sử dụng JWT để phân quyền người dùng với các chức vụ như Customer/Staff/Manager cho các quyền hạn về người dùng
### Công nghệ sử dụng
 * Python (FastAPI)
 * MySQL (Docker)
### Hướng dẫn chạy
Tạo môi trường ảo 
```
python -m venv venv
```
Kích hoạt môi trường
```
source venv/scripts/activate
```
Cài thư viện
```
pip install -r requirements.txt
``` 
Database
```
docker-compose up -d
``` 
Run App
```
python app/main.py
``` 
