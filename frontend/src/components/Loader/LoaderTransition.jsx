import React from "react";
import "./LoaderTransition.css";
import loaderGif from "../Static/giphy.gif";
import { useNavigate } from "react-router-dom";

const LoaderTransition = () => {
  return (
    <div className="LoaderTransition_top_div">
      <div className="LoaderTransition_loader">
        <img src={loaderGif} />
      </div>
    </div>
  );
};

export default LoaderTransition;
