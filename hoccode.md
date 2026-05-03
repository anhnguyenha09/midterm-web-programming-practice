Sự khác biệt quan trọng: .get() vs []
Dùng .get() (an toàn hơn)
username = request.args.get('username')
Nếu không có username → trả về None
Không crash
Phù hợp với API (client có thể không truyền)
Dùng [] (nguy hiểm hơn)
username = request.args['username']
Nếu thiếu param → crash ngay:
BadRequestKeyError: 'username'
5. Khi nào nên dùng cái nào?
Dùng .get() khi:
Param optional
API cần linh hoạt
Dùng [] khi:
Param bắt buộc
Bạn muốn fail ngay nếu thiếu

Nhưng thực tế, người ta thường viết rõ hơn:

username = request.args.get('username')
if not username:
    return jsonify({'error': 'username is required'}), 400

=> kiểm soát được lỗi → clean hơn

6. Insight quan trọng (rất nên nhớ)

.get() = “cho tao xin, không có cũng được”
[] = “phải có, không có là tao crash”


1. Quy tắc cốt lõi (chỉ cần nhớ đúng 1 câu)

Server (Flask) làm việc bằng Python object,
Client (Postman) nhận JSON

2. Dòng code của bạn đang làm gì?
return jsonify([dict(row) for row in users])

Tách từng lớp:

Bước 1: users
là list các sqlite3.Row
Bước 2: dict(row)
chuyển từng row → dict

Ví dụ:

row = ('anh', 'a@gmail.com')

→

dict(row) = {
  "username": "anh",
  "email": "a@gmail.com"
}
Bước 3: [dict(row) for row in users]

→ tạo list:

[
  {"username": "anh", "email": "a@gmail.com"},
  {"username": "binh", "email": "b@gmail.com"}
]
Bước 4: jsonify(...)
chuyển Python list/dict → JSON
set luôn header:
Content-Type: application/json
3. Tại sao không trả thẳng dict/list?

Bạn có thể:

return {"username": "anh"}

Flask vẫn hiểu (new version OK)

NHƯNG:

return jsonify(...)

là:

chuẩn hơn
rõ ràng hơn
tránh bug edge-case
4. Vậy “quy tắc API” thực sự là gì?

Không hề loạn đâu, nó chỉ là 1 pipeline:

INPUT (client → server)

Client gửi:

{
  "username": "anh"
}

Flask nhận:

data = request.get_json()  # dict
XỬ LÝ (server)

Bạn làm việc bằng Python:

data['username']
OUTPUT (server → client)

Bạn trả:

return jsonify(data)

Flask gửi:

{
  "username": "anh"
}
5. Tại sao phải dict(row)?

Vì:

sqlite3.Row không phải JSON serializable
jsonify không hiểu nó

=> phải convert:

dict(row)
6. Ví dụ “sai” để bạn thấy rõ
return jsonify(users)

=> lỗi kiểu:

TypeError: Object of type Row is not JSON serializable
7. Cách nghĩ cho đỡ lú (rất quan trọng)

Đừng nghĩ:

“API phải trả JSON nên phải dùng dict…”

Mà hãy nghĩ:

“Backend luôn dùng Python object
→ trước khi trả về thì convert sang JSON”

8. Mental model chuẩn (nên thuộc)
DB → Row → dict → list → jsonify → JSON → Postman
9. Viết lại theo kiểu “dễ hiểu hơn”
users_list = []

for row in users:
    users_list.append(dict(row))

return jsonify(users_list)

=> giống y hệt, chỉ là dễ đọc hơn comprehension

10. Chốt lại cho bạn (rất gọn)
DB → trả về Row
Python → xử lý bằng dict/list
API → trả JSON
jsonify = cầu nối


à mà nói chuyện get()
cái username tui để trong db là bắt buộc đó (not null)

nếu như tui để trống username khi post thì chuyện gì sẽ xảy ra?

nếu như tui để trống username khi post nhưng viết là  u [username] thì chuyện gì sẽ xảy ra?


Câu này rất hay vì nó đụng đúng ranh giới giữa Python layer và database layer. Mình tách rõ từng case để bạn không bị “lú” nữa.

1. Trường hợp dùng u.get('username')
u.get('username')
Case A: client KHÔNG gửi field username
{
  "email": "a@gmail.com",
  "class_id": 1
}

→ u.get('username') = None

→ SQL chạy:

username = NULL

→ nhưng DB của bạn có NOT NULL

=> Kết quả:

Lỗi ngay tại database
sqlite3.IntegrityError: NOT NULL constraint failed

Case B: client gửi nhưng để rỗng
{
  "username": "",
  "email": "a@gmail.com",
  "class_id": 1
}

→ u.get('username') = "" (chuỗi rỗng, KHÔNG phải NULL)

→ SQL:

username = ""

=> SQLite cho qua vì:

"" ≠ NULL

=> Không lỗi, nhưng:

Data bẩn (username rỗng)

2. Trường hợp dùng u['username']
u['username']
Case A: KHÔNG có key username
{
  "email": "a@gmail.com"
}

=> Python nổ ngay:

KeyError: 'username'

→ code dừng luôn, chưa kịp xuống DB

Case B: có key nhưng rỗng
{
  "username": "",
  "email": "a@gmail.com"
}

→ u['username'] = ""

→ SQL vẫn insert bình thường

=> giống hệt .get()

3. So sánh nhanh cho bạn
Tình huống	u.get()	u['']
Thiếu key	None → lỗi DB (NOT NULL)	KeyError (lỗi Python)
Có key = ""	insert bình thường	insert bình thường
4. Insight cực quan trọng (nên nhớ)

Database chỉ chặn NULL, không chặn ""

=> nếu bạn không validate:

API của bạn vẫn có thể chứa dữ liệu rác

5. Cách viết chuẩn (backend xịn sẽ làm)

Không phụ thuộc vào get hay [], mà:

username = u.get('username')

if not username:
    return jsonify({'error': 'username is required'}), 400

if not username sẽ bắt luôn:

None
""
" " (nếu strip thêm)
6. Nếu muốn chặt chẽ hơn
username = u.get('username')

if not username or not username.strip():
    return jsonify({'error': 'username cannot be empty'}), 400
7. Chốt lại cho bạn (rất gọn)
get() → an toàn, không crash
[] → strict, thiếu là chết ngay
DB NOT NULL → chỉ chặn None, không chặn ""
validate ở backend là bắt buộc
Một câu nhớ lâu

get() cứu bạn khỏi crash
nhưng chỉ validation mới cứu data của bạn