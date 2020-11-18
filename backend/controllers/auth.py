from flask import current_app as app

from modules.authenticate import _login, _new_user, _logout, _modify_user

@app.route('/login', methods=['POST'], bypass_session_validation=True)
def login():
    return _login()

@app.route('/new_user', methods=['POST'], bypass_session_validation=True)
def new_user():
    return _new_user()

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return _logout()

@app.route('/modify_user', methods=['POST'])
def _modify_user():
    return _modify_user()