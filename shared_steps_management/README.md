


# Testrail_testcase_management
### 쉐어드 스텝 추가 작업 코드

# Setup Guide
### —————— Shared step 삭제 및 추가 후 등록작업
* Test project에서는 데이터 전체를 복사해와야함 (01. 파일 실행)

1. 기존 쉐어드 스텝을 json 형식으로 복사 (02. 파일 실행)
2. 새로 생성해야 할 json을 추가 (Manual로 작업)
3. 수정한 json 파일을 쉐어드 스텝 api로 등록 (03. 파일 실행)

4. 04.app_csv_to_json.py 는 app 대상으로만 진행합니다.(이 파일은 Mobile TestCase의 testrail_management 참조해야함)
5. csv를 json으로 변경 (05.app_add_modifued_json_shared_step.py 실행)
6. 수정한 json 파일을 쉐어드 스텝 api로 등록 (03. 파일 실행)