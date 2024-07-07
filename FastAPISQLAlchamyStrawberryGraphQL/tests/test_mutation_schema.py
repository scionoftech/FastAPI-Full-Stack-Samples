import pytest

# ------------------ Mutation Test Cases ------------------ #

new_article_data = {
    "articleId": None,
    "userId": "1",
    "articleTitle": "test",
    "articleText": "test",
    "tags": ""
}

add_article_mutation = {
    "query": """
        mutation($articleInput: ArticleInput!) {
            addEditArticle(articleInput: $articleInput) {
            articleId
            userId
            articleTitle
            articleText
            tags
            }
        }
    
    """,
    "variables": {"articleInput": new_article_data}
}

update_article_data = {
    "articleId": "1",
    "userId": "1",
    "articleTitle": "test",
    "articleText": "test",
    "tags": ""
}

edit_article_mutation = {
    "query": """
        mutation($articleInput: ArticleInput!) {
            addEditArticle(articleInput: $articleInput) {
            articleId
            userId
            articleTitle
            articleText
            tags
            }
        }

    """,
    "variables": {"articleInput": update_article_data}
}


@pytest.mark.asyncio
async def test_add_article(authorized_client):
    response = await authorized_client.post("/graphql",
                                            json=add_article_mutation)

    results = response.json()

    assert response is not None
    assert response["data"]["addEditArticle"]["articleTitle"] == \
           add_article_mutation["articleTitle"]


@pytest.mark.asyncio
async def test_edit_article(authorized_client):
    response = await authorized_client.post("/graphql",
                                            json=edit_article_mutation)

    results = response.json()

    assert response is not None
    assert response["data"]["addEditArticle"]["articleTitle"] == \
           edit_article_mutation["articleTitle"]

# ------------------ Mutation Test Cases ------------------ #