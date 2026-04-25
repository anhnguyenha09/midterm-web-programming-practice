#CAU 5 - VIET CLIENT FLASK
from flask import Flask, render_template, request, jsonify, redirect, url_for
#import cac thu vien gom flask (co ban), render_template de render file html, request de xu lieu gui tu client, jsonify de tra ve dlieu dang json, redirect va url_for de chuyen huong trang
import urllib.request
# import thu vien de goi API (urllib.request)
import urllib.error
# import thu vien de xu ly loi khi goi API (urllib.error)
import json
# import thu vien de xu ly du lieu dang json

app = Flask(__name__) # khoi tao ung dung flask

API_URL = "http://127.0.0.1:5000" # dia chi API ma client se goi de lay du lieu (phai trung voi dia chi API trong app.py)

#hàm helper để gọi API và trả về dữ liệu dạng JSON, hàm này sẽ nhận vào endpoint (đường dẫn cụ thể trên API) và trả về dl sau khi gọi thành công, nếu có lỗi thì trả về none
def call_api(endpoint, method='GET', data=None):
    """
    Gọi API backend:
    - endpoint: ví dụ '/users', '/users/1'
    - method: GET, POST, PUT, DELETE
    - data: dữ liệu gửi lên, dùng cho post, put
    """

    url = f'{API_URL}{endpoint}' # tạo url đầy đủ để gọi API

    try:
        if method == 'GET':
            with urllib.request.urlopen(url) as response: 
                # gửi http request tới url, trả về 1 đối tượng giống file gọi là response; dùng context manager để tự động đóng kết nối sau khi dùng xong
                return json.loads(response.read().decode()) # read du lieu tu response, decode tu bytes sang string, sau do load tu string sang dict
            
        elif method == 'POST' or method == 'PUT':
            req_data = json.dumps(data).encode('utf-8') #chuyen du lieu tu dict sang json string, sau do encode sang bytes de gui len API
            req = urllib.request.Request(
                url, 
                data = req_data,
                headers={'Content-Type': 'application/json'}
                method=method
            ) #tao request de goi API, truyen url, du lieu da duoc encode va phuong thuc (POST hoac PUT)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())

        elif method == 'DELETE':
            req = urllib.request.Request(
                url,
                method='DELETE'
            )
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        return {'error': f'Lỗi kết nối API: {e.reason}'}
    except json.JSONDecodeError:
        return {'error': 'Lỗi xử lý dữ liệu'}

# danh sách các route cho client
 
#route hiển thị danh sách user ở trang chủ
@app.route('/')
def index():
    users = call_api('/users')
    if 'error' in users:
        return f"<h1>Lỗi: {users['error']}</h1>"
    return render_template('index.html', users=users)
    # gọi API '/users' de lay danh sách user, nếu có lỗi thì hiển thị lỗi, nếu thành công thì render template 'index.html' và truyền danh sách user vào template de hiển thị

#route thêm user
@app.route('/add', methods=['POST', 'GET']) # chỉ cho phép gọi route này bằng phương thức POST và GET, GET de hiển thị form thêm user, POST de xử lý du lieu form khi nguoi dung submit
def add_user():
    if request.method == 'POST':
        data = {
            'username': request.form['username'], # lay du lieu tu form, request.form la mot dict chua du lieu tu form, truy cap bang key 'username' de lay gia tri tu form
            'email': request.form['email'], 
            'class_id': request.form['class_id']
        }
        result = call_api('/users', method='POST', data=data) # goi API '/users' bang phuong thuc POST de them user moi, truyen du lieu tu form vao data
        return redirect(url_for('index')) # sau khi them xong thi chuyen huong ve trang chu de hien thi danh sach user da duoc cap nhat
    return render_template('add_user.html') # neu la GET thi render form de them user moi

#route xóa user
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    call_api(f'/users/{user_id}', method='DELETE') # goi API '/users/<user_id>' bang phuong thuc DELETE de xoa user co id la user_id
    return redirect(url_for('index')) # sau khi xoa xong thi chuyen huong ve trang chu de hien thi danh sach user da duoc cap nhat

# route sửa user
@app.route('/edit/<int:user_id>', methods=['POST', 'GET'])
def edit_user(user_id):
    if request.method == 'POST':
        data = {
            'username': request.form.get('username'), # lay du lieu tu form, su dung request.form.get de tranh loi neu key khong ton tai trong form, tra ve None thay vi loi
            'email': request.form.get('email'),
            'class_id': request.form.get('class_id')
        }
        call_api(f'/users/{user_id}', method='PUT', data=data) # goi API '/users/<user_id>' bang phuong thuc PUT de cap nhat thong tin user co id la user_id, truyen du lieu tu form vao data
        return redirect(url_for('index')) #sau khi cap nhat xong thi chuyen huong ve trang chu de hien thi danh sach user da duoc cap nhat
    
    users = call_api('/users') # goi API '/users' de lay danh sach user, de tim user co id la user_id de hien thi thong tin trong form edit
    user = next((u for u in users if u['id'] == user_id), None)
    # sử dụng next và generator expression để tìm user có id bằng user_id trong danh sách users, nếu không tìm thấy thì trả về None
    return render_template('edit_user.html', user=user)

#route tìm kiếm
@app.route('/search')
def search():
    keyword = request.args.get('q', '') # lấy dữ liệu từ query string, request.args là 1 dict chứa dữ liệu từ query string
    results = call_api(f'/users/search?q={keyword}') # goi API '/users/search' bang phuong thuc GET de tim kiem user theo keyword, truyen keyword vao query string
    return render_template('index.html', users=results) # render lại trang chủ để hiển thị kết quả tìm kiếm, truyền danh sách user là kết quả tìm kiếm vào template để hiển thị

if __name__ == '__main__':
    app.run(debug=True, port=5001) # chay ung dung flask, debug=True de cho phep tu dong tai lai khi co thay doi trong code va hien thi loi chi tiet khi co loi xay ra
    # port=5001 de chay ung dung tren cong 5001, khac voi API de tranh xung dot cong
    