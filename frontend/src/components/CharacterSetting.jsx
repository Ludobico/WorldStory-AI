import React, { useEffect, useRef, useState } from 'react';
import './CharacterSetting.css';
import CharracterSettingRange from './CharracterSettingRange';
import Logo from './Header/Logo';

const CharacterSetting = () => {
  // llamaCPP에서 받은 chunk 단위로 나누어진 텍스트데이터
  const [streamToken, setStreamToken] = useState([]);

  // 텍스트가 늘어나면 그에따라 텍스트를 담는 바운딩박스로 늘림
  const text_div_ref = useRef();
  const [reset_text_div_ref, setReset_text_div_ref] = useState();

  // text_div_ref가 늘어나면 전체화면도 늘어남
  const container_div_ref = useRef();
  const [reset_container_div_ref, setReset_container_div_ref] = useState();

  // stream_token에 있는 값들을 저장하는 ref
  const span_ref = useRef();

  const [genLoader, SetGenLoader] = useState(false);

  //   하이퍼파라미터
  const [top_k, setTop_k] = useState(40);
  const [top_p, setTop_p] = useState(0.95);
  const [temperature, setTemperature] = useState(0.8);
  const [last_n_tokens, setLast_n_tokens] = useState(64);
  const [max_new_tokens, setMax_new_tokens] = useState(256);
  const [gpu_layers, setGpu_layers] = useState(0);

  // 드롭다운 관련 함수
  const [selectedModel, SetSelectedModel] = useState();

  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('Model select');
  const options = ['Model select', 'GPT3.5', 'n', 'd', 'e', 'x'];

  // 초기 text_div와 container_div의 height 값
  useEffect(() => {
    setReset_text_div_ref(text_div_ref.current.style.height);
    setReset_container_div_ref(container_div_ref.current.style.height);
  }, []);
  // llm 모델이 text 생성에 따라 div가 화면을 초과하면 그에맞춰 화면을 늘림
  useEffect(() => {
    if (text_div_ref.current) {
      text_div_ref.current.style.height = text_div_ref.current.scrollHeight + 'px';
      container_div_ref.current.style.height = container_div_ref.current.scrollHeight + 'px';
    }
  }, [streamToken]);
  const sendMessage = async () => {
    if (selectedOption == 'Model select') {
      console.log('You need to select a model');
      return;
    }
    text_div_ref.current.style.height = reset_text_div_ref;
    container_div_ref.current.style.height = reset_container_div_ref;
    SetGenLoader(true);
    setStreamToken([]);
    var message = 'generate start';
    var response = await fetch('http://localhost:8000/stream_chat', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        top_k: top_k,
        top_p: top_p,
        temperature: temperature,
        last_n_tokens: last_n_tokens,
        max_new_tokens: max_new_tokens,
        gpu_layers: gpu_layers,
        content: message,
      }),
    });

    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');

    reader.read().then(function processResult(result) {
      if (result.done) return SetGenLoader(false);
      let token = decoder.decode(result.value);
      if (token.endsWith('!') || token.endsWith('?')) {
        // document.getElementById('CharacterSetting_generate_result').innerHTML += token + '<br>';
        setStreamToken((streamToken) => [...streamToken, token + '\n']);
      } else {
        // document.getElementById('CharacterSetting_generate_result').innerHTML += token + '';
        setStreamToken((streamToken) => [...streamToken, token + '']);
      }
      return reader.read().then(processResult);
    });
  };
  const sendMessage_OAI = async () => {
    text_div_ref.current.style.height = reset_text_div_ref;
    container_div_ref.current.style.height = reset_container_div_ref;
    SetGenLoader(true);
    setStreamToken([]);
    var message = 'generate start';
    var response = await fetch('http://localhost:8000/stream_chat_OAI', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        content: message,
      }),
    });

    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');

    async function processText() {
      while (true) {
        const result = await reader.read();
        if (result.done) {
          SetGenLoader(false);
          break;
        }
        let token = decoder.decode(result.value);
        if (token.endsWith('!') || token.endsWith('?')) {
          setStreamToken((streamToken) => [...streamToken, token + '\n']);
        } else {
          setStreamToken((streamToken) => [...streamToken, token + '']);
        }
        // 자연스러운 streaming을 위해 제한시간을 걸어둠
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
    }
    processText();
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectOption = (option) => {
    console.log(selectedOption);
    setSelectedOption(option);
    SetSelectedModel(option);
    setIsOpen(false);
  };

  // 하이퍼파라미터 관련 함수
  // const handleTopKChange = (newValue) => {
  //   setTop_k(newValue);
  // };
  // const handleTopQChange = (newValue) => {
  //   setTop_p(newValue);
  // };
  // const handleTemperatureChange = (newValue) => {
  //   setTemperature(newValue);
  // };
  // const handleLastNChange = (newValue) => {
  //   setLast_n_tokens(newValue);
  // };
  // const handleMaxNewChange = (newValue) => {
  //   setMax_new_tokens(newValue);
  // };
  // const handleGpuLayersChange = (newValue) => {
  //   setGpu_layers(newValue);
  // };
  const handleChange = (key) => (newValue) => {
    switch (key) {
      case 'top_k':
        setTop_k(newValue);
        break;
      case 'top_p':
        setTop_p(newValue);
        break;
      case 'temperature':
        setTemperature(newValue);
        break;
      case 'last_n_tokens':
        setLast_n_tokens(newValue);
        break;
      case 'max_new_tokens':
        setMax_new_tokens(newValue);
        break;
      case 'gpu_layers':
        setGpu_layers(newValue);
        break;
      default:
        // 예외 처리: 유효한 키가 아닌 경우
        console.error('Invalid key');
    }
  };

  const generating = () => {
    SetGenLoader(!genLoader);
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
      {/* generate 버튼 */}
      <div
        className="CharacterSetting_generate_button"
        onClick={selectedOption === 'GPT3.5' ? sendMessage_OAI : sendMessage}
      >
        {genLoader ? (
          <div className="CharacterSetting_generate_not_loading loading_active"></div>
        ) : (
          <div className="CharacterSetting_generate_not_loading">Generate</div>
        )}
      </div>
      {/* save 버튼 */}
      <div className="CharacterSetting_generate_save" onClick={generating}>
        Save Setting
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
                className={`${selectedOption === option ? 'Charsetting_active' : ''}`}
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
        {selectedOption !== 'GPT3.5' && (
          <>
            <CharracterSettingRange
              min={5}
              max={80}
              step={1}
              value={top_k}
              name={'top_k'}
              onChange={handleChange('top_k')}
            />
            <CharracterSettingRange
              min={0}
              max={1}
              step={0.01}
              value={top_p}
              name={'top_p'}
              onChange={handleChange('top_p')}
            />
            <CharracterSettingRange
              min={0}
              max={1}
              step={0.01}
              value={temperature}
              name={'temperature'}
              onChange={handleChange('temperature')}
            />
            <CharracterSettingRange
              min={0}
              max={1024}
              step={1}
              value={last_n_tokens}
              name={'last_n_tokens'}
              onChange={handleChange('last_n_tokens')}
            />
            <CharracterSettingRange
              min={0}
              max={4096}
              step={1}
              value={max_new_tokens}
              name={'max_new_tokens'}
              onChange={handleChange('max_new_tokens')}
            />
            <CharracterSettingRange
              min={0}
              max={16}
              step={1}
              value={gpu_layers}
              name={'gpu_layers'}
              onChange={handleChange('gpu_layers')}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default CharacterSetting;
