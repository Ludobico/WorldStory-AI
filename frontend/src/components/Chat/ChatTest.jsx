import React from 'react';

const ChatTest = ({ chatComponent, inputMessage, selectedCharacter }) => {
  // chatComponent, inputMessage, selectedCharacter 등의 값 사용
  return (
    <div className="chat_message_top_div">
      {/* <div className={`chat_message_name`}>{message.name}</div> */}
      <div className="chat_message_name">{selectedCharacter}</div>
      <div className="chat_message_chat_message">
        <div className="chat_message_avatar_wrapper">
          {/* <div className={`chat_message_avatar ${isUser ? 'user' : 'chatbot'}`}></div> */}
          <div className="chat_message_avatar user"></div>
        </div>
        {/* <div className={`chat_message_message ${isUser ? 'user' : 'chatbot'}`}>{message.message}</div> */}
        <div className="chat_message_message user">{inputMessage}</div>
      </div>
    </div>
  );
};

export default ChatTest;
