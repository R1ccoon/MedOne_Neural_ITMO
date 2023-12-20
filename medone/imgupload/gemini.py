import google.generativeai as genai
from PIL import Image
import re


def start_recognition(image):
    GOOGLE_API_KEY = "AIzaSyD4VHlxPS_rI7cfccJTlci0FlCWVrd58sY"
    QUERY = '''Read a table of test results and convert the results to JSON format. Only provide JSON in the 
    response. Preserve the original Russian names of the tests: { "rows": [array of rows of test results] }, 
    where each test result can have one of the following formats: {"is_composite": True, 
    "name": NAME_OF_COMPOSITE_TEST} - for a composite test, composite tests are typically written in uppercase 
    letters and do not have a result, norm, or unit of measurement; {"is_composite": False, 
    "name": NAME_OF_COMPONENT_TEST, "value": TEST_RESULT, "norm": TEST_NORM, "measurement_unit": UNIT_OF_MEASUREMENT} 
    Example: { "rows": [ {"is_composite": True, "name": "Анализ крови"}, {"is_composite": False, "name": "Анализ на 
    эритроциты", "value": "116,0", "norm": "130-160", "measurement_unit": "г/л"}]}'''
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([QUERY, image], stream=True)
    response.resolve()
    try:
        return re.search(r"```json(.*?)```", response.text, flags=re.DOTALL).group(1).strip()
    except:
        return None


if __name__ == '__main__':
    img = Image.open('анализы/analysis1.jpg')

    result = start_recognition(img)
    print(result)
