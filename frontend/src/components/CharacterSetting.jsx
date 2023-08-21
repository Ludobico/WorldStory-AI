import React, { useEffect, useRef, useState } from "react";
import "./CharacterSetting.css";
import Logo from "./Header/Logo";
import axios from "axios";

const CharacterSetting = () => {
  const [data, setData] = useState();
  const [isLoading, setIsLoading] = useState(true);

  // llamaCPP에서 받은 chunk 단위로 나누어진 텍스트데이터
  const [token, setToken] = useState([]);

  // 텍스트가 늘어나면 그에따라 텍스트를 담는 바운딩박스로 늘림
  const text_div_ref = useRef();

  // text_div_ref가 늘어나면 전체화면도 늘어남
  const container_div_ref = useRef();

  useEffect(() => {
    if (text_div_ref.current) {
      text_div_ref.current.style.height = text_div_ref.current.scrollHeight + "px";
      container_div_ref.current.style.height = container_div_ref.current.scrollHeight + "px";
    }
  }, [token]);
  const get_data = () => {
    setIsLoading(true);
    setData("");

    axios
      .post("http://localhost:8000/langdocs_stream")
      .then((response) => {
        setToken(response);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };
  const log_test = () => {
    // setTestText(testText.concat("test asdasd asdasd asdasd asdasd "));
  };
  return (
    <div className="CharacterSetting_top_div" ref={container_div_ref}>
      <div className="CharacterSetting_logo">
        <Logo />
      </div>
      <div className="CharacterSetting_codeblock" ref={text_div_ref}>
        {/* <p>{data}</p> */}
        <p>{token}</p>
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
