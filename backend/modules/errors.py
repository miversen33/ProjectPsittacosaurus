class AuthenticationError(Exception):
    def __init__(self, message='', *args):
        super().__init__(args)
        self.message = message

class ParseError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class OverFreeLimitError(Exception):
    def __init__(self, user_id, *args):
        message = f'User: {user_id} has exceeded the Free Tier League Limit'
        super().__init__(message, *args)
