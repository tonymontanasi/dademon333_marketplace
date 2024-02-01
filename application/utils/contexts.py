from contextvars import ContextVar

REQUEST_ID_CONTEXT_VAR = ContextVar("REQUEST_ID_CONTEXT_VAR", default=None)
