from flask import Flask, render_template
from flask_mysqldb import MySQL
import pymysql
import os

# Tell flask-mysqldb to use pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- MYSQL CONFIG (RENDER / CLOUD) ----------------

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        return render_template('index.html', events=events)
    except Exception as e:
        return f"MySQL Error: {e}"

# ---------------- MAIN ----------------

if __name__ == "__main__":
    app.run(host='0.0.0',debug=True)
