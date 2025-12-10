from google import genai
from src.util.config import Config
import json
import re
import time

gemini_key = Config().gemini_api_key

TITLE_QUERY = ('This is an advertisement for a film from The New York Times. '
               'Identify the title of the film and return ONLY the title.')

BOXES_QUERY = ('This is a page from the New York Times. '
               'Return a list of boxes (List[Box]) that bound film advertisements. '
               'Please scale everything for an image with width {} and height {}.')

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

    def analyze_image(self, query, image, model='gemini-2.5-flash'):
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model=model, contents=[query, image]
        )
        self.augment()
        return response.text

    def get_title_for_image(self, image):
        return self.analyze_image(TITLE_QUERY, image)

    def get_boxes_for_image(self, image):
        output = []
        text = self.analyze_image(BOXES_QUERY.format(image.size[0], image.size[1]), image, 'gemini-2.5-pro')
        print(text)
        try:
            json_response = json.loads(re.findall(r'```json([\s\S]*)```', text)[0].strip())
            for box in json_response:
                output.append({
                    'top': box['box_2d'][0],
                    'left': int(box['box_2d'][1] / 1000 * image.size[0]),
                    'height': box['box_2d'][2] - box['box_2d'][0],
                    'width': int((box['box_2d'][3] - box['box_2d'][1]) / 1000 * image.size[0])
                })
            print(image.size, output)
            return output
        except:
            return []
