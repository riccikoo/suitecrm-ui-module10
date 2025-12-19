import requests
from services.suitecrm_service import SuiteCRMService

RELATION_NAME = "ha_doctor_ha_hospital_1"  # nama relasi yang tepat, bukan tabel relasi langsung

def assign_doctor_to_hospital(doctor_id, hospital_id, token):
    url = f"{SuiteCRMService.API_V8}/ha_hospital/{hospital_id}/relationships/{RELATION_NAME}"
    payload = {
        "data": {
            "type": "ha_doctor",
            "id": doctor_id
        }
    }
    response = requests.post(url, json=payload, headers=SuiteCRMService.headers(token))
    if response.status_code in (200, 201, 204):
        return True, "Doctor assigned to hospital successfully."
    else:
        print("Payload ke SuiteCRM:", payload)
        print("Response dari SuiteCRM:", response.text)
        return False, f"Failed to assign doctor: {response.text}"

def unassign_doctor_from_hospital(doctor_id, hospital_id, token):
    url = f"{SuiteCRMService.API_V8}/ha_hospital/{hospital_id}/relationships/{RELATION_NAME}/{doctor_id}"
    response = requests.delete(url, headers=SuiteCRMService.headers(token))
    if response.status_code in (200, 204):
        return True, "Doctor unassigned from hospital successfully."
    else:
        return False, f"Failed to unassign doctor: {response.text}"
