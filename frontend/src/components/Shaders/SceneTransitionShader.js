import * as THREE from "three";
// React Three Fiber
import { extend } from "@react-three/fiber";
import { shaderMaterial } from "@react-three/drei";
import glsl from "glslify";
// Shaders

const SceneTransitionShader = shaderMaterial(
  {
    direction: (-1.0, 1.0),
  },
  glsl`
  uniform vec2 direction
  const float smoothness = 0.5;
const vec2 center = vec2(0.5, 0.5);

vec4 transition (vec2 uv) {
  vec2 v = normalize(direction);
  v /= abs(v.x) + abs(v.y);
  float d = v.x * center.x + v.y * center.y;
  float m = 1.0 - smoothstep(-smoothness, 0.0, v.x * uv.x + v.y * uv.y - (d - 0.5 + progress * (1.0 + smoothness)));
  return mix(getFromColor((uv - 0.5) * (1.0 - m) + 0.5), getToColor((uv - 0.5) * m + 0.5), m);
}
  `
);
extend({
  SceneTransitionShader,
});

export default SceneTransitionShader;
