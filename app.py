from flask import Flask, render_template, request
import sqlite3
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# SQLite Database Connection
db = sqlite3.connect("contacts.db", check_same_thread=False)

cursor = db.cursor()

# Create Table Automatically
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT
)
""")

db.commit()


@app.route("/", methods=["GET", "POST"])
def form():

    if request.method == "POST":

        # Get Form Data
        name = request.form["name"]
        contact = request.form["contact"]

        # Save Data Into SQLite
        sql = "INSERT INTO contacts (name, contact) VALUES (?, ?)"

        values = (name, contact)

        cursor.execute(sql, values)

        db.commit()

        # EMAIL SECTION

        sender_email = os.getenv("EMAIL")
        
        sender_password = os.getenv("PASSWORD")

        receiver_email = "bhavyarathore5551@gmail.com"

        body = f"""
New Contact Submission

Name: {name}

Contact: {contact}
"""

        msg = MIMEText(body)

        msg["Subject"] = "New Contact Form"

        msg["From"] = sender_email

        msg["To"] = receiver_email

        # Connect To Gmail Server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        # Login
        server.login(sender_email, sender_password)

        # Send Email
        server.send_message(msg)

        # Close Server
        server.quit()

        return "Form Submitted Successfully!"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)