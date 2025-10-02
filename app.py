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
    if 'type' in request.args:
        type = request.args.get('type')
        if type:
            conn = sqlite3.connect('gestion_contact.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM info")
            reponses = cur.fetchall()
            cur.close()
            conn.close()
            if len(reponses)>0:
                if type == "api":
                    return jsonify(reponses)
                elif type == "all":
                    titre = "Tous les contacts"
                    return render_template('contacts.html', list_contact = reponses, titre = titre)
                else:
                    return "<p>Pas de résultat</p>"
            else:
                return "<p>Pas encore de contact</p>"
        else:
            return "<p>Pas de résultat</p>"
    elif 'index' in request.args:
        index = request.args.get('index')
        if index:
            conn = sqlite3.connect('gestion_contact.db')
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM info wHERE ID = {index}")
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
        return redirect("/contacts?type=all")

@app.route('/contact/suppression')
def suppression():
    id = request.args.get('id')
    # conn = sqlite3.connect('gestion_contact.db')
    # cur = conn.cursor()
    # cur.close()
    # conn.close()
    return "<p>Le script de suppression n'est pas encore établi</p>"

@app.route('/contact/update')
def update():
    id = request.args.get('id')
    # conn = sqlite3.connect('gestion_contact.db')
    # cur = conn.cursor()
    # cur.close()
    # conn.close()
    return "<p>Le script de mise à jour n'est pas encore établi</p>"

if __name__ == '__main__':
    app.run(debug=True)