import React, { Fragment } from "react";
import "./InsideStory.css";
import { Html } from "@react-three/drei";

const InsideStory = () => {
  function Plane() {
    return (
      <>
        <ambientLight intensity={1} color={"white"} />
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[50, 50]} />
        </mesh>
      </>
    );
  }

  return (
    <>
      <Plane />
    </>
  );
};

export default InsideStory;
