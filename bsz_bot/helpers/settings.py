import json
import threading
import os
import discord

GUILD_SETTINGS_LOCK = threading.Lock()


class GuildSettings:
    def __init__(self, guild : discord.Guild):
        """
        Initializes a new instance of the GuildSettings class.

        Args:
            guild_id (int): The ID of the guild.

        Initializes the instance with the given guild ID and sets the file path to "/settings/guild_settings.json".
        Initializes the settings dictionary to an empty dictionary.
        Calls the load_settings method to load the settings from the file.
        If the "routine" key is not present in the settings dictionary, sets the following keys with their respective values:
        - "name" with an empty string
        - "routine" with False
        - "routine_channel_id" with 0
        """
        
        self.guild_id = guild.id
        self.file_path = "/settings/guild_settings.json"
        self.settings = {}

        self.load_settings()

        if not "routine" in self.settings:
            self.set("name", guild.name)
            self.set("routine", False)
            self.set("routine_channel_id", 0)
            self.set("file_url", "(use default)")
            self.set("username", "(use default)")
            self.set("password", "(use default)")
            self.set("output_name", f"{guild.id}")

        self.__backwards_compatibility_check(guild)

    def __backwards_compatibility_check(self, guild : discord.Guild):
        """
        Check if the settings file is in the old format and convert it to the new format if necessary.

        This method checks if the settings file is in the old format by checking if the "name" key is present.
        """
        if not "name" in self.settings:
            self.set("name", guild.name)
        if not "routine" in self.settings:
            self.set("routine", False)
        if not "routine_channel_id" in self.settings:
            self.set("routine_channel_id", 0)
        if not "file_url" in self.settings:
            self.set("file_url", "(use default)")
        if not "username" in self.settings:
            self.set("username", "(use default)")
        if not "password" in self.settings:
            self.set("password", "(use default)")
        if not "output_name" in self.settings:
            self.set("output_name", f"{guild.id}")


    def load_settings(self):
        """
        Load the settings for the current guild from a JSON file.

        This method reads the settings from a JSON file specified by the `file_path` attribute of the class.
        It retrieves the settings for the current guild by looking up the guild ID in the JSON file.
        If the guild ID is not found in the JSON file, an empty dictionary is assigned to the `settings` attribute.

        Parameters:
            None

        Returns:
            None
        """
        with GUILD_SETTINGS_LOCK:
            try:
                with open(self.file_path, 'r') as file:
                    all_guild_settings = json.load(file)
                    self.settings = all_guild_settings.get(str(self.guild_id), {})
            except FileNotFoundError:
                self.settings = {}

    def save_settings(self):
        """
        Save the settings for the current guild to a JSON file.

        This method saves the guild settings to a JSON file specified by the `file_path` attribute of the class.
        It updates the all_guild_settings dictionary with the current guild settings.
        If the file path exists, it loads existing settings from the file and then updates them.
        If the file does not exist, it creates a new file and writes the current guild settings to it.

        Parameters:
            None

        Returns:
            None
        """
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
        """
        Get the value associated with the given key from the settings dictionary.

        Parameters:
            key (Any): The key to retrieve the value for.

        Returns:
            Any: The value associated with the key, or "Does not exist!" if the key is not found.
        """
        return self.settings.get(key, "Does not exist!")

    def set(self, key, value):
        """
        Set the value of a key in the settings dictionary and save the updated settings.

        Parameters:
            key (Any): The key to set the value for.
            value (Any): The value to set for the key.

        Returns:
            None
        """
        self.settings[key] = value
        self.save_settings()

    def get_all_settings(self):
        """
        Returns a copy of all the settings stored in the object.

        :return: A dictionary containing all the settings.
        :rtype: dict
        """
        return self.settings.copy()
