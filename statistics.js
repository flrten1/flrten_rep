// Функция для загрузки статистики с сервера и обновления информации на странице
function loadStatistics() {
    fetch('/statistics.php')
        .then(response => response.json())
        .then(statistics => {
            const statisticsContainer = document.getElementById('statistics');
            statisticsContainer.innerHTML = ''; // Очистка контейнера перед обновлением

            statistics.forEach(stat => {
                const statElement = document.createElement('div');
                statElement.textContent = `Short URL: ${stat.short_url}, Clicks: ${stat.count}`;
                statisticsContainer.appendChild(statElement);
            });
        })
        .catch(error => console.error('Error loading statistics:', error));
}

// Загрузка статистики при загрузке страницы
document.addEventListener('DOMContentLoaded', loadStatistics);
