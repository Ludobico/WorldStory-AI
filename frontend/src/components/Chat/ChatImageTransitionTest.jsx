import React, { useRef } from 'react';
import fantasyimage from '../Static/chat_background/fantasy_desktop.jpg';
import cyberpunkimage from '../Static/chat_background/cyberpunk-city-buildings-art.jpg';
import westernimage from '../Static/chat_background/western.jpg';
import apocalypseimage from '../Static/chat_background/Apocalypse.jpg';
import * as THREE from 'three'
import { OrbitControls, PerspectiveCamera, shaderMaterial, useTexture } from '@react-three/drei';
import { Canvas, extend, useFrame } from '@react-three/fiber';
import glsl from "glslify";
import gsap from 'gsap'

const ImageTransitionMaterial = shaderMaterial(
  // uniforms
  {
    dispFactor : 0,
    currentImage : new THREE.Texture(),
    nextImage : new THREE.Texture(),
  
  },
  // vertex
  glsl`
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 0.7 );
  }
  `,

  // fragment
  glsl`
  varying vec2 vUv;

      uniform sampler2D currentImage;
      uniform sampler2D nextImage;

      uniform float dispFactor;

      void main() {

          vec2 uv = vUv;
          vec4 _currentImage;
          vec4 _nextImage;
          float intensity = 0.6;

          vec4 orig1 = texture2D(currentImage, uv);
          vec4 orig2 = texture2D(nextImage, uv);
          
          _currentImage = texture2D(currentImage, vec2(uv.x, uv.y + dispFactor * (orig2 * intensity)));

          _nextImage = texture2D(nextImage, vec2(uv.x, uv.y + (1.0 - dispFactor) * (orig1 * intensity)));

          vec4 finalTexture = mix(_currentImage, _nextImage, dispFactor);

          gl_FragColor = finalTexture;
      }
  `
);

extend({
  ImageTransitionMaterial
})


const ImageTransition = ({ currentImage, nextImage}) => {
  const materialRef = useRef();

  // useFrame((state, delta) => {
  //   materialRef.current.uniforms.dispFactor.value += delta * 0.1
  // });

  const ChangeImages = () => {
    console.log(materialRef.current.uniforms.dispFactor.value)
    gsap.to(materialRef.current.uniforms.dispFactor, {
      value: 1,
      duration: 1,
      ease: "power2.out",
    })
  }

  return(
    <mesh position={[0,0,0]} onClick={ChangeImages}>
      <planeGeometry args={[1,1]} />
      <imageTransitionMaterial ref={materialRef} currentImage={currentImage} nextImage={nextImage} />
    </mesh>
  )
}

const Scene = () => {
  const backgroundList = useTexture([fantasyimage, cyberpunkimage, westernimage, apocalypseimage]);
  return(
    <>
    <OrbitControls />
    <PerspectiveCamera makeDefault position={[0,0,3]}/>
    <ImageTransition currentImage={backgroundList[0]} nextImage={backgroundList[1]} />
    <ambientLight intensity={3} />
    </>
  )
}
const ChatImageTransitionTest = () => {
  return (
<Canvas style={{width : '100vw', height : '100vh'}}>
<Scene />
</Canvas>
  );
};

export default ChatImageTransitionTest;