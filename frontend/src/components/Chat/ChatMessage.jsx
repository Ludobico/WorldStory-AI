import React from 'react';
import './ChatMessage.scss';
import giga from '../Static/maxresdefault.jpg';

const ChatMessage = () => {
  return (
    <>
      <div className="chat_message chat_owner">
        <div className="chat_message_info">
          <img src={giga} alt="" />
          <span>just now</span>
        </div>
        <div className="chat_message_content">
          <p>hi</p>
          {/* <img src={giga} /> */}
        </div>
      </div>
    </>
  );
};

export default ChatMessage;
