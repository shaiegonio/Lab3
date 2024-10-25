import requests
import json
from fastapi import FastAPI
from typing import Optional, List

app = FastAPI()

@app.get("/posts/")
def get_posts(postId: Optional[int] = None):
    if postId is None:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts')
        response = json.loads(posts.text)
    else:
        posts = requests.get(f'https://jsonplaceholder.typicode.com/posts/{postId}')
        response = json.loads(posts.text)
    
    return response

@app.get("/comments/")
def get_comments(postId: Optional[int] = None):
    if postId is None:
        comments = requests.get('https://jsonplaceholder.typicode.com/comments')
        response = json.loads(comments.text)
    else:
        comments = requests.get(f'https://jsonplaceholder.typicode.com/comments?postId={postId}')
        response = json.loads(comments.text)
    
    return response


@app.get("/formatted_posts/{userID}")
def get_post_then_format_according_to_user(userID: int):
    posts = get_posts() 
    data = {"userID": userID, "posts": []}

    for u in posts:
        if u['userId'] == userID:
            data["posts"].append({
                "post_title": u["title"],
                "post_body": u["body"],
            })
    return data

@app.get("/formatted_comment/{postID}")
def get_post_then_format_according_to_comment(postID: int):
    req = requests.get(f'http://127.0.0.1:8000/comments/?postId={postID}')
    comments = json.loads(req.text)

    data = {"post_id": postID, "comments": []}
    for c in comments:
        if c['postId'] == postID:
            data["comments"].append({
                "commenter_email": c["email"],
                "commenter_name": c["name"],
                "comment": c["body"],
            })
    return data

@app.get("/detailed_post/{userID}")
def detailed_post(userID: int):
    posts = get_posts() 
    comments = get_comments()  
    data = {"userID": userID, "posts": []}

    for post in posts:
        if post['userId'] == userID:
            post_details = {
                "post_title": post["title"],
                "post_body": post["body"],
                "comments": []
            }

            for comment in comments:
                if comment['postId'] == post['id']:
                    post_details["comments"].append({
                        "commenter_email": comment["email"],
                        "commenter_name": comment["name"],
                        "comment": comment["body"],
                    })
            data["posts"].append(post_details)

    return data
