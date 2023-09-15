import React, { useState, useEffect } from 'react';
import Logo from '../Header/Logo';
import Icon, { SettingOutlined, UserOutlined } from '@ant-design/icons';
import { Layout, Menu, theme, Switch, Slider, Tooltip } from 'antd';
import { useNavigate } from 'react-router-dom';
import './CharacterChat.css';
import Input from './Input';
import ChatMessage from './ChatMessage';
import { OpenAIlogo, SelectModelLogo, LLMLogo } from './SVGStorage';

const { Header, Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const sliderMenuItem = {
  key: 'sliderKey', // 고유한 키값
  label: 'Slider Label', // 메뉴 아이템 라벨
  children: (
    <Slider
      defaultValue={50} // 초기값 설정
      tooltip={{ open: true }}
    />
  ),
};

const CharacterChat = () => {
  // 슬라이드 setting
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const navigate = useNavigate();
  const handleButtonClick = () => {
    // 버튼 클릭 시 / 경로로 이동
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
    getItem('LocalModel', 'LocalModel', <LLMLOGO />, [getItem('model1', 'model1')]),
  ]);

  // CharacterItems 상태
  const [characterItems, setCharacterItems] = useState([
    getItem('Character', 'sub1', <UserOutlined />, [getItem('Tom', '3'), getItem('Bill', '4'), getItem('Alex', '5')]),
    // getItem('Setting', 'sub2', <SettingOutlined />, [getItem('Team 1', '6'), getItem('Team 2', '8')]),
  ]);

  // LLM setting
  const [llmSetting, setLlmSetting] = useState([getItem('Setting', 'sub2', <SettingOutlined />)]);

  // 선택된 모델
  const handleModelSelet = (item) => {
    setSelectedModelItem([getItem(item.key, item.key, <SELECT_MODEL_LOGO />)]);
  };

  // light, dark 모드
  const [lightTheme, setLightTheme] = useState('dark');
  const changeTheme = (value) => {
    setLightTheme(value ? 'dark' : 'light');
  };

  return (
    <div className="chat_top_div">
      <Layout
        style={{
          minHeight: '100vh',
        }}
      >
        <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)} theme={lightTheme}>
          <div className="demo-logo-vertical" onClick={handleButtonClick}>
            <span>{collapsed ? 'WS' : 'WORLD STORY AI'}</span>
          </div>
          <div
            className="light_switch"
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'left', marginLeft: '20px' }}
          >
            <Switch
              checked={lightTheme === 'dark'}
              onChange={changeTheme}
              checkedChildren="Dark"
              unCheckedChildren="Light"
            />
          </div>
          <Menu theme={lightTheme} mode="inline" items={selectedModelItem} selectable={false} />
          <Menu theme={lightTheme} mode="inline" items={modelItems} onClick={handleModelSelet} />
          <Menu theme={lightTheme} mode="inline" items={characterItems} />
          <Menu theme={lightTheme} mode="vertical" items={llmSetting} />
        </Sider>
        <Content style={{ width: '100vw', height: '100vh' }}>
          <div className="chat_background">
            <div className="chat_content">
              <ChatMessage />
            </div>
            <Input />
          </div>
        </Content>
      </Layout>
    </div>
  );
};

export default CharacterChat;
