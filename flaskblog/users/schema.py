
from flaskblog import ma
from flaskblog.models import User

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'image_file', 'posts')


user_schema = UserSchema()
users_schema = UserSchema(many=True)