import React, { useRef } from "react";
import LensFlare from "./UltimateLensFlare";
import "../Static/WorldStory.css";
import { Canvas } from "@react-three/fiber";
import { EffectComposer } from "@react-three/postprocessing";
import { OrbitControls, PerspectiveCamera, Stars, useTexture } from "@react-three/drei";
import lensIMG from "../Static/lensDirtTexture.png";
import { folder, useControls } from "leva";
import background from "../Static/background1.jpg";
import * as THREE from "three";
import Header from "../Header/Header";

function Skybox() {
  const texture = useTexture(background);
  return (
    <mesh userData={{ LensFlare: "no-occlusion" }} scale={[-1, 1, 1]}>
      <sphereBufferGeometry castShadow={false} receiveShadow={false} args={[5, 64, 64]} />
      <meshBasicMaterial toneMapped={false} map={texture} side={THREE.FrontSide} />
    </mesh>
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
    </>
  );
};

export default WorldStory;
