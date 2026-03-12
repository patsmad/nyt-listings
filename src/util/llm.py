import os
from src.util.local_llm import LocalLLMAPI
from src.util.ai_studio import AIStudioAPI

class LLM:
    llm = None

    def get_llm(self):
        if self.llm is None:
            if os.environ.get('USE_LOCAL', False):
                self.llm = LocalLLMAPI()
            else:
                self.llm = AIStudioAPI()
        return self.llm
