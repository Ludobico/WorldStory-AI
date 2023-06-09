import * as THREE from "three";
import { shaderMaterial } from "@react-three/drei";
import { extend } from "@react-three/fiber";
import glsl from "glslify";

const BackgroundTransition = shaderMaterial(
  {
    progress: 0,
    texture1: new THREE.Texture(),
    texture2: new THREE.Texture(),
    texture3: new THREE.Texture(),
  },
  glsl`
    precision mediump float;
    uniform sampler2D texture1;
    uniform sampler2D texture2;
    uniform sampler2D texture3;
    uniform float progress;
  
    varying vec2 vUv;
  
    void main() {
      vec4 color1 = texture2D(texture1, vUv);
      vec4 color2 = texture2D(texture2, vUv);
      vec4 color3 = texture2D(texture3, vUv);
      
      if (progress < 0.33) {
        gl_FragColor = mix(color1, color2, progress * 3.0);
      } else if (progress < 0.66) {
        gl_FragColor = mix(color2, color3, (progress - 0.33) * 3.0);
      } else {
        gl_FragColor = mix(color3, color1, (progress - 0.66) * 3.0);
      }
    }`
);
extend({
  BackgroundTransition,
});

export default BackgroundTransition;
