document.addEventListener('DOMContentLoaded', function() {
    // Инициализация начальных анимаций
    const tl = gsap.timeline();

    tl.from('h2.text-light', {
            y: -50,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        })
        .from('h3.text-light', {
            x: -30,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.2')
        .from('#upload-column', {
            x: -50,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.3')
        .from('#upload-column .upload-card', {
            y: 30,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.3')
        .from('.arrow-right', {
            scale: 0,
            opacity: 0,
            duration: 0.1,
            ease: 'back.out(1.7)'
        }, '-=0.3')
        .from('#download-column', {
            x: 50,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.4')
        .from('#download-column .upload-card', {
            y: 30,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.3')
        .from('#linkFilesBtn, #viewDataBtn', {
            y: 20,
            opacity: 0,
            duration: 0.1,
            stagger: 0.2,
            ease: 'power2.out'
        }, '-=0.2')
        .from('#clearFilesBtn', {
            x: -20,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.2')
        .from('#filesQueue', {
            y: 50,
            opacity: 0,
            duration: 0.1,
            ease: 'power2.out'
        }, '-=0.2');
});

// Функция анимации появления нового файла
function animateFileAppearance(row) {
    gsap.from(row, {
        y: 20,
        opacity: 0,
        duration: 0.1,
        ease: 'power2.out'
    });
}

// Функция анимации удаления файлов
function animateFilesClear(rows, onComplete) {
    gsap.to(rows, {
        y: -20,
        opacity: 0,
        duration: 0.1,
        stagger: 0.1,
        ease: 'power2.in',
        onComplete: onComplete
    });
}

// Функция анимации уведомления
function animateNotification(notification) {
    gsap.fromTo(notification, 
        {
            opacity: 0,
            x: 100,
            visibility: 'visible'
        },
        {
            opacity: 1,
            x: 0,
            duration: 0.1,
            ease: 'power2.out',
            onComplete: () => {
                // Автоматическое скрытие через 3 секунды
                gsap.to(notification, {
                    opacity: 0,
                    x: 100,
                    delay: 3,
                    duration: 0.1,
                    ease: 'power2.in',
                    onComplete: () => {
                        notification.style.visibility = 'hidden';
                    }
                });
            }
        }
    );
}