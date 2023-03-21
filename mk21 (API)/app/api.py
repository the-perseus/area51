from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Logbooktable

api = Blueprint('api', __name__, url_prefix='/api')

@app.route('/logbookapi')
@login_required
def logbook_entries():
    entries = Logbooktable.query.filter_by(user_id=current_user.id).all()
    serialized_entries = [entry.serialize() for entry in entries]
    return jsonify(serialized_entries)
