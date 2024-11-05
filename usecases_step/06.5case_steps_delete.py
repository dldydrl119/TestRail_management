import os
import requests
from dotenv import load_dotenv

class TestRailApi:
    def __init__(self, base_url, user, api_key):
        self.base_url = base_url
        self.auth = (user, api_key)  # API 키를 사용하여 인증 정보 설정

    def update_all_test_cases_steps(self, project_id):
        endpoint = f"{self.base_url}/index.php?/api/v2/get_cases/{project_id}"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(endpoint, headers=headers, auth=self.auth)

        if response.status_code == 200:
            test_cases = response.json()
            for test_case in test_cases:
                test_case_id = test_case['id']
                self.update_test_case_steps(test_case_id, [])
            print("모든 테스트 케이스의 스텝이 성공적으로 업데이트되었습니다.")
        else:
            print(f"API 호출이 실패하였습니다. 응답 코드: {response.status_code}")
            print(response.text)

    def update_test_case_steps(self, test_case_id, steps):
        endpoint = f"{self.base_url}/index.php?/api/v2/update_case/{test_case_id}"
        headers = {'Content-Type': 'application/json'}
        data = {'custom_steps_separated': steps}
        response = requests.post(endpoint, headers=headers, json=data, auth=self.auth)  # POST 방식 사용

        if response.status_code == 200:
            print(f"테스트 케이스 {test_case_id}의 스텝이 성공적으로 업데이트되었습니다.")
        else:
            print(f"API 호출이 실패하였습니다. 응답 코드: {response.status_code}")
            print(response.text)

load_dotenv()
TESTRAIL_BASE_URL = os.getenv("TESTRAIL_BASE_URL")
TESTRAIL_USER = os.getenv("TESTRAIL_USER")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY")  # API 키 환경 변수 추가

api = TestRailApi(TESTRAIL_BASE_URL, TESTRAIL_USER, TESTRAIL_API_KEY)  # API 키 전달

api.update_all_test_cases_steps(project_id=113)
