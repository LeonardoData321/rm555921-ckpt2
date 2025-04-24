from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados MySQL
db_config = {
    'host': '129.213.193.177',
    'user': 'aluno',
    'password': 'Aluno#1234',
    'database': 'pf0807'
}

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de busca de produtos
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        termo_busca = request.form['termo_busca']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produto WHERE nome LIKE %s", ('%' + termo_busca + '%',))
        produtos = cursor.fetchall()
        conn.close()
        return render_template('buscar.html', produtos=produtos)
    else:
        return render_template('buscar.html', produtos=[])

# Rota para a página de atualização de produtos
@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        data = request.form
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE produto SET nome = %s, valor = %s WHERE codigo = %s", (data['nome'], data['valor'], id))
        conn.commit()
        conn.close()
        return redirect(url_for('buscar'))
    else:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produto WHERE codigo = %s", (id,))
        produto = cursor.fetchone()
        conn.close()
        return render_template('atualizar.html', produto=produto)

if __name__ == '__main__':
    app.run(debug=True)