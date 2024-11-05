import base64
import requests
import json
import os
from dotenv import load_dotenv

class TestRailManager:
    def __init__(self, base_url, user, api_key):
        self.base_url = base_url
        self.auth_value = self.get_basic_auth_string(user, api_key)

    def get_basic_auth_string(self, username, api_key):
        """Basic Auth 문자열을 반환합니다."""
        credentials = base64.b64encode(
            f"{username}:{api_key}".encode("utf-8")).decode("utf-8")
        return f"Basic {credentials}"

    def get_all_shared_steps(self, source_project_id):
        endpoint = f"{self.base_url}/index.php?/api/v2/get_shared_steps/{source_project_id}"
        response = requests.get(endpoint, headers={'Authorization': self.auth_value})

        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to get shared steps from source project. Status Code: {response.status_code}")
            return None

    def copy_all_shared_steps(self, source_project_id, destination_project_id):
        shared_steps_data = self.get_all_shared_steps(source_project_id)

        if not shared_steps_data:
            print(f"프로젝트 쉐어드 스텝 리스트가 없습니다.")
            return

        for shared_step_data in shared_steps_data:
            title = shared_step_data.get('title')
            custom_steps_separated = shared_step_data.get('custom_steps_separated')

            if not title or not custom_steps_separated:
                print(f"복사 프로젝트의 쉐어드 스텝 {title}의 데이터가 올바르지 않습니다.")
                continue

            destination_endpoint = f"{self.base_url}/index.php?/api/v2/add_shared_step/{destination_project_id}"
            data = {
                "title": title,
                "custom_steps_separated": custom_steps_separated,
            }

            destination_response = requests.post(destination_endpoint, headers={
                                                 'Authorization': self.auth_value, 'Content-Type': 'application/json'}, json=data)

            if destination_response.status_code == 200:
                print(f"공유 단계 '{title}'이(가) 성공적으로 추가되었습니다.")
            else:
                print(
                    f"공유 단계 '{title}'의 추가에 실패했습니다. Status Code: {destination_response.status_code}")
                print(f"Response Content: {destination_response.content}")

# 실행.
load_dotenv()

TESTRAIL_BASE_URL = os.getenv("TESTRAIL_BASE_URL")
TESTRAIL_USER = os.getenv("TESTRAIL_USER")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY")

# 사용자로부터 source_project_id 입력 받기
source_project_id = input("Enter the source project ID: ")

# 사용자로부터 destination_project_id 입력 받기
destination_project_id = input("Enter the destination project ID: ")

# 입력 받은 값을 출력하여 확인
print(f"Source Project ID: {source_project_id}")
print(f"Destination Project ID: {destination_project_id}")

manager = TestRailManager(TESTRAIL_BASE_URL, TESTRAIL_USER, TESTRAIL_API_KEY)
manager.copy_all_shared_steps(source_project_id, destination_project_id)