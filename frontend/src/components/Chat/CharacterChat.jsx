import React, { useState, useEffect, useRef, useMemo } from 'react';
import './ChatMessage.css';
import './CharacterChat.css';
import './Input.scss';
import Icon, { SettingOutlined, UserOutlined } from '@ant-design/icons';
import { Layout, Menu, theme, Switch, Slider, Tooltip } from 'antd';
import { useNavigate } from 'react-router-dom';
import { OpenAIlogo, SelectModelLogo, LLMLogo } from './SVGStorage';
import fantasyimage from '../Static/chat_background/fantasy_desktop.jpg';
import cyberpunkimage from '../Static/chat_background/cyberpunk-city-buildings-art.jpg';
import westernimage from '../Static/chat_background/western.jpg';
import apocalypseimage from '../Static/chat_background/Apocalypse.jpg';
import futuristicimage from '../Static/chat_background/futuristic.jpg';
import blackimage from '../Static/chat_background/635b6e3b30bfeae7b713cb8162aa2c9a.jpg';
import axios from 'axios';
import { SendOutlined } from '@ant-design/icons';
import { useAlert } from 'react-alert';
import Chat from './Chat';
import * as THREE from 'three';
import { OrbitControls, PerspectiveCamera, shaderMaterial, useAspect, useTexture } from '@react-three/drei';
import { Canvas, extend, useFrame, useThree } from '@react-three/fiber';
import glsl from 'glslify';
import gsap from 'gsap';

const { Content, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}
const ImageTransitionMaterial = shaderMaterial(
  // uniforms
  {
    dispFactor: 0,
    currentImage: new THREE.Texture(),
    nextImage: new THREE.Texture(),
  },
  // vertex
  glsl`
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 0.7 );
  }
  `,

  // fragment
  glsl`
  varying vec2 vUv;

      uniform sampler2D currentImage;
      uniform sampler2D nextImage;

      uniform float dispFactor;

      void main() {

          vec2 uv = vUv;
          vec4 _currentImage;
          vec4 _nextImage;
          float intensity = 0.6;

          vec4 orig1 = texture2D(currentImage, uv);
          vec4 orig2 = texture2D(nextImage, uv);
          
          _currentImage = texture2D(currentImage, vec2(uv.x, uv.y + dispFactor * (orig2 * intensity)));

          _nextImage = texture2D(nextImage, vec2(uv.x, uv.y + (1.0 - dispFactor) * (orig1 * intensity)));

          vec4 finalTexture = mix(_currentImage, _nextImage, dispFactor);

          gl_FragColor = finalTexture;
      }
  `
);

extend({
  ImageTransitionMaterial,
});

const ImageTransition = ({ prevImage, nextImage }) => {
  const materialRef = useRef();
  const [animationFlag, setAnimationFlag] = useState(false);
  const { size } = useThree();
  const scale = useAspect(size.width, size.height, 1);

  const ChangeImage = () => {
    const currentValue = materialRef.current.uniforms.dispFactor.value;
    setAnimationFlag(true);
    gsap.to(materialRef.current.uniforms.dispFactor, {
      value: currentValue === 0 ? 1 : 0,
      duration: 1,
      ease: 'power2.out',
      oninit: () => {
        if (currentValue === 1) {
          materialRef.current.uniforms.currentImage.value = nextImage;
          materialRef.current.uniforms.nextImage.value = prevImage;
        } else {
          materialRef.current.uniforms.currentImage.value = prevImage;
          materialRef.current.uniforms.nextImage.value = nextImage;
        }
      },
      onComplete: () => {
        setAnimationFlag(false);
      },
    });
  };
  useEffect(() => {
    if (animationFlag === false) {
      ChangeImage();
    }
  }, [nextImage]);
  return (
    <mesh position={[0, 0, 0]} scale={scale}>
      <planeGeometry />
      <imageTransitionMaterial ref={materialRef} />
    </mesh>
  );
};

const Scene = ({ image1, image2 }) => {
  const prevImage = useTexture(image1);
  const nextImage = useTexture(image2);

  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 0, 1]} />
      <ImageTransition prevImage={prevImage} nextImage={nextImage} />
      <ambientLight intensity={3} />
    </>
  );
};
const CharacterChat = () => {
  // 알림
  const alert = useAlert();
  // 슬라이드 setting
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const navigate = useNavigate();
  const handleButtonClick = () => {
    navigate('/');
  };

  //  svg icons
  const OPENAI_LOGO = (props) => <Icon component={OpenAIlogo} {...props} />;
  const SELECT_MODEL_LOGO = (props) => <Icon component={SelectModelLogo} {...props} />;
  const LLMLOGO = (props) => <Icon component={LLMLogo} {...props} />;
  // modelItems 상태
  const [selectedModelItem, setSelectedModelItem] = useState([getItem('Model select', null, <SELECT_MODEL_LOGO />)]);
  const [modelItems, setModelItems] = useState([
    getItem('GPT3.5', 'GPT3.5', <OPENAI_LOGO />),
    getItem('LocalModel', 'LocalModel', <LLMLOGO />, null),
  ]);
  // LLM list를 출력해 modelItems 에 업데이트
  useEffect(() => {
    axios.get('http://localhost:8000/LLM_model_list').then((res) => {
      const LLM_model_list = res.data.map((item) => ({
        label: item.label,
        value: item.value,
        RAM: item.RAM,
      }));
      const modelItemsForLLM = LLM_model_list.map((model) => getItem(model.label, model.label, null, null));

      setModelItems((prevModelItems) => {
        const updatedModelItems = [...prevModelItems];
        if (updatedModelItems.length > 1) {
          updatedModelItems[1].children = modelItemsForLLM;
        }
        return updatedModelItems;
      });
    });
  }, []);

  // Character list
  const [characterItems, setCharacterItems] = useState([getItem('Character', 'sub1', <UserOutlined />, null)]);
  // 선택된 캐릭터
  const [selectedCharacter, setSeletedCharacter] = useState(false);
  useEffect(() => {
    axios.get('http://localhost:8000/char_list_check').then((res) => {
      const charracter_list = res.data.map((item) => getItem(item, item, null, null));

      setCharacterItems((prevCharItems) => {
        const updatedCharItems = [...prevCharItems];
        if (updatedCharItems.length >= 1) {
          updatedCharItems[0].children = charracter_list;
        }
        return updatedCharItems;
      });
    });
  }, []);

  // LLM setting
  const [top_k, setTop_k] = useState(40);
  const [top_p, setTop_p] = useState(0.95);
  const [temperature, setTemperature] = useState(0.8);
  const [last_n_tokens, setLast_n_tokens] = useState(64);
  const [max_new_tokens, setMax_new_tokens] = useState(256);
  const [gpu_layers, setGpu_layers] = useState(0);

  const handleChange_top_k = (value) => {
    setTop_k(value);
  };
  const handleChange_top_p = (value) => {
    setTop_p(value);
  };
  const handleChange_temperature = (value) => {
    setTemperature(value);
  };
  const handleChange_last_n_tokens = (value) => {
    setLast_n_tokens(value);
  };
  const handleChange_max_new_tokens = (value) => {
    setMax_new_tokens(value);
  };
  const handleChange_gpu_layers = (value) => {
    setGpu_layers(value);
  };
  const [llmSetting, setLlmSetting] = useState([
    getItem('LLM Setting', 'sub2', <SettingOutlined />, [
      getItem('top_k', top_k, null, [
        getItem(<Slider defaultValue={top_k} onChange={handleChange_top_k} min={5} max={80} />, 'top_k_key'),
      ]),
      getItem('top_p', 'top_p', null, [
        getItem(<Slider defaultValue={top_p} onChange={handleChange_top_p} min={0} max={1} step={0.01} />, 'top_p_key'),
      ]),
      getItem('temperature', 'temperature', null, [
        getItem(
          <Slider defaultValue={temperature} onChange={handleChange_temperature} min={0} max={1} step={0.01} />,
          'temperature_key'
        ),
      ]),
      getItem('last_n_tokens', 'last_n_tokens', null, [
        getItem(
          <Slider defaultValue={last_n_tokens} onChange={handleChange_last_n_tokens} min={0} max={1024} step={12} />,
          'last_n_tokens_key'
        ),
      ]),
      getItem('max_new_tokens', 'max_new_tokens', null, [
        getItem(
          <Slider defaultValue={max_new_tokens} onChange={handleChange_max_new_tokens} min={0} max={4096} step={256} />,
          'max_new_tokens_key'
        ),
      ]),
      getItem('gpu_layers', 'gpu_layers', null, [
        getItem(
          <Slider defaultValue={gpu_layers} onChange={handleChange_gpu_layers} min={0} max={16} step={1} />,
          'gpu_layers_key'
        ),
      ]),
    ]),
  ]);

  // 선택된 모델
  const handleModelSelet = (item) => {
    setSelectedModelItem([getItem(item.key, item.key, <SELECT_MODEL_LOGO />)]);
  };
  // 선택된 캐릭터
  const handleCharacterSelet = (item) => {
    setSeletedCharacter(item.key);
  };
  // light, dark 모드
  const [lightTheme, setLightTheme] = useState('dark');
  const changeTheme = (value) => {
    setLightTheme(value ? 'dark' : 'light');
  };

  // 채팅
  // 인풋메시지
  const [inputMessage, setInputMessage] = useState('');
  const [chatLog, setChatLog] = useState([{}]);
  const [userName, setUserName] = useState();
  const [userImage, setUserImage] = useState();
  const [characterImage, setCharacterImage] = useState();
  // 스크롤 트리거
  const scrollRef = useRef();

  useEffect(() => {
    const scrollToBottom = () => {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight - scrollRef.current.clientHeight;
    };
    scrollToBottom();
  }, [chatLog]);
  // 유저 이름 확인
  useEffect(() => {
    axios.get('http://localhost:8000/user_name_check').then((res) => {
      setUserName(res.data);
    });
  }, [userName]);
  // 유저 이미지 확인
  useEffect(() => {
    axios.get('http://localhost:8000/user_image_check').then((res) => {
      // base64로 인코딩된 이미지를 디코딩할때는 아래와 같은 형식으로 받아야함
      setUserImage(`data:image/png;base64, ${res.data}`);
    });
  }, [userImage]);
  // 캐릭터 이미지 확인
  useEffect(() => {
    if (selectedCharacter !== false) {
      axios
        .post('http://localhost:8000/character_image_check', {
          name: selectedCharacter,
        })
        .then((res) => {
          setCharacterImage(`data:image/png;base64, ${res.data}`);
        });
    }
  }, [selectedCharacter]);

  // 채팅 로그 불러오기 (log_flag가 true이면 chat의 로그저장수행x, false면 수행)
  useEffect(() => {
    // 다른 캐릭터를 선택할수도 있으므로 초기화해야함
    setChatLog([{}]);
    if (selectedCharacter !== false) {
      axios
        .post('http://localhost:8000/chat_history_import', {
          AI_name: selectedCharacter,
        })
        .then((res) => {
          if (res.data.chat_log !== null) {
            res.data.chat_log.map((chat) => {
              setChatLog((prevLog) => [
                ...prevLog,
                {
                  index: prevLog.length,
                  character_name: chat.AI_name,
                  character_image: `data:image/png;base64, ${res.data.char_image}`,
                  user_name: chat.user_name,
                  user_image: `data:image/png;base64, ${res.data.user_image}`,
                  message: chat.user_chat,
                  Ai_message: chat.AI_chat,
                  log_flag: true,
                },
              ]);
            });
          }
        });
    }
  }, [selectedCharacter]);

  const chat_start_count = () => {
    if (selectedCharacter === false) {
      return alert.error(<div style={{ textTransform: 'initial' }}>Choose the Character!</div>);
    }
    setChatLog((prevLog) => [
      ...prevLog,
      {
        index: prevLog.length,
        character_name: selectedCharacter,
        character_image: characterImage,
        user_name: userName,
        user_image: userImage,
        message: inputMessage,
        Ai_message: null,
        log_flag: false,
      },
    ]);
    setInputMessage('');
  };
  const createDynamicChatComponent = (chatLog) => {
    return chatLog.map(
      (chat, index) =>
        index !== 0 && (
          <Chat
            key={index}
            inputMessage={chat.message}
            selectedCharacter={chat.character_name}
            userName={chat.user_name}
            userImage={chat.user_image}
            characterImage={chat.character_image}
            Ai_message={chat.Ai_message}
            log_flag={chat.log_flag}
          />
        )
    );
  };
  const dynamicChatComponents = createDynamicChatComponent(chatLog);

  // background image
  const [backgorundImage, setBackgroundImage] = useState([
    getItem('Background', 'Background', <SettingOutlined />, [
      getItem('Fantasy', 'Fantasy', null),
      getItem('Cyberpunk', 'Cyberpunk', null),
      getItem('Western', 'Western', null),
      getItem('Apocalypse', 'Apocalypse', null),
      getItem('Futuristic', 'Futuristic', null),
    ]),
  ]);
  const [selectedBackground, setSelectedBackground] = useState(fantasyimage);
  const [previousBackground, setPreviousBackground] = useState(blackimage);

  const handleBackgroundSelet = (item) => {
    setPreviousBackground(selectedBackground);

    if (item.key === 'Fantasy') {
      setSelectedBackground(fantasyimage);
    } else if (item.key === 'Cyberpunk') {
      setSelectedBackground(cyberpunkimage);
    } else if (item.key === 'Western') {
      setSelectedBackground(westernimage);
    } else if (item.key === 'Apocalypse') {
      setSelectedBackground(apocalypseimage);
    } else if (item.key === 'Futuristic') {
      setSelectedBackground(futuristicimage);
    }
  };

  // useMemo(() => {
  //   // 현재 선택한 배경화면에 따라 testBackground 변경
  //   if (selectedBackground === 'Fantasy') {
  //     setTestBackground(fantasyimage);
  //   } else if (selectedBackground === 'Cyberpunk') {
  //     setTestBackground(cyberpunkimage);
  //   } else if (selectedBackground === 'Western') {
  //     setTestBackground(westernimage);
  //   } else if (selectedBackground === 'Apocalypse') {
  //     setTestBackground(apocalypseimage);
  //   }
  // }, [selectedBackground]);

  // 백엔드에서 배경화면 이미지 불러오기
  useEffect(() => {
    axios.get('http://localhost:8000/chat_background_select').then((res) => {
      for (let i = 0; i < res.data.length; i++) {
        const newBackgorundImage = getItem(res.data[i], res.data[i], null);
        const updatedBackgroundImage = [...backgorundImage];
        updatedBackgroundImage[0].children.push(newBackgorundImage);

        setBackgroundImage(updatedBackgroundImage);
      }
    });
  }, []);

  return (
    <div className="chat_top_div">
      <Layout
        style={{
          minHeight: '100vh',
        }}
      >
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          theme={lightTheme}
          style={{ zIndex: 1 }}
        >
          <div className="demo-logo-vertical" onClick={handleButtonClick}>
            <span>{collapsed ? 'WS' : 'WORLD STORY AI'}</span>
          </div>
          <div
            className="light_switch"
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', paddingBottom: '20px' }}
          >
            <Switch
              checked={lightTheme === 'dark'}
              onChange={changeTheme}
              checkedChildren="Dark"
              unCheckedChildren="Light"
            />
          </div>
          {/* GPT3.5 */}
          {/* <Menu theme={lightTheme} mode="inline" items={selectedModelItem} selectable={false} /> */}
          {/* LocalModel */}
          <Menu
            theme={lightTheme}
            mode="inline"
            items={modelItems}
            onClick={handleModelSelet}
            defaultSelectedKeys={'GPT3.5'}
          />
          {/* Character */}
          <Menu theme={lightTheme} mode="inline" items={characterItems} onClick={handleCharacterSelet} />
          {/* setting */}
          <Menu theme={lightTheme} mode="inline" items={llmSetting} selectable={false} />
          {/* Background */}
          <Menu
            theme={lightTheme}
            mode="inline"
            items={backgorundImage}
            onClick={handleBackgroundSelet}
            defaultSelectedKeys={['Fantasy']}
          />
        </Sider>
        <Content style={{ width: '100vw', height: '100vh' }}>
          <Canvas style={{ width: '100vw', height: '100vh', position: 'absolute' }}>
            <Scene image1={previousBackground} image2={selectedBackground} />
          </Canvas>
          {/* <div className="chat_background" style={{ backgroundImage: `url(${testbackground})` }}> */}
          <div className="chat_background">
            {/* 메시지 */}
            <div className="chat_content" ref={scrollRef}>
              <div className="chat_message_log">{dynamicChatComponents}</div>
            </div>
            <div className="chat_input">
              {/* 버튼 */}
              <input
                type="text"
                placeholder="Type something..."
                onChange={(e) => {
                  setInputMessage(e.target.value);
                }}
                value={inputMessage}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    chat_start_count();
                  }
                }}
              />
              <div className="chat_send">
                <button
                  onClick={() => {
                    chat_start_count();
                  }}
                >
                  <SendOutlined />
                </button>
              </div>
            </div>
          </div>
        </Content>
      </Layout>
    </div>
  );
};

export default CharacterChat;
