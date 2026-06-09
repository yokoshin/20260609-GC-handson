"""Settings model for Pomodoro timer customization."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Settings:
    """User settings for Pomodoro timer.
    
    Attributes:
        work_duration: Work session duration in minutes (15, 25, 35, or 45)
        break_duration: Break duration in minutes (5, 10, or 15)
        theme: Color theme ('light', 'dark', or 'focus')
        sound_start: Enable start sound (True/False)
        sound_end: Enable end sound (True/False)
        sound_tick: Enable tick sound (True/False)
    """
    
    work_duration: int = 25
    break_duration: int = 5
    theme: str = 'light'
    sound_start: bool = True
    sound_end: bool = True
    sound_tick: bool = False
    
    # Valid values
    VALID_WORK_DURATIONS = [15, 25, 35, 45]
    VALID_BREAK_DURATIONS = [5, 10, 15]
    VALID_THEMES = ['light', 'dark', 'focus']
    
    def validate(self) -> bool:
        """Validate settings values."""
        if self.work_duration not in self.VALID_WORK_DURATIONS:
            return False
        if self.break_duration not in self.VALID_BREAK_DURATIONS:
            return False
        if self.theme not in self.VALID_THEMES:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create settings from dictionary."""
        return cls(
            work_duration=data.get('work_duration', 25),
            break_duration=data.get('break_duration', 5),
            theme=data.get('theme', 'light'),
            sound_start=data.get('sound_start', True),
            sound_end=data.get('sound_end', True),
            sound_tick=data.get('sound_tick', False),
        )
