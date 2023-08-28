import React, { useEffect, useRef, useState } from 'react';
import './CharacterSetting.css';
import Logo from './Header/Logo';
import axios from 'axios';

const CharacterSetting = () => {
  // llamaCPP에서 받은 chunk 단위로 나누어진 텍스트데이터
  const [streamToken, setStreamToken] = useState([]);

  // 텍스트가 늘어나면 그에따라 텍스트를 담는 바운딩박스로 늘림
  const text_div_ref = useRef();

  // text_div_ref가 늘어나면 전체화면도 늘어남
  const container_div_ref = useRef();

  // stream_token에 있는 값들을 저장하는 ref
  const span_ref = useRef();

  useEffect(() => {
    if (text_div_ref.current) {
      text_div_ref.current.style.height = text_div_ref.current.scrollHeight + 'px';
      container_div_ref.current.style.height = container_div_ref.current.scrollHeight + 'px';
    }
  });
  const sendMessage = async () => {
    var message = 'generate start';
    var response = await fetch('http://localhost:8000/stream_chat', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({ content: message }),
    });

    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');

    reader.read().then(function processResult(result) {
      if (result.done) return;
      let token = decoder.decode(result.value);
      if (token.endsWith(':') || token.endsWith('!') || token.endsWith('?')) {
        // document.getElementById('CharacterSetting_generate_result').innerHTML += token + '<br>';
        setStreamToken((streamToken) => [...streamToken, token + '\n']);
      } else {
        // document.getElementById('CharacterSetting_generate_result').innerHTML += token + '';
        setStreamToken((streamToken) => [...streamToken, token + '']);
      }
      return reader.read().then(processResult);
    });
  };

  const stateManager = () => {
    console.log(span_ref);
  };
  return (
    <div className="CharacterSetting_top_div" ref={container_div_ref}>
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      {/* stream 된 텍스트가 출력되는 div */}
      <div className="CharacterSetting_codeblock" ref={text_div_ref} id="CharacterSetting_generate_result">
        {streamToken.map((token, index) => (
          <span key={index} className="stream_token_span" ref={span_ref}>
            {token}
          </span>
        ))}
      </div>
      <div className="CharacterSetting_generate_button" onClick={sendMessage}>
        Generate
      </div>
      <div className="CharacterSetting_generate_button" onClick={stateManager}>
        test
      </div>
      <div className="CharacterSetting_generate_button">check</div>
    </div>
  );
};

export default CharacterSetting;
