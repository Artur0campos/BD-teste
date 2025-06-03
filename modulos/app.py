from flask import Flask, flash, redirect, render_template, request, url_for

from modulos.data_base import (atualizar_assinante, deletar_assinante,
                               inserir_assinante, listar_assinantes,
                               obter_assinante_por_id)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    try:
        assinantes = listar_assinantes()
        return render_template('index.html', assinantes=assinantes)
    except Exception as e:
        flash(f"Erro ao listar assinantes: {str(e)}", "danger")
        return render_template('index.html', assinantes=[])

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        fk_cd_tipo = request.form['fk_cd_tipo']
        fk_cd_ramo = request.form['fk_cd_ramo']
        
        try:
            inserir_assinante(nome, fk_cd_tipo, fk_cd_ramo)
            flash("Assinante adicionado com sucesso!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), "danger")
    
    return render_template('adicionar.html')

@app.route('/editar/<int:cd_assinante>', methods=['GET', 'POST'])
def editar(cd_assinante):
    if request.method == 'POST':
        nome = request.form['nome']
        fk_cd_tipo = request.form['fk_cd_tipo']
        fk_cd_ramo = request.form['fk_cd_ramo']
        
        try:
            atualizar_assinante(cd_assinante, nome, fk_cd_tipo, fk_cd_ramo)
            flash("Assinante atualizado com sucesso!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), "danger")
    
    try:
        assinante = obter_assinante_por_id(cd_assinante)
        if not assinante:
            flash("Assinante não encontrado!", "danger")
            return redirect(url_for('index'))
        return render_template('editar.html', assinante=assinante)
    except Exception as e:
        flash(f"Erro ao carregar assinante: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/deletar/<int:cd_assinante>')
def deletar(cd_assinante):
    try:
        deletar_assinante(cd_assinante)
        flash("Assinante deletado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao deletar assinante: {str(e)}", "danger")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)