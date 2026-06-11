import os
import openai
import re

from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

#openai.api_key = os.environ['OPENAI_API_KEY']

def index(request):
    return render(request, 'code_converter/index.html')

def convert_c_to_rust(input_language, input_code, output_language):
    # 여기서 입력 언어의 코드를 타겟 언어의 코드로 변환하는 로직을 구현합니다.
    # TODO:api 코드의 중복이 많아지고 있음 -> 단일 함수로 통합?
    '''
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                당신은 {input_language} 언어로 작성된 코드를 동일한 동작을 하는 {output_language} 코드로 변환하는 작업을 합니다.
                답변에는 {output_language} 코드와, 원본 코드를 해당 코드로 변환한 이유를 포함해야 합니다.
            """},
            {"role": "user", "content": input_code},
        ],
    )
    rust_code = response.choices[0].message.content  
    '''
    rust_code = "이 기능은 현재 지원하지 않습니다."
    return rust_code

def make_testcode(input_code):
    '''
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                당신은 입력받은 django 코드에 대한 테스트 코드를 반환하는 작업을 합니다.
                답변에는 django 테스트 코드와, 해당 코드로 반환한 이유를 포함해야 합니다.
            """},
            {"role": "user", "content": input_code},
        ],
    )

    auto_testcode = response.choices[0].message.content 
    '''
    auto_testcode = "이 기능은 현재 지원하지 않습니다."
    return auto_testcode

def make_project_todolist(input_project, input_framework):
    '''
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                당신은 입력받은 프로젝트를 {input_framework}로 구현할 구체적인 명세 리스트를 만드는 역할을 합니다.
                답변에는 리스트 이외의 내용이 포함되어서는 안 됩니다.
            """},
            {"role": "user", "content": input_project},
        ],
    )

    todoList = response.choices[0].message.content  
    '''
    todoList = "이 기능은 현재 지원하지 않습니다."
    return todoList

def make_project_part(input_project, input_part, input_framework):
    # api 값이 너무 듬->당분간 더미로만
    '''
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""
                전체 프로젝트: {input_project}
                당신은 전체 프로젝트 중 입력받은 일부분을 {input_framework}로 구현하는 역할을 합니다.
            """},
            {"role": "user", "content": input_part},
        ],
    )

    actual_part = response.choices[0].message.content  
    '''
    actual_part = '이 기능은 현재 지원하지 않습니다.'
    return actual_part
    
def split_tasks(text):
    # Remove all newline characters in the string and retain 'number. item' format
    # Using regular expression to ensure splitting correctly
    items = re.sub(r'\n', '', text.strip())
    # Use regular expression to split based on the pattern 'number.'
    # \d+ captures one or more digits
    # We use a lookbehind assertion '(?<=\d\.)' for the splitting point.
    tasks = re.split(r'(?<=\d\.)\s*', items)
    # Return a list with 'number. item' strings
    return [task.strip() for task in tasks if task]
    
def extract_backtick_sections(text):
    # 정규표현식 패턴 정의
    pattern = r'```(.*?)```'

    # non-greedy 매칭 사용과 패턴 컴파일
    compiled_pattern = re.compile(pattern, re.DOTALL)

    # 매칭된 부분과 매칭되지 않은 부분을 각각 리스트에 담기
    matches = compiled_pattern.findall(text)
    non_matches = compiled_pattern.split(text)
    non_matches = [segment for i, segment in enumerate(non_matches) if i % 2 == 0]

    # 매칭된 부분과 매칭되지 않은 부분을 각각 리스트로 반환
    return matches, non_matches
    
def convert_code(request):
    if request.method == 'POST':
        input_language = request.POST.get('inputLanguage', '')
        input_code = request.POST.get('code', '')
        output_language = request.POST.get('outputLanguage', '')
        
        total_output = convert_c_to_rust(input_language, input_code, output_language)
        extracted_code, extracted_comment = extract_backtick_sections(total_output)
        context_dict = {'totalOutput': total_output, 
                        'extractedCode': extracted_code, 
                        'extractedComment':extracted_comment,
                       }
        return render(request, 'code_converter/code_convert.html', context_dict)
    elif request.method == 'GET':
        context_dict = {'totalOutput': '', 
                        'extractedCode': '', 
                        'extractedComment':''}
        return render(request, 'code_converter/code_convert.html', context_dict)

def auto_test(request):
    if request.method == "POST":
        input_code = request.POST.get('code', '')

        total_output = make_testcode(input_code)
        extracted_code, extracted_comment = extract_backtick_sections(total_output)
        print(type(extracted_code).__name__)  # 자료형 확인
        context_dict = {'input_code':input_code, 
                        'totalOutput': total_output, 
                        'extractedCode': extracted_code, 
                        'extractedComment':extracted_comment,
                       }
        return render(request, 'code_converter/auto_test.html', context_dict)
    else:
        return render(request, 'code_converter/auto_test.html')

def auto_project(request):
    if request.method == "POST":
        input_project = request.POST.get('inputProject', '')
        input_framework = request.POST.get('inputFramework', '')

        total_output = make_project_todolist(input_project, input_framework)
        cleaned_list = split_tasks(total_output)
        actual_part = []
        for part in cleaned_list:
            actual_part.append(make_project_part(input_project, part, input_framework))
        context_dict = {'totalOutput': total_output, 
                        'cleaned_list': cleaned_list,
                        'actual_part': actual_part
                       }
        return render(request, 'code_converter/auto_project.html', context_dict)
    else:
        return render(request, 'code_converter/auto_project.html')
        