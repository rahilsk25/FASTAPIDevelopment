from typing import List
from app import schemas
import pytest

def test_get_all_posts(client, test_posts):
    res=client.get("/posts/")
    def validate(post):
        return schemas.Post(**post)
    posts_map=map(validate, res.json())
    posts_list=list(posts_map)
    # print(posts_list)
    assert res.status_code==200


def test_user_get_one_posts(client, test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post=schemas.Post(**res.json())
    # print(post)
    assert res.status_code == 200
    assert post.id == test_posts[0].id

def test_user_get_one_posts_not_exits(client, test_posts):
    res=client.get(f"/posts/{22222}")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ('awesome new title', "awesome new content", True),
    ('Favourite Pizza', "I love cheeze", False),
    ('tallest skyscrapper', "Wahoooo", True)

])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res= authorized_client.post("/posts/", json={"title": title, "content":content,
                                                 "published":published})
    created_post = schemas.Post(**res.json())
    assert res.status_code==201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code==401

def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403



def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404