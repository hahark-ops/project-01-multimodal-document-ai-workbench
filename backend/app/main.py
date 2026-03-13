from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.router import api_router
from app.core.config import get_frontend_origin
from app.errors import APIException
from app.schemas.documents import APIErrorDetail, APIErrorResponse

app = FastAPI(
    title="Multimodal Document AI Workbench API",
    description="Backend API for Phase 1 PDF upload and parsing.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_frontend_origin()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
def handle_api_exception(_: Request, exc: APIException) -> JSONResponse:
    payload = APIErrorResponse(
        error=APIErrorDetail(code=exc.code, message=exc.message)
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
    first_error = exc.errors()[0] if exc.errors() else None
    message = "Invalid request."
    if first_error is not None and "msg" in first_error:
        message = str(first_error["msg"])

    payload = APIErrorResponse(
        error=APIErrorDetail(code="VALIDATION_ERROR", message=message)
    ).model_dump()
    return JSONResponse(status_code=422, content=payload)


app.include_router(api_router)
