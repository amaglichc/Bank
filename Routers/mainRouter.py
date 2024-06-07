from fastapi import APIRouter
from fastapi import Response, Request, status

router = APIRouter(
    prefix="/main",
    tags=["main"]
)


@router.get("", status_code=status.HTTP_418_IM_A_TEAPOT)
async def root(res: Response, req: Request):
    return {"message": "Hello World"}