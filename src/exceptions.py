from datetime import date

from fastapi.exceptions import HTTPException


class NabronirovalException(Exception):
    detail = "Что-то пошло не так..."

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Похожий объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь с данным email уже существует"


class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с данным email уже существует!"


class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Данного пользователя не существует"


class NonValidTokenException(NabronirovalException):
    detail = "Невалидный токен"


class NonValidTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Невалидный токен"


class IncorrectPasswordException(NabronirovalException):
    detail = "Пароль неверный"


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Все номера забронированы"


class IncorrectDateRangeHTTPException(NabronirovalHTTPException):
    status_code = 422
    detail = "Дата заезда не может быть позже даты выезда"

class FacilityAlreadyExistsException(NabronirovalException):
    detail = "Такое удобство уже существует"

class FacilityAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Такое удобство уже существует"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to < date_from:
        raise IncorrectDateRangeHTTPException
