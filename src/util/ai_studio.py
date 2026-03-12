from google import genai
from src.util.config import Config
import time

gemini_key = Config().gemini_api_key

TITLE_QUERY = ('This is an advertisement for a film from The New York Times. '
               'Identify the title of the film and return ONLY the title.')

VCR_CODE_QUERY = ('This is a television listing for a film in The New York Times. '
                  'Identify the vcr code, a 4-8 digit number, at the end of the listing. '
                  'Return ONLY that number.')

class AIStudioAPI:
    request_times = []

    def augment(self):
        curr_time = time.time()
        self.request_times.append(curr_time)
        self.request_times = [t for t in self.request_times if (curr_time - t) <= 60]
        if len(self.request_times) % 15 == 0:
            time_to_sleep = 60 - (self.request_times[-1] - self.request_times[0])
            print(f'Back off for a second to prevent failure ({time_to_sleep} seconds)')
            time.sleep(time_to_sleep)

    def analyze_image(self, query, image):
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite', contents=[query, image]
        )
        self.augment()
        return response.text

    def get_title_for_image(self, image):
        return self.analyze_image(TITLE_QUERY, image)

    def get_vcr_code_for_image(self, image):
        return self.analyze_image(VCR_CODE_QUERY, image)
