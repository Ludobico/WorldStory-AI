import { Canvas } from "@react-three/fiber";
import React from "react";
import WorldStory from "./Canvas/WorldStory";

const Main = () => {
  return (
    <>
      <Canvas gl={{ alpha: false, stencil: false, antialias: false, depth: false }} dpr={1}>
        <WorldStory />
      </Canvas>
    </>
  );
};

export default Main;
