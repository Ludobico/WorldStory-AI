from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from pydantic import BaseModel, Field

from typing import List, Dict, Literal
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """
    In memory implementation of chat message history
    """

    messages : List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages : List[BaseMessage]) -> None:
        self.messages.extend(messages)
    
    def clear(self) -> None:
        self.messages = []
    

def get_by_session_id(session_id : str, store : Dict) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

class HistoryMessageExtractor:
    """
    Extracts the messages human and AI talked. This class may use JSON file parsing for saving history instead of redis.
    """
    def __init__(self, session_id : str, store : Dict):
        self.session_id = session_id
        self.store = store
    
    def human(self, return_type : Literal['all', 'last'] = 'last'):
        result = []
        messages = self.store[self.session_id].messages
        for message in messages:
            if isinstance(message, HumanMessage):
                result.append(message.content)

        if return_type == 'all':
            return result
        elif return_type == 'last':
            return result[-1]
        else:
            raise ValueError(f"Parameter {return_type} is not supported")

    
    def ai(self, return_type : Literal['all', 'last'] = 'last'):
        result = []
        messages = self.store[self.session_id].messages

        for message in messages:
            if isinstance(message, AIMessage):
                result.append(message.content)
        if return_type == 'all':
            return result
        elif return_type == 'last':
            return result[-1]
        else:
            raise ValueError(f"Parameter {return_type} is not supported")