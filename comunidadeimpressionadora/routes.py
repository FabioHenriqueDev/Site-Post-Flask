from flask import render_template, flash, redirect, url_for, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


lista_usuarios = ['Fábio', 'Lira', 'Mariana', 'Diogo', 'Lucena']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form: # Se o formulario login for validado quando clicar em Fazer Login
        # Login Bem Sucedido
        usuario = Usuario.query.filter_by(email=form_login.email_login.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha_login.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)

            flash(f'Login feito com sucesso no E-mail: {form_login.email_login.data}', 'alert-success')
            par_next = request.args.get('next')

            if par_next:
                return redirect(par_next)

            else:
                return redirect(url_for('home'))

        else:
            flash('Falha no Login. E-mail ou Senha incorretos', 'alert-danger')


    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #senha criptografada
        senha_criptografada = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # Criar usuario
        usuario = Usuario(
                          username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_criptografada
                         )

        database.session.add(usuario)
        database.session.commit()



        flash(f'Conta Criada para o E-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))


    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso!', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        database.session.commit()
        flash('Perfil Atualizado com Sucesso!', 'alert-success')
        return redirect(url_for('perfil'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)