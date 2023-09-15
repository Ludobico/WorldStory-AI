import React, { useState, useEffect } from 'react';
import Logo from '../Header/Logo';
import { DesktopOutlined, FileOutlined, PieChartOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { useNavigate } from 'react-router-dom';
import './CharacterChat.css';
import Input from './Input';
import ChatMessage from './ChatMessage';

const { Header, Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const CharacterChat = () => {
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const navigate = useNavigate();
  const handleButtonClick = () => {
    // 버튼 클릭 시 / 경로로 이동
    navigate('/');
  };

  const [selectedModelItem, setSelectedModelItem] = useState([getItem('Model select', null, <PieChartOutlined />)]);

  // modelItems 상태
  const [modelItems, setModelItems] = useState([
    getItem('GPT3.5', 'GPT3.5', <PieChartOutlined />),
    getItem('LlamaCPP', 'LlamaCPP', <DesktopOutlined />, [getItem('model1', 'model1')]),
  ]);

  // CharacterItems 상태
  const [characterItems, setCharacterItems] = useState([
    getItem('Character', 'sub1', <UserOutlined />, [getItem('Tom', '3'), getItem('Bill', '4'), getItem('Alex', '5')]),
    getItem('Setting', 'sub2', <TeamOutlined />, [getItem('Team 1', '6'), getItem('Team 2', '8')]),
  ]);

  const handleModelSelet = (item) => {
    setSelectedModelItem([getItem(item.key, item.key)]);
  };

  return (
    <div className="chat_top_div">
      <Layout
        style={{
          minHeight: '100vh',
        }}
      >
        <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
          <div className="demo-logo-vertical" onClick={handleButtonClick}>
            <span>{collapsed ? 'WS' : 'WORLD STORY AI'}</span>
          </div>
          <Menu theme="dark" mode="inline" items={selectedModelItem} />
          <Menu theme="dark" mode="inline" items={modelItems} onClick={handleModelSelet} />
          <Menu theme="dark" mode="inline" items={characterItems} />
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
