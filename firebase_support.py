import requests
from firebase_admin import credentials


def _get_access_token() -> str:
    cred = credentials.Certificate("files/firebase.json")
    access_token_info = cred.get_access_token()
    return access_token_info.access_token


class RemoteConfig:
    def __init__(self):
        self.access_token = _get_access_token()

    def get_regions(self) -> list:
        """
        :return: [{"name": region_name, "url": region_url}]
        """
        r = requests.get(
            "https://firebaseremoteconfig.googleapis.com/v1/projects/919516648232/remoteConfig",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Accept-Encoding": "gzip"
            }
        )
        return r.json()

    def send_regions(self, list_of_regions):
        r = requests.put(
            "https://firebaseremoteconfig.googleapis.com/v1/projects/919516648232/remoteConfig",
            headers={
                "Content-Length": "",
                "Content-Type": "application/json;UTF8",
                "Authorization": f"Bearer {self.access_token}",
                "If-Match": "*",
                "Accept-Encoding": "gzip"
            },
            data={"parameters": {"regions": {"defaultValue": {"value": list_of_regions}}}}
        )
        print(r.json())


print(RemoteConfig().send_regions([{"name": "Челябинская область", "url": "https://sgo.edu-74.ru/"}]))