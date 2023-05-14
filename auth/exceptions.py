from fastapi import HTTPException, status

UnAuthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})

NotFoundToken = HTTPException(status_code=401, detail="Токен не найден")

IncorrectToken = HTTPException(status_code=401, detail="Неверный токен")