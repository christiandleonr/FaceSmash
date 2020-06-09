from flask import Flask, g, render_template, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, AnonymousUserMixin
from flask_bcrypt import check_password_hash
import models
import forms

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'as5d65as4d5a5s4c87as5d47asc8.as,asd.,asd.,'


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Invitado'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # The view that login manager will open
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def load_user(userid):
    """This method that we define is used for specify how we obtain the users in our app"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect the database before each request """
    g.db = models.DB
    if g.db.is_closed():
        g.db.connect()
        g.user = current_user


@app.after_request
def after_request(response):
    """Close the connection to the database"""
    g.db.close()
    return response


@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 0:
        abort(404)
    return render_template('stream.html', stream=posts)


@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash('now you follow to {}'.format(to_user.username), 'success')

    return redirect(url_for('stream', username=to_user.username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user = g.user._get_current_object(),
                to_user = to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash('yo have stopped following {}'.format(to_user.username), 'success')

    return redirect(url_for('stream', username=to_user.username))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('¡You have been registered!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Your username or password does not exist', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have logged in', 'success')
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have left FaceSmash', 'success')
    return redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),
                           content=form.content.data.strip())
        flash('Posted message', 'success')
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            streams = user.posts.limit(100)
    else:
        streams = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'

    return render_template(template, stream=streams, user=user)


@app.route('/')
def index():
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream=stream)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    try:
        models.initialize()
    except ValueError:
        print('error')
    app.run(debug=DEBUG, host=HOST, port=PORT)