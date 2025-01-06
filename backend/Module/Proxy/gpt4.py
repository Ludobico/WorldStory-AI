from uuid import uuid4
from re import findall
from curl_cffi.requests import get, RequestsError

class Completion:
    """
    This class provides methods for generating completions based on prompts.
    """

    def create(self, prompt:str):
        """
        Create a completion for the given prompt using an AI text generation API.

        Args:
            prompt (str): The input prompt for generating the text.

        Returns:
            str: The generated text as a response from the API.

        Raises:
            requests.exceptions.RequestException: If there is an issue with sending the request or fetching the response.
        """
        resp = get(
            "https://you.com/api/streamingSearch",
            headers={
                "cache-control": "no-cache",
                "referer": "https://you.com/search?q=gpt4&tbm=youchat",
                "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            },
            params={
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
                "domain": "youchat",
                "queryTraceId": str(uuid4()),
                "chat": [],
            },
            impersonate="chrome107",
        )
        for chunk in resp.iter_content(chunk_size=1024):
            # cleaned_chunk = chunk.decode('utf-8').replace('b', '').replace("'", '')
            cleaned_chunk = chunk.decode('utf-8')
            yield cleaned_chunk
        if "youChatToken" not in resp.text:
            raise RequestsError("Unable to fetch the response.")

    def create_non_stream(self, prompt:str):
        resp = get(
            "https://you.com/api/streamingSearch",
            headers={
                "cache-control": "no-cache",
                "referer": "https://you.com/search?q=gpt4&tbm=youchat",
                "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            },
            params={
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
                "domain": "youchat",
                "queryTraceId": str(uuid4()),
                "chat": [],
            },
            impersonate="chrome107",
        )
        if "youChatToken" not in resp.text:
            raise RequestsError("Unable to fetch the response.")
        return (
            "".join(
                findall(
                    r"{\"youChatToken\": \"(.*?)\"}",
                    resp.content.decode("unicode-escape"),
                )
            )
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )
    
    