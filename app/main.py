import uvicorn
import asyncio
from fastapi import FastAPI

from app.router import router

app = FastAPI(
    title='Line-provider'
)

app.include_router(router)

# async def main() -> None:
#     config = uvicorn.Config(
#         app='main:app',
#         host='0.0.0.0',
#         port=8000,
#         reload=True
#     )
#     server = uvicorn.Server(config)
#
#     await asyncio.gather(
#         server.serve(),
#     )

if __name__ == '__main__':
    # asyncio.run(main())
    uvicorn.run('main:app', host="0.0.0.0", reload=True)