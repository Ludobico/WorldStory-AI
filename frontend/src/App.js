import "./App.css";
import { Routes, Route, useNavigate } from "react-router-dom";
import WorldStory from "./components/Canvas/WorldStory";
import Main from "./components/Main";
import LoaderTransition from "./components/Loader/LoaderTransition";
import CharacterSetting from "./components/CharacterSetting";
import LoaderCSS from "./components/Loader/LoaderCSS";

function App() {
  const navigator = useNavigate();
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/charsetting" element={<CharacterSetting />} />
        <Route path="loader" element={<LoaderCSS />} />
      </Routes>
    </div>
  );
}

export default App;
