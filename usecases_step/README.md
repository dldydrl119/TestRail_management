


# Testrail_testcase_management
### 쉐어드 스텝 추가 작업 코드

# Setup Guide
—————— Test cases 연동 작업

1. 기존 테스트 케이스 복제 해놓기( test rail의 복제 Copy or Move Cases 클릭 후 csv로 변경 그 후 json으로 변경 후 데이터 전처리)
2. testcase 데이터 csv 저장 (04.testcase_data.csv 매뉴얼로 저장)  
3. 04.csv_to_json.py 실행
4. 05.preprocess_json_data.py 실행
4. 복제한 테스트 케이스에 step들 전부 제거 (test_update_all_test_cases_steps api)
3. Import_shared_step.py로 셀레니움 자동화 작입 실행 
4. 완성.

config_example.json -> 별도의 복제파일

# Read me 내용 기입등등..
