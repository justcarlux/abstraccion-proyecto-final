from storage import StorageDriver

class SettingsManager:
    def __init__(self, storage: StorageDriver):
        self.storage = storage
        self.music_enabled = storage.get_setting("music_enabled", True)
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        self.storage.set_setting("music_enabled", self.music_enabled)
