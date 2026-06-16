from .util_io import readJSON
from flask import request, jsonify
from functools import wraps
from typing import Callable

import httpx
from clerk_backend_api import Clerk, RequestState
from clerk_backend_api.security.types import AuthenticateRequestOptions

class Config:
    def __init__(self) -> None:
        config: dict = readJSON('config')
        self.headers: dict = config['headers']
        self.tmdb_api_key = config['tmdb_api_key']
        self.clerk_secret_key = config['clerk_secret_key']
        self.origin = config['origin']
        self.sdk = Clerk(bearer_auth=self.clerk_secret_key)

    def get_request_state(self, flask_request: request) -> RequestState:
        request_state = self.sdk.authenticate_request(
            flask_request,
            AuthenticateRequestOptions(
                authorized_parties=[self.origin]
            )
        )
        return request_state

    def api_check(self, fnc: Callable) -> Callable:
        @wraps(fnc)
        def inner_api_check(*args, **kwargs):
            request_state = self.get_request_state(request)
            if not request_state.is_signed_in:
                return jsonify({"error": request_state.reason.name}), 401
            else:
                return fnc(*args, **kwargs)
        return inner_api_check
