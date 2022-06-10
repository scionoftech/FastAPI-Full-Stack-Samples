from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import sys

sys.path.append("..")
from util import deps, schemas, get_json
from crud import crud_users, crud_login, crud_articles
from util import response_schemas

router = APIRouter()


@router.post("/", responses=response_schemas.general_responses)
def create_article(article: schemas.ArticleCreate,
                   current_user: schemas.UserVerify = Depends(
                       deps.get_current_user)) -> JSONResponse:
    """ create a article"""
    data = crud_articles.create_article(article=article)
    if data is None:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/{article_id}",
            responses=response_schemas.general_responses)
def update_article(article_id: str, article: schemas.ArticleUpdate,
                   current_user: schemas.UserVerify = Depends(
                       deps.get_current_user)) -> JSONResponse:
    """ update a article"""

    data = crud_articles.update_article(article_id=article_id,
                                        article=article)
    if data is None:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.delete("/{article_id}",
               responses=response_schemas.general_responses)
def delete_artcle(article_id: str,
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_user)) -> JSONResponse:
    """ Delete A User"""
    data = crud_articles.delete_article(article_id=article_id)
    if data is None:
        return JSONResponse(status_code=500,
                            content={
                                "message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("/", responses=response_schemas.all_users_responses)
def get_articles(article_id: str = None, article_title: str = None,
                 tag: str = None, page_num: int = 1,
                 page_size: int = 30,
                 current_user: schemas.UserVerify = Depends(
                     deps.get_current_user)) -> JSONResponse:
    """ Return All Articles"""
    if article_id is not None:
        data = crud_articles.get_article(article_id=article_id)
        if data is None:
            return JSONResponse(status_code=500,
                                content={
                                    "message": "No Records Found"})
        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(status_code=200,
                            content=json_compatible_item_data)
    else:
        data = crud_articles.get_all_articles(tag=tag,
                                              article_title=article_title,
                                              page_num=page_num,
                                              page_size=page_size)
        if data is None:
            return JSONResponse(status_code=500,
                                content={
                                    "message": "No Articles Found"})
        return JSONResponse(status_code=200,
                            content={"total_pages": data.pages,
                                     "total_items": data.total_items,
                                     "page_data": {
                                         "page_num": page_num,
                                         "item_count": data.page_size,
                                         "items": get_json(
                                             data.items)}})
