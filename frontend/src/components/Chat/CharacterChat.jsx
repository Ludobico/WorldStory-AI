import React, { useState } from 'react';
import './CharacterChat.css';
import Logo from '../Header/Logo';
import { Layout, Menu, theme, Button } from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

const CharacterChat = () => {
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
    <div className="CharacterChat_top_div" style={{ height: '100vh' }}>
      {/* <div className="CharacterChat_logo">
        <Logo />
      </div> */}
      <div className="CharacterChat_layout">
        <Layout style={{ height: '100vh' }}>
          <Sider trigger={null} collapsible collapsed={collapsed}>
            <div className="CharacterChat_demo_logo" />
            <Menu
              theme="dark"
              mode="inline"
              defaultSelectedKeys={['1']}
              items={[
                {
                  key: '1',
                  icon: <UserOutlined />,
                  label: 'nav 1',
                },
                {
                  key: '2',
                  icon: <VideoCameraOutlined />,
                  label: 'nav 2',
                },
                {
                  key: '3',
                  icon: <UploadOutlined />,
                  label: 'nav 3',
                },
              ]}
            />
          </Sider>
          <Layout>
            <Header style={{ padding: 0, background: colorBgContainer }}>
              <Button
                type="text"
                icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                onClick={() => setCollapsed(!collapsed)}
                style={{
                  fontSize: '16px',
                  width: 64,
                  height: 64,
                }}
              />
            </Header>
            <Content
              style={{
                margin: '24px 16px',
                padding: 24,
                minHeight: 280,
                background: 'rgb(30 41 59)',
                color: 'white',
              }}
            >
              Content
            </Content>
          </Layout>
        </Layout>
      </div>
    </div>
  );
};

export default CharacterChat;
