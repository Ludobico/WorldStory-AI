import React from "react";
import LensFlare from "./UltimateLensFlare";
import "../Static/WorldStory.css";
import { Canvas } from "@react-three/fiber";
import { EffectComposer } from "@react-three/postprocessing";
import { OrbitControls } from "@react-three/drei";
import lensIMG from "../Static/lensDirtTexture.png";
import { folder, useControls } from "leva";
import * as THREE from "three";

const WorldStory = () => {
  //   const lensFlareProps = useControls({
  //     LensFlare: folder(
  //       {
  //         enabled: { value: true, label: "enabled?" },
  //         opacity: { value: 1.0, min: 0.0, max: 1.0, label: "opacity" },
  //         position: { value: { x: -25, y: 6, z: -60 }, step: 1, label: "position" },
  //         glareSize: { value: 0.35, min: 0.01, max: 1.0, label: "glareSize" },
  //         starPoints: { value: 6.0, step: 1.0, min: 0, max: 32.0, label: "starPoints" },
  //         animated: { value: true, label: "animated?" },
  //         followMouse: { value: false, label: "followMouse?" },
  //         anamorphic: { value: false, label: "anamorphic?" },
  //         colorGain: { value: new THREE.Color(56, 22, 11), label: "colorGain" },

  //         Flare: folder({
  //           flareSpeed: { value: 0.4, step: 0.001, min: 0.0, max: 1.0, label: "flareSpeed" },
  //           flareShape: { value: 0.1, step: 0.001, min: 0.0, max: 1.0, label: "flareShape" },
  //           flareSize: { value: 0.005, step: 0.001, min: 0.0, max: 0.01, label: "flareSize" },
  //         }),

  //         SecondaryGhosts: folder({
  //           secondaryGhosts: { value: true, label: "secondaryGhosts?" },
  //           ghostScale: { value: 0.1, min: 0.01, max: 1.0, label: "ghostScale" },
  //           aditionalStreaks: { value: true, label: "aditionalStreaks?" },
  //         }),

  //         StartBurst: folder({
  //           starBurst: { value: true, label: "starBurst?" },
  //           haloScale: { value: 0.5, step: 0.01, min: 0.3, max: 1.0 },
  //         }),
  //       },
  //       { collapsed: true }
  //     ),
  //   });
  return (
    <>
      <Canvas gl={{ alpha: false, stencil: false, antialias: false, depth: false }} dpr={1}>
        <OrbitControls />
        <EffectComposer>
          {/* 테스트용 */}
          {/* <LensFlare dirtTextureFile={lensIMG} {...lensFlareProps} /> */}

          <LensFlare dirtTextureFile={lensIMG} colorGain={new THREE.Color(56, 22, 11)} opacity={0.8} flareShape={0.37} flareSize={0.008} flareSpeed={0.4} glareSize={0.01} starPoints={0.1} ghostScale={0.1} haloScale={0.5} />
        </EffectComposer>
      </Canvas>
    </>
  );
};

export default WorldStory;
