import os
import csv
import json

class CSVtoJSONConverter:
    def __init__(self, script_directory):
        self.script_directory = script_directory

    def csv_to_json(self, csv_file, json_file):
        """CSV 파일을 JSON 형식으로 변환하는 메서드입니다."""

        # CSV 파일의 절대 경로 생성
        csv_file_path = os.path.join(self.script_directory, '../shared_steps_management/output', csv_file)

        # JSON으로 변환할 데이터 리스트
        json_data = []

        # CSV 파일 읽기
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # 데이터 읽기
            for row in csv_reader:
                # custom_steps_separated 객체 생성
                custom_steps_separated = [{
                    "content": row["custom_steps_separated_content"],
                    "expected": row["custom_steps_separated_expected"]
                }]

                # JSON 객체 생성 및 추가
                json_obj = {
                    "title": row["title"],
                    "project_id": int(row["project_id"]),
                    "created_by": int(row["created_by"]),
                    "created_on": int(row["created_on"]),
                    "updated_by": int(row["updated_by"]),
                    "updated_on": int(row["updated_on"]),
                    "custom_steps_separated": custom_steps_separated,
                    "case_ids": []  # 예제에 따라 case_ids는 빈 배열로 설정
                }
                json_data.append(json_obj)

        # JSON 파일 쓰기
        json_file_path = os.path.join(self.script_directory, '../shared_steps_management/output', json_file)
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=2)

        print(f"CSV 파일 '{csv_file}'이 JSON 파일 '{json_file}'로 변환되었습니다.")

    def run_csv_to_json_conversion(self):
        csv_file_name = '04.app_csv_to_json.csv'
        json_file_name = '04.app_csv_to_json.json'
        self.csv_to_json(csv_file_name, json_file_name)


# 실행.
script_directory = os.path.dirname(os.path.abspath(__file__))
converter = CSVtoJSONConverter(script_directory)
converter.run_csv_to_json_conversion()
