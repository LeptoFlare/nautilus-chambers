"""Set up database client."""
import requests

from . import env, deep

if env.get("debug"):
    from mongomock import MongoClient
else:
    from pymongo import MongoClient


class DatabaseHandler:
    """Custom database handler that works with mongodb."""

    def __init__(self):
        # Client & Database
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client["nautilus"]

        # Collections
        self.profiles = self.db["profiles"]

    def find_profile(self, discord):
        """Find a profile in the database."""
        profile = self.profiles.find_one(discord)
        return {"status": bool(profile), "profile": profile}

    def insert_profile(self, discord, profile):
        """Insert a new profile into the database."""
        profile = deep.update(self.empty_profile(), profile)
        return {"profile": profile, "status": self.profiles.insert_one({**profile, **self.by_id(discord)}).acknowledged}

    def update_profile(self, discord, profile):
        """Update a profile in the database."""
        profile = deep.update(self.profiles.find_one(discord), profile)
        return {"profile": profile, "status": self.profiles.replace_one(self.by_id(discord), profile).acknowledged}

    def delete_profile(self, discord):
        """Delete a profile in the database."""
        return {"status": self.profiles.delete_one(self.by_id(discord)).acknowledged}

    @staticmethod
    def by_id(discord):
        """Return a query using discord as the _id."""
        return {"_id": discord}

    @staticmethod
    def empty_profile():
        """Return an empty profile."""
        return {
            "meta": {
                "private": None
            },
            "status": {
                "ign": None,
                "sw": None,
                "level": None,
                "rank": {
                    "sz": None,
                    "tc": None,
                    "rm": None,
                    "cb": None,
                    "sr": None,
                },
                "gear": {
                    "weapon": {
                        "id": None,
                        "class": None,
                    },
                    "head": {
                        "id": None,
                        "abilities": {"main": None, "subs": [None]}
                    },
                    "clothes": {
                        "id": None,
                        "abilities": {"main": None, "subs": [None]}
                    },
                    "shoes": {
                        "id": None,
                        "abilities": {"main": None, "subs": [None]}
                    }
                }
            }
        }


dbh = DatabaseHandler()
