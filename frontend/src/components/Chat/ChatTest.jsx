import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './ChatMessage.css';

const ChatTest = ({ inputMessage, selectedCharacter, characterImage, userName, userImage }) => {
  const [streamToken, setStreamToken] = useState([]);
  const [aiChatResponse, setAiChatResponse] = useState();

  // Chat with AI
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
          await save_history();
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

  // Save conversation history to backend
  const save_history = () => {
    const ai_chat_response = streamToken.join('');
    axios.post('http://localhost:8000/chat_history_save', {
      user_chat: inputMessage,
      user_name: userName,
      AI_chat: ai_chat_response,
      AI_name: selectedCharacter,
    });
  };
  useEffect(() => {
    sendMessage_OAI();
  }, []);

  const testconsole = () => {
    console.log(streamToken);
  };
  return (
    <div className="chat_message_top_div">
      {/* User message */}
      <div className="chat_message_top_div_user">
        <div className="chat_message_name chat_message_user_name">{userName}</div>
        <div className="user_info_wrapper ">
          <div className="chat_message_message user_message">{inputMessage}</div>
          <div className="chat_message_avatar_wrapper">
            <div className="chat_message_avatar">
              <img src={userImage} />
            </div>
          </div>
        </div>
      </div>
      <div className="chat_message_divider">
        <button
          onClick={() => {
            testconsole();
          }}
        />
      </div>
      {/* AI message */}
      <div className="chat_message_top_div_AI">
        <div className="chat_message_name chat_message_AI_name">{selectedCharacter}</div>
        <div className="AI_info_wrapper">
          <div className="chat_message_avatar_wrapper">
            <div className="chat_message_avatar">
              <img src={characterImage} />
            </div>
          </div>
          <div className="chat_message_message AI_message">
            {streamToken.map((token, index) => (
              <span key={index}>{token}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatTest;
