# -*- coding: utf-8 -*-
from . import admin
from .forms import LoginForm, SettingForm, EditorForm
from ..models import User, Post, Tag
from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, login_user, logout_user, current_user  # 保护路由只让认证用户登陆, 保存登陆用户


@admin.route('/')
@login_required
def index():
    """后台首页"""
    return render_template('admin.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=True)  # True，在cookie中写入长期有效的cookie
            return redirect(request.args.get('next') or url_for('admin.index'))  # 后台默认页
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@login_required
@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@login_required
@admin.route('/settings', methods=['GET', 'POST'])
def setting():
    """博客设置"""
    form = SettingForm()
    if form.validate_on_submit():
        current_user.blog_title = form.blog_title.data
        current_user.blog_description = form.blog_description.data
        current_user.blog_cover = form.blog_cover.data
        current_user.Posts_per_page = form.Posts_per_page.data
        current_user.author_detail = form.author_detail.data
        db.session.add(current_user)
        flash(u'资料已更新')
        return redirect(url_for('admin.setting'))
    form.blog_title.data = current_user.blog_title
    form.blog_description.data = current_user.blog_description
    form.blog_cover.data = current_user.blog_cover
    form.Posts_per_page.data = current_user.Posts_per_page
    form.author_detail.data = current_user.author_detail
    return render_template('setting.html', form=form)


@login_required
@admin.route('/editor', methods=['GET', 'POST'])
def new_post():
    """新增文章"""
    form = EditorForm()
    if form.validate_on_submit():
        post = Post(
                title=form.title.data,
                cover=form.cover.data,
                body=form.body.data,
                # summary=form.summary.data,
                publish=form.publish.data,
                url_name=form.url_name.data,
                publish_date=form.publish_date.data)
        db.session.add(post)
        flash(u'文章添加成功')
        return redirect(url_for('admin.editor', form=form, url_name=form.url_name.data))
    return render_template('setting.html', form=form)


@login_required
@admin.route('/editor/<url_name>', methods=['GET', 'POST'])
def editor(url_name):
    """编辑文章"""
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    form = EditorForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.cover = form.cover.data
        post.body = form.body.data
        # post.summary = form.summary.data
        post.publish = form.publish.data
        post.url_name = form.url_name.data
        post.publish_date = form.publish_date.data
        # post.tags = form.tags.data
        flash(u'文章状态已更新')
        return redirect(url_for('admin.editor', url_name=post.url_name))
    form.title.data = post.title
    form.cover.data = post.cover
    form.body.data = post.body
    # form.summary.data = post.summary
    form.publish.data = post.publish
    form.url_name.data = post.url_name
    form.publish_date.data = post.publish_date
    # form.tags.data = post.tags
    return render_template('editor.html', form=form, post=post)


@login_required
@admin.route('/manage', methods=['GET', 'POST'])
def manage_posts():
    """管理文章"""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.publish_date.desc()).paginate(
        page, per_page=current_app.config['MANAGE_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('manage_posts.html', posts=posts, pagination=pagination)


@login_required
@admin.route('/manage/delete/post', methods=['GET', 'POST'])
def delete_post():
    """删除文章"""
    post_name = request.args.get('url_name')
    post = Post.query.filter_by(url_name=post_name).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash(u'已成功删除文章')
    return redirect(url_for('admin.manage_posts'))
