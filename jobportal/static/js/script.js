const bar = document.querySelector('#bar');
const menu = document.querySelector('#menu');

if( bar ){
bar.addEventListener('click',()=>{
  menu.classList.toggle('active');
});
}

function adjustLayout() {
  const container = document.querySelector('#contract-container');
  if (window.innerWidth > 768) {
    container.classList.add('md:flex-row-reverse');
  } else {
    container.classList.remove('md:flex-row-reverse');
  }
}
adjustLayout();
window.addEventListener('resize', adjustLayout);







