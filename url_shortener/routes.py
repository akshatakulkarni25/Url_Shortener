from flask import Blueprint, render_template, request, redirect

from models import Link
from extensions import db
from authenticate import requires_auth


short = Blueprint('short', __name__)


@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()
    return redirect(link.original_url)


@short.route('/')
def index():
    return render_template('index.html')


@short.route('/add_link', methods=["POST"])
@requires_auth
def add_link():
    original_url = request.form['original_url']
    is_link_present = Link.query.filter_by(original_url=original_url).first()
    if not is_link_present:
        link = Link(original_url=original_url)
        db.session.add(link)
        db.session.commit()

    return render_template('link_added.html', new_link=is_link_present.short_url, original_url=original_url)


@short.route('/stats')
@requires_auth
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)


@short.errorhandler(404)
def page_not_found(e):
    return '<h1> 404</h1>', 404