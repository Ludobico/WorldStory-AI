import React, { Fragment, useRef } from "react";
import "./InsideStory.css";
import { Environment, Html, MeshReflectorMaterial, OrbitControls, PerspectiveCamera, useTexture } from "@react-three/drei";
import testimg from "../Static/lensDirtTexture.png";
import testimg2 from "../Static/background2.jpg";
import NoiseSwirlsShader from "../Shaders/NoiseSwirlsShader";
import { Canvas } from "@react-three/fiber";

function Test() {
  const shaderRef = useRef();
  const texture1 = useTexture(testimg);
  const texture2 = useTexture(testimg2);
  return (
    <>
      <mesh>
        <planeBufferGeometry args={[1, 3]} />
        <noiseSwirlsShader dispFactor={1} currentImage={texture1} nextImage={texture2} />
      </mesh>
    </>
  );
}
function Scene() {
  return (
    <Canvas>
      <Test />
    </Canvas>
  );
}
const InsideStory = () => {
  return (
    <>
      <Scene />
    </>
  );
};

export default InsideStory;
