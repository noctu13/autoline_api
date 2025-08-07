from fastapi import HTTPException, status

class BaseException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class RoleNotExistsException(BaseException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail='Роль не существует'

class UserNotExistsException(BaseException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail='Пользователь не существует'

class UserAlreadyExistsException(BaseException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail='Пользователь уже существует'

class WrongCredentialsException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Неверные учетные данные'

class PermissionsException(BaseException):
    status_code=status.HTTP_403_FORBIDDEN
    detail='Недостаточно прав'

class TokenMissingException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class TokenExpiredException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен просрочен"

class TokenInvalidClaimsException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен не соответствует требованиям"

class TokenInvalidException(BaseException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Недействительный токен"

class DatabaseException(BaseException):
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    detail="Ошибка базы данных"