import React, { useEffect, useRef, useState } from "react";
import LensFlare from "./UltimateLensFlare";
import "./WorldStory.css";
import { EffectComposer } from "@react-three/postprocessing";
import { Html, OrbitControls, PerspectiveCamera, Stars, useTexture } from "@react-three/drei";
import lensIMG from "../Static/lensDirtTexture.png";
import background_1 from "../Static/background1.jpg";
import background_2 from "../Static/background2.jpg";
import background_3 from "../Static/background3.jpg";
import * as THREE from "three";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useFrame } from "@react-three/fiber";
import TransitionShaderMaterial from "../Shaders/TransitionShader";
import SceneTransitionShader from "../Shaders/SceneTransitionShader";

function Skybox() {
  const backgroundList = useTexture([background_1, background_2, background_3]);
  const [textureIndex, setTextureIndex] = useState(0);
  const shaderMaterialRef = useRef();

  useFrame(({ mouse }) => {
    if (mouse.x < -0.3333) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 0,
        onStart: () => {
          shaderMaterialRef.current.uTexture1 = backgroundList[0];
        },
      });
    } else if (mouse.x < 0.3333) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 1,
        onComplete: () => {
          shaderMaterialRef.current.uTexture1 = backgroundList[1];
        },
      });
    } else if (mouse.x > 0.3333) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 0,
      });
    }
  });

  return (
    <mesh userData={{ LensFlare: "no-occlusion" }} scale={[-1, 1, 1]}>
      <sphereBufferGeometry castShadow={false} receiveShadow={false} args={[5, 64, 64]} />
      {/* <meshBasicMaterial toneMapped={false} map={backgroundList[textureIndex]} side={THREE.FrontSide} /> */}
      <transitionShaderMaterial ref={shaderMaterialRef} uTexture1={backgroundList[0]} uTexture2={backgroundList[2]} uTexture3={backgroundList[1]} uProgress={0} attach="material" />
    </mesh>
  );
}

function Introduce() {
  useEffect(() => {
    const reveal = gsap.utils.toArray(".project_reveal");
    reveal.forEach((text, i) => {
      ScrollTrigger.create({
        trigger: text,
        toggleClass: "active",
        start: "top 100%",
        end: "bottom 10%",
      });
    });
  });
  return (
    <>
      <div className="Introduce_intro project_reveal">Create</div>
      <div className="Introduce_intro1 project_reveal">Your own</div>
      <div className="Introduce_intro2 project_reveal">Fictional</div>
      <div className="Introduce_intro3 project_reveal">Characters</div>
    </>
  );
}

const WorldStory = () => {
  const OrbitcameraRef = useRef();
  const cameraRef = useRef();
  const cameraHandler = () => {
    console.log(cameraRef.current);
  };
  return (
    <>
      <sceneTransitionShader />
      <OrbitControls ref={OrbitcameraRef} autoRotate enableZoom={false} />
      <PerspectiveCamera makeDefault position={[-2.129, 0.177, 27.08]} ref={cameraRef} />
      <EffectComposer>
        {/* 테스트용 */}
        {/* <LensFlare dirtTextureFile={lensIMG} {...lensFlareProps} /> */}
        <LensFlare dirtTextureFile={lensIMG} colorGain={new THREE.Color(56, 22, 11)} opacity={0.8} flareShape={0.37} flareSize={0.004} flareSpeed={0.4} glareSize={0.01} starPoints={0.1} ghostScale={0.1} haloScale={0.5} />
      </EffectComposer>
      <directionalLight intensity={1} position={[0, 0, 0]} />
      <Skybox />
      <Stars radius={100} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
      <Html fullscreen wrapperClass="Introduce_top_div" zIndexRange={[100, 0]}>
        <Introduce />
      </Html>
    </>
  );
};

export default WorldStory;
