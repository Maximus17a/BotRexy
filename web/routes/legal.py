from flask import Blueprint, render_template

bp = Blueprint('legal', __name__)

@bp.route('/privacy')
def privacy():
    """Política de privacidad"""
    return render_template('privacy.html')

@bp.route('/terms')
def terms():
    """Términos de servicio"""
    return render_template('terms.html')
