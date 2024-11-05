


# Testrail_testcase_management
Testrail_testcase_management

쉐어드 스텝 추가 작업 코드

# Setup Guide
—————— Shared step 삭제 및 추가 후 등록작업
Test project에서는 데이터 전체를 복사해와야함 (get_all_shared_steps)

1. 기존 쉐어드 스텝을 json 형식으로 복사 (get_shared_steps)
2. 새로 생성해야 할 json을 추가 (Manual로 작업)
3. 수정한 json 파일을 쉐어드 스텝 api로 등록 (add_shared_step 메서드로 TestRail에 등록한다.)
 
—————— Test cases 연동 작업

1. 기존 테스트 케이스 복제 해놓기 ( test rail의 복제 Copy or Move Cases 클릭 후 csv로 변경 그 후 json으로 변경 후 데이터 전처리) 
1.1) ex : testcase_data.csv 로 저장, 1.2) csv_to_json 실행 1.3), modify_json_data 실행 
2. 복제한 테스트 케이스에 step들 전부 제거 (test_update_all_test_cases_steps api)
3. Import_shared_step.py로 셀레니움 자동화 작입 실행 
4. 완성.
config_example.json -> 별도의 복제파일 (해당 파일을 )

# Read me 내용 기입등등..
