import pytest
from faker import Faker
from app.models.user import User
from app.models.analysis import Analysis, AnalysisStatus
from app.core.security import create_access_token

fake = Faker()

@pytest.mark.integration
class TestAnalysisEndpoints:
    """Integration tests for analysis endpoints"""
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create a test user"""
        from app.core.security import get_password_hash
        user = User(
            email=fake.email(),
            password_hash=get_password_hash("test_password_123")
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    
    @pytest.fixture
    def auth_token(self, test_user):
        """Create auth token for test user"""
        return create_access_token(data={"sub": test_user.id})
    
    @pytest.fixture
    def auth_headers(self, auth_token):
        """Create auth headers"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_create_analysis(self, client, auth_headers):
        """Test creating a new analysis"""
        response = client.post(
            "/api/analyses",
            json={"company_name": "Test Company"},
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["company_name"] == "Test Company"
        assert data["status"] == "pending"
        assert "id" in data
    
    def test_list_analyses(self, client, auth_headers, db_session, test_user):
        """Test listing user's analyses"""
        # Create some analyses
        analysis1 = Analysis(
            user_id=test_user.id,
            company_name="Company 1",
            status=AnalysisStatus.COMPLETED
        )
        analysis2 = Analysis(
            user_id=test_user.id,
            company_name="Company 2",
            status=AnalysisStatus.PENDING
        )
        db_session.add_all([analysis1, analysis2])
        db_session.commit()
        
        response = client.get("/api/analyses", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert any(a["company_name"] == "Company 1" for a in data)
        assert any(a["company_name"] == "Company 2" for a in data)
    
    def test_get_analysis(self, client, auth_headers, db_session, test_user):
        """Test getting analysis details"""
        analysis = Analysis(
            user_id=test_user.id,
            company_name="Test Company",
            status=AnalysisStatus.COMPLETED,
            company_context="Test context"
        )
        db_session.add(analysis)
        db_session.commit()
        db_session.refresh(analysis)
        
        response = client.get(f"/api/analyses/{analysis.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["company_name"] == "Test Company"
        assert data["status"] == "completed"
        assert "scenarios" in data
        assert "strategies" in data
    
    def test_get_analysis_unauthorized(self, client, db_session):
        """Test getting analysis without authentication"""
        response = client.get("/api/analyses/1")
        
        assert response.status_code == 403  # FastAPI returns 403 for missing auth

