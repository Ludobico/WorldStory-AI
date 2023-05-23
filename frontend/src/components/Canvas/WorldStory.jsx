import React from "react";
import LensFlare from "./UltimateLensFlare";
import "../Static/WorldStory.css";
import { Canvas } from "@react-three/fiber";
import { EffectComposer } from "@react-three/postprocessing";
import { OrbitControls } from "@react-three/drei";
import lensIMG from "../Static/lensDirtTexture.png";

const WorldStory = () => {
  return (
    <>
      <Canvas>
        <OrbitControls />
        <EffectComposer>
          <LensFlare dirtTextureFile={lensIMG} />
        </EffectComposer>
      </Canvas>
    </>
  );
};

export default WorldStory;
