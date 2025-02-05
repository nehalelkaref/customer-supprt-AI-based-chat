from flask import Blueprint, request


bp = Blueprint('bp', __name__, )
# not sure about this, register bp in init?
@bp.route('/chat', methods=['POST'])
def get_message():
    msg = request.json['msg']
    return msg

    