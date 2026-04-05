#CAU 1A
# import cac thu vien can thiet
from flask import Flask, request, jsonify
import sqlite3
import json

#khoi tao ung dung flask
app = Flask(__name__)

#bien tro toi csdl
db = 'ShoppingDB.db'

#util - ket noi db va tra ve dict
def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row # de truy cap cot theo ten
    return conn

#CAU 1B
@app.route('/')
def index():
    return "1_Nguyen_Thi_Qua_Dua_1"

#CAU 2A - GET: lay toan bo danh sach Employees
@app.route('/Employee', methods=['GET'])
def get_Employee():
    conn = get_db()
    employees = conn.execute("SELECT * FROM Employee").fetchall()
    conn.close()
    #chuyen ket qua sang dang list dict roi tra ve json
    return jsonify([dict(e) for e in employees])

#CAU 2B - DELETE: xoa employee theo id
@app.route('/Employee', methods=['DELETE'])
def delete_Employee():
    data = request.get_json()
    employee_id = data['Employee_id']
    conn = get_db()
    conn.execute("DELETE FROM Employee WHERE Employee_id = ?", (employee_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Da xoa Employee co ID = {employee_id}"})

#CAU 3A - POST: them Employee moi
@app.route('/Employee', methods=['POST'])
def add_Employee():
    data = request.get_json()
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO Employee (first_name, last_name, department, address, email) VALUES (?, ?, ?, ?, ?)",
        (data['first_name'], data['last_name'], data['department'], data['address'], data['email'])
    )
    conn.commit()
    new_id = cursor.lastrowid # lay id vua duoc tao
    conn.close()
    return jsonify({"message":"Them thanh cong", "Employee_id": new_id})

#CAU 3B - PUT: cap nhat thong tin employee
@app.route('/Employee', methods=['PUT'])
def update_Employee():
    data = request.get_json()
    employee_id = data['Employee_id']
    conn = get_db()
    conn.execute(
        "UPDATE Employee SET first_name=?, last_name=?, department=?, address=?, email=? WHERE Employee_id = ?",
        (data['first_name'], data['last_name'], data['department'], data['address'], data['email'], employee_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Da cap nhat Employee ID = {employee_id}"})

#CAU 4A: Kiem tra employee da ton tai theo Email + FirstName
@app.route('/Employee/check', methods=['GET'])
def check_Employee():
    #Nhan email va first_name tu query string: /Employee/check?email=...&first_name=...
    email = request.args.get('email')
    first_name = request.args.get('first_name')

    conn = get_db()
    #tim employee khop ca email va first_name
    result = conn.execute(
        "SELECT * FROM Employee WHERE email = ? AND first_name = ?",
        (email, first_name)
    ).fetchone()
    conn.close()

    if result:
        return jsonify({"exists": True, "employee": dict(result)})
    else:
        return jsonify({"exists": False, "message": "Khong tim thay Employee"})

#CAU 4B: Tim kiem Employee theo chuoi (LIKE trong sql)
@app.route('/Employee/search', methods=['GET'])
def search_Employee():
    #Nhan chuoi tim kiem tu query string: /Employee/search?q=...
    keyword = request.args.get('q', '')
    pattern = f'%{keyword}%' # dung LIKE de tim gan dung

    conn = get_db()
    #tim trong tat ca cac cot text
    results = conn.execute(
        "SELECT * FROM Employee WHERE first_name LIKE ? OR last_name LIKE ? OR department LIKE ? OR address LIKE ? OR email LIKE ?",
        (pattern, pattern, pattern, pattern, pattern)
    ).fetchall()
    conn.close()

    return jsonify([dict(r) for r in results])

#CAU 4C: lay danh sach don hang theo EmployeeID
#gia su co bang order lien ket voi employee
@app.route('/Employee/orders', methods=['GET'])
def get_orders_by_employee():
    #nhan employeeid tu query string
    employee_id = request.args.get('Employee_id')

    conn = get_db()
    #kiem tra employee ton tai
    emp = conn.execute(
        "SELECT * FROM Employee WHERE Employee_id = ?", (employee_id,)
    ).fetchone()

    if not emp:
        conn.close()
        return jsonify({"message":"Khong tim thay employee"}), 404

    #lay danh sach don hang (neu co bang orders)
    try:
        orders = conn.execute(
            "SELECT * FROM Orders WHERE Employee_id = ?", (employee_id,)
        ).fetchall()
        conn.close()
        return jsonify({"employee": dict(emp), "orders": [dict(o) for o in orders]})
    except:
        conn.close()
        return jsonify({"message": "Chua co bang order trong db", "employee": dict(emp)})

#CAU 4D: nhap hang loat danh sach khach hang
@app.route('/Employee/bulk', methods=['POST'])
def bulk_add_customers():
    #Nhan vao 1 list cac object khach hang
    data_list = request.get_json() # la 1 mang json

    conn = get_db()
    inserted_ids = []

    #lan luot insert tung ban ghi
    for data in data_list:
        cursor = conn.execute(
            "INSERT INTO Employee (first_name, last_name, department, address, email) VALUES (?,?,?,?)",
            (data['first_name'], data['last_name'], data['department'], data['address'], data['email'])
        )
        inserted_ids.append(cursor.lastrowid)

    conn.commit()
    conn.close()
    return jsonify({"message":f"Da them {len(inserted_ids)} ban ghi", "ids": inserted_ids})

#chay ung dung o cong 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)


