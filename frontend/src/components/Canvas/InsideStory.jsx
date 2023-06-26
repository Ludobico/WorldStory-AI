import React, { Fragment, useEffect, useRef } from "react";
import "./InsideStory.css";
import { Environment, Html, MeshReflectorMaterial, OrbitControls, PerspectiveCamera, useTexture, useVideoTexture } from "@react-three/drei";
import testimg from "../Static/lensDirtTexture.png";
import testimg2 from "../Static/background2.jpg";
import example1 from "../Static/example1.mp4";
import example2 from "../Static/example2.mp4";
import NoiseSwirlsShader from "../Shaders/NoiseSwirlsShader";
import { Canvas, useFrame } from "@react-three/fiber";
import { gsap } from "gsap";

function Test() {
  const shaderRef = useRef();
  const texture1 = useTexture(testimg);
  const texture2 = useTexture(testimg2);
  const videoTexture1 = useVideoTexture(example1);

  const OnclickTestShader = () => {
    let tl = gsap.timeline();
    tl.to(shaderRef.current.material.uniforms.dispFactor, {
      value: 1,
      duration: 2,
      ease: "Expo.easeOut",
      onComplete: () => {
        shaderRef.current.material.uniforms.dispFactor.value = 0.0;
      },
    });
  };

  return (
    <>
      <mesh position={[4, 0, 0]} ref={shaderRef} onClick={OnclickTestShader}>
        <planeBufferGeometry args={[3, 3]} />
        <noiseSwirlsShader dispFactor={0} currentImage={texture1} nextImage={texture2} />
      </mesh>
      <mesh position={[-3.5, 0, 0]}>
        <planeGeometry args={[8, 9]} />
        <meshBasicMaterial map={videoTexture1} toneMapped={false} />
      </mesh>
    </>
  );
}
function Introduce() {
  return (
    <div className="Introduce_top_div">
      <div className="Introduce_top_intro">Create personal characters</div>
    </div>
  );
}
function Scene() {
  return (
    <Canvas>
      <Test />
      <Html fullscreen>
        <Introduce />
      </Html>
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
