import { Canvas } from "@react-three/fiber";
import React from "react";
import WorldStory from "./Canvas/WorldStory";
import Header from "./Header/Header";
import "./Main.css";
import "./Static/Header.css";
import { Html } from "@react-three/drei";

const Main = () => {
  return (
    <>
      <Canvas gl={{ alpha: false, stencil: false, antialias: false, depth: false }} dpr={1} style={{ width: "100vw", height: "100vh" }}>
        <Html fullscreen wrapperClass="html_header_top_div">
          <Header />
        </Html>
        <WorldStory />
      </Canvas>
    </>
  );
};

export default Main;
