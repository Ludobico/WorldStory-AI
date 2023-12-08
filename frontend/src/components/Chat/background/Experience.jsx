import React, { useMemo } from 'react';
import * as THREE from 'three';
import { DissolveMaterial } from '../../Shaders/DissolveMaterial';
import { ContactShadows, Environment, Image, OrbitControls } from '@react-three/drei';
import { Canvas, useThree } from '@react-three/fiber';
import testimage from '../../Static/chat_background/fantasy_desktop.jpg';
import testimage2 from '../../Static/chat_background/cyberpunk-city-buildings-art.jpg';

const InsideCanvas = () => {
  const boxMaterial = useMemo(() => {
    const texture = new THREE.TextureLoader().load(testimage);
    return new THREE.MeshStandardMaterial({ map: texture });
  }, []);
  const { viewport } = useThree();

  return (
    <>
      <group>
        <mesh>
          <planeGeometry args={[viewport.width, viewport.height]} />
          <DissolveMaterial baseMaterial={boxMaterial} color="#ff8243" visible={true} intensity={10} thickness={0.1} />
        </mesh>
        <Environment preset="park" />
      </group>
    </>
  );
};
const Experience = () => {
  return (
    <Canvas style={{ position: 'absolute', width: '100%', height: '100%', top: 0, left: 0 }}>
      <InsideCanvas />
    </Canvas>
  );
};

export default Experience;
