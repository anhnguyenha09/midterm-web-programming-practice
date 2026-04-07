#Cau1: Câu 1: Tạo web và dữ liệu (2 điểm)
#a) Tạo một ứng dụng Project Web Flask Python import các thư viện Flask, SQLite, Json và
#đặt tên biến trỏ tới cơ sở dữ liệu ShoppingDB.db
#b) Tạo hàm Index để khi web này hiện lên, sẽ hiện thông tin của sinh viên bao gồm
#STT_HoVaTen_MaDe
#c) Hãy tạo file json gồm 5 bản ghi tương ứng để nhập dữ liệu vào bảng sau Customer gồm
#các thông tin sau đây: "customer_id", "first_name", "last_name", "company", "address",
#"email"
#a
import sqlite3
import json
from flask import Flask, render_template, request, jsonify

app = Flask(_name_)
db_name = 'ShoppingDB.db'
#b
@app.route('/')
def index():
    return "_LeThiLinh_01"
#c
def get_db():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

#Câu 2: Tạo các API cơ bản (2 điểm)
#a) Hãy tạo hàm get_Customer với định tuyến cho hàm @app.route('/Customers',
#methods=['GET']): Hàm này sẽ đọc toàn bộ dữ liệu từ bảng Customer và trả về dạng Json
#b) Hãy tạo hàm delete_Customer với định tuyến cho hàm @app.route('/Customers',
#methods=[' DELETE']): Hàm này sẽ tuyền vào ID của 1 đối tượng Customer, và sẽ xóa dữ
#liệu bản ghi này
# GET all customers
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # tạo bảng Customer
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        company TEXT,
        address TEXT,
        email TEXT
    )
    """)

    # đọc file json
    with open("customers_db.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # insert dữ liệu
    for c in data:
        cur.execute("""
        INSERT OR IGNORE INTO Customer VALUES (?, ?, ?, ?, ?, ?)
        """, (
            c["customer_id"],
            c["first_name"],
            c["last_name"],
            c["company"],
            c["address"],
            c["email"]
        ))

    conn.commit()
    conn.close()
@app.route('/Customers', methods=['GET'])
def get_customers():
    conn = get_db()
    customers = conn.execute("SELECT * FROM Customer").fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers])

# DELETE customer by id
@app.route('/Customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    conn = get_db()
    conn.execute("DELETE FROM Customer WHERE customer_id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted successfully"})

#Câu 3: Tạo các API nâng cao (2 điểm)
#a) Hãy tạo hàm add_Customer với định tuyến cho hàm @app.route('/Customers',
#methods=['POST']): Hàm này sẽ tuyền vào 1 đối tượng Customer, và lưu vào cơ sở dữ liệu
#rồi trả ra Id mới nhất của bản ghi vừa được truyền vào
#b) Hãy tạo hàm update_Customer với định tuyến cho hàm @app.route('/Customers',
#methods=[' PUT]): Hàm này sẽ tuyền vào ID của 1 đối tượng Customer. Hàm này sẽ nhận
#giá trị ID và các thông tin khác của Customer rồi cập nhật các thông tin Customer này

#a
@app.route('/Customers', methods=['POST'])
def add_customer():
    data = request.get_json()  #lấy dữ liê từ body
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO Customer (first_name, last_name, email, company, address) VALUES (?, ?, ?, ?, ?)", (
        data["first_name"],
        data["last_name"],
        data["email"],
        data["company"],
        data["address"]
    ))
    conn.commit()
    new_id = cur.lastrowid #lấy id vừa thêm
    conn.close()
    return jsonify({"message": "Customer added successfully: " + str(new_id)})
#b
@app.route('/Customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE Customer SET first_name = ?, last_name = ?, email = ?, company = ?, address = ? WHERE customer_id = ?",  (
        data["first_name"],
        data["last_name"],
        data["email"],
        data["company"],
        data["address"],
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer updated successfully: " + str(id)})
#Câu 4: Sáng tạo API mới (2 điểm)
#Hãy tạo và mô tả hoạt động chi tiết của các method sau đây (comment đầy đủ vào từng hoạt động
#chính trong hàm):
#a) Tạo một method để nhận vào một Email và FirstName, Hàm này sẽ trả về Json của chỉ ra
#Customer này có tồn tại trong CSDL hay không?
#b) Tạo method để nhận vào một chuỗi tìm kiếm. Hàm này sẽ trả về Json của những bản ghi
#Customer mà có thông tin hoặc là "first_name", "last_name", "company", "address",
#"email" gần đúng với nội dung chuỗi tìm kiếm
#c) Tạo một method để nhận vào CustomerID, hệ thống sẽ trả về danh sách các đơn hàng mà
#khách hàng này đã mua
#d) Tạo một method để nhận vào một danh sách khách hàng, hệ thống sẽ lần lượt nhập toàn bộ
#danh sách này vào cơ sở dữ liệu/
# a) Kiểm tra tồn tại theo Email + FirstName
@app.route('/checkCustomer', methods=['GET'])
def check_customer():
    # 1. Nhận dữ liệu từ request (query params)
    email = request.args.get('email')
    first_name = request.args.get('first_name')

    # 2. Kết nối tới cơ sở dữ liệu
    conn = get_db()
    cur = conn.cursor()

    # 3. Thực hiện truy vấn kiểm tra xem có Customer nào thỏa mãn điều kiện không
    cur.execute("""
        SELECT * FROM Customer
        WHERE email = ? AND first_name = ?
    """, (email, first_name))

    # 4. Lấy 1 bản ghi đầu tiên (nếu có)
    result = cur.fetchone()

    # 5. Đóng kết nối DB
    conn.close()

    # 6. Trả về kết quả dạng JSON
    if result:
        return jsonify({"exists": True})   # tồn tại
    else:
        return jsonify({"exists": False})  # không tồn tại

# b) Tìm kiếm gần đúng theo keyword
@app.route('/searchCustomer', methods=['GET'])
def search_customer():
    # 1. Nhận chuỗi tìm kiếm từ request
    keyword = request.args.get('q')

    # 2. Kết nối database
    conn = get_db()
    cur = conn.cursor()

    # 3. Thực hiện truy vấn với LIKE để tìm kiếm gần đúng
    cur.execute("""
        SELECT * FROM Customer
        WHERE first_name LIKE ?
        OR last_name LIKE ?
        OR company LIKE ?
        OR address LIKE ?
        OR email LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    # 4. Lấy tất cả kết quả
    rows = cur.fetchall()

    # 5. Chuyển dữ liệu sang dạng list JSON
    result = [dict(row) for row in rows]

    # 6. Đóng kết nối
    conn.close()

    # 7. Trả về kết quả
    return jsonify(result)

# c) Lấy danh sách đơn hàng theo CustomerID
@app.route('/orders/<int:customer_id>', methods=['GET'])
def get_orders(customer_id):
    # 1. Nhận customer_id từ URL

    # 2. Kết nối database
    conn = get_db()
    cur = conn.cursor()

    # 3. Truy vấn danh sách đơn hàng theo customer_id
    # (Giả sử bảng Orders đã tồn tại và có cột customer_id)
    cur.execute("""
        SELECT * FROM Orders
        WHERE customer_id = ?
    """, (customer_id,))

    # 4. Lấy danh sách đơn hàng
    rows = cur.fetchall()

    # 5. Chuyển sang JSON
    result = [dict(row) for row in rows]

    # 6. Đóng kết nối
    conn.close()

    # 7. Trả về kết quả
    return jsonify(result)
# d) Thêm danh sách nhiều khách hàng vào DB
@app.route('/bulkInsert', methods=['POST'])
def bulk_insert():
    # 1. Nhận dữ liệu JSON từ request (danh sách khách hàng)
    data = request.json

    # 2. Kết nối database
    conn = get_db()
    cur = conn.cursor()

    # 3. Duyệt từng khách hàng trong danh sách
    for customer in data:
        # 4. Thực hiện insert từng bản ghi
        cur.execute("""
            INSERT INTO Customer(first_name, last_name, company, address, email)
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer['first_name'],
            customer['last_name'],
            customer['company'],
            customer['address'],
            customer['email']
        ))

    # 5. Lưu thay đổi vào database
    conn.commit()

    # 6. Đóng kết nối
    conn.close()

    # 7. Trả về thông báo thành công
    return jsonify({"message": "Inserted all customers successfully"})
# =========================
# CÂU 5: WEB HIỂN THỊ
# =========================

@app.route('/view')
def view():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Customer")
    rows = cur.fetchall()

    return render_template("index.html", customers=rows)



if _name_ == "_main_":
    init_db()
    app.run(debug=True)