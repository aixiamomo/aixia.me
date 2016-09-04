# -*- coding: utf-8 -*-
from . import main
from app.models import Post, Tag
from flask import render_template, request, current_app, abort


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(publish=True).order_by(Post.create_date.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)  # 只显示提交了的文章
    if post.publish is None or False:
        abort(404)
    return render_template('post.html', post=post)


@main.route('/tag/<url_name>')
def tag(url_name):
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = tag.posts.order_by(Post.create_date.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('tag.html', tag=tag, posts=posts, pagination=pagination)
