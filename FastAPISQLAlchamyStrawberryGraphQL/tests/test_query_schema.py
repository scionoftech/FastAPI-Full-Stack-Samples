import pytest

get_aricles_query1 = {
    "query": """
     query MyQuery {
        getArticles {
            articleId
            userId
            articleTitle
            articleText
            tags
        }
     
     }
    
    """
}


@pytest.mark.asyncio
async def test_articles(authorized_client):
    response = await authorized_client.post("/graphql",
                                            json=get_aricles_query1)

    results = response.json()
    assert response is not None
    assert len(results["data"]["articles"]) > 0
