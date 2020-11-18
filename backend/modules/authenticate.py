from datetime import datetime, timedelta
from passlib.hash import bcrypt as hasher
from flask import request, g, current_app as app, session, json
from json import JSONDecodeError

from sqlalchemy.sql import select, insert
from sqlalchemy.exc import InterfaceError

from modules.server_response_statuses import INTERNAL_SERVER_ERROR, SUCCESS, NOT_AUTHORIZED_ERROR, BAD_REQUEST
from modules.errors import AuthenticationError, ParseError
from modules.response import Response
from models.auth import User, UserSession
# from models.user import User
# from models.usersession import UserSession

_INVALID_DATA_FORMAT_ERROR = 'Invalid Data Format'
_INVALID_DATA_PROVIDED_ERROR = 'Invalid Data Provided'
_INCORRECT_USERNAME_OR_PASSWORD_ERROR = 'Incorrect Username or Password'

_SESSION_TYPE_WEB = 'w'
_SESSION_TYPE_MOBILE = 'm'
# Not currently supported
_SESSION_TYPE_DESKTOP = 'd'
_LOGIN_FAILURE_LIMIT = 3


def _decode_auth_info():
    # Do auth decoding here. For now, just load the auth info into a js style dictionary.
    try:
        return json.loads(request.data)
    except TypeError:
        # TODO(Mike) We need to dump the input so we know what happened.
        print(request.data)
        raise ParseError('Unable to parse provided data')
    except JSONDecodeError:
        return dict(
            username=request.cookies.get('username', None),
            userid=request.cookies.get('userid', None),
            session_id=request.cookies.get('session_id', None),
            session_type=request.cookies.get('session_type', None)
        )


def _login():
    status = SUCCESS
    status_text = ''
    try:
        data = _decode_auth_info()
    except ParseError as error:
        print(repr(error), error)
        status_text = _INVALID_DATA_FORMAT_ERROR
        status = BAD_REQUEST
        return Response({}, status_code=status, status_text=status_text)
    matches = User.query.filter_by(user_name=data['username'])
    if len(matches.all()) > 1:
        # TODO(Mike) Convert to logging!
        print(
            f'Username {data["username"]} has multiple occurrences! How the fuck did you manage to do this????')

    user = None
    try:
        user = matches.first()
        if not user.is_active:
            matches_credentials = False
        else:
            matches_credentials = _validate_user_creds(
                matches.first(), data['password'])
    except (AttributeError, AuthenticationError):
        matches_credentials = False

    if not matches_credentials or user is None:
        # TODO(Mike): Figure out how exactly we want to handle locked accounts?
        """
            We could have it just continue to say incorrect username/password and have
            the user follow the recovery process, without indicating to them that the account was 
            locked. This would allow some form of "anonymity" in that the "attacker" would
            have no idea if they are indeed hitting a valid account or not. In addition, we could 
            send an email upon locking of the account to inform the user that their account has been locked.

            The latter may not be a great idea though, if the email address is comprimised. However, that is
            generally not our problem.
        """
        status = NOT_AUTHORIZED_ERROR
        status_text = _INCORRECT_USERNAME_OR_PASSWORD_ERROR
        return Response({}, status_code=status, status_text=status_text)

    session_id = _get_session_id(user, data['session_type'])
    user.consecutive_failed_logins = 0
    response = Response()
    response.set_cookie('username', user.user_name)
    response.set_cookie('userid', str(user.id))
    response.set_cookie('session_id', session_id)
    response.set_cookie('session_type', data['session_type'])
    return response


def _logout():
    status = SUCCESS
    status_text = ''
    try:
        data = _decode_auth_info()
        _invalidate_session(user_id=data['userid'])
    except ParseError as error:
        print(error)
        status_text = _INVALID_DATA_FORMAT_ERROR
        status = BAD_REQUEST

    response = Response(status_code=status, status_text=status_text)

    response.set_cookie('username', '', expires=0)
    response.set_cookie('userid', '', expires=0)
    response.set_cookie('session_id', '', expires=0)
    response.set_cookie('session_type', '', expires=0)
    return response


def _new_user():
    # TODO(Mike) Eventually we need to return a link that can be clicked to "authenticate" the new user. For now, just a 200 works
    status = BAD_REQUEST
    status_text = ''
    try:
        data = _decode_auth_info()
        user_name = data['username']
        password = hasher.hash(data['password'])
        email_address = data['email_address']

        _store_user_info(
            {
                'user_name': user_name,
                'password': password,
                'email_address': email_address
            }
        )

        status = SUCCESS
    # TODO(Mike) log the error to a log indicating some sort of shit so we know what the fuck happened?
    except ParseError as error:
        print(error)
        status = INTERNAL_SERVER_ERROR
        status_text = _INVALID_DATA_FORMAT_ERROR
    except KeyError as error:
        print(error)
        status = INTERNAL_SERVER_ERROR
        status_text = _INVALID_DATA_PROVIDED_ERROR

    r = Response(data={}, status_code=status, status_text=status_text)
    return r


def _modify_user():
    # This func serves 2 purposes.
    # If the request only contains the needed information to pass the
    # session validation, it will return a response with what is needed in order to modify
    # the user.
    # If the request contains more than just the bare minimum, it will attempt to
    # perform the change in the request.

    # Expectation is that the request contains every field provided in the initial hit,
    # as those fields will be whats saved. If a field is not provided, it will be assumed
    # to be null and will be cleared out. Dont use this as a feature, this is just an effort
    # to try and cover up bad requests.
    request.data = json.loads(request.data)
    fields_key = 'fields'
    prepare_user_data_info = _prepare_modify_user(request.data['userid'])
    if fields_key in request.data.keys():
        data = _modify_user(request.data['userid'], request.data['password'],
                            prepare_user_data_info[fields_key].keys(), request.data[fields_key])
    else:
        data = prepare_user_data_info
    return Response(data=data)


def _validate_user_creds(user: User, check_password, increment_failure_count=True):
    try:
        matches_credentials = hasher.verify(check_password, user.password)
    except AttributeError:
        matches_credentials = False

    if not matches_credentials or not user.is_active:
        if increment_failure_count:
            _handle_invalid_login(user)
        raise AuthenticationError(
            f'User {user.username} did not authenticate correctly')
    return True


def _prepare_modify_user(user_id):
    db = app.db
    user = User.query.filter_by(user_id=user_id)
    if len(user.all()) == 0:
        # TODO(Mike): Enable Logging
        raise AuthenticationError(
            f"Something happened with userid {user_id}. Couldn't find any users!")
    if len(user.all()) > 1:
        # TODO(Mike): Enable Logging
        print(f"Somehow userid {user_id} is associated with more than 1 user?")
    user = user.first()
    user_data = {key: user.__getattribute__(
        key) for key in User.editable_fields}

    # Just a bit of data clensing to avoid passing back private info to the client
    user_data['2fa_active'] = (
        user_data['secret'] is not None and len(user_data['secret']) > 0)
    del(user_data['password'])
    del(user_data['secret'])

    return {'fields': user_data}


def _modify_user(user_id, user_password, keys, new_user_data):
    db = app.db
    user_model = User.query.filter_by(user_id=user_id)
    if len(user_model.all()) == 0:
        raise AuthenticationError(
            f"Something happened with userid {user_id}. Couldn't find any users!")
    if len(user_model.all()) > 1:
        print(f"Somehow userid {user_id} is associated with more than 1 user?")
    user = user_model.first()
    if not _validate_user_creds(user, user_password, False):
        raise AuthenticationError(
            f'Unable to modify user {user_id}:{user.username} as invalid credentials were passed')

    restricted_keys = ['2fa_active', 'is_active', 'new_password']
    # Might be better performance to have the for loop be a foreach loop (IE, get the key,value pair instead of just the key)
    for key in new_user_data.keys():
        if key not in restricted_keys and key not in keys:
            print(
                f'Im not processing key:{key} value:{new_user_data[key]} because its not in the native keys for the user model. Stop trying to break me')
            continue
        if key in restricted_keys:
            if key == 'is_active':
                _handle_user_active_change(user, new_user_data['is_active'])
            if key == '2fa_active':
                _handle_user_2fa_change(user, new_user_data['2fa_active'])
            if key == 'new_password':
                _handle_user_password_change(
                    user, new_user_data['new_password'])
        else:
            user.__setattr__(key, new_user_data[key])
    return {}


def _store_user_info(user_info):
    db = app.db
    newUser = User(**user_info)
    db.session.add(newUser)
    db.session.attempt_commit()


def _get_session_id(user, session_type):
    _invalidate_session(user=user)

    db = app.db

    try:
        user_session = UserSession(user_id=user.id, session_type=session_type)
    except ValueError:
        raise ValueError('Incorrect session_type')
    db.session.add(user_session)
    db.session.attempt_commit()
    return user_session.session_key


def _invalidate_session(user=None, user_id=None):
    db = app.db
    if user:
        db.session.delete(UserSession.query.filter_by(user_id=user.id).first())
        # UserSession.query.filter_by(user_id=user.id).delete()
    elif user_id:
        db.session.delete(UserSession.query.filter_by(user_id=user_id).first())
        # UserSession.query.filter_by(user_id=user_id).delete()
    else:
        print("I have no idea what you're expecting here idiot. Nothing is going to happen with your user_session")
    db.session.attempt_commit()
    _start_session_invalidater()


def _start_session_invalidater():
    # if app.config['DEBUG'] or 'scheduler' not in app.__dict__.keys():
    #     return
    # job = app.scheduler.get_job('session_terminator')
    # if job:
    #     return
    # app.scheduler.add_job(_session_invalidator, 'interval', minutes=15, replace_existing=True, max_instances=1, next_run_time=datetime.now())
    pass


def _session_invalidator():
    # db.query(UserSession).filter_by(last_hit <= datetime.now() - timedelta(minutes=15)).delete()
    # matches = db.query(UserSession).filter_by(last_hit <= datetime.now() - timedelta(minutes=15)).select()
    # db.session.attempt_commit()
    pass


def _handle_invalid_login(user: User):
    user.consecutive_failed_logins += 1
    if user.consecutive_failed_logins >= _LOGIN_FAILURE_LIMIT:
        user.is_active = 0
        print(
            f'Locking User {user.user_name}:{user.id} as it has reached the login failure limit')
    return


def _handle_user_2fa_change(user: User, fa_active_change):
    pass


def _handle_user_active_change(user: User, is_active):
    user.is_active = is_active
    if not is_active:
        _invalidate_session(user=user)


def _handle_user_password_change(user: User, new_password):
    user.password = hasher.hash(new_password)
    _invalidate_session(user=user)


def validate_session():
    valid_session = False
    required_keys = ['session_id', 'userid', 'session_type']
    for key in required_keys:
        if key not in request.cookies.keys():
            return False

    sessions = UserSession.query.filter_by(
        user_id=request.cookies.get('userid'),
        session_key=request.cookies.get('session_id'),
        session_type=request.cookies.get('session_type')
    )

    valid_session = len(sessions.all()) == 1
    if len(sessions.all()) > 1:
        print(
            f'Somehow the User:{request.cookies.get("userid")} has multiple sessions with the same UserSession Type:{request.cookies.get("session_type")}')
        valid_session = True

    if valid_session:
        sessions.first().last_hit = datetime.now()

    return valid_session
