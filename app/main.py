from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import randrange
from . import models
from .database import engine
from .routers import post, user, auth,vote
# from fastapi.params import Body
from .config import settings

#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


# my_post=[{"title":"title of post1", "content":"content of post 1","id":1},{"title":"Favorite food", "content":"I like pizza","id":2}]
# def find_post(id):
#     for p in my_post:
#         if p["id"]==id:
#             return p
    
# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p["id"]==id:
#             return i









