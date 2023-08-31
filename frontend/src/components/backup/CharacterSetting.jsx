import React from 'react';

const CharacterSetting = () => {
  // useEffect(() => {
  //   const dropdowns = document.querySelectorAll('.Charsetting_dropdown');
  //   dropdowns.forEach((dropdown) => {
  //     const select = dropdown.querySelector('.Charsetting_select');
  //     const caret = dropdown.querySelector('.Charsetting_caret');
  //     const menu = dropdown.querySelector('.Charsetting_menu');
  //     const options = dropdown.querySelectorAll('.Charsetting_menu li');
  //     const selected = dropdown.querySelector('.Charsetting_selected');

  //     select.addEventListener('click', () => {
  //       select.classList.toggle('Charsetting_select-clicked');
  //       caret.classList.toggle('Charsetting_caret-rotate');
  //       menu.classList.toggle('Charsetting_menu-open');
  //     });
  //     options.forEach((option) => {
  //       option.addEventListener('click', () => {
  //         selected.innerText = option.innerText;
  //         select.classList.remove('Charsetting_select-clicked');
  //         caret.classList.remove('Charsetting_caret-rotate');
  //         menu.classList.remove('Charsetting_menu-open');
  //         options.forEach((option) => {
  //           option.classList.remove('Charsetting_active');
  //         });
  //         option.classList.add('Charsetting_active');
  //       });
  //     });
  //   });
  // });
  return (
    <div>
      {/* model select */}
      {/* <div className="Charsetting_dropdown_body">
        <div className="Charsetting_dropdown">
          <div className="Charsetting_select">
            <span className="Charsetting_selected">Model select</span>
            <div className="Charsetting_caret"></div>
          </div>
          <ul className="Charsetting_menu">
            <li className="Charsetting_active">Model select</li>
            <li>i</li>
            <li>n</li>
            <li>d</li>
            <li>e</li>
            <li>x</li>
          </ul>
        </div>
      </div> */}
    </div>
  );
};

export default CharacterSetting;
