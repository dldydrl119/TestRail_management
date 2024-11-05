import base64
import requests
import json
import os

from dotenv import load_dotenv

class SharedStepsManager:

    def __init__(self, base_url, user, api_key):
        self.base_url = base_url
        auth_value = f"{user}:{api_key}".encode('utf-8')
        self.auth_value = f"Basic {base64.b64encode(auth_value).decode('utf-8')}"
    def add_shared_step(self, project_id, title, steps):

        endpoint = f"{self.base_url}/index.php?/api/v2/add_shared_step/{project_id}"
        data = {
            "title": title,
            "custom_steps_separated": steps
        }

        response = requests.post(endpoint, headers={
                                 'Authorization': self.auth_value, 'Content-Type': 'application/json'}, json=data)

        if response.status_code == 200:
            print(
                f"등록 성공 ------------------------- Step ID: {response.json()['id']}")
        else:
            print(
                f"등록 실패 ------------------------- 에러 코드: {response.status_code}")
            print(f"서버 응답 내용:\n{response.text}")

    def upload_shared_steps_from_json(self, project_id, json_file_path):
        """JSON 파일로부터 쉐어드 스텝 데이터를 읽어와서 추가하는 메서드입니다."""
        with open(json_file_path, 'r', encoding='utf-8') as file:
            shared_steps_data = json.load(file)

        for output in shared_steps_data:
            title = output.get("title", "")
            steps = output.get("custom_steps_separated", [])

            self.add_shared_step(project_id, title, steps)

#실행
load_dotenv()

TESTRAIL_BASE_URL = os.getenv("TESTRAIL_BASE_URL")
TESTRAIL_USER = os.getenv("TESTRAIL_USER")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY")

# 사용자로부터 project_id 입력 받기
project_id = input("Enter the project ID: ")

# 입력 받은 값을 출력하여 확인
print(f"Project ID: {project_id}")

manager = SharedStepsManager(TESTRAIL_BASE_URL, TESTRAIL_USER, TESTRAIL_API_KEY)
json_file_path = os.path.join(os.path.dirname(
    __file__), "output", "02.shared_steps_data.json")
manager.upload_shared_steps_from_json(project_id, json_file_path)