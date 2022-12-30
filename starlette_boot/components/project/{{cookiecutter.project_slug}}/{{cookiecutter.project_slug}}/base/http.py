from starlette.datastructures import State
from starlette.requests import Request


class RequestState(State):
    pass


class HttpRequest(Request):
    state: RequestState
