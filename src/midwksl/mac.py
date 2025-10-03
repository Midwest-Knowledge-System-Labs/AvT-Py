import functools
from typing import List
from avesterra import AuthorizationError
from avesterra.avial import AvAuthorization

_chain: List[AvAuthorization] = None

def include_auth_to_chain(authorization: AvAuthorization):
    global _chain
    if _chain is None:
        _chain = []
    _chain = list(set(_chain + [authorization]))

def init(auths: List[AvAuthorization]):
    global _chain
    if _chain is not None:
        _chain = auths
    else:
        _chain = auths

def chain():
    global _chain
    if _chain is None:
        _chain = []
    return _chain

def aca():
    """
    Decorator to repeat access for avt based commands
    """
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(**kwargs):
            _chain = chain()

            if 'auth' not in func.__code__.co_varnames and 'authorization' not in func.__code__.co_varnames:
                raise ValueError("Error: Function provided to aca neither has auth nor authorization argument")

            if 'authorization' in kwargs:
                tmp_chain = [kwargs['authorization']] + _chain
            elif 'auth' in kwargs:
                tmp_chain = [kwargs['auth']] + _chain
            else:
                tmp_chain = _chain


            for auth in tmp_chain:
                if 'authorization' in func.__code__.co_varnames:
                    kwargs['authorization'] = auth
                else:
                    kwargs['auth'] = auth
                try:
                    return func(**kwargs)
                except AuthorizationError:
                    pass
            raise AuthorizationError("AuthorizationError: No authorizations in chain support access needed to execute function")
        return wrapper_repeat
    return decorator_repeat