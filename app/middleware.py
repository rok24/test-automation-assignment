import os
from jose import JWTError, jwt
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

async def protect_endpoints(request: Request, call_next):
    # Check if the request is exempt from authentication
    request_type = request.headers.get("X-REQUEST-TYPE")
    request_path = request.url.path

    for endpoint in ["/users", '/token', '/docs', '/openapi.json']:
        if request_path.endswith(endpoint) or (request_type and request_type.endswith(endpoint)):
            return await call_next(request)

    # Check if the request contains a valid bearer token
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "A valid bearer token is required to access this endpoint"},
        )

    # Extract the bearer token
    bearer_token = authorization_header.split(" ")[1].strip()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(bearer_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return await call_next(request)  # pragma: no cover
