import React from "react";
import "../Static/Header.css";
import "gsap";
import SplitText from "gsap/SplitText";

const Header = () => {
  return (
    <header>
      <nav className="header_bar">
        <ul className="nav_list">
          <li className="intro" id="gsap_reveal">
            Intro
          </li>
          <li className="intro">Usage</li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
