import React, { useEffect, useRef, useState } from 'react';
import LensFlare from './UltimateLensFlare';
import './WorldStory.css';
import { EffectComposer } from '@react-three/postprocessing';
import { Html, OrbitControls, PerspectiveCamera, Stars, useTexture } from '@react-three/drei';
import lensIMG from '../Static/lensDirtTexture.png';
import background_1 from '../Static/background1.jpg';
import background_2 from '../Static/background2.jpg';
import background_3 from '../Static/background3.jpg';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Canvas, useFrame } from '@react-three/fiber';
import TransitionShaderMaterial from '../Shaders/TransitionShader';
import SceneTransitionShader from '../Shaders/SceneTransitionShader';
import InsideStory from './InsideStory';
import Header from '../Header/Header';
import Logo from '../Header/Logo';
import { useNavigate } from 'react-router';
import { Link } from 'react-router-dom';

function Skybox() {
  const backgroundList = useTexture([background_1, background_2, background_3]);
  const [textureIndex, setTextureIndex] = useState(0);
  const tl = gsap.timeline();
  const [texture_change_trigger, set_texture_change_trigger] = useState(0);
  const [texture_change_trigger_flag, set_texture_change_trigger_flag] = useState(false);
  // 머터리얼에 적용하는 ref
  const shaderMaterialRef = useRef();

  // 매쉬에 적용하는 ref
  const meshRef = useRef();

  useEffect(() => {
    const interval = setInterval(() => {
      set_texture_change_trigger((prevTrigger) => {
        if (prevTrigger === 2) {
          set_texture_change_trigger(prevTrigger - 1);
          set_texture_change_trigger_flag(true);
        } else if (prevTrigger === 1 && texture_change_trigger_flag === false) {
          set_texture_change_trigger(prevTrigger + 1);
        } else if (prevTrigger === 1 && texture_change_trigger_flag === true) {
          set_texture_change_trigger(prevTrigger - 1);
        } else if (prevTrigger === 0) {
          set_texture_change_trigger(prevTrigger + 1);
          set_texture_change_trigger_flag(false);
        }
      });
    }, 3000);
    return () => {
      clearInterval(interval);
    };
  });

  useFrame(() => {
    if (texture_change_trigger == 0) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 0,
        onStart: () => {
          shaderMaterialRef.current.uTexture1 = backgroundList[0];
        },
      });
    } else if (texture_change_trigger == 1) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 1,
        onComplete: () => {
          shaderMaterialRef.current.uTexture1 = backgroundList[1];
        },
      });
    } else if (texture_change_trigger == 2) {
      gsap.to(shaderMaterialRef.current, {
        uProgress: 0,
      });
    }
  });

  return (
    <mesh userData={{ LensFlare: 'no-occlusion' }} scale={[-1, 1, 1]} ref={meshRef}>
      <sphereBufferGeometry args={[5, 64, 64]} />
      {/* <meshBasicMaterial toneMapped={false} map={backgroundList[textureIndex]} side={THREE.FrontSide} /> */}
      <transitionShaderMaterial
        ref={shaderMaterialRef}
        uTexture1={backgroundList[0]}
        uTexture2={backgroundList[2]}
        uTexture3={backgroundList[1]}
        uProgress={0}
        attach="material"
      />
    </mesh>
  );
}

const Introduce = () => {
  useEffect(() => {
    const tl = gsap.timeline();

    tl.from('.intro_reveal span', 1.8, {
      y: 100,
      ease: 'power4.out',
      delay: 1,
      skewY: 5,
      stagger: {
        amount: 0.5,
      },
    });
  });
  return (
    <>
      <div className="Introduce_intro intro_reveal">
        <span>Create</span>
      </div>
      <div className="Introduce_intro1 intro_reveal">
        <span>Your own</span>
      </div>
      <div className="Introduce_intro2 intro_reveal">
        <span>Fictional</span>
      </div>
      <div className="Introduce_intro3 intro_reveal">
        <span>Characters</span>
      </div>
      <div className="button_container">
        <div className="intro_button2 button_reveal">Chat with Character</div>
        <div className="intro_button button_reveal">
          <a href="/charsetting" className="Introduce_a">
            Character setting
          </a>
        </div>
      </div>
    </>
  );
};

const WorldStory = () => {
  const OrbitcameraRef = useRef();
  const cameraRef = useRef();
  const cameraHandler = () => {
    console.log(cameraRef.current);
  };
  const MemoOrbitControl = React.memo(OrbitControls)
  return (
    <>
      {/* <OrbitControls ref={OrbitcameraRef} autoRotate enableZoom={false} /> */}
      <MemoOrbitControl ref={OrbitcameraRef} autoRotate enableZoom={false} />
      <PerspectiveCamera makeDefault position={[-2.129, 0.177, 27.08]} ref={cameraRef} />
      <EffectComposer>
        {/* 테스트용 */}
        {/* <LensFlare dirtTextureFile={lensIMG} {...lensFlareProps} /> */}
        <LensFlare
          dirtTextureFile={lensIMG}
          colorGain={new THREE.Color(56, 22, 11)}
          opacity={0.8}
          flareShape={0.37}
          flareSize={0.004}
          flareSpeed={0.4}
          glareSize={0.01}
          starPoints={0.1}
          ghostScale={0.1}
          haloScale={0.5}
        />
      </EffectComposer>
      <directionalLight intensity={1} position={[0, 0, 0]} />
      <Skybox />
      <Stars radius={100} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
      <Html fullscreen wrapperClass="Introduce_top_div">
        <Introduce />
        <Logo />
      </Html>
    </>
  );
};

export default WorldStory;
