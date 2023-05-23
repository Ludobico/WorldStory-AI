import "./App.css";
import { Routes, Route } from "react-router-dom";
import WorldStory from "./components/Canvas/WorldStory";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/test" element={<WorldStory />} />
      </Routes>
    </div>
  );
}

export default App;
