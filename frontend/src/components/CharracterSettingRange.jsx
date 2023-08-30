import React, { useEffect, useRef, useState } from 'react';
import './CharracterSettingRange.css';

const CharracterSettingRange = ({ min, max, value, step, name }) => {
  const [sliderRange, setSliderRange] = useState(value);
  const [inputValue, setInputValue] = useState(value);
  const sliderRef = useRef(null);

  function handleSliderInput() {
    const range = max - min;
    const distance = sliderRef.current.value - min;
    const percentage = (distance / range) * 100;
    setSliderRange(percentage);
    setInputValue(sliderRef.current.value);
  }

  function handleNumberInput(e) {
    const newValue = parseInt(e.target.value);
    if (newValue < min) {
      setInputValue(min);
      setSliderRange(0);
    } else if (newValue > max) {
      setInputValue(max);
      setSliderRange(100);
    } else {
      setInputValue(newValue);
      const range = max - min;
      const distance = newValue - min;
      const percentage = (distance / range) * 100;
      setSliderRange(percentage);
    }
  }

  useEffect(() => {
    handleSliderInput();
  }, [sliderRef]);

  return (
    <div className="CharracterSettingRange_top_div">
      <div className="range-slider">
        <div className="setting-name">{name}</div>
        <div className="slider-values">
          <small>{min}</small>
          <input
            type="number"
            className="number-input"
            value={inputValue}
            min={min}
            max={max}
            step={step}
            onInput={handleNumberInput}
          />
          <small>{max}</small>
        </div>

        <div className="slider-container">
          <input
            type="range"
            className="slider"
            onInput={handleSliderInput}
            value={inputValue}
            min={min}
            max={max}
            ref={sliderRef}
            step={step}
          />
          <div
            className="slider-thumb"
            style={{ left: `calc(${sliderRange}% - 0.5em)`, transition: `left 0.3s ease` }}
          ></div>
          <div className="progress" style={{ width: `${sliderRange}%`, transition: `width 0.3s ease` }}></div>
        </div>
      </div>
    </div>
  );
};

export default CharracterSettingRange;