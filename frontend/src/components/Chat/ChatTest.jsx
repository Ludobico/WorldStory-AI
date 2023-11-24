import React from 'react';
import './ChatMessage.css';

const ChatTest = ({ inputMessage, selectedCharacter, userName, userImage }) => {
  return (
    <>
      {/* User message */}
      <div className="chat_message_top_div_user">
        <div className="chat_message_user_name">{userName}</div>
        <div className="user_info_wrapper ">
          <div className="chat_message_message user_message">{inputMessage}</div>
          <div className="chat_message_avatar_wrapper">
            <div className="chat_message_avatar">
              <img src={userImage} />
            </div>
          </div>
        </div>
      </div>
      {/* AI message */}
      <div className="chat_message_top_div_AI">
        <div className="chat_message_AI_name">{userName}</div>
        <div className="AI_info_wrapper">
          <div className="chat_message_avatar_wrapper">
            <div className="chat_message_avatar">
              <img src={userImage} />
            </div>
          </div>
          <div className="chat_message_message AI_message">{inputMessage}</div>
        </div>
      </div>
    </>
  );
};

export default ChatTest;
