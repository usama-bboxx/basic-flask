from flask import render_template, redirect, url_for, flash, abort, request, Blueprint
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask_restful import Resource, Api
from flaskblog.posts.schema import post_schema, posts_schema

posts = Blueprint('posts', __name__)
posts_api = Api(posts)


class GetPost(Resource):
    def get(self, id):
        """
        This endpoint is used to get the post info.
        """
        post = None
        try:
            post = Post.query.get(id=int(id))
        except:
            pass
        if post:
            return post_schema.dump(post), 200
        return {"message": f"Post with ID {id} doesn't exists!"}
    
    def post(self):
        """
        This endpoint is used to add new posts.
        """
        title = request.json['title']
        content = request.json['content']
        new_post = Post(title=title, content=content, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post), 201

    def delete(self, id):
        """
        This endpoint is used to delete the post.
        """
        post = None
        try:
            post = Post.query.get(id=int(id))
        except:
            pass
        if post:
            db.session.delete(post)
            db.session.commit()
            return {"message": "Post has been deleted successfully!"}
        return {"message": f"Post with ID {id} doesn't exists!"}
    
    def put(self, id):
        """
        This endpoint is used to update the post info.
        """
        post = None
        try:
            post = Post.query.get(id=int(id))
        except:
            pass
        if post:
            post.title = request.json['title']
            post.content = request.json['content']
            db.session.commit()
            return post_schema.dump(post)

        return {"message": f"Post with ID {id} doesn't exists!"}

class ListPost(Resource):
    def get(self):
        """
        This endpoint is used to list all posts.
        """
        posts = Post.query.all()
        return posts_schema.dump(posts)

# @posts.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, content=form.content.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_post.html', title='New Post',
#                            form=form, legend='New Post')


# @posts.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)


# @posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('posts.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')


# @posts.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('main.home'))