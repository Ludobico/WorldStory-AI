import * as THREE from "three";
// React Three Fiber
import { extend } from "@react-three/fiber";
import { shaderMaterial } from "@react-three/drei";
import glsl from "glslify";
// Shaders

const TransitionShaderMaterial = shaderMaterial(
  // Uniforms
  {
    uProgress: 0,
    uTexture1: new THREE.Texture(),
    uTexture2: new THREE.Texture(),
    uTexture3: new THREE.Texture(),
    uUVAspect: 1,
  },
  glsl`
    precision mediump float;

    varying vec2 vUv;
    uniform float uTime; 

    void main()
    {
      vUv = uv;

      vec4 modelPosition = modelMatrix * vec4(position, 1.0);
      vec4 viewPosition = viewMatrix * modelPosition;
      vec4 projectedPosition = projectionMatrix * viewPosition;

      gl_Position = projectedPosition;
    }
  `,
  glsl`
  precision mediump float;
  uniform sampler2D uTexture1;
  uniform sampler2D uTexture2;
  uniform sampler2D uTexture3;
  uniform float uProgress;
  
  varying vec2 vUv;
  
  mat2 rotate(float a) {
    float s = sin(a);
    float c = cos(a);
    return	mat2(c, -s, s, c);
  }
  
  void main()
  { 
    vec2 uvDivided = fract(vUv*vec2(30.,1.));
    vec2 uvDisplaced1 = vUv + rotate(3.14)*uvDivided*vec2(uProgress*vUv.x/4., 0. ) * 0.5;
    vec2 uvDisplaced2 = vUv + rotate(3.14)*uvDivided*vec2((1.- uProgress)*vUv.x/4., 0. ) * 0.5;
    vec2 uvDisplaced3 = vUv + rotate(3.14) * uvDivided * vec2((2. - uProgress) * vUv.x / 4., 0.) * 0.5;

    vec4 img1 = texture2D(uTexture1, uvDisplaced1);
    vec4 img2 = texture2D(uTexture2, uvDisplaced2);
    vec4 img3 = texture2D(uTexture3, uvDisplaced3);
    gl_FragColor = mix(img1, img2, uProgress);
  }
  `
);
extend({
  TransitionShaderMaterial,
});

export default TransitionShaderMaterial;
