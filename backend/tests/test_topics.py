import pytest

create_branch_mock = {
    "title": "Test",
    "description": "Test"
}

@pytest.mark.asyncio
async def test_topic(client, db_session, test_user_admin):
    
    # Create branch for new topic
    response = await client.post("/branches/", json=create_branch_mock)
    assert response.status_code == 201
    
    branch_id = int(response.json()["id"])
    
    new_topic_mock = {
        "title" : "New topic",
        "description" : "New topic description",
        "branch_id" : branch_id
    }
    
    # Create topic in branch
    response = await client.post("/topics/", json=new_topic_mock)
    topic_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json()["id"] == topic_id
    assert response.json()["title"] == new_topic_mock["title"]
    assert response.json()["description"] == new_topic_mock["description"]
    assert response.json()["is_active"] == True
    assert response.json()["creator_id"] == test_user_admin.id
    
    # Read the topic
    response = await client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["id"] == topic_id
    assert response.json()["title"] == new_topic_mock["title"]
    assert response.json()["description"] == new_topic_mock["description"]
    assert response.json()["is_active"] == True
    assert response.json()["creator_id"] == test_user_admin.id

    # Update topic
    update_topic = {"description": new_topic_mock["description"] + "123"}
    response = await client.put(f"/topics/{topic_id}", json=update_topic)
    assert response.status_code == 200
    assert response.json()["description"] == update_topic["description"]
    
    # Read the updated topic
    response = await client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["description"] == update_topic["description"]