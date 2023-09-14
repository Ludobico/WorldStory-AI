import React from 'react';
import './Input.css';
import { SendOutlined } from '@ant-design/icons';

const Input = () => {
  return (
    <div className="chat_input">
      <input type="text" placeholder="Type something..." />
      <div className="chat_send">
        <button>
          <SendOutlined />
        </button>
      </div>
    </div>
  );
};

export default Input;
