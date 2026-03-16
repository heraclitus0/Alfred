class AlfredError(Exception):
    pass


class InvalidModeTransition(AlfredError):
    pass


class ApprovalRequired(AlfredError):
    pass
