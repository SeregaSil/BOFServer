from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import auth, game
from schemas import BOFRequest

app = FastAPI(title='BOFServer')

app.include_router(auth.router)
app.include_router(game.router)


@app.get("/", response_model=BOFRequest)
async def root():
    return BOFRequest(status=status.HTTP_200_OK, detail='Server Work')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "detail": exc.errors()}),
    )

@app.exception_handler(OSError)
async def server_unexpected_error(request: Request, exc: OSError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder({"status": status.HTTP_503_SERVICE_UNAVAILABLE, 
                                 "detail": "The Server is sick"}),
    )