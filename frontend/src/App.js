import './App.css';
import { Routes, Route } from 'react-router-dom';
import WorldStory from './components/Canvas/WorldStory';
import Main from './components/Main';
import LoaderTransition from './components/Loader/LoaderTransition';
import CharacterSetting from './components/CharacterSetting';
import LoaderCSS from './components/Loader/LoaderCSS';
import { positions, Provider } from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';
import CharacterChat from './components/Chat/CharacterChat';
import ChatImageTransitionTest from './components/Chat/ChatImageTransitionTest';

function App() {
  const options = {
    timeout: 5000,
    position: positions.BOTTOM_CENTER,
  };
  return (
    <div className="App">
      <Provider template={AlertTemplate} {...options}>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/charsetting" element={<CharacterSetting />} />
          <Route path="loader" element={<LoaderCSS />} />
          <Route path="/chat" element={<CharacterChat />} />
          <Route path="/t" element={<ChatImageTransitionTest />} />
        </Routes>
      </Provider>
    </div>
  );
}

export default App;
