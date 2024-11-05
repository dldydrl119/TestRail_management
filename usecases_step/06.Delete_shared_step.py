import os
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class TestLogout:
    def __init__(self, base_url, username, password, shared_step_project_id, chrome_driver_path):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.shared_step_project_id = shared_step_project_id
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
    def setup_driver(self):
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=self.chrome_driver_path))

    def login(self):
        self.driver.get(self.base_url)
        self.driver.find_element("id", "name").send_keys(self.username)
        self.driver.find_element("id", "password").send_keys(self.password)
        self.driver.find_element("id", "button_primary").click()
        time.sleep(2)

    def delete_shared_step(self):
        delete_url = f"{self.base_url}/index.php?/shared_steps/overview/{self.shared_step_project_id}"
        self.driver.get(delete_url)
        time.sleep(4)

        while True:
            elements = self.driver.find_elements(By.CLASS_NAME, "caseRow.row")
            if elements:
                first_element = elements[0]
                if first_element.is_enabled():
                    ActionChains(self.driver).move_to_element(first_element).perform()
                else:
                    print("첫 번째 요소가 비활성화되었습니다. 호버 동작을 건너뜁니다.")
            else:
                print("지정한 클래스의 요소를 찾을 수 없습니다. 종료 중입니다.")
                break

            try:
                delete_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-small-delete.hidden.action-hover"))
                )
                delete_button.click()

                # 팝업 오버레이 숨기기
                script = "document.querySelector('.ui-widget-overlay').style.display='none';"
                self.driver.execute_script(script)

                try:
                    # "dialog-body" 클래스를 가진 div 요소 확인
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".dialog-body"))
                    )

                    # 라디오 버튼 클릭
                    radio_button = self.driver.find_element(By.ID, "shared_steps_convert")
                    radio_button.click()

                    # "Delete" 버튼 클릭
                    delete_full_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "deleteFullButton"))
                    )
                    delete_full_button.click()

                except Exception as e:
                    print("HTML 요소가 존재하지 않습니다. 대체 스크립트 실행합니다.")

                    self.driver.execute_script("App.SharedSteps.deleteSimplifiedSharedStepsSet();")


                self.driver.refresh()
                time.sleep(2)

            except StaleElementReferenceException:
                print("오래된 요소 참조 예외. 다시 시도하는 중...")
                continue

    def run_test_logout(self):
        try:
            self.setup_driver()  # WebDriver 설정
            self.login()
            self.delete_shared_step()
        finally:
            if self.driver:
                self.driver.quit()


# 실행
load_dotenv()

base_url = os.getenv("TESTRAIL_BASE_URL")
username = os.getenv("TESTRAIL_USER")
password = os.getenv("TESTRAIL_PASSWORD")
chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

# 사용자로부터 shared_step_project_id 입력 받기
shared_step_project_id = input("Enter the shared step project ID: ")

# 입력 받은 값을 출력하여 확인
print(f"Shared Step Project ID: {shared_step_project_id}")

test_logout = TestLogout(base_url, username, password, shared_step_project_id, chrome_driver_path)
test_logout.run_test_logout()
