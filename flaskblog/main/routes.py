from flask import render_template, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    """
        This method is responsible to display all posts on the main home page.
        """
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    """
        This method takes us to the about's page"
        """
    return render_template('about.html', title='About')