import "./App.css";
import { Routes, Route } from "react-router-dom";
import WorldStory from "./components/Canvas/WorldStory";
import Main from "./components/Main";
import LoaderTransition from "./components/Loader/LoaderTransition";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/test" element={<LoaderTransition />} />
      </Routes>
    </div>
  );
}

export default App;
