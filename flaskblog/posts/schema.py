from flaskblog import ma
from flaskblog.models import Post
from flaskblog.users.schema import UserSchema

class PostSchema(ma.Schema):
    user_id = ma.Nested(UserSchema, many=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'date_posted', 'content', 'user_id')


post_schema = PostSchema()
posts_schema = PostSchema(many=True)