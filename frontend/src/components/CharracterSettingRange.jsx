import React, { useEffect, useRef, useState } from 'react';
import './CharracterSettingRange.css';

const CharracterSettingRange = ({ min, max, value, step, name, onChange }) => {
  const [sliderRange, setSliderRange] = useState(value);
  const [inputValue, setInputValue] = useState(value);
  const sliderRef = useRef(null);

  const handleValueChange = (event) => {
    const newValue = parseFloat(event.target.value);
    onChange(newValue); // 값이 변경될 때 부모 컴포넌트에 전달
  };

  function handleSliderInput() {
    const range = max - min;
    const distance = sliderRef.current.value - min;
    const percentage = (distance / range) * 100;
    setSliderRange(percentage);
    setInputValue(sliderRef.current.value);
  }

  function handleNumberInput(e) {
    const newValue = parseFloat(e.target.value);
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
            onChange={handleValueChange}
          />
          <small>{max}</small>
        </div>

        <div className="slider-container">
          <input
            type="range"
            className="slider"
            onInput={handleSliderInput}
            onChange={handleValueChange}
            value={inputValue}
            min={min}
            max={max}
            ref={sliderRef}
            step={step}
          />
          <div className="slider-thumb" style={{ left: `calc(${sliderRange}% - 0.5em)` }}></div>
          <div className="progress" style={{ width: `${sliderRange}%` }}></div>
        </div>
      </div>
    </div>
  );
};

export default CharracterSettingRange;
