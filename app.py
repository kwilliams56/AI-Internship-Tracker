from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            recruiter TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        recruiter = request.form["recruiter"]
        status = request.form["status"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (company, position, recruiter, status)
            VALUES (?, ?, ?, ?)
        """, (company, position, recruiter, status))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, position, recruiter, status FROM applications")
    applications = cursor.fetchall()
    conn.close()

    return render_template("index.html", applications=applications)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)