# MCI_intern

# ERD

![ERD](demo/MCI_INTERN.png)



# RUN PROJECT

## 1. Clone project

```bash
git clone https://github.com/nguyenvanvutlv/MCI_intern.git
cd MCI_intern
pip install -r requirements.txt
```

## 2. Create database [MySQL]


```sql
CREATE DATABASE name_database;
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name_database',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'your_user',
        'PASSWORD' : 'your_password'
    }
}
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```



# MODEL

## 1. ROLE

Các vai trò mẫu có thể có trong công ty

```txt
Developer (Dev) : Nhân viên phát triển
Tester (QC: Quality Control) – Nhân viên kiểm thử
Business Analysis (BA) : Nhân viên phân tích
Support Analysis (SPA) : Nhân viên hỗ trợ
Quality assurance (QA) : Nhân viên đảm bảo chất lượng
Technical Architect (TA) : Kiến trúc sư
Project Manager (PM) : Quản lý dự án
```

Người dùng có thể thêm các vai trò khác vào hệ thống, 
nhưng các vai trò này là bắt buộc phải có trong hệ thống,
và không thể xóa các vai trò này khỏi hệ thống.

Các vai trò thêm mới chỉ hiển thị trong dự án của người dùng thêm mới.