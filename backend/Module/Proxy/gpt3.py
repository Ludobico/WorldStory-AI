"""
freeGPT's gpt3 module
https://github.com/Ruu3f/freeGPT

"""

from requests import post
from requests.exceptions import RequestException


class Completion:
    """
    This class provides methods for generating completions based on prompts.
    """

    def create(self, prompt):
        """
        Create a completion for the given prompt using an AI text generation API.

        Args:
            prompt (str): The input prompt for generating the text.

        Returns:
            str: The generated text as a response from the API.

        Raises:
            requests.exceptions.RequestException: If there is an issue with sending the request or fetching the response.
        """
        resp = post(
            url="https://api.binjie.fun/api/generateStream",
            headers={
                "origin": "https://chat.jinshutuan.com",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
            },
            data={
                "prompt": prompt,
                "withoutContext": True,
                "stream": True,
            },
            stream=True
        )
        for chunk in resp.iter_content(chunk_size=1024):
            cleaned_chunk = chunk.decode('utf-8').replace('b', '').replace("'", '')
            yield cleaned_chunk