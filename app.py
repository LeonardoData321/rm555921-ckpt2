from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados MySQL
db_config = {
    'host': '129.213.193.177',
    'user': 'aluno',
    'password': 'Aluno#1234',
    'database': 'pf0807'
}

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de busca
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

# Página para adicionar produto
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produto (nome, valor) VALUES (%s, %s)", (nome, valor))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('adicionar.html')

# Página para atualizar produto
@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        data = request.form
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE produto SET nome = %s, valor = %s WHERE codigo = %s",
                       (data['nome'], data['valor'], id))
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
