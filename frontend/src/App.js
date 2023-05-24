import "./App.css";
import { Routes, Route } from "react-router-dom";
import WorldStory from "./components/Canvas/WorldStory";
import Main from "./components/Main";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Main />} />
      </Routes>
    </div>
  );
}

export default App;
