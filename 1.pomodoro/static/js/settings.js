/**
 * Settings Manager - Handle user preferences for Pomodoro timer
 */

class SettingsUI {
  constructor() {
    this.settingsPanel = document.getElementById('settings-panel');
    this.settingsToggle = document.getElementById('settings-toggle');
    this.settingsClose = document.getElementById('settings-close');
    
    // Settings controls
    this.workDurationSelect = document.getElementById('work-duration');
    this.breakDurationSelect = document.getElementById('break-duration');
    this.themeSelect = document.getElementById('theme');
    this.soundStartCheckbox = document.getElementById('sound-start');
    this.soundEndCheckbox = document.getElementById('sound-end');
    this.soundTickCheckbox = document.getElementById('sound-tick');
    
    this.init();
  }
  
  init() {
    this.attachEventListeners();
    this.loadSettings();
  }
  
  attachEventListeners() {
    // Toggle panel
    this.settingsToggle.addEventListener('click', () => this.togglePanel());
    this.settingsClose.addEventListener('click', () => this.closePanel());
    
    // Settings changes
    this.workDurationSelect.addEventListener('change', () => this.saveSettings());
    this.breakDurationSelect.addEventListener('change', () => this.saveSettings());
    this.themeSelect.addEventListener('change', () => this.saveSettings());
    this.soundStartCheckbox.addEventListener('change', () => this.saveSettings());
    this.soundEndCheckbox.addEventListener('change', () => this.saveSettings());
    this.soundTickCheckbox.addEventListener('change', () => this.saveSettings());
    
    // Close panel when clicking outside
    document.addEventListener('click', (event) => {
      if (!this.settingsPanel.contains(event.target) && 
          !this.settingsToggle.contains(event.target)) {
        this.closePanel();
      }
    });
  }
  
  togglePanel() {
    this.settingsPanel.classList.toggle('hidden');
  }
  
  closePanel() {
    this.settingsPanel.classList.add('hidden');
  }
  
  async loadSettings() {
    try {
      const response = await fetch('/api/settings');
      if (!response.ok) throw new Error('Failed to load settings');
      
      const settings = await response.json();
      
      // Update UI
      this.workDurationSelect.value = settings.work_duration;
      this.breakDurationSelect.value = settings.break_duration;
      this.themeSelect.value = settings.theme;
      this.soundStartCheckbox.checked = settings.sound_start;
      this.soundEndCheckbox.checked = settings.sound_end;
      this.soundTickCheckbox.checked = settings.sound_tick;
      
      // Apply theme
      this.applyTheme(settings.theme);
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }
  
  async saveSettings() {
    const settings = {
      work_duration: parseInt(this.workDurationSelect.value),
      break_duration: parseInt(this.breakDurationSelect.value),
      theme: this.themeSelect.value,
      sound_start: this.soundStartCheckbox.checked,
      sound_end: this.soundEndCheckbox.checked,
      sound_tick: this.soundTickCheckbox.checked,
    };
    
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });
      
      if (!response.ok) throw new Error('Failed to save settings');
      
      const saved = await response.json();
      
      // Apply theme
      this.applyTheme(saved.theme);
      
      // Dispatch event for other parts of the app
      window.dispatchEvent(new CustomEvent('settingsChanged', { detail: saved }));
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  }
  
  applyTheme(theme) {
    document.body.classList.remove('dark-theme', 'focus-theme');
    
    if (theme === 'dark') {
      document.body.classList.add('dark-theme');
    } else if (theme === 'focus') {
      document.body.classList.add('focus-theme');
    }
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new SettingsUI();
});
