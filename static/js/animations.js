document.addEventListener("DOMContentLoaded", () => {
    // Основная timeline для анимации загрузки
    const tl = gsap.timeline();

    // Анимация появления body
    tl.to("body", {
        opacity: 1,
        duration: 0.5,
        ease: "power2.inOut"
    });

    // Анимация заголовка
    tl.to("h2", {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: "back.out(1.7)"
    }, "-=0.3");

    // Анимация формы
    tl.to("#uploadForm", {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: "power2.out"
    }, "-=0.3");

    // Анимация футера
    tl.to("footer", {
        opacity: 0.7,
        duration: 0.4,
        ease: "power2.out"
    }, "-=0.3");

    // Функция для показа уведомлений
    window.showNotification = (message, isError = false) => {
        const notification = document.getElementById("notification");
        if (!notification) return; // Проверка на существование элемента

        notification.textContent = message;
        notification.style.backgroundColor = isError ? "#dc3545" : "#198754";
        notification.style.display = "block";

        gsap.fromTo(notification, 
            { x: 100, opacity: 0 },
            { x: 0, opacity: 1, duration: 0.5, ease: "power2.out" }
        );

        // Автоматически скрываем уведомление через 3 секунды
        setTimeout(() => {
            gsap.to(notification, {
                x: 100,
                opacity: 0,
                duration: 0.5,
                ease: "power2.in",
                onComplete: () => {
                    notification.style.display = "none";
                }
            });
        }, 3000);
    };
});