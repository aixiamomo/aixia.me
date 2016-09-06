# -*- coding: utf-8 -*-
from . import main
from app.models import Post, Tag, User
from flask import render_template, request, current_app, abort


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(1)
    pagination = Post.query.filter_by(publish=True).order_by(Post.publish_date.desc()).paginate(
        page, per_page=user.Posts_per_page,
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, user=user)


@main.route('/post/<url_name>')
def post(url_name):
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    page = post.id
    pagination = Post.query.filter_by(publish=True).order_by(Post.publish_date.desc()).paginate(
        page, per_page=1,
        error_out=False
    )
    user = User.query.get_or_404(1)
    if post.publish is None or False:  # 只显示提交了的文章
        abort(404)
    return render_template('post.html', post=post, pagination=pagination, user=user)


@main.route('/tag/<url_name>')
def tag(url_name):
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(1)
    pagination = tag.posts.order_by(Post.publish_date.desc()).paginate(
        page, per_page=user.Posts_per_page,
        error_out=False
    )
    posts = pagination.items
    return render_template('tag.html', tag=tag, posts=posts, pagination=pagination, user=user)
