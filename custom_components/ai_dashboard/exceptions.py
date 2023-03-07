"""Custom Exceptions for HACS."""


class AIDashboardExecutionStillInProgress(Exception):
    """Super basic."""

class AIDashboardExecutionStillInProgress(AIDashboardExecutionStillInProgress):
    """Exception to raise if execution is still in progress."""

class NoUsablePhotoException(Exception):
    """Exception to raise if no usable photos are send to the backend. A usable photo has to contain one and only one face"""