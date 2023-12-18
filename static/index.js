document.getElementById("add_task").addEventListener("click", function(){
    document.getElementById("popup").classList.add("open")
})

//Закртыть модальное окно при нажатии эскейп
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("popup").classList.remove("open")
    }
});

// Закрыть модальное окно при клике вне его
document.querySelector("#popup .popup_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("popup").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});

//autho
document.getElementById("autho_btn").addEventListener("click", function(){
    document.getElementById("autho").classList.add("open")
})

//Закртыть модальное окно при нажатии эскейп
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("autho").classList.remove("open")
    }
});

// Закрыть модальное окно при клике вне его
document.querySelector("#autho .autho_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("autho").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});

//registr

document.getElementById("registr_btn").addEventListener("click", function(){
    document.getElementById("registr").classList.add("open")
})

//Закртыть модальное окно при нажатии эскейп
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("registr").classList.remove("open")
    }
});

// Закрыть модальное окно при клике вне его
document.querySelector("#registr .registr_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("registr").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});

//logout

document.getElementById("logout_btn").addEventListener("click", function(){
    document.getElementById("logout").classList.add("open")
})

//Закртыть модальное окно при нажатии эскейп
window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("logout").classList.remove("open")
    }
});

// Закрыть модальное окно при клике вне его
document.querySelector("#logout .logout_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("logout").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.remove('open');
});

//flash сообщения
document.querySelector("#flash .flash_box").addEventListener('click', event => {
    event._isClickWithInModal = true;
});
document.getElementById("flash").addEventListener('click', event => {
    if (event._isClickWithInModal) return;
    event.currentTarget.classList.add('close');
});