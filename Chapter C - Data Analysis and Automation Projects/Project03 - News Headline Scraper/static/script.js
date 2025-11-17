document.addEventListener('DOMContentLoaded', () => {

    const fetchBtn = document.getElementById('fetch-btn');
    const clearBtn = document.getElementById('clear-btn');
    const newsGrid = document.getElementById('news-grid');
    const loader = document.getElementById('loader');
    const emptyState = document.getElementById('empty-state');
    const articleCount = document.getElementById('article-count');
    const lastUpdated = document.getElementById('last-updated');
    const statusBadge = document.getElementById('status');

    function updateStatus(text, isActive = false) {
        statusBadge.innerHTML = `<span class="status-dot ${isActive ? 'active' : ''}"></span>${text}`;
    }

    function formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'});
    }

    async function fetchNews() {
        loader.style.display = 'flex';
        emptyState.style.display = 'none';
        newsGrid.innerHTML = '';
        updateStatus('Fetching...', true);

        try {
            const response = await fetch('/api/news');
            const result = await response.json();

            if (result.success && result.data.length > 0) {
                displayNews(result.data);
                articleCount.textContent = result.count;
                lastUpdated.textContent = formatTime(result.timestamp);
                updateStatus('Live', true);
            } else {
                emptyState.style.display = 'flex';
                updateStatus('No Data', false);
            }
        } catch (error) {
            console.error('Error:', error);
            emptyState.style.display = 'flex';
            emptyState.querySelector('h2').textContent = 'Error Fetching News';
            emptyState.querySelector('p').textContent = 'Please try again later';
            updateStatus('Error', false);
        } finally {
            loader.style.display = 'none';
        }
    }

    function displayNews(newsData) {
        newsGrid.innerHTML = '';

        newsData.forEach((article, index) => {
            const card = document.createElement('div');
            card.className = 'news-card';
            card.style.animationDelay = `${index * 0.05}s`;

            card.innerHTML = `
                    <div class="card-header">
                        <span class="card-number">#${article.id}</span>
                        <span class="card-source">${article.source}</span>
                    </div>
                    <h3 class="card-title">${article.title}</h3>
                    <a href="${article.url}" target="_blank" class="card-link">
                        Read Full Article
                    </a>
                `;

            newsGrid.appendChild(card);
        });
    }

    function clearNews() {
        newsGrid.innerHTML = '';
        emptyState.style.display = 'flex';
        articleCount.textContent = '0';
        lastUpdated.textContent = '--:--';
        updateStatus('Ready', false);
    }

    document.body.insertBefore(loader, document.body.firstChild);

    fetchBtn.addEventListener('click', fetchNews);
    clearBtn.addEventListener('click', clearNews);

    fetchNews();
})