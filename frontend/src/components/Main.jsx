import { Canvas } from "@react-three/fiber";
import React from "react";
import WorldStory from "./Canvas/WorldStory";
import Header from "./Header/Header";
import "./Main.css";
import "./Header/Header.css";
import { Html, Scroll, ScrollControls } from "@react-three/drei";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import LoaderTransition from "./Loader/LoaderTransition";
import InsideStory from "./Canvas/InsideStory";
import "./Canvas/InsideStory.css";

const Main = () => {
  gsap.registerPlugin(ScrollTrigger);
  return (
    <div>
      <Canvas gl={{ alpha: false, stencil: false, antialias: false, depth: false }} dpr={1} style={{ width: "100vw", height: "100vh" }}>
        <Html fullscreen wrapperClass="html_header_top_div">
          <Header />
        </Html>
        <WorldStory />
      </Canvas>
      <Canvas>
        <InsideStory />
      </Canvas>
    </div>
  );
};

export default Main;
