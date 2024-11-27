const linkFilesBtn = document.getElementById('linkFilesBtn');
const linkingLoader = document.getElementById('linkingLoader');
const viewDataBtn = document.getElementById('viewDataBtn');

linkFilesBtn.addEventListener('click', function() {
    linkingLoader.classList.remove('d-none');
    linkFilesBtn.disabled = true;

    // Здесь будет ваша логика связывания файлов
    setTimeout(() => {
        linkingLoader.classList.add('d-none');
        linkFilesBtn.disabled = false;
        showNotification('Файлы успешно связаны', 'success');
    }, 2000); // Замените на реальный запрос к серверу
});

viewDataBtn.addEventListener('click', function() {
    window.location.href = '/view_data';
});

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const filesQueue = document.getElementById('filesQueue');
    const clearFilesBtn = document.getElementById('clearFilesBtn');

    function getFileIcon(extension) {
        const icons = {
            'csv': 'bi-file-earmark-spreadsheet',
            'rar': 'bi-file-earmark-zip',
            'zip': 'bi-file-earmark-zip'
        };
        return icons[extension] || 'bi-file-earmark';
    }

    function formatDate(date) {
        return date.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function addFileToQueue(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        const nameWithoutExt = file.name.replace(`.${extension}`, '');
        const uploadTime = formatDate(file.uploadTime || new Date());

        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="text-light">
                <i class="bi bi-file-earmark me-2"></i>
                ${nameWithoutExt}
            </td>
            <td>
                <span class="badge bg-primary">
                    <i class="bi ${getFileIcon(extension)} me-1"></i>
                    ${extension}
                </span>
            </td>
            <td class="text-end">
                <span class="text-light me-3">${uploadTime}</span>
                <button class="btn btn-link text-danger p-0" onclick="deleteFile('${file.name}', this)">
                    <i class="bi bi-x-lg"></i>
                </button>
            </td>
        `;
        filesQueue.querySelector('tbody').appendChild(row);
        animateFileAppearance(row);
    }

    function loadExistingFiles() {
        fetch('/files/')
            .then(response => response.json())
            .then(files => {
                filesQueue.querySelector('tbody').innerHTML = '';
                files.forEach(fileData => {
                    const file = {
                        name: fileData.name,
                        uploadTime: new Date(fileData.uploadTime * 1000)
                    };
                    addFileToQueue(file);
                });
            })
            .catch(error => {
                showNotification('Ошибка при загрузке списка файлов', 'error');
            });
    }

    window.deleteFile = function(filename, button) {
        fetch(`/files/${filename}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            const row = button.closest('tr');
            animateFilesClear([row], () => {
                row.remove();
            });
            showNotification('Файл успешно удален', 'success');
        })
        .catch(error => {
            showNotification('Ошибка при удалении файла', 'error');
        });
    };

    fileInput.addEventListener('change', function(e) {
        const files = Array.from(this.files);
        files.forEach(file => {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loadExistingFiles();
                showNotification('Файл успешно загружен', 'success');
            })
            .catch(error => {
                showNotification('Ошибка при загрузке файла', 'error');
            });
        });
    });

    clearFilesBtn.addEventListener('click', function() {
        const rows = filesQueue.querySelectorAll('tbody tr');

        fetch('/clear-files/', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            animateFilesClear(rows, () => {
                filesQueue.querySelector('tbody').innerHTML = '';
            });
            showNotification('Все файлы удалены', 'success');
            loadExistingFiles(); // Обновляем список файлов
        })
        .catch(error => {
            showNotification('Ошибка при удалении файлов', 'error');
        });
    });

    // Загрузите существующие файлы при загрузке страницы
    loadExistingFiles();
});
