const activePage = window.location.pathname;

const navLinks = document.querySelectorAll('nav a').forEach(link => {
  if (link.href.includes(`${activePage}`)) {
    link.classList.add('active');
  }
});

const ReadMoreButton = document.querySelector('.readMoreButton');
const text = document.querySelector('.text');

ReadMoreButton.addEventListener('click', (e) => {
  text.classList.toggle('show-more');
  if (ReadMoreButton.innerText == "Click hear to read more") {
    ReadMoreButton.innerText = "Click hear to read less";
  }
  else {
    ReadMoreButton.innerText = "Click hear to read more";
  }
})