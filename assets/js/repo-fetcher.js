document.addEventListener('DOMContentLoaded', function() {
    const repoContainer = document.getElementById('repo-list');
    const loadingElement = document.getElementById('loading-repos');
    const username = 'vaishnavak2001';
    
    // List of pinned repos to exclude from the main list (since they are already shown at top)
    // We will populate this based on the HTML data attribute if needed, or just hardcode for now
    // to match the _config.yml "projects" list.
    const pinnedRepos = [
        'diabetic-retinopathy-detection',
        'pneumonia-detection',
        'skin-disorder-detection',
        'face-gender-prediction',
        'handwritten-digit-recognition',
        'auto-price-prediction',
        'fifa20-clustering'
    ];

    async function fetchRepos() {
        try {
            const response = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`);
            if (!response.ok) throw new Error('Failed to fetch repositories');
            
            let repos = await response.json();
            
            // Filter: Exclude forks (unless critical) and pinned repos
            repos = repos.filter(repo => {
                return !repo.fork && !pinnedRepos.includes(repo.name);
            });

            // Sort: Most stars, then most recently updated
            repos.sort((a, b) => {
                if (b.stargazers_count !== a.stargazers_count) {
                    return b.stargazers_count - a.stargazers_count;
                }
                return new Date(b.updated_at) - new Date(a.updated_at);
            });

            renderRepos(repos);
        } catch (error) {
            console.error('Error fetching repos:', error);
            loadingElement.textContent = 'Failed to load repositories. Please check GitHub directly.';
        }
    }

    function renderRepos(repos) {
        loadingElement.style.display = 'none';
        
        if (repos.length === 0) {
            repoContainer.innerHTML = '<p>No additional public repositories found.</p>';
            return;
        }

        repos.forEach(repo => {
            const li = document.createElement('li');
            li.className = 'project-item';
            
            const description = repo.description || 'No description available.';
            const language = repo.language ? `<span class="tech-tag">${repo.language}</span>` : '';
            const stars = repo.stargazers_count > 0 ? ` • ⭐ ${repo.stargazers_count}` : '';
            
            li.innerHTML = `
                <h3 class="project-title">
                    <a href="${repo.html_url}" target="_blank">${formatTitle(repo.name)}</a>
                </h3>
                <div class="project-meta">
                    ${language}${stars} • Updated: ${new Date(repo.updated_at).toLocaleDateString()}
                </div>
                <p class="project-description">${description}</p>
            `;
            
            repoContainer.appendChild(li);
        });
    }

    function formatTitle(str) {
        return str.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    fetchRepos();
});
