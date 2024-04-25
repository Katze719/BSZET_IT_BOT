import json
import threading
import os

GUILD_SETTINGS_LOCK = threading.Lock()


class GuildSettings:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.file_path = "guild_settings.json"
        self.settings = {}

        self.load_settings()

        if not "routine" in self.settings:
            self.set("name", "")
            self.set("routine", False)
            self.set("routine_channel_id", 0)

    def load_settings(self):
        with GUILD_SETTINGS_LOCK:
            try:
                with open(self.file_path, 'r') as file:
                    all_guild_settings = json.load(file)
                    self.settings = all_guild_settings.get(str(self.guild_id), {})
            except FileNotFoundError:
                self.settings = {}

    def save_settings(self):
        with GUILD_SETTINGS_LOCK:
            all_guild_settings = {}
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, 'r') as file:
                        all_guild_settings = json.load(file)
                except FileNotFoundError:
                    pass

            all_guild_settings[str(self.guild_id)] = self.settings

            with open(self.file_path, 'w') as file:
                json.dump(all_guild_settings, file, indent=4)

    def get(self, key):
        return self.settings.get(key, "Does not exist!")

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get_all_settings(self):
        return self.settings.copy()
