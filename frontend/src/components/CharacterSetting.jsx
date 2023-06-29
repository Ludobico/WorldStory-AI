import React, { useEffect, useState } from "react";
import "./CharacterSetting.css";
import Logo from "./Header/Logo";
import axios from "axios";

const CharacterSetting = () => {
  const [data, setData] = useState();
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/test");
    eventSource.onmessage = (e) => {
      const data = JSON.parse(e.data);
      console.log(data);
    };
    return () => {
      eventSource.close();
    };
  }, []);
  const get_data = () => {
    const fetch_data = async () => {
      try {
        setData("");
        const response = await axios.get("http://localhost:8000/test");
        setData(response);
      } finally {
        setIsLoading(false);
        console.log(data);
      }
    };
    fetch_data();
  };

  const log_test = () => {
    console.log(data);
  };
  return (
    <div className="CharacterSetting_top_div">
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      <pre className="CharacterSetting_codeblock">
        <code>{data}</code>
      </pre>
      <div className="CharacterSetting_generate_button" onClick={get_data}>
        Generate
      </div>
      <div className="CharacterSetting_generate_button" onClick={log_test}>
        test
      </div>
      <div className="CharacterSetting_setting_letter">Setting</div>
      <div className="CharacterSetting_setting_settings">
        <div className="CharacterSetting_setting_1 CharacterSetting_setting">1</div>
        <div className="CharacterSetting_setting_2 CharacterSetting_setting">2</div>
        <div className="CharacterSetting_setting_3 CharacterSetting_setting">3</div>
        <div className="CharacterSetting_setting_4 CharacterSetting_setting">4</div>
      </div>
    </div>
  );
};

export default CharacterSetting;
