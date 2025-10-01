from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        donnees = request.form
        contact = donnees.get('contact')
        inventaire = donnees.get('inventaire')
        insert = (contact, inventaire)
        conn = sqlite3.connect('gestion_contact.db')
        cur = conn.cursor()
        sql = "INSERT INTO info (contact, inventaire) VALUES (?, ?)"
        cur.execute(sql, insert)
        conn.commit
        cur.close()
        conn.close()
        return render_template('index.html')
    else:
        conn = sqlite3.connect('gestion_contact.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS info(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact TEXT,
                    inventaire TEXT)
                    ''')
        cur.close()
        conn.close()
        return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)