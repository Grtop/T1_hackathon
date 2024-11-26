document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы
        
        const file = fileInput.files[0];
        if (!file) {
            showNotification("Пожалуйста, выберите файл", true);
            return;
        }

        // Проверяем расширение файла
        const allowedExtensions = ['.rar', '.zip', '.7z', '.csv'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(fileExtension)) {
            showNotification("Неподдерживаемый формат файла. Разрешены только RAR, ZIP, 7Z и CSV", true);
            return;
        }

        // Отключаем кнопку на время загрузки
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        // Показываем уведомление о начале загрузки
        showNotification("Пожалуйста, подождите. Файл загружается...", false);
        
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                showNotification(result.info, false);
                form.reset(); // Очищаем форму после успешной загрузки
            } else {
                showNotification(result.detail || "Произошла ошибка при загрузке файла", true);
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification("Произошла ошибка при загрузке файла", true);
        } finally {
            // Включаем кнопку обратно
            submitButton.disabled = false;
        }
    });

    // Добавляем обработчик изменения файла для мгновенной валидации
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const allowedExtensions = ['.rar', '.zip', '.7z', '.csv'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            if (!allowedExtensions.includes(fileExtension)) {
                showNotification("Неподдерживаемый формат файла. Разрешены только RAR, ZIP, 7Z и CSV", true);
                this.value = ''; // Очищаем поле файла
            }
        }
    });
});
