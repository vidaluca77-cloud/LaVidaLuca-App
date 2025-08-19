def test_create_user(client, test_user):
    """Test de création d'utilisateur"""
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data

def test_create_duplicate_user(client, test_user):
    """Test de création d'utilisateur avec email déjà existant"""
    # Créer le premier utilisateur
    client.post("/users/", json=test_user)
    
    # Tenter de créer un duplicata
    response = client.post("/users/", json=test_user)
    assert response.status_code == 400

def test_login_success(client, test_user):
    """Test de connexion réussie"""
    # Créer l'utilisateur
    client.post("/users/", json=test_user)
    
    # Se connecter
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test de connexion avec mauvais mot de passe"""
    # Créer l'utilisateur
    client.post("/users/", json=test_user)
    
    # Tenter de se connecter avec un mauvais mot de passe
    login_data = {
        "email": test_user["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401

def test_get_current_user(client, test_user):
    """Test d'obtention des informations utilisateur"""
    # Créer l'utilisateur
    client.post("/users/", json=test_user)
    
    # Se connecter pour obtenir le token
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Obtenir les informations utilisateur
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]