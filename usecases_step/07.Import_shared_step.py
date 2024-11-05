import os
import re
import json
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

class TestCaseHandler:
    def __init__(self, base_url, username, password, chrome_driver_path):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.chrome_driver_path = chrome_driver_path
        self.driver = None

    def setup_driver(self):
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=self.chrome_driver_path))

    def login(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "name").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "button_primary").click()
        time.sleep(2)

    def copy_steps(self, test_case_url, cases):
        try:
            self.driver.get(test_case_url)

            test_cases_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "navigation-suites"))
            )
            test_cases_link.click()
            time.sleep(4)

            filter_menu = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "filterBy"))
            )

            if "toolbar-highlighted" not in filter_menu.get_attribute("class"):
                filter_menu.click()
                time.sleep(2)
                print("Filter menu clicked.")
            else:
                print("Filter menu is already applied. Skipping click.")

            section_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "filterByChange"))
            )
            section_option.click()
            time.sleep(2)

            section_filter = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='filter-cases:section_id']"))
            )

            if "filterCollapse" not in section_filter.get_attribute("class"):
                print("Section filter is currently expanded. Collapsing...")

                section_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='link-noline' and text()='Section']"))
                )
                section_link.click()
                time.sleep(2)  # 필요에 따라 조절

                print("Section filter collapsed.")
            else:
                print("Section filter is already collapsed. Skipping collapse.")

            gmarket_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), '1.1 회원가입 / ID & 비밀번호 찾기')]"))
            )
            gmarket_option.click()
            time.sleep(2)

            ok_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "filterCasesApply"))
            )
            ok_button.click()
            time.sleep(3)


            # 특정 행의 링크를 찾아서 클릭
            try:
                row_id = "row-288121"
                row_xpath = f"//tr[@id='{row_id}']//td[@class='id']//a[@class='link-noline']"

                row_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, row_xpath))
                )
                row_link.click()
                print(f"해당 열을 클릭합니다. {row_id}")
            except Exception as e:
                print(f"에러 : 클릭하지 못했습니다. {e}")
            time.sleep(3)

            for case in cases:
                try:
                    if self.compare_and_add_steps(case):
                        print(f"'{case['Title']}'이 성공적으로 추가되었습니다.")
                        # 저장 버튼 클릭
                        save_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save Test Case')]"))
                        )
                        save_button.click()
                        time.sleep(2)

                        # 다음 버튼 클릭
                        next_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "directionNext"))
                        )
                        next_button.click()
                        time.sleep(3)
                    else:
                        print(f"'{cases[0]['Title']}'이 추가되지 않았습니다.")
                    time.sleep(2)

                except TimeoutException:
                    print("다음 버튼을 찾을 수 없습니다. 작업을 종료합니다.")
                    break
                except Exception as e:
                    print(f"에러 발생: {e}")
                    break

        finally:
            # 웹 드라이버 종료
            self.driver.quit()

    def normalize_step(self, step):
        normalized_step = step.replace('\n', '\\n').replace(' ', '')
        return normalized_step

    def increase_numbers(match):
        number = int(match.group(1))
        return f'selectSharedStepsSet_chzn_o_{number + 1}'

    # def apply_number_increase(html_content):
    #     pattern = re.compile(r'selectSharedStepsSet_chzn_o_(\d+)')
    #     return pattern.sub(increase_numbers, html_content)

    def teardown_driver(self):
        self.driver.quit()

    def compare_and_add_steps(self, case):
        try:


            # Edit 버튼 클릭
            edit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'button-edit')]"))
            )
            edit_button.click()
            time.sleep(3)

            # Edit 버튼 클릭 후 대기 시간 추가 (페이지가 변경될 때까지)
            WebDriverWait(self.driver, 20).until(
                EC.staleness_of(edit_button)
            )

            # 페이지가 변경되었으므로 Title 값을 새로 가져옴
            title_div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='content-header-title page_title']"))
            )
            title_input_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "title"))
            )

            # 각 타이틀 요소의 값을 가져옴
            page_title_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "title"))
            ).get_attribute("value").strip().replace('\n', '')

            # JSON 데이터의 Title 값과 페이지의 Title 값을 비교 (정확한 비교로 수정)
            if case['Title'].strip() != page_title_input:
                print(f"페이지의 Title과 JSON 데이터의 Title이 일치하지 않습니다: '{page_title_input}' != '{case['Title'].strip()}'")
                print(f"JSON 데이터의 Title: '{case['Title'].strip()}'")
                print(f"페이지의 Title (input): '{page_title_input}'")
                return False
            else:
                print(f"JSON 데이터의 Title과 페이지의 Title이 일치합니다.")
                print(f"J'{page_title_input}' != '{case['Title'].strip()}'")

            # Preconditions 데이터가 존재하는 경우, 해당 데이터를 입력 필드에 추가
            if case.get('Preconditions', '').strip():
                preconditions_textarea = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "custom_preconds"))
                )
                preconditions_textarea.clear()
                preconditions_textarea.send_keys(case['Preconditions'].strip())
                print(f"Preconditions 데이터가 추가되었습니다: {case['Preconditions'].strip()}")
            else:
                print("Preconditions 데이터가 없으므로 건너뜁니다.")

            # Add Step 버튼 클릭
            add_step_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='addStep']"))
            )
            add_step_button.click()
            time.sleep(2)
            # Test Case
            next_option_id = 0  # 초기값 설정

            matched_steps = set()  # 이미 일치한 단계를 저장할 집합

            for step_index, step in enumerate(case['Steps']):
                normalized_step = self.normalize_step(step)
                step_found = False  # 일치하는 스텝을 찾았는지 여부 초기화

                try:
                    # Import 버튼 찾기 (모든 importStep 클래스를 가져옴)
                    import_buttons = self.driver.find_elements(By.CLASS_NAME, "importStep")
                    time.sleep(2)
                    # 리스트의 마지막 요소 (즉, HTML에서 마지막 'importStep' 클래스를 가진 요소)를 선택합니다.
                    if import_buttons:
                        last_import_button = import_buttons[-1]
                        last_import_button.click()
                        print("마지막 Import 버튼을 성공적으로 클릭했습니다.")
                    else:
                        print("Import 버튼을 찾을 수 없습니다.")

                except Exception as e:
                    print("Import 버튼을 찾을 수 없습니다.")
                    print(f"오류 메시지: {e}")

                # WebDriverWait를 사용하여 요소를 찾을 때까지 대기
                try:
                    # JavaScript 코드 실행
                    script = "document.querySelector('.ui-widget-overlay').style.display='none';"
                    self.driver.execute_script(script)
                    print("Overlay 요소의 display 속성을 변경했습니다.")
                except Exception as e:
                    print(f"오류 발생: {e}")
                    print("Overlay 요소를 찾을 수 없습니다.")

                # select 요소를 찾습니다.
                select_element = self.driver.find_element(By.ID, "selectInsertWhere")
                # Select 객체를 생성합니다.
                select_object = Select(select_element)

                # 'after' 옵션을 선택합니다.
                select_object.select_by_value("before")

                # steps_to_select 변수 정의
                steps_to_select = case['Steps']

                for step_option in steps_to_select:
                    option_normalized_step = self.normalize_step(step_option)

                    if option_normalized_step == normalized_step:
                        # 옵션 상자 열기
                        option_box_id = "selectSharedStepsSet_chzn"
                        option_box = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.ID, option_box_id))
                        )
                        # 클릭하기
                        option_box.click()
                        time.sleep(1)
                        # 다음 옵션의 index 계산

                        # 다음 옵션의 id 생성
                        next_option_id = int(next_option_id)
                        next_option_id_str = f"selectSharedStepsSet_chzn_o_{next_option_id + 1}"
                        time.sleep(1)
                        # 다음 옵션 선택
                        next_option = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.ID, next_option_id_str))
                        )
                        next_option.click()
                        # 선택 후 대기
                        time.sleep(2)
                        step_with_newline = step.replace('\n', '\\n')
                        option_xpath = f'//td[@class="step-content"]//input[contains(@value, "{step_with_newline}")]'

                        # 간단한 대기 시간 추가
                        time.sleep(2)

                        while not step_found:
                            try:
                                # 현재 선택된 옵션에 대한 preview 요소 찾기
                                preview_elements = self.driver.find_elements(By.CLASS_NAME, "shared_steps_preview")
                                active_preview_elements = [elem for elem in preview_elements if
                                                           "hidden" not in elem.get_attribute("class")]

                                for preview_element in active_preview_elements:
                                    # 현재 스텝에 해당하는 preview_element에서 <input> 요소 찾기
                                    input_element = preview_element.find_element(By.TAG_NAME, "input")
                                    input_value = self.normalize_step(input_element.get_attribute("value"))

                                    if input_value == normalized_step:
                                        # 일치하는 스텝을 찾았으므로 Import 버튼 클릭 및 처리
                                        import_steps_button = WebDriverWait(self.driver, 20).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//button[contains(text(), 'Import steps')]"))
                                        )
                                        import_steps_button.click()
                                        step_found = True
                                        print(f"'{normalized_step}' 단계가 일치하여 추가되었습니다.")
                                        break

                                if step_found:
                                    break  # 일치하는 스텝을 찾았으면 루프 종료

                                if not step_found:
                                    print(f"'{normalized_step}' 단계와 일치하는 항목을 찾을 수 없습니다.")
                                    # 다음 옵션 선택을 위해 옵션 id를 증가시킵니다.
                                    # 옵션 상자 열기
                                    option_box_id = "selectSharedStepsSet_chzn"
                                    option_box = WebDriverWait(self.driver, 10).until(
                                        EC.presence_of_element_located((By.ID, option_box_id))
                                    )
                                    # 클릭하기
                                    option_box.click()
                                    time.sleep(1)
                                    # 다음 옵션의 index 계산

                                    # 다음 옵션의 id 생성
                                    next_option_id += 1
                                    next_option_id_str = f"selectSharedStepsSet_chzn_o_{next_option_id + 1}"
                                    time.sleep(1)
                                    print(f"'{next_option_id_str}' ")
                                    # 다음 옵션 선택
                                    next_option = WebDriverWait(self.driver, 10).until(
                                        EC.element_to_be_clickable((By.ID, next_option_id_str))
                                    )
                                    next_option.click()

                                    # 선택 후 대기
                                    time.sleep(2)

                            except Exception as e:
                                print(f"예외 발생: {e}")
                                break

                        if not step_found:
                            print(f"모든 옵션을 검토했으나 '{normalized_step}' 단계와 일치하는 항목을 찾을 수 없습니다.")

                        if step_index == len(case['Steps']) - 1:
                            print("모든 단계가 검토되었습니다.")
                            # 닫기 버튼을 찾아 클릭
                            try:
                                close_button = WebDriverWait(self.driver, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-dialog-titlebar-close"))
                                )
                                close_button.click()
                                print("모달 창이 닫혔습니다.")
                            except Exception as e:
                                print(f"모달 창을 닫을 수 없습니다: {e}")

        except TimeoutException:
            print(f"옵션 '{normalized_step}'을(를) 찾을 수 없습니다.")
        except Exception as e:
            print(f"에러 발생ㅠ: {e}")

        return True


def main():
    # .env 파일에서 환경 변수 읽어오기
    load_dotenv()

    # .env 파일에서 값 가져오기
    base_url = os.getenv("TESTRAIL_BASE_URL")
    username = os.getenv("TESTRAIL_USER")
    password = os.getenv("TESTRAIL_PASSWORD")
    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")

    # 테스트 데이터 읽어오기
    with open('usecases_step/output/05.clean_data.json', 'r', encoding='utf-8') as json_file:
        cases = json.load(json_file)

    # TestCaseHandler 인스턴스 생성
    test_handler = TestCaseHandler(base_url, username, password, chrome_driver_path)

    try:
        # 드라이버 설정
        test_handler.setup_driver()

        # 로그인
        test_handler.login()

        # 특정 테스트 케이스 URL
        test_case_url = "http://172.30.2.20/index.php?/shared_steps/overview/113"

        # 테스트 케이스 복사 및 스텝 추가
        test_handler.copy_steps(test_case_url, cases)

    finally:
        # 드라이버 종료
        test_handler.teardown_driver()

if __name__ == "__main__":
    main()