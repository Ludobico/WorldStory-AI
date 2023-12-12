import { Canvas } from '@react-three/fiber';
import { React } from 'react';
import WorldStory from './Canvas/WorldStory';
import Header from './Header/Header';
import './Main.css';
import './Header/Header.css';
import { Html, PerformanceMonitor, Stats } from '@react-three/drei';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import LoaderTransition from './Loader/LoaderTransition';
import InsideStory from './Canvas/InsideStory';
import './Canvas/InsideStory.css';
import Logo from './Header/Logo';

const Main = () => {
  gsap.registerPlugin(ScrollTrigger);
  return (
    <div className="Main_top_div">
      <Canvas
        gl={{ alpha: false, stencil: false, antialias: false, depth: false }}
        dpr={1}
        style={{ width: '100vw', height: '100vh' }}
      >
        <Html fullscreen>
          {/* <Header />
          <Logo /> */}
        </Html>
        <WorldStory />
        <Stats />
      </Canvas>
      {/* <div className="inside">
        <InsideStory />
      </div> */}
    </div>
  );
};

export default Main;
