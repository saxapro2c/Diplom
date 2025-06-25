from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("diplom2.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/comments/<int:news_id>", methods=["GET"])
def get_comments(news_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_login, text, created_at FROM Comments WHERE news_id=?", (news_id,))
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO Comments (news_id, user_login, text) VALUES (?, ?, ?)",
                (data["news_id"], data["user_login"], data["text"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["GET"])
def get_chat():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT login, message, timestamp FROM TeacherChat ORDER BY timestamp")
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/chat", methods=["POST"])
def send_message():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO TeacherChat (login, message) VALUES (?, ?)", (data["login"], data["message"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/check_user", methods=["POST"])
def check_user():
    data = request.json
    login, password = data.get("login"), data.get("password")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Account_Data WHERE login=? AND password=?", (login, password))
    result = cur.fetchone()
    conn.close()
    return jsonify({"valid": result is not None})

@app.route("/user_role/<string:login>", methods=["GET"])
def user_role(login):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT role FROM Account_Data WHERE login=?", (login,))
    row = cur.fetchone()
    conn.close()
    return jsonify({"role": row["role"] if row else "студент"})

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    login = data["login"]
    password = data["password"]
    role = data["role"]
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Account_Data (login, password, role) VALUES (?, ?, ?)", (login, password, role))
        conn.commit()
        return jsonify({"status": "ok"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Login already exists"}), 400
    finally:
        conn.close()

@app.route("/like", methods=["POST"])
def add_like():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM Likes WHERE news_id=? AND user_login=?", (data["news_id"], data["user_login"]))
    if not cur.fetchone():
        cur.execute("INSERT INTO Likes (news_id, user_login) VALUES (?, ?)", (data["news_id"], data["user_login"]))
        conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/like/<int:news_id>", methods=["GET"])
def count_likes(news_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS count FROM Likes WHERE news_id=?", (news_id,))
    count = cur.fetchone()["count"]
    conn.close()
    return jsonify({"count": count})

@app.route("/specialty_like", methods=["POST"])
def add_specialty_like():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""INSERT OR IGNORE INTO SpecialtyLikes (specialty_id, user_login)
                   VALUES (?, ?)""", (data["specialty_id"], data["user_login"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/specialty_like/<int:specialty_id>", methods=["GET"])
def count_specialty_likes(specialty_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS count FROM SpecialtyLikes WHERE specialty_id=?", (specialty_id,))
    count = cur.fetchone()["count"]
    conn.close()
    return jsonify({"count": count})

@app.route("/news", methods=["GET"])
def get_all_news():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM News ORDER BY created_at DESC")
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/news", methods=["POST"])
def upload_news():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT OR IGNORE INTO News (title, content, image_path, external_link)
            VALUES (?, ?, ?, ?)
        """, (data["title"], data["content"], data["image_path"], data["external_link"]))
        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

@app.route("/specialties", methods=["GET"])
def get_specialties():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, code, name, descript, places, pass_score FROM Specialties")
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
