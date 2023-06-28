import React from "react";
import "./CharacterSetting.css";
import Logo from "./Header/Logo";
const CharacterSetting = () => {
  return (
    <div className="CharacterSetting_top_div">
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      <pre className="CharacterSetting_codeblock">
        <code></code>
      </pre>
      <div className="CharacterSetting_generate_button">Generate</div>
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
