import React, { useEffect, useState } from 'react';
import './ChatMessage.css';

const ChatTest = ({ inputMessage, selectedCharacter, userName, userImage }) => {
  const [streamToken, setStreamToken] = useState([]);
  const [chracterImage, setCharacterImage] = useState();
  // 캐릭터 이미지 가져오기
  useEffect(() => {});
  const sendMessage_OAI = async () => {
    setStreamToken([]);

    var message = inputMessage;
    var prompt = selectedCharacter;
    var response = await fetch('http://localhost:8000/character_chat_OAI', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        content: message,
        prompt: prompt,
      }),
    });

    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');

    async function processText() {
      while (true) {
        const result = await reader.read();
        if (result.done) {
          break;
        }
        let token = decoder.decode(result.value);
        if (token.endsWith('!') || token.endsWith('?')) {
          setStreamToken((streamToken) => [...streamToken, token + '\n']);
        } else {
          setStreamToken((streamToken) => [...streamToken, token + '']);
        }
        // 자연스러운 streaming을 위해 제한시간을 걸어둠
        await new Promise((resolve) => setTimeout(resolve, 50));
      }
    }
    processText();
  };
  useEffect(() => {
    sendMessage_OAI();
  }, []);
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
        <div className="chat_message_AI_name">{selectedCharacter}</div>
        <div className="AI_info_wrapper">
          <div className="chat_message_avatar_wrapper">
            <div className="chat_message_avatar">
              <img src={userImage} />
            </div>
          </div>
          <div className="chat_message_message AI_message">
            {streamToken.map((token, index) => (
              <span key={index}>{token}</span>
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatTest;
