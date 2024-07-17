import json
import logging
import os

from version import __version__
from datetime_unique_code import current_time


class JsonHelper:
    def __init__(self, path):
        self.path = path
        # TODO:self.vault_id = "UUID"
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.path):
            return self.create_new_vault()
        with open(self.path, 'r') as f:
            data = json.load(f)
        return data

    def save_data(self):
        self.data["metadata"]["last_modified_at"] = current_time(self)
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)
        print("save data successfully")

    def create_new_vault(self):
        return {
            # "vault_id": "UUID",
            "version": __version__,
            "vault_name": "Vault Name",
            "data": {
                "records": []
            },
            "metadata": {
                "created_at": current_time(self),
                "last_modified_at": current_time(self)
            }
        }

    def get_records(self):
        print("getting records")
        return self.data["data"]["records"]

    def add_record(self, site, username, password, notes=""):
        new_id = len(self.data["data"]["records"]) + 1
        new_record = {
            "id": new_id,
            "site": site,
            "username": username,
            "password": password,
            "notes": notes,
            "created_at": current_time(self),
            "last_modified_at": current_time(self)
        }
        self.data["data"]["records"].append(new_record)
        self.save_data()
        print("add record successfully")

    def get_record(self, id):
        for record in self.data["data"]["records"]:
            if record["id"] == id:
                return record
        return None

    def update_record(self, id, site=None, username=None, password=None, notes=None):
        for record in self.data["data"]["records"]:
            if record["id"] == id:
                if site is not None:
                    record["site"] = site
                if username is not None:
                    record["username"] = username
                if password is not None:
                    record["password"] = password
                if notes is not None:
                    record["notes"] = notes
                record["last_modified_at"] = current_time(self)
                self.save_data()
                print("update record successfully")
                return True
        return False

    def delete_record(self, id):
        for record in self.data["data"]["records"]:
            if record["id"] == id:
                self.data["data"]["records"].remove(record)
                self.save_data()
                return True
        return False


if __name__ == "__main__":
    manager = JsonHelper(f"../test/testFile{__version__}.json")
    manager.add_record("example.com", "user@example.com", "mypassword123", "This is an example entry")
    print(manager.get_records())
    manager.update_record(1, password="newpassword123")
    print(manager.get_record(1))
    # manager.delete_record(1)
    # print(manager.get_records())
