from flask import Blueprint
from flask import render_template

from models import Post, Tag, post_tags
from .forms import PostForm, TagForm

from flask import request
from app import db

from flask import redirect
from flask import url_for

from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag_name = request.form['tags']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            tag = Tag.query.filter(Tag.name == tag_name).first()
            post = Post.query.filter(Post.title == title).first()
            post.tags.append(tag)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something')
        return redirect(url_for('posts.blueprint'))

    form = PostForm()
    tags = Tag.query.order_by(Tag.name).all()
    form.tags.choices = [(tags[key], tags[key]) for key in range(len(tags))]
    return render_template('posts/create_post.html', form=form, tags=tags)


@posts.route('/create-tag', methods=['POST', 'GET'])
@login_required
def create_tag():

    if request.method == 'POST':
        name = request.form['name']

        try:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
        except:
            print('Something')
        return redirect(url_for('posts.all_tags'))

    form = TagForm()
    return render_template('posts/create_tag.html', form=form)


@posts.route('/all-tags')
def all_tags():
    tags = Tag.query.order_by(Tag.name.desc())
    return render_template('posts/all_tags.html', tags=tags)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags

    if request.method == 'POST':
        if request.form.get('title') or request.form.get('body'):
            post.title = request.form['title']
            post.body = request.form['body']
            db.session.commit()
            return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form, tags=tags)


@posts.route('/')
def blueprint():
    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/index.html', posts=posts, pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)