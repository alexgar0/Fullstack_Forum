import pytest

create_branch_mock = {
    "title": "Test Branch Title",
    "description": "Test Branch Description"
}

@pytest.mark.asyncio
async def test_create_and_read_branch(client, db_session):
    response = await client.post("/branches/", json=create_branch_mock)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == create_branch_mock["title"]
    branch_id = data["id"]
    
    response = await client.get(f"/branches/{branch_id}")
    assert response.status_code == 200
    assert response.json()["id"] == branch_id
    assert response.json()["title"] == create_branch_mock["title"]
    assert response.json()["description"] == create_branch_mock["description"]
    
    
@pytest.mark.asyncio
async def test_read_all_branches(client, db_session):
    initial_response = await client.get("/branches/")
    initial_count = len(initial_response.json())
    
    branch_count = 4
    for i in range(branch_count):
        mock = {"title": f"Branch {i}", "description": "Desc"}
        await client.post("/branches/", json=mock)
    
    response = await client.get("/branches/")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == initial_count + branch_count
    
@pytest.mark.asyncio
async def test_delete_branch(client, db_session):
    response = await client.post("/branches/", json=create_branch_mock)
    
    assert response.status_code == 201
    data = response.json()
    branch_id = data["id"]
    
    response = await client.delete(f"/branches/{branch_id}")
    assert response.status_code == 204
    
    response = await client.get(f"/branches/{branch_id}")
    data = response.json()
    assert data["is_active"] == False
