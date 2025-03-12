let slideIndex = 0;
showSlides();

// Funkcja do automatycznego pokazu slajdów
function showSlides() {
  let i;
  const slides = document.getElementsByClassName("mySlides");
  const dots = document.getElementsByClassName("dot");

  // Ukryj wszystkie slajdy
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  // Zwiększ indeks slajdu i wróć do początku, jeśli konieczne
  slideIndex++;
  if (slideIndex > slides.length) {
    slideIndex = 1;
  }

  // Oznacz aktywną kropkę
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  // Pokaż aktualny slajd i zaznacz kropkę
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";

  // Zmień slajd co 3 sekundy
  setTimeout(showSlides, 3000);
}

// Funkcja do ręcznej zmiany slajdu
function plusSlides(n) {
  slideIndex += n - 1; // Dostosuj indeks
  showSlides();
}

// Funkcja do przejścia do konkretnego slajdu
function currentSlide(n) {
  slideIndex = n - 1; // Dostosuj indeks
  showSlides();
}
