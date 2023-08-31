import React, { useEffect, useRef, useState } from 'react';
import './CharacterSetting.css';
import CharracterSettingRange from './CharracterSettingRange';
import Logo from './Header/Logo';
import { Html } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
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

  const [genLoader, SetGenLoader] = useState(false);

  //   테스트용 텍스트
  const [test, setTest] = useState([]);

  const [top_k, setTop_k] = useState(40);
  const [top_q, setTop_q] = useState(0.95);
  const [temperature, setTemperature] = useState(0.8);
  const [last_n_tokens, setLast_n_tokens] = useState(64);
  const [max_new_toekns, setMax_new_tokens] = useState(256);
  const [gpu_layers, setGpu_layers] = useState(0);

  useEffect(() => {
    if (text_div_ref.current) {
      text_div_ref.current.style.height = text_div_ref.current.scrollHeight + 'px';
      container_div_ref.current.style.height = container_div_ref.current.scrollHeight + 'px';
    }
  }, [text_div_ref]);
  const sendMessage = async () => {
    SetGenLoader(true);
    setStreamToken([]);
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
      if (result.done) return SetGenLoader(false);
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
  // 드롭다운 관련 함수
  const [selectedModel, SetSelectedModel] = useState();

  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('Model select');
  const options = ['Model select', 'i', 'n', 'd', 'e', 'x'];

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectOption = (option) => {
    setSelectedOption(option);
    setIsOpen(false);
  };

  const handleTopKChange = (newValue) => {
    setTop_k(newValue);
  };
  const handleTopQChange = (newValue) => {
    setTop_q(newValue);
  };
  const handleTemperatureChange = (newValue) => {
    setTemperature(newValue);
  };
  const handleLastNChange = (newValue) => {
    setLast_n_tokens(newValue);
  };
  const handleMaxNewChange = (newValue) => {
    setMax_new_tokens(newValue);
  };
  const handleGpuLayersChange = (newValue) => {
    setGpu_layers(newValue);
  };
  return (
    // <Canvas style={{ height: '140vh', backgroundColor: '#1E293B' }} ref={container_div_ref}>
    //   <Html fullscreen zIndexRange={[1, 0]}>
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
      {/* generate 버튼 */}
      <div className="CharacterSetting_generate_button" onClick={sendMessage}>
        {genLoader ? (
          <div className="CharacterSetting_generate_loading"></div>
        ) : (
          <div className="CharacterSetting_generate_not_loading">Generate</div>
        )}
      </div>
      {/* setting 글자 */}
      <div className="CharacterSetting_setting_name">Setting</div>
      {/* model select */}
      <div className="Charsetting_dropdown_body">
        <div className="Charsetting_dropdown">
          <div className={`Charsetting_select ${isOpen ? 'Charsetting_select-clicked' : ''}`} onClick={toggleDropdown}>
            <span className="Charsetting_selected">{selectedOption}</span>
            <div className={`Charsetting_caret ${isOpen ? 'Charsetting_caret-rotate' : ''}`} />
          </div>
          <ul className={`Charsetting_menu ${isOpen ? 'Charsetting_menu-open' : ''}`}>
            {options.map((option, index) => (
              <li
                key={index}
                className={`Charsetting_active ${selectedOption === option ? 'Charsetting_active' : ''}`}
                onClick={() => selectOption(option)}
              >
                {option}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 하이퍼파라미터 세팅 */}
      <div className="setting_range_container">
        <CharracterSettingRange min={5} max={80} step={1} value={top_k} name={'top_k'} onChange={handleTopKChange} />
        <CharracterSettingRange min={0} max={1} step={0.01} value={top_q} name={'top_p'} onChange={handleTopQChange} />
        <CharracterSettingRange
          min={0}
          max={1}
          step={0.01}
          value={temperature}
          name={'temperature'}
          onChange={handleTemperatureChange}
        />
        <CharracterSettingRange
          min={0}
          max={1024}
          step={1}
          value={last_n_tokens}
          name={'last_n_tokens'}
          onChange={handleLastNChange}
        />
        <CharracterSettingRange
          min={0}
          max={4096}
          step={1}
          value={max_new_toekns}
          name={'max_new_tokens'}
          onChange={handleMaxNewChange}
        />
        <CharracterSettingRange
          min={0}
          max={16}
          step={1}
          value={gpu_layers}
          name={'gpu_layers'}
          onChange={handleGpuLayersChange}
        />
      </div>
    </div>
    //   </Html>
    // </Canvas>
  );
};

export default CharacterSetting;
