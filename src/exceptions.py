class NabronirovalException(Exception):
    detail = "Что-то пошло не так..."


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class ObjectAddConflictException(NabronirovalException):
    detail = "Добавление объекта вызывает конфликт"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"
