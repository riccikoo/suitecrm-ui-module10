import requests
from config import API_V8

class SuiteCRMService:

    API_V8 = API_V8

    @staticmethod
    def headers(token):
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def create(token, data):
        return requests.post(API_V8, json=data, headers=SuiteCRMService.headers(token))

    @staticmethod
    def get_all(module, token):
        return requests.get(
            f"{API_V8}/{module}",
            headers=SuiteCRMService.headers(token)
        )

    @staticmethod
    def get_by_id(module, record_id, token):
        return requests.get(
            f"{API_V8}/{module}/{record_id}",
            headers=SuiteCRMService.headers(token)
        )

    @staticmethod
    def update(token, data):
        return requests.patch(
            API_V8,
            json=data,
            headers=SuiteCRMService.headers(token)
        )

    @staticmethod
    def delete(module, record_id, token):
        return requests.delete(
            f"{API_V8}/{module}/{record_id}",
            headers=SuiteCRMService.headers(token)
        )
