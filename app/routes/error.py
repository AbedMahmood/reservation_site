from . import main_bp
from app.utils import render_page

@main_bp.route('/404')
def page_404():
    return render_page('components/404.html', page_title='Page Not Found', is_404=True)
