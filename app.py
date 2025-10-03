from flask import Flask, render_template, request, jsonify, redirect, url_for
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
        conn.commit()
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

@app.route('/contacts')
def contacts():
    if 'id' in request.args:
        id = request.args.get('id')
        if id:
            conn = sqlite3.connect('gestion_contact.db')
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM info wHERE ID = {id}")
            reponses = cur.fetchall()
            cur.close()
            conn.close()
            if len(reponses)>0:
                titre = "Résultats de la recherche"
                return render_template('contacts.html', list_contact = reponses, titre = titre)
            else:
                return "<p>Aucun résultat trouvé</p>"
        else:
            return "<p>Pas de résultat</p>"
    else:
        conn = sqlite3.connect('gestion_contact.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM info")
        reponses = cur.fetchall()
        cur.close()
        conn.close()
        titre = "Tous les contacts"
        return render_template('contacts.html', list_contact = reponses, titre = titre)
    

@app.route('/api/contacts')
def api_contacts():
    if 'id' in request.args:
        id = request.args.get('id')
        if id:
            conn = sqlite3.connect('gestion_contact.db')
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM info wHERE ID = {id}")
            reponses = cur.fetchall()
            cur.close()
            conn.close()
            if len(reponses)>0:
                return jsonify(reponses)
            else:
                return "<p>Aucun résultat trouvé</p>"
        else:
            return "<p>Pas de résultat</p>"
    else:
        conn = sqlite3.connect('gestion_contact.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM info")
        reponses = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(reponses)

@app.route('/contact/suppression')
def suppression():
    if 'id' in request.args and 'choix' in request.args:
        id = request.args.get('id')
        choix = request.args.get('choix')
        if choix == 'yes':
            conn = sqlite3.connect('gestion_contact.db')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS contact_supprime(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    old_id INTEGER,
                    contact TEXT,
                    inventaire TEXT)
                    ''')
            cur.execute(f"SELECT * FROM info WHERE id = {id}")
            reponses = cur.fetchall()
            print(reponses)
            insert = (reponses[0][0], reponses[0][1], reponses[0][2])
            sql = "INSERT INTO contact_supprime (old_id, contact, inventaire) VALUES (?, ?, ?)"
            cur.execute(sql, insert)
            conn.commit()
            cur.execute(f"DELETE FROM info WHERE id = {id}")
            conn.commit()
            cur.close()
            conn.close()
        return redirect(url_for("contacts"))
    elif 'id' in request.args and 'choix' not in request.args:
        id = request.args.get('id')
        return render_template('delete.html', id=id)
    else:
        return redirect(url_for('home'))

@app.route('/contact/update')
def update():
    id = request.args.get('id')
    # conn = sqlite3.connect('gestion_contact.db')
    # cur = conn.cursor()
    # cur.close()
    # conn.close()
    return "<p>Le script de mise à jour n'est pas encore établi</p>"

@app.route('/test')
def test():
    conn = sqlite3.connect('gestion_contact.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM contact_supprime")
    reponses = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(reponses)

if __name__ == '__main__':
    app.run(debug=True)