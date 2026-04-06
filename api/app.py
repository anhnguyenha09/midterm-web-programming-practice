# Import các thư viện cần thiết
from flask import Flask, request, jsonify
import sqlite3
import json

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Biến trỏ tới cơ sở dữ liệu
DATABASE = 'ShoppingDB.db'

# Hàm tiện ích: kết nối DB và trả về dict
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Để truy cập cột theo tên
    return conn

# =============================================
# CÂU 1b: Hàm Index - Hiện thông tin sinh viên
# =============================================
@app.route('/')
def index():
    return "1_NguyenVanA_2"  # Thay bằng thông tin của bạn

# =============================================
# CÂU 2a: GET - Lấy toàn bộ danh sách Employee
# =============================================
@app.route('/Employee', methods=['GET'])
def get_Employee():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM Employee').fetchall()
    conn.close()
    # Chuyển kết quả sang dạng list dict rồi trả về JSON
    return jsonify([dict(e) for e in employees])

# =============================================
# CÂU 2b: DELETE - Xóa Employee theo ID
# =============================================
@app.route('/Employee', methods=['DELETE'])
def delete_Employee():
    data = request.get_json()
    employee_id = data.get('Employee_id')
    conn = get_db_connection()
    conn.execute('DELETE FROM Employee WHERE Employee_id = ?', (employee_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Đã xóa Employee có ID = {employee_id}"})

# =============================================
# CÂU 3a: POST - Thêm Employee mới
# =============================================
@app.route('/Employee', methods=['POST'])
def add_Employee():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO Employee (first_name, last_name, department, address, email) VALUES (?, ?, ?, ?, ?)',
        (data['first_name'], data['last_name'], data['department'], data['address'], data['email'])
    )
    conn.commit()
    new_id = cursor.lastrowid  # Lấy ID vừa được tạo
    conn.close()
    return jsonify({"message": "Thêm thành công", "Employee_id": new_id})

# =============================================
# CÂU 3b: PUT - Cập nhật thông tin Employee
# =============================================
@app.route('/Employee', methods=['PUT'])
def update_Employee():
    data = request.get_json()
    employee_id = data.get('Employee_id')
    conn = get_db_connection()
    conn.execute(
        'UPDATE Employee SET first_name=?, last_name=?, department=?, address=?, email=? WHERE Employee_id=?',
        (data['first_name'], data['last_name'], data['department'], data['address'], data['email'], employee_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Đã cập nhật Employee ID = {employee_id}"})

# =============================================
# CÂU 4a: Kiểm tra Employee tồn tại theo Email + FirstName
# =============================================
@app.route('/Employee/check', methods=['GET'])
def check_Employee():
    # Nhận email và first_name từ query string: /Employee/check?email=...&first_name=...
    email = request.args.get('email')
    first_name = request.args.get('first_name')

    conn = get_db_connection()
    # Tìm employee khớp cả email và first_name
    result = conn.execute(
        'SELECT * FROM Employee WHERE email = ? AND first_name = ?',
        (email, first_name)
    ).fetchone()
    conn.close()

    if result:
        return jsonify({"exists": True, "employee": dict(result)})
    else:
        return jsonify({"exists": False, "message": "Không tìm thấy Employee"})

# =============================================
# CÂU 4b: Tìm kiếm Employee theo chuỗi (LIKE)
# =============================================
@app.route('/Employee/search', methods=['GET'])
def search_Employee():
    # Nhận chuỗi tìm kiếm từ query string: /Employee/search?q=...
    keyword = request.args.get('q', '')
    pattern = f'%{keyword}%'  # Dùng LIKE để tìm gần đúng

    conn = get_db_connection()
    # Tìm trong tất cả các cột text
    results = conn.execute(
        '''SELECT * FROM Employee
           WHERE first_name LIKE ? OR last_name LIKE ?
              OR department LIKE ? OR address LIKE ? OR email LIKE ?''',
        (pattern, pattern, pattern, pattern, pattern)
    ).fetchall()
    conn.close()

    return jsonify([dict(r) for r in results])

# =============================================
# CÂU 4c: Lấy danh sách đơn hàng theo EmployeeID
# (Giả sử có bảng Orders liên kết với Employee)
# =============================================
@app.route('/Employee/orders', methods=['GET'])
def get_orders_by_employee():
    # Nhận EmployeeID từ query string
    employee_id = request.args.get('Employee_id')

    conn = get_db_connection()
    # Kiểm tra Employee tồn tại
    emp = conn.execute(
        'SELECT * FROM Employee WHERE Employee_id = ?', (employee_id,)
    ).fetchone()

    if not emp:
        conn.close()
        return jsonify({"message": "Không tìm thấy Employee"}), 404

    # Lấy danh sách đơn hàng (nếu có bảng Orders)
    try:
        orders = conn.execute(
            'SELECT * FROM Orders WHERE Employee_id = ?', (employee_id,)
        ).fetchall()
        conn.close()
        return jsonify({"employee": dict(emp), "orders": [dict(o) for o in orders]})
    except:
        conn.close()
        return jsonify({"message": "Chưa có bảng Orders trong DB", "employee": dict(emp)})

# =============================================
# CÂU 4d: Nhập hàng loạt danh sách khách hàng
# =============================================
@app.route('/Employee/bulk', methods=['POST'])
def bulk_add_customers():
    # Nhận vào một list các object khách hàng
    data_list = request.get_json()  # Là một mảng JSON

    conn = get_db_connection()
    inserted_ids = []

    # Lần lượt insert từng bản ghi
    for data in data_list:
        cursor = conn.execute(
            'INSERT INTO Employee (first_name, last_name, department, address, email) VALUES (?, ?, ?, ?, ?)',
            (data['first_name'], data['last_name'], data['department'], data['address'], data['email'])
        )
        inserted_ids.append(cursor.lastrowid)

    conn.commit()
    conn.close()
    return jsonify({"message": f"Đã thêm {len(inserted_ids)} bản ghi", "ids": inserted_ids})

# Chạy ứng dụng ở cổng 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)