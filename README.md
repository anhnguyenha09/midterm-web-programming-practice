# Huong dan chay app va test

## Terminal 1 (bash)
```
cd 1_NguyenVanA_2/api
python app.py
```

## Terminal 2 (bash)
```
cd 1_NguyenVanA_2/client
python client.py
```

## Cach test tren trinh duyet
Kiểm tra nhanh trên trình duyệt:
```
URL                                                                             Mục đích

http://127.0.0.1:5000/                                                          Xem thông tin sinh viên
http://127.0.0.1:5000/users                                                     Xem toàn bộ danh sách
http://127.0.0.1:5000/users/search?q=John                                       Tìm kiếm
http://127.0.0.1:5000/users/check?email=john.doe@email.com&username=John        Kiểm tra tồn tại
http://127.0.0.1:5001/                                                          Giao diện web hiển thị danh sách
```

## Postman TEST API
http://127.0.0.1:5000/users (GET)

http://127.0.0.1:5000/users (POST)
body
```
{
  "username": "beo",
  "email": "beomap@gmail.com"
}
```
http://127.0.0.1:5000/users/{id} (PUT)
body
```
{
  "username": "newname",
  "email": "new@gmail.com"
}
```

http://127.0.0.1:5000/users/{id} (DELETE)

--search user
GET /users/search?q=keyword

--check user existence
GET /users/check?email=...&username=...

--Lay user theo class
GET /users/class/{class_id}

--batch users
POST /users/batch
body
```
[
  {
    "username": "user1",
    "email": "u1@gmail.com",
    "class_id": 1
  },
  {
    "username": "user2",
    "email": "u2@gmail.com",
    "class_id": 2
  }
]
```
