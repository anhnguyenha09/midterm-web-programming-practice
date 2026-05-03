from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:5000/users'

@app.route('/')
def index():
    try:
        # gửi yêu cầu GET đến API để lấy danh sách user
        api_response = requests.get(API_URL) #api_response là đối tượng phản hồi từ API, chứa thông tin về mã trạng thái và dữ liệu trả về

        #kiểm tra nếu phản hồi thành công
        if api_response.status_code == 200:
            #parse dữ liệu JSON
            responses = api_response.json() #responses là dữ liệu đã được chuyển đổi từ JSON sang định dạng Python (thường là list hoặc dict) để dễ dàng sử dụng trong ứng dụng Flask
            #truyeefn du lieu vao template va hien thi
            return render_template('index.html',users=responses)
        else:
            #neu loi thi hien thi ma loi
            flash(f'Loi lay du lieu tu API {api_response.status_code}')
    except Exception as e:
        # neu co loi ngoai le vd nhu k ket noi duoc thi in ra log
        flash(f'Loi ket noi den API: {str(e)}')
        #trong trg hop loi, van render template nma ko co du lieu
        return render_template('index.html', users=[])
if __name__ == '__main__':
    app.run(port=5001, debug=True)

