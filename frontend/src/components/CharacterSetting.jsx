import React, { useEffect, useRef, useState } from 'react';
import './CharacterSetting.css';
import './ResponsiveCSS/Tablet/CharacterSetting_Tablet.css';
import CharracterSettingRange from './CharracterSettingRange';
import Logo from './Header/Logo';
import transParentImage from './Static/transparent.png';
import ImageGenLoading from './Static/giphy_loading.gif';
import axios from 'axios';
import { Select } from 'antd';
import { useAlert } from 'react-alert';
import { AnimatedCounter } from 'react-animated-counter';

const CharacterSetting = () => {
  const alert = useAlert();
  // LLM에서 받은 chunk 단위로 나누어진 텍스트데이터
  const [streamToken, setStreamToken] = useState([]);

  // (beta) 텍스트데이터가 끝날때 나오는 image flag
  const [imageFlag, setImageFlag] = useState(false);
  const [characterImage, setCharacterImage] = useState(transParentImage);
  const [imageGenLoader, setImageGenLoader] = useState(false);

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
  const [selectedOption, setSelectedOption] = useState('Model select');
  const [modelList, setModelList] = useState([
    {
      label: 'GPT API',
      options: [{ label: 'GPT4o', value: 'GPT3.5' }],
    },
    {
      label: 'Local Models',
      options: [],
    },
  ]);
  const [modelRam, setModelRam] = useState([]);
  const [showRam, setShowRam] = useState(0.0);

  // save setting 버튼 관련 함수
  const [settingPrompt, setSettingPrompt] = useState();
  const [settingName, setSettingName] = useState();

  const upDateGeneratedText = () => {
    if (imageFlag) {
      alert.error(<div style={{ textTransform: 'initial' }}>Image Generating!</div>);
      return false;
    }
    const spans = text_div_ref.current.querySelectorAll('span');
    const textArray = Array.from(spans).map((span) => span.textContent);
    const allText = textArray.join('');
    setSettingPrompt(allText);
    const nameMatch = /(?:\*\*?)?Name:?(?:\*\*?)?\s*(.+)/i.exec(allText);

    if (nameMatch) {
      const extractedName = nameMatch[1].replace(/\s+/g, '');
      setSettingName(extractedName);
    } else {
      // alert.error('No name found');
      alert.error(<div style={{ textTransform: 'initial' }}>Cannot Find Name</div>);
    }
  };
  // 프롬프트랑 텍스트 업데이트되면 axios 요청해라
  useEffect(() => {
    if (settingPrompt && settingName) {
      axios
        .post('http://localhost:8000/make_character', {
          name: settingName,
          prompt: settingPrompt,
          image: characterImage,
        })
        .then(() => {
          alert.success(
            <div style={{ textTransform: 'initial' }}>
              The Character was Generated in your backend/Characters folder
            </div>
          );
        });
    }
  }, [settingPrompt, settingName]);

  //   models 폴더에있는 파일들을 select box로 표시
  useEffect(() => {
    axios.get('http://localhost:8000/LLM_model_list').then((res) => {
      const LLM_model_list = res.data.map((item) => ({
        label: item.label,
        value: item.value,
        RAM: item.RAM,
      }));
      setModelList((prevModelList) => {
        const localModelsIndex = prevModelList.findIndex((item) => item.label === 'Local Models');
        if (localModelsIndex !== -1) {
          const updatedLocalModels = [...prevModelList[localModelsIndex].options, ...LLM_model_list];
          prevModelList[localModelsIndex].options = updatedLocalModels;
        }
        return [...prevModelList];
      });
      const ramValueArray = LLM_model_list.map((item) => ({
        value: item.value,
        RAM: item.RAM,
      }));
      setModelRam(ramValueArray);
    });
  }, []);
  useEffect(() => {
    modelRam.map((option, index) => {
      if (option.value === selectedOption) {
        const extractedNumber = parseFloat(option.RAM.match(/[\d.]+/)[0]);
        setShowRam(extractedNumber);
      } else if (selectedOption === 'GPT3.5') {
        window.scrollTo({ top: 0 });
        setShowRam(0);
      }
    });
  }, [selectedOption]);

  // 초기 text_div와 container_div의 height 값
  useEffect(() => {
    setReset_text_div_ref(text_div_ref.current.style.height);
    // setReset_container_div_ref(container_div_ref.current.style.height);
    setReset_container_div_ref(container_div_ref.current.scrollHeight);
  }, []);

  // llm 모델이 text 생성에 따라 div가 화면을 초과하면 그에맞춰 화면을 늘림
  useEffect(() => {
    if (text_div_ref.current) {
      text_div_ref.current.style.height = text_div_ref.current.scrollHeight + 'px';
      container_div_ref.current.style.height = container_div_ref.current.scrollHeight + 'px';
    }
  }, [streamToken]);
  const sendMessage = async () => {
    if (selectedOption === 'Model select') {
      alert.error(<div style={{ textTransform: 'initial' }}>Choose the Model</div>);
      return;
    }
    text_div_ref.current.style.height = reset_text_div_ref;
    container_div_ref.current.style.height = reset_container_div_ref;
    SetGenLoader(true);
    setStreamToken([]);
    // setSettingPrompt('');
    // setSettingName('');
    window.scrollTo({ top: 0 });

    const message = 'generate start';
    const response = await fetch('http://localhost:8000/stream_chat', {
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
        model_name: selectedOption,
        content: message,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

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
    // setImageFlag(true);
    setImageGenLoader(false);
    setCharacterImage(transParentImage);
    text_div_ref.current.style.height = reset_text_div_ref;
    container_div_ref.current.style.height = reset_container_div_ref;
    SetGenLoader(true);
    setStreamToken([]);

    window.scrollTo({ top: 0 });
    const message = 'generate start';
    const response = await fetch('http://localhost:8000/char_setting_OAI', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        content: message,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    async function processText() {
      while (true) {
        const result = await reader.read();
        if (result.done) {
          setImageFlag(true);
          SetGenLoader(false);
          setImageGenLoader(true);
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
    await processText();
  };

  // image generation 관련 함수
  useEffect(() => {
    if (imageGenLoader) {
      image_generation_start();
    }
  }, [imageGenLoader]);
  const image_generation_start = () => {
    setImageFlag(true);
    const ai_chat_response = streamToken.join('');
    axios
      .post('http://localhost:8000/Character_image_generation', {
        prompt: ai_chat_response,
      })
      .then((res) => {
        setCharacterImage(`data:image/png;base64, ${res.data}`);
        setImageFlag(false);
      });
  };

  // ant design 에서 모델을 선택할때
  const model_Select = (value) => {
    setSelectedOption(value);
  };

  // 하이퍼파라미터 관련 함수
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

  return (
    <div className="CharacterSetting_top_div" ref={container_div_ref}>
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      {/* stream 된 텍스트가 출력되는 div */}
      <div className="CharacterSetting_codeblock" ref={text_div_ref} id="CharacterSetting_generate_result">
        <div className="stream_token_div">
          {streamToken.map((token, index) => (
            <span key={index} className="stream_token_span" ref={span_ref}>
              {token}
            </span>
          ))}
          {/* 이미지 */}
          <div className="CharacterSetting_generate_image_div">
            {imageFlag ? (
              <img src={ImageGenLoading} className="CharacterSetting_generate_image" />
            ) : (
              <img src={characterImage} className="CharacterSetting_generate_image" />
            )}
          </div>
        </div>
      </div>
      {/* generate 버튼 */}
      <div className="CharacterSetting_button">
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
        <div className="CharacterSetting_generate_save" onClick={upDateGeneratedText}>
          Save Setting
        </div>
        {/* 이미지 재생성 버튼 */}
        <div className="CharacterSetting_regenetate_image" onClick={image_generation_start}>
          {/* <span>Image Regeneration</span> */}
          {imageFlag ? (
            <div className="CharacterSetting_generate_not_loading loading_active"></div>
          ) : (
            <div className="CharacterSetting_generate_not_loading">Image Regeneration</div>
          )}
        </div>
      </div>
      <div className="CharacterSetting_setting_section">
        {/* setting 글자 */}
        <span className="CharacterSetting_setting_name">Setting</span>

        {/* model select */}
        <div className="Charsetting_dropdown_body">
          {/* <p className="Charsetting_ram">Max RAM required : {showRam}</p> */}
          <div className="Charsetting_ram">
            &nbsp; Max RAM required &nbsp;
            <AnimatedCounter value={showRam} color="#fff" />
            GB
          </div>

          <Select
            defaultValue="Model select"
            options={modelList}
            onChange={model_Select}
            className="Charsetting_dropdown"
          />
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
