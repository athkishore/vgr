from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import Permission, Role, User, Post, Initiative
from ..decorators import admin_required
from werkzeug import secure_filename
from os import listdir
from os.path import isfile, join

@main.route('/', methods=['GET', 'POST'])
def index():
    photofiles = [f for f in listdir('app/static/galleria/img') if isfile(join('app/static/galleria/img',f))]
    form = PostForm()
    form.category.choices = [(i.id, i.name) for i in Initiative.query.order_by('name')]
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        if form.photo.data.filename != '':
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save('app/static/uploads/'+filename)
            form.body.data += '<p>\
                    <a href="http://localhost:5000/static/uploads/'+\
                    filename+'">\
                    <img alt="" src="http://localhost:5000/static/uploads/'+\
                    filename+'" style="height:141px; width:200px" /></a></p>'
                    
        post = Post(body=form.body.data,
                    author=current_user._get_current_object(),
                    category=Initiative.query.filter_by(id=form.category.data).first().name, category_id=form.category.data)
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    filename = None
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination, photofiles=photofiles)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    form.category.choices = [(i.id, i.name) for i in Initiative.query.order_by('name')]
    if form.validate_on_submit():
        post.body = form.body.data
        post.category_id = form.category.data
        post.category = Initiative.query.get(form.category.data).name
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    form.category.data = post.category_id
    print post.category
    return render_template('edit_post.html', form=form)

@login_required
@main.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    db.session.delete(post)
    flash('The post has been deleted.')
    return redirect(url_for('.index'))
    

@main.route('/work/<area>')
@login_required
def initiative(area):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=area).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('initiative.html', user=current_user, posts=posts,
                           pagination=pagination, area=area)

