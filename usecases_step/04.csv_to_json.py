import os
import csv
import json

class CSVtoJSONConverter:
    def __init__(self, script_directory):
        self.script_directory = script_directory

    def csv_to_json(self, csv_file, json_file):
        """CSV 파일을 JSON 형식으로 변환하는 메서드입니다."""

        # CSV 파일의 절대 경로 생성
        csv_file_path = os.path.join(self.script_directory, '../usecases_step/output', csv_file)

        # JSON으로 변환할 데이터 리스트
        data_list = []

        # CSV 파일 읽기
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)

            # 헤더 정보 읽기
            header = next(csv_reader)

            # 데이터 읽기
            for row in csv_reader:
                data = {}
                for i, value in enumerate(row):
                    # 각 열의 데이터를 헤더의 이름으로 매핑하여 딕셔너리에 추가
                    data[header[i]] = value.strip()

                # Steps 열의 데이터를 리스트로 변환하여 추가
                data['Steps'] = data.get('Steps', '').split('\n')

                # 변환된 데이터를 리스트에 추가
                data_list.append(data)

        # JSON 파일 쓰기
        json_file_path = os.path.join(self.script_directory, '../usecases_step/output', json_file)
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_list, json_file, ensure_ascii=False, indent=2)

        print(f"CSV 파일 '{csv_file}'이 JSON 파일 '{json_file}'로 변환되었습니다.")

    def run_csv_to_json_conversion(self):

        csv_file_name = '04.testcase_data.csv'
        json_file_name = '04.csv_to_json.json'
        self.csv_to_json(csv_file_name, json_file_name)


# 실행.
script_directory = os.path.dirname(os.path.abspath(__file__))
converter = CSVtoJSONConverter(script_directory)
converter.run_csv_to_json_conversion()
