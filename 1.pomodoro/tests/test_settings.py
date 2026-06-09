"""Tests for Settings model."""

import pytest
from models.settings import Settings


class TestSettings:
    """Test Settings model."""
    
    def test_default_values(self):
        """Test default settings values."""
        settings = Settings()
        assert settings.work_duration == 25
        assert settings.break_duration == 5
        assert settings.theme == 'light'
        assert settings.sound_start is True
        assert settings.sound_end is True
        assert settings.sound_tick is False
    
    def test_valid_work_durations(self):
        """Test valid work duration values."""
        for duration in [15, 25, 35, 45]:
            settings = Settings(work_duration=duration)
            assert settings.validate() is True
    
    def test_invalid_work_duration(self):
        """Test invalid work duration."""
        settings = Settings(work_duration=20)
        assert settings.validate() is False
    
    def test_valid_break_durations(self):
        """Test valid break duration values."""
        for duration in [5, 10, 15]:
            settings = Settings(break_duration=duration)
            assert settings.validate() is True
    
    def test_invalid_break_duration(self):
        """Test invalid break duration."""
        settings = Settings(break_duration=7)
        assert settings.validate() is False
    
    def test_valid_themes(self):
        """Test valid theme values."""
        for theme in ['light', 'dark', 'focus']:
            settings = Settings(theme=theme)
            assert settings.validate() is True
    
    def test_invalid_theme(self):
        """Test invalid theme."""
        settings = Settings(theme='invalid')
        assert settings.validate() is False
    
    def test_to_dict(self):
        """Test converting settings to dictionary."""
        settings = Settings(
            work_duration=35,
            break_duration=10,
            theme='dark',
            sound_start=False,
            sound_end=False,
            sound_tick=True,
        )
        data = settings.to_dict()
        
        assert data['work_duration'] == 35
        assert data['break_duration'] == 10
        assert data['theme'] == 'dark'
        assert data['sound_start'] is False
        assert data['sound_end'] is False
        assert data['sound_tick'] is True
    
    def test_from_dict(self):
        """Test creating settings from dictionary."""
        data = {
            'work_duration': 45,
            'break_duration': 15,
            'theme': 'focus',
            'sound_start': False,
            'sound_end': False,
            'sound_tick': True,
        }
        settings = Settings.from_dict(data)
        
        assert settings.work_duration == 45
        assert settings.break_duration == 15
        assert settings.theme == 'focus'
        assert settings.sound_start is False
        assert settings.sound_end is False
        assert settings.sound_tick is True
    
    def test_from_dict_with_defaults(self):
        """Test from_dict with missing fields uses defaults."""
        data = {'work_duration': 35}
        settings = Settings.from_dict(data)
        
        assert settings.work_duration == 35
        assert settings.break_duration == 5  # default
        assert settings.theme == 'light'  # default
