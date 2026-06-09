"""Settings manager for persistent user configuration."""

import json
import os
from pathlib import Path
from models.settings import Settings


class SettingsManager:
    """Manager for reading and writing user settings."""
    
    def __init__(self, config_dir: str = None):
        """Initialize SettingsManager.
        
        Args:
            config_dir: Directory to store settings file. Defaults to ~/.pomodoro_timer
        """
        if config_dir is None:
            config_dir = os.path.expanduser('~/.pomodoro_timer')
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_file = self.config_dir / 'settings.json'
        self._settings = None
    
    def load(self) -> Settings:
        """Load settings from file or return defaults."""
        if self._settings is not None:
            return self._settings
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._settings = Settings.from_dict(data)
            except (json.JSONDecodeError, IOError):
                self._settings = Settings()
        else:
            self._settings = Settings()
        
        return self._settings
    
    def reset_cache(self):
        """Reset the cached settings. Useful for testing."""
        self._settings = None
    
    def save(self, settings: Settings) -> bool:
        """Save settings to file.
        
        Args:
            settings: Settings object to save
            
        Returns:
            True if successful, False otherwise
        """
        if not settings.validate():
            return False
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings.to_dict(), f, indent=2, ensure_ascii=False)
            self._settings = settings
            return True
        except IOError:
            return False
    
    def update(self, **kwargs) -> Settings:
        """Update specific settings fields.
        
        Args:
            **kwargs: Setting fields to update
            
        Returns:
            Updated Settings object
        """
        current = self.load()
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(current, key):
                setattr(current, key, value)
        
        if current.validate():
            self.save(current)
        
        return current
