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
            status TEXT NOT NULL,
            date_applied TEXT
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
        date_applied = request.form["date_applied"]
        status = request.form["status"]

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (company, position, recruiter, status, date_applied)
            VALUES (?, ?, ?, ?, ?)
        """, (company, position, recruiter, status, date_applied))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    search = request.args.get("search")

    if search:
        cursor.execute("""
            SELECT id, company, position, recruiter, status, date_applied
            FROM applications
            WHERE company LIKE ?
        """, ("%" + search + "%",))
    else:
        cursor.execute("""
            SELECT id, company, position, recruiter, status, date_applied
            FROM applications
        """)

    applications = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'")
    applied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Interview'")
    interview = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Offer'")
    offer = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        applications=applications,
        total=total,
        applied=applied,
        interview=interview,
        offer=offer,
        rejected=rejected
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        recruiter = request.form["recruiter"]
        date_applied = request.form["date_applied"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE applications
            SET company = ?, position = ?, recruiter = ?, status = ?, date_applied = ?
            WHERE id = ?
        """, (company, position, recruiter, status, date_applied, id))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("""
        SELECT id, company, position, recruiter, status, date_applied
        FROM applications
        WHERE id = ?
    """, (id,))

    application = cursor.fetchone()
    conn.close()

    return render_template("edit.html", application=application)

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