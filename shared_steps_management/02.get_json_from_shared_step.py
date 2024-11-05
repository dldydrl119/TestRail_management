import base64
import requests
import json
import os

from dotenv import load_dotenv

class SharedStepsManager:
    def __init__(self, base_url, user, api_key):
        self.base_url = base_url
        self.auth_value = self.get_basic_auth_string(user, api_key)

    def get_basic_auth_string(self, username, api_key):
        """Basic Auth 문자열을 반환합니다."""
        credentials = base64.b64encode(
            f"{username}:{api_key}".encode("utf-8")).decode("utf-8")
        return f"Basic {credentials}"

    def remove_ids(self, obj):
        """ID를 제거하는 메서드입니다."""
        if isinstance(obj, dict):
            return {k: v for k, v in obj.items() if k.lower() != 'id'}
        elif isinstance(obj, list):
            return [self.remove_ids(item) for item in obj]
        else:
            return obj

    def export_to_json(self, data, filepath):
        """데이터를 JSON 파일로 저장하는 메서드입니다."""
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(self.remove_ids(data), json_file,
                      ensure_ascii=False, indent=4)

    def get_shared_steps(self, project_id, output_file=None):
        """쉐어드 스텝 전체 리스트를 조회하고 데이터를 저장하는 메서드입니다."""
        endpoint = f"{self.base_url}/index.php?/api/v2/get_shared_steps/{project_id}"
        response = requests.get(endpoint, headers={'Authorization': self.auth_value})

        if response.status_code == 200:
            shared_steps_data = response.json()

            if isinstance(shared_steps_data, list):
                for step in shared_steps_data:
                    print(f"ID: {step.get('id')}")
                    print(f"Title: {step.get('title')}")
                    print("-----------------------")

                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    self.export_to_json(shared_steps_data, output_file)
                    print(f"데이터를 {output_file} 파일로 저장했습니다.")
            else:
                print("공유 단계가 없습니다.")
        else:
            print(f"예상치 못한 오류: {response.status_code}")


# 실행.
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
manager.get_shared_steps(project_id, output_file=json_file_path)
