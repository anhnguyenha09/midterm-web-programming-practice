# Huong dan chay app va test

## Terminal 1 (bash)
```
cd 1_NguyenVanA_2/api
python app.py
```

## Terminal 2 (bash)
cd 1_NguyenVanA_2/client
python client.py

## Cach test
Kiểm tra nhanh trên trình duyệt:
URL                                                                             Mục đích

http://127.0.0.1:5000/                                                          Xem thông tin sinh viên
http://127.0.0.1:5000/Employee                                                  Xem toàn bộ danh sách
http://127.0.0.1:5000/Employee/search?q=John                                    Tìm kiếm
http://127.0.0.1:5000/Employee/check?email=john.doe@email.com&first_name=John   Kiểm tra tồn tại
http://127.0.0.1:5001/                                                          Giao diện web hiển thị danh sách