from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'projeto-academico-local'
DB = Path(__file__).with_name('estoque.db')

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def iniciar():
    with conectar() as db:
        db.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, categoria TEXT NOT NULL, quantidade INTEGER NOT NULL DEFAULT 0, minimo INTEGER NOT NULL DEFAULT 5)')
        db.execute('CREATE TABLE IF NOT EXISTS movimentacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER NOT NULL, tipo TEXT NOT NULL, quantidade INTEGER NOT NULL, data TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(produto_id) REFERENCES produtos(id))')

@app.route('/')
def inicio():
    busca = request.args.get('busca', '').strip()
    with conectar() as db:
        produtos = db.execute('SELECT * FROM produtos WHERE nome LIKE ? OR categoria LIKE ? ORDER BY nome', (f'%{busca}%', f'%{busca}%')).fetchall()
        total = db.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
        baixos = db.execute('SELECT COUNT(*) FROM produtos WHERE quantidade <= minimo').fetchone()[0]
        movimentos = db.execute('SELECT m.data, m.tipo, m.quantidade, p.nome FROM movimentacoes m JOIN produtos p ON p.id=m.produto_id ORDER BY m.id DESC LIMIT 8').fetchall()
    return render_template('index.html', produtos=produtos, total=total, baixos=baixos, movimentos=movimentos, busca=busca)

@app.post('/produto')
def adicionar():
    nome = request.form.get('nome','').strip()
    categoria = request.form.get('categoria','').strip()
    try:
        quantidade = int(request.form.get('quantidade','0'))
        minimo = int(request.form.get('minimo','5'))
        if not nome or not categoria or quantidade < 0 or minimo < 0: raise ValueError()
    except ValueError:
        flash('Confira os dados do produto.', 'erro')
        return redirect(url_for('inicio'))
    with conectar() as db:
        db.execute('INSERT INTO produtos (nome,categoria,quantidade,minimo) VALUES (?,?,?,?)', (nome,categoria,quantidade,minimo))
    flash('Produto cadastrado!', 'ok')
    return redirect(url_for('inicio'))

@app.post('/movimentar/<int:produto_id>')
def movimentar(produto_id):
    tipo = request.form.get('tipo')
    try:
        quantidade = int(request.form.get('quantidade','0'))
        if tipo not in ('entrada','saida') or quantidade <= 0: raise ValueError()
    except ValueError:
        flash('Movimentação inválida.', 'erro')
        return redirect(url_for('inicio'))
    with conectar() as db:
        produto = db.execute('SELECT quantidade FROM produtos WHERE id=?',(produto_id,)).fetchone()
        if produto is None or (tipo == 'saida' and produto['quantidade'] < quantidade):
            flash('Produto inexistente ou estoque insuficiente.', 'erro')
            return redirect(url_for('inicio'))
        saldo = produto['quantidade'] + (quantidade if tipo == 'entrada' else -quantidade)
        db.execute('UPDATE produtos SET quantidade=? WHERE id=?',(saldo,produto_id))
        db.execute('INSERT INTO movimentacoes (produto_id,tipo,quantidade) VALUES (?,?,?)',(produto_id,tipo,quantidade))
    flash('Estoque atualizado!', 'ok')
    return redirect(url_for('inicio'))

@app.post('/excluir/<int:produto_id>')
def excluir(produto_id):
    with conectar() as db:
        db.execute('DELETE FROM movimentacoes WHERE produto_id=?',(produto_id,))
        db.execute('DELETE FROM produtos WHERE id=?',(produto_id,))
    flash('Produto excluído.', 'ok')
    return redirect(url_for('inicio'))

iniciar()
if __name__ == '__main__':
    app.run(debug=True)
