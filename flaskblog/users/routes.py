from flask import render_template, redirect, url_for, request, flash, Blueprint
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_required, logout_user, current_user, login_user
from flaskblog import db
from flaskblog.models import User
from flaskblog import bcrypt
from flaskblog.users.utils import save_picture
from flask_restful import Resource, Api
from flaskblog.users.schema import user_schema, users_schema


users = Blueprint('users', __name__)
users_api = Api(users)

class GetUser(Resource):
    def get(self, id):
        """
        This endpoint is used to get the user info.
        """
        users = list(User.query.all())
        user = next(filter(lambda x: x.id == int(id), users), None)
        if user is not None:
            return user_schema.dump(user), 200
        return {"message": f"User with id {id} doesn't exist!"}, 404

class ListUsers(Resource):
    def get(self):
        """
        This endpoint lists all the users we have in the database.
        """
        users = User.query.all()
        return users_schema.dump(users), 200

class UpdateAccount(Resource):
    def post(self, id):
        """
        This endpoint update the account information for user.
        """
        user = User.query.filter_by(id=id).first()
        if user:
            print(request.json)
            user.username = request.json['username']
            user.email = request.json['email']
            db.session.commit()
            print(user)
            return user_schema.dump(user), 204
        return {"message": "User with this ID doesn't exist!"}, 404

users_api.add_resource(GetUser, '/users/<string:id>')
users_api.add_resource(ListUsers, '/users')
users_api.add_resource(UpdateAccount, '/updateAccount/<string:id>')


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
        This endpoint is responsible for authenticating the user while login.
        """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """
        This endpoint is used to logout the user.
        """
    logout_user()
    return redirect(url_for('main.home'))


# @users.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)





