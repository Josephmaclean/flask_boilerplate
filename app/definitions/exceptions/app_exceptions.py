from flask import Response
from flask import json
from sqlalchemy.exc import DBAPIError


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - context = {self.context}"
        )


def app_exception_handler(exc: AppExceptionCase):
    if isinstance(exc, DBAPIError):
        return Response(
            json.dumps({"app_exception": "Database Error", "context": exc.orig.pgerror}),
            status=400,
        )
    return Response(
        json.dumps({"app_exception": exc.exception_case, "context": exc.context}),
        status=exc.status_code,
        mimetype="application/json",
    )


class AppException:
    class ResourceCreationFailed(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, context):

            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceExists(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, context):

            status_code = 400
            AppExceptionCase.__init__(self, status_code, context)

    class ResourceDoesNotExist(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Resource does not exist
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class Unauthorized(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Unauthorized
            :param context: extra dictionary object to give the error more context
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)
