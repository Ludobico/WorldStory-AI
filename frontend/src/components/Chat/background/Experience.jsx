import React, { useMemo, useState } from 'react';
import * as THREE from 'three';
import { DissolveMaterial } from '../../Shaders/DissolveMaterial';
import { ContactShadows, Environment, Image, OrbitControls } from '@react-three/drei';
import { Canvas, useThree } from '@react-three/fiber';
import testimage from '../../Static/chat_background/fantasy_desktop.jpg';
import testimage2 from '../../Static/chat_background/cyberpunk-city-buildings-art.jpg';

const InsideCanvas = ({ backgroundValue }) => {
  const [visibleItem, setVisibleItem] = useState(backgroundValue);
  const fantasy_boxMaterial = useMemo(() => {
    const fantasy_texture = new THREE.TextureLoader().load(testimage);
    return new THREE.MeshStandardMaterial({ map: fantasy_texture });
  }, []);
  const cyberpunk_boxMaterial = useMemo(() => {
    const cyberpunk_texture = new THREE.TextureLoader().load(testimage2);
    return new THREE.MeshStandardMaterial({ map: cyberpunk_texture });
  }, []);
  const { viewport } = useThree();
  const onFadeOut = () => {
    setVisibleItem(backgroundValue);
  };

  return (
    <>
      {visibleItem == 'Fantasy' && (
        <group>
          <mesh>
            <planeGeometry args={[viewport.width, viewport.height]} />
            <DissolveMaterial
              baseMaterial={fantasy_boxMaterial}
              color="#0000cd"
              visible={backgroundValue == 'Fantasy'}
              intensity={10}
              thickness={0.1}
              onFadeOut={onFadeOut}
            />
          </mesh>
          <Environment preset="forest" />
        </group>
      )}
      {visibleItem == 'Cyberpunk' && (
        <group>
          <mesh>
            <planeGeometry args={[viewport.width, viewport.height]} />
            <DissolveMaterial
              baseMaterial={cyberpunk_boxMaterial}
              color="#0000cd"
              visible={backgroundValue == 'Cyberpunk'}
              intensity={10}
              thickness={0.1}
              onFadeOut={onFadeOut}
            />
          </mesh>
          <Environment preset="forest" />
        </group>
      )}
    </>
  );
};
const Experience = ({ backgroundValue }) => {
  return (
    <Canvas style={{ position: 'absolute', width: '100%', height: '100%', top: 0, left: 0 }}>
      <InsideCanvas backgroundValue={backgroundValue} />
    </Canvas>
  );
};

export default Experience;
