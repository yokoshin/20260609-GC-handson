"""Tests for SettingsManager and API endpoints."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from services.settings_manager import SettingsManager
from models.settings import Settings
from app import app, settings_manager


@pytest.fixture
def temp_config_dir():
    """Create temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(autouse=True)
def reset_settings_manager():
    """Reset settings manager cache between tests."""
    yield
    settings_manager.reset_cache()


class TestSettingsManager:
    """Test SettingsManager class."""
    
    def test_load_default_settings(self, temp_config_dir):
        """Test loading default settings when no file exists."""
        manager = SettingsManager(temp_config_dir)
        settings = manager.load()
        
        assert settings.work_duration == 25
        assert settings.break_duration == 5
        assert settings.theme == 'light'
    
    def test_save_settings(self, temp_config_dir):
        """Test saving settings to file."""
        manager = SettingsManager(temp_config_dir)
        settings = Settings(work_duration=35, break_duration=10)
        
        success = manager.save(settings)
        assert success is True
        
        # Verify file was created
        settings_file = Path(temp_config_dir) / 'settings.json'
        assert settings_file.exists()
    
    def test_load_saved_settings(self, temp_config_dir):
        """Test loading previously saved settings."""
        manager1 = SettingsManager(temp_config_dir)
        original = Settings(
            work_duration=45,
            break_duration=15,
            theme='dark',
            sound_start=False,
        )
        manager1.save(original)
        
        # Load with new manager instance
        manager2 = SettingsManager(temp_config_dir)
        loaded = manager2.load()
        
        assert loaded.work_duration == 45
        assert loaded.break_duration == 15
        assert loaded.theme == 'dark'
        assert loaded.sound_start is False
    
    def test_update_settings(self, temp_config_dir):
        """Test updating specific settings."""
        manager = SettingsManager(temp_config_dir)
        
        updated = manager.update(work_duration=35, theme='focus')
        
        assert updated.work_duration == 35
        assert updated.theme == 'focus'
        assert updated.break_duration == 5  # unchanged
    
    def test_save_invalid_settings(self, temp_config_dir):
        """Test that invalid settings are not saved."""
        manager = SettingsManager(temp_config_dir)
        invalid_settings = Settings(work_duration=20)  # invalid
        
        success = manager.save(invalid_settings)
        assert success is False


class TestSettingsAPI:
    """Test Settings API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create Flask test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_get_settings(self, client):
        """Test GET /api/settings returns settings."""
        response = client.get('/api/settings')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'work_duration' in data
        assert 'break_duration' in data
        assert 'theme' in data
        assert 'sound_start' in data
        assert 'sound_end' in data
        assert 'sound_tick' in data
    
    def test_get_settings_default_values(self, client):
        """Test GET /api/settings returns correct default values."""
        response = client.get('/api/settings')
        data = response.get_json()
        
        # Should be defaults
        assert data['work_duration'] in [15, 25, 35, 45]
        assert data['break_duration'] in [5, 10, 15]
        assert data['theme'] in ['light', 'dark', 'focus']
    
    def test_post_settings_valid(self, client):
        """Test POST /api/settings with valid data."""
        new_settings = {
            'work_duration': 35,
            'break_duration': 10,
            'theme': 'dark',
            'sound_start': False,
            'sound_end': True,
            'sound_tick': True,
        }
        
        response = client.post(
            '/api/settings',
            data=json.dumps(new_settings),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['work_duration'] == 35
        assert data['break_duration'] == 10
        assert data['theme'] == 'dark'
    
    def test_post_settings_partial_update(self, client):
        """Test POST /api/settings with partial update."""
        response = client.post(
            '/api/settings',
            data=json.dumps({'theme': 'focus'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['theme'] == 'focus'
        # Other values should be present
        assert 'work_duration' in data

