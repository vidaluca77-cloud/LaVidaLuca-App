from models import Activity

def test_get_activities(client):
    """Test d'obtention de la liste des activités"""
    response = client.get("/activities/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_categories(client):
    """Test d'obtention des catégories"""
    response = client.get("/activities/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_skills(client):
    """Test d'obtention des compétences"""
    response = client.get("/activities/skills")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)