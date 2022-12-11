from fastapi import FastAPI
from routers.orders import router as OrderRouter
from routers.products import router as ProductRouter
from routers.users import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to SV Shpping Center."}


app.include_router(OrderRouter, tags=["Orders"], prefix="/orders")
app.include_router(ProductRouter, tags=["Products"], prefix="/products")
app.include_router(UserRouter, tags=["Users"], prefix="/users")