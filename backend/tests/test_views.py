
import pytest


@pytest.mark.asyncio
async def test_views_on_topic(client, mock_topic):
    assert mock_topic.view_count == 0
    
    response = await client.get(f"/topics/{mock_topic.id}")
    assert response.json()["view_count"] == 1
    
@pytest.mark.asyncio
async def test_views_on_branch(client, mock_branch):
    assert mock_branch.view_count == 0
    
    response = await client.get(f"/branches/{mock_branch.id}")
    assert response.json()["view_count"] == 1
    
@pytest.mark.asyncio
async def test_views_on_user(client, test_user_admin):
    assert test_user_admin.view_count == 0
    
    response = await client.get(f"/users/{test_user_admin.id}")
    assert response.json()["view_count"] == 1