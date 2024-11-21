import os
import hashlib
import requests

class OTAUpdateManager:
    def __init__(self, update_path):
        self.update_path = update_path

    def download_file(self, url, version):
        file_path = f"{self.update_path}/{version}/update.tar.gz"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        response = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path

    def verify_checksum(self, file_path, expected_checksum):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest() == expected_checksum

    def apply_update(self, file_path, version):
        os.system(f"tar -xzf {file_path} -C /web_ivi")
        with open(f"{self.update_path}/current_version.txt", "w") as f:
            f.write(version)

    def download_and_apply_update(self, version, url, checksum):
        file_path = self.download_file(url, version)
        if not self.verify_checksum(file_path, checksum):
            raise ValueError("Checksum mismatch")
        self.apply_update(file_path, version)
