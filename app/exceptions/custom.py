class AppException(Exception):
    def __init__(self,message:str,status_code:int):
        self.message = message 
        self.status_code = status_code

class NotFoundError(AppException):
    def __init__(self,message="Resource not found"):
        super().__init__(message,404)

class BadRequestError(AppException):
    def __init__(self,message="Bad request"):
        super().__init__(message,400)

class Unauthorized(AppException):
    def __init__(self,message="Not authorized"):
        super().__init__(message,401)