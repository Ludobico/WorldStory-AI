import os
import json
from datetime import datetime

class ChatHistory:
  def save_history_to_json( user_chat, user_name, AI_chat, AI_name):
    date = datetime.now()
    cur_dir = os.getcwd()
    history_path = os.path.join(cur_dir, 'Characters', AI_name)
    if not os.path.exists(os.path.join(history_path, 'history.json')):
      chat_history = {}
    else:
      with open(os.path.join(history_path ,'history.json'), 'r', encoding='utf-8') as f:
        chat_history = json.load(f)
    
    index = str(date.strftime('%Y-%m-%d %H:%M:%S'))

    chat_history[index] = {
      'user_name': user_name,
      'user_chat': user_chat,
      'AI_name': AI_name,
      'AI_chat': AI_chat
    }

    with open(os.path.join(history_path, 'history.json'), 'w', encoding='utf-8') as f:
      json.dump(chat_history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
  ChatHistory.save_history_to_json('user_chat', 'user_name', 'asdasd', 'asdasd')

