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

const Main = () => {
  gsap.registerPlugin(ScrollTrigger);
  return (
    <>
      <Canvas gl={{ alpha: false, stencil: false, antialias: false, depth: false }} dpr={1} style={{ width: "100vw", height: "100vh" }}>
        <ScrollControls pages={1} damping={0.3}>
          <Scroll>
            <Html fullscreen wrapperClass="html_header_top_div">
              <Header />
            </Html>
            <WorldStory />
          </Scroll>
          <Scroll>
            <Html fullscreen>
              <LoaderTransition />
            </Html>
          </Scroll>
        </ScrollControls>
      </Canvas>
    </>
  );
};

export default Main;
