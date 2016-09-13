# -*- coding: utf-8 -*-
from . import admin
from .forms import LoginForm, SettingForm, EditorForm, TagForm
from ..models import User, Post, Tag
from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, login_user, logout_user, current_user  # 保护路由只让认证用户登陆, 保存登陆用户


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)  # True，在cookie中写入长期有效的cookie
            return redirect(request.args.get('next') or url_for('admin.index'))  # 后台默认页
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@admin.route('/')
@login_required
def index():
    return render_template('dashboard.html')


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
@admin.route('/new_post', methods=['GET', 'POST'])
def new_post():
    """新增文章"""
    form = EditorForm()
    if form.validate_on_submit():
        if Post.query.filter_by(url_name=form.url_name.data).first():
            flash(u'url_name已存在')
            return render_template('new_post.html', form=form)
        tag_temp = str_to_tag(form)
        post = Post(
                title=form.title.data,
                cover=form.cover.data,
                body=form.editor.data,
                summary=form.summary.data,
                publish=form.publish.data,
                url_name=form.url_name.data,
                publish_date=form.publish_date.data,
                tags=tag_temp)
        db.session.add(post)
        flash(u'文章添加成功')
        return redirect(url_for('admin.editor', form=form, url_name=form.url_name.data))
    return render_template('new_post.html', form=form)


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
@admin.route('/editor/<url_name>', methods=['GET', 'POST'])
def editor(url_name):
    """编辑文章"""
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    form = EditorForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.cover = form.cover.data
        post.body = form.editor.data
        post.summary = form.summary.data
        post.publish = form.publish.data
        post.url_name = form.url_name.data
        post.publish_date = form.publish_date.data

        tag_temp = str_to_tag(form)
        post.tags = tag_temp
        flash(u'文章状态已更新')
        return redirect(url_for('admin.editor', url_name=post.url_name))
    form.title.data = post.title
    form.cover.data = post.cover
    form.editor.data = post.body
    form.summary.data = post.summary
    form.publish.data = post.publish
    form.url_name.data = post.url_name
    form.publish_date.data = post.publish_date
    tag_temp = ''
    for tag in post.tags:
        tag = tag.name + ' '
        tag_temp += tag
    form.tags.data = tag_temp
    return render_template('editor.html', form=form, post=post)


@login_required
@admin.route('/manage/delete/post', methods=['GET', 'POST'])
def delete_post():
    """删除文章"""
    url_name = request.args.get('url_name')
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash(u'已成功删除文章')
    return redirect(url_for('admin.manage_posts'))


@login_required
@admin.route('/tags', methods=['GET', 'POST'])
def manage_tags():
    """管理标签"""
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.paginate(
        page, per_page=8, error_out=False
    )
    tags = pagination.items
    return render_template('manage_tags.html', tags=tags, pagination=pagination)


@login_required
@admin.route('/tags/<url_name>', methods=['GET', 'POST'])
def modify_tag(url_name):
    """修改标签"""
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.url_name = form.url_name.data
        tag.cover = form.cover.data
        flash(u'标签信息已更新')
        return redirect(url_for('admin.modify_tag', url_name=tag.url_name))
    form.name.data = tag.name
    form.url_name.data = tag.url_name
    form.cover.data = tag.cover
    return render_template('modify_tag.html', form=form, tag=tag)


@login_required
@admin.route('/new_tag', methods=['GET', 'POST'])
def new_tag():
    """新增标签"""
    form = TagForm()
    if form.validate_on_submit():
        if Tag.query.filter_by(url_name=form.url_name.data).first():
            flash(u'Tag_URL已存在')
            return render_template('new_tag.html', form=form)
        tag = Tag(
                name=form.name.data,
                cover=form.cover.data,
                url_name=form.url_name.data,)
        db.session.add(tag)
        flash(u'标签添加成功')
        return redirect(url_for('admin.new_tag'))
    return render_template('new_tag.html', form=form)


@login_required
@admin.route('/tags/delete', methods=['GET', 'POST'])
def delete_tag():
    """删除标签"""
    url_name = request.args.get('url_name')
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash(u'已成功删除标签')
    return redirect(url_for('admin.manage_tags'))


def str_to_tag(form):
    """标签字符串与tag对象的转换"""
    tag_temp = []
    tag_list = form.tags.data.split()  # 默认空格分割
    for tag_name in tag_list:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:  # 数据库不存在标签，以tag_name生成一个
            tag = Tag(name=tag_name,
                      url_name=tag_name)
            db.session.add(tag)
            db.session.commit()
        tag_temp.append(Tag.query.filter_by(name=tag_name).first())  # 返回一个列表，包含所有关联的Tag对象
    return tag_temp

