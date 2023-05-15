from fastapi import HTTPException, status

UnAuthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Некорректное имя или пароль",
    headers={"WWW-Authenticate": "Bearer"})

NotFoundToken = HTTPException(status_code=401, detail="Токен не найден")

IncorrectToken = HTTPException(status_code=401, detail="Неверный токен")

NotFoundData = HTTPException(status_code=404, detail="Не найдено")

DatabaseError = HTTPException(status_code=500, detail="Ошибка при сохранении в базу данных")


class NotFoundSQL(Exception):
    pass
