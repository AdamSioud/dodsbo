//Ved åpning av burger meny skjer det i navOpen()
const navOpen = () => {
    //Linker sammen attributter i CSS til konstanter i JavaScript
    const burger = document.querySelector('.burger-meny');
    const nav = document.querySelector('.nav-lenker');
    const navLenker = document.querySelectorAll('.nav-lenker li');

    //Hva som skjer når burger-menyen åpnes
    burger.addEventListener('click', () => {
        //Åpner selve meny-baren (bagrkunnen i burger-menyen)
        nav.classList.toggle('nav-aktiv');

         //Animerer lenker som blir vist i burger-menyen
        navLenker.forEach((link) => {
            if (link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = 'navLenkerFadeIn 0.5s ease forwards 0.3s';
            }
        })

        //Animasjonen for burger-menyen sine linjer (ikon) ved klikk
        burger.classList.toggle('toggle');
    });
}

    
//Kjører animasjonen(e) til appen
navOpen();