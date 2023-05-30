import React, { useEffect, useReducer, useRef, useState } from "react";
import "../Static/Header.css";
import { gsap } from "gsap";

const Header = () => {
  const textRef = useRef();
  const textRef2 = useRef();
  const underlineRef = useRef();

  var tl = gsap.timeline();
  let [animationFlag, setAnimationFlag] = useState(false);
  let [animationFlag2, setAnimationFlag2] = useState(false);

  useEffect(() => {
    const textElement = textRef.current;
    const charElement = textElement.querySelectorAll("span");

    const textElement2 = textRef2.current;
    const charElement2 = textElement2.querySelectorAll("span");

    // gsap text animation
    if (animationFlag === true) {
      tl.set(charElement, {
        yPercent: 0,
      });
      tl.to(charElement, {
        duration: 1,
        yPercent: 110,
        stagger: 0.08,
        ease: "Power1.inOut",
      });
    }

    if (animationFlag2 === true) {
      tl.set(charElement2, {
        yPercent: 0,
      });
      tl.to(charElement2, {
        duration: 1,
        yPercent: 110,
        stagger: 0.08,
        ease: "Power1.inOut",
      });
    }
  });

  const handle_mouse_enter = () => {
    setAnimationFlag(true);
  };
  const handle_mouse_leave = () => {
    setAnimationFlag(false);
  };
  const handle_mouse_enter2 = () => {
    setAnimationFlag2(true);
  };
  const handle_mouse_leave2 = () => {
    setAnimationFlag2(false);
  };

  return (
    <header>
      <nav className="header_bar">
        <ul className="nav_list">
          <li className="intro" ref={textRef} onMouseEnter={handle_mouse_enter} onMouseLeave={handle_mouse_leave}>
            <span data-char="C">C</span>
            <span data-char="r">r</span>
            <span data-char="e">e</span>
            <span data-char="a">a</span>
            <span data-char="t">t</span>
            <span data-char="i">i</span>
            <span data-char="v">v</span>
            <span data-char="e">e</span>
          </li>
          <li className="intro" ref={textRef2} onMouseEnter={handle_mouse_enter2} onMouseLeave={handle_mouse_leave2}>
            <span data-char="T">T</span>
            <span data-char="u">u</span>
            <span data-char="t">t</span>
            <span data-char="o">o</span>
            <span data-char="r">r</span>
            <span data-char="i">i</span>
            <span data-char="a">a</span>
            <span data-char="l">l</span>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
