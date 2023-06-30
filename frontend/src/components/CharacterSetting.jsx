import React, { useEffect, useState } from "react";
import "./CharacterSetting.css";
import Logo from "./Header/Logo";
import axios from "axios";

const CharacterSetting = () => {
  const [data, setData] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const get_data = () => {
    setIsLoading(true);
    setData("");

    axios
      .get("http://localhost:8000/test", { responseType: "stream" })
      .then((response) => {
        setData(response.data);
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };
  const log_test = () => {
    console.log(data);
  };

  const test_data = `
  ,"Name": "Evelyn",
          "Gender": "Female",
         "Age": "28",
        "Personality": "Brave, curious, and adventurous. She is always seeking out new experiences and is not afraid of the unknown.",
      "Background": "Evelyn was born in a small town on the coast of France. Her parents were both scientists who spent most of their time researching in remote locations around the world. From an early age, Evelyn was exposed to different cultures and ways of life that inspired her sense of adventure.",
         "Dialogue Style": "Evelyn speaks with a French accent and often uses metaphors and analogies to describe her experiences. She has a knack for storytelling and can captivate an audience with her words.",
       "Appearance": "Evelyn has long, curly brown hair and deep green eyes. She is tall and slender, with a graceful gait that conveys both strength and elegance."
  `;
  const formatted_data = test_data
    .split("\n")
    .map((line) => line.trim())
    .join("\n");
  return (
    <div className="CharacterSetting_top_div">
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      <div className="CharacterSetting_codeblock">
        {/* <div className="CharacterSetting_code">{formatted_data}</div> */}
        <p>{data}</p>
      </div>
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
