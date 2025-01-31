from ..import models, schemas, utils, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router=APIRouter(
    prefix="/posts", tags=['Posts']
)



# class TextWithNumber:
#     def __init__(self, Post, votes):
#         self.Post = Post
#         self.votes = int(votes)  # Ensure number is stored as int
    
#     def __str__(self):
#         return f"{self.Post} {self.votes}"
    
#     def __repr__(self):
#         return str(self)
    


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session=Depends(get_db), limit=10, skip=0, search: Optional[str]=""):
    #cur.execute("""Select * from posts""")
    #post=cur.fetchall()
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    

    # converted_list = [TextWithNumber(Post, votes) for Post, votes in results]
    # print(type(results))
    return posts
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_user(payload: schemas.PostCreate, db: Session=Depends(get_db), current_user = Depends
    (oauth2.get_current_user)):
    #the comment section show how to create post using the sql command like using psycopg2
    #cur.execute("""Insert into posts (id, title, content, published) values (%s,%s,%s,%s) returning * """, 
    #(payload.id,payload.title,payload.content,payload.published))
    #post=cur.fetchone()
    #conn.commit()

    #new_post=models.Post(title=payload.title, content=payload.content)
    print(f"created by {current_user}")
    new_post=models.Post(owner_id=current_user,**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session=Depends(get_db)):

    #cur.execute("""SELECT * FROM posts where id=%s """, (str(id),))
    #post=cur.fetchone()
    #--------------------------
    #post=find_post(id) it is using function written up
    #--------------------------

    post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} was not found")
        #response.status_code =status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} was not found"}"""
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session=Depends(get_db), current_user = Depends
    (oauth2.get_current_user)):
    #cur.execute("""Delete from posts where id=%s returning * """,(str(id),))
    #deleted_post=cur.fetchone()
    #conn.commit()
    #index=find_index_post(id)
    print(f"Deleted by {current_user}")
    post= db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} doesn't exist already")

    if current_user!=post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail= f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    #my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post2: schemas.PostCreate, db: Session=Depends(get_db), current_user = Depends
    (oauth2.get_current_user)):
    #cur.execute("""Update posts set title=%s, content=%s, published=%s where id=%s returning * """,
    #(post.title, post.content, post.published, str(id)))
    #updated_post=cur.fetchone()
    #conn.commit()
    #index=find_index_post(id)
    print(f"Updated by {current_user}")
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"post with id {id} doesn't exist already")
    
    if current_user!=post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail= f"Not authorized to perform requested action")

    post_query.update(post2.dict(), synchronize_session=False)
    db.commit()
    #post_dict=post.dict()
    #post_dict['id']=id
    #my_post[index]=post_dict
    return post_query.first()