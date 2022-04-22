import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cruds.auth import *
from cruds.article import *
from cruds.notice import *

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    nickname: str
    avater: str = None

    class Config:
        orm_mode = True

@app.get("/extraResource/{file_name}")
async def main(file_name):
    """アップロードされたファイルを参照する"""
    return FileResponse("./extra/"+file_name)

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    print(form.username)
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)


@app.get("/refresh_token/", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)


@app.get("/user/me/", response_model=User)
async def read_users_me(user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return user

@app.put("/user/logout/")
async def delete(user_id: User = Depends(get_current_user)):
    """ログアウト用"""
    # print(user_id)
    delete_token(user_id)
    return {"detail": "Success"}

@app.get("/user/article/list/")
async def return_my_article_list(articles: Article = Depends(getMyArticleList)):
    """ユーザーの記事リスト"""
    return articles

@app.get("/user/article/{article_id}")
async def return_user_article_detail(article: Article = Depends(getUserArticleDetail)):
    return article


#お知らせ
@app.get("/notice/list/")
async def getNotice(article: Notice = Depends(getNotice)):
    """お知らせ"""
    return article

#記事リスト
@app.get("/article/list/")
async def return_article_list(article: Article = Depends(getArticleList)):
    """記事リスト"""
    return article

# 検索機能
@app.get("/article/search/{search_text}")
async def search_article_list(article: Article = Depends(searchArticleList)):
    """記事検索"""
    return article

# タグリスト（使用頻度が多い順）
@app.get("/article/tags/list")
async def getTagList(tags: Article = Depends(getTagList)):
    """タグリスト　使用頻度が多い順"""
    return tags

@app.get("/article/tags/list_all")
async def getTagList(tags: Article = Depends(getTagList)):
    """タグリスト　一覧"""
    return tags

# タグに関連する記事一覧を取得する
@app.get("/article/tag/{tag_id}")
async def getTagList(article_list: Article = Depends(getRelateTagArticleList)):
    """タグに関連する記事一覧を取得"""
    return article_list

# タグidからタグ名を取得
@app.get("/tag/name/{tag_id}")
async def getTagList(tag_name: Article = Depends(getTagName)):
    """タグIDから取得"""
    return tag_name

@app.get("/member/user/{user_id}")
async def getMemberUser(user: Article = Depends(getMemberUser)):

    return user


@app.get("/article/{article_id}")
async def return_article_detail(article: Article = Depends(getArticleDetail)):
    return article

@app.get("/article/user/{user_id}")
async def return_article_detail(article: Article = Depends(getUserArticle)):
    return article


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)