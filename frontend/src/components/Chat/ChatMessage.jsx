import React from 'react';
import giga from '../Static/maxresdefault.jpg';

const ChatMessage = (props) => {
  return <div className="chat_message_top_div">{props.inputMessage}</div>;
};

export default ChatMessage;
