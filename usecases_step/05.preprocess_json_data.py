import json
import os

class JSONDataPreprocessor:
    def __init__(self, script_directory):
        self.script_directory = script_directory

    def preprocess_json_data(self, input_file, output_file, remove_assertion=True):
        """JSON 데이터를 전처리하는 메서드입니다."""

        # JSON 파일의 절대 경로 생성
        input_file_path = os.path.join(self.script_directory, '../usecases_step/output', input_file)


        # JSON 파일 읽기
        with open(input_file_path, 'r', encoding='utf-8') as json_file:
            cases = json.load(json_file)

        for case in cases:
            first_pass_steps = []
            current_step = ""

            # 첫 번째 병합 패스
            for step in case['Steps']:
                if step.startswith('*') or step.startswith(' ') or step.startswith('"'):
                    current_step += step.strip()
                elif "Expected Result:" in step:
                    continue
                else:
                    if current_step:
                        first_pass_steps.append(current_step)
                    current_step = step.strip()
            if current_step:
                first_pass_steps.append(current_step)

            # 두 번째 병합 패스
            modified_steps = []
            current_step = ""
            for step in first_pass_steps:
                if step.startswith('*') or step.startswith(' ') or step.startswith('"'):
                    current_step += step.strip()
                else:
                    if current_step:
                        modified_steps.append(current_step)
                    current_step = step.strip()
            if current_step:
                modified_steps.append(current_step)

            if current_step:
                modified_steps.append(current_step)

            # 기존 Steps를 수정된 Steps로 교체
            case['Steps'] = modified_steps
            # Assertion 단어가 들어간 데이터 제거
            if remove_assertion:
                case['Steps'] = [step for step in modified_steps if "Assertion" not in step]

        # 전처리된 데이터를 새로운 JSON 파일로 저장
        output_file_path = os.path.join(self.script_directory, '../usecases_step/output', output_file)
        with open(output_file_path, 'w', encoding='utf-8') as modified_json_file:
            json.dump(cases, modified_json_file, ensure_ascii=False, indent=2)

        print(f"JSON 파일 '{input_file}'이 전처리되어 '{output_file}'로 저장되었습니다.")

    def run_preprocess_json_data(self):

        input_file_name = '04.csv_to_json.json'
        output_file_name = '05.clean_data.json'
        self.preprocess_json_data(input_file_name, output_file_name)

# 실행.
script_directory = os.path.dirname(os.path.abspath(__file__))
preprocessor = JSONDataPreprocessor(script_directory)
preprocessor.run_preprocess_json_data()
