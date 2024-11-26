document.addEventListener('DOMContentLoaded', function() {
    // Инициализация начальных анимаций
    const tl = gsap.timeline();
    
    tl.from('h2.text-light', {
        y: -50,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    })
    .from('h3.text-light', {
        x: -30,
        opacity: 0,
        duration: 0.4,
        ease: 'power2.out'
    }, '-=0.2')
    .from('.col-md-4:nth-child(1)', {
        x: -50,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    }, '-=0.3')
    .from('.col-md-4:nth-child(1) .upload-card', {
        y: 30,
        opacity: 0,
        duration: 0.5,
        ease: 'power2.out'
    }, '-=0.3')
    .from('.fa-arrow-right', {
        scale: 0,
        opacity: 0,
        duration: 0.4,
        ease: 'back.out(1.7)'
    }, '-=0.3')
    .from('.col-md-4:nth-child(3)', {
        x: 50,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    }, '-=0.4')
    .from('.col-md-4:nth-child(3) .upload-card', {
        y: 30,
        opacity: 0,
        duration: 0.5,
        ease: 'power2.out'
    }, '-=0.3')
    .from('#linkFilesBtn, #viewDataBtn', {
        y: 20,
        opacity: 0,
        duration: 0.4,
        stagger: 0.2,
        ease: 'power2.out'
    }, '-=0.2')
    .from('#clearFilesBtn', {
        x: -20,
        opacity: 0,
        duration: 0.3,
        ease: 'power2.out'
    }, '-=0.2')
    .from('.container:nth-child(2) .upload-card', {
        y: 50,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
    }, '-=0.2');
});

// Функция анимации появления нового файла
function animateFileAppearance(row) {
    gsap.from(row, {
        y: 20,
        opacity: 0,
        duration: 0.4,
        ease: 'power2.out'
    });
}

// Функция анимации удаления файлов
function animateFilesClear(rows, onComplete) {
    gsap.to(rows, {
        y: -20,
        opacity: 0,
        duration: 0.3,
        stagger: 0.1,
        ease: 'power2.in',
        onComplete: onComplete
    });
}