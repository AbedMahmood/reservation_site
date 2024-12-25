from flask import current_app, redirect, url_for
from . import main_bp
from app.utils import render_page

@main_bp.route('/')
@main_bp.route('/<page_name>')
def dynamic_page(page_name='home'):
    template = current_app.config['TEMPLATE_PATHS'].get(page_name)
    if not template:
        return redirect(url_for('main_bp.page_404'))
    return render_page(template, page_name.capitalize())
