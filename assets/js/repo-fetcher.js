<<<<<<< Updated upstream
document.addEventListener('DOMContentLoaded', function() {
    const repoContainer = document.getElementById('repo-list');
    const loadingElement = document.getElementById('loading-repos');
    const username = 'vaishnavak2001';
    
    // List of pinned repos to exclude from the main list (since they are already shown at top)
    // We will populate this based on the HTML data attribute if needed, or just hardcode for now
    // to match the _config.yml "projects" list.
=======
document.addEventListener('DOMContentLoaded', function () {
    const repoContainer = document.getElementById('repo-list');
    const loadingElement = document.getElementById('loading-repos');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const modal = document.getElementById('doc-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModal = document.getElementById('close-modal');

    const username = 'vaishnavak2001';
    let allRepos = []; // Store fetched repos for filtering

    // Pinned repos to exclude from main list
>>>>>>> Stashed changes
    const pinnedRepos = [
        'diabetic-retinopathy-detection',
        'pneumonia-detection',
        'skin-disorder-detection',
        'face-gender-prediction',
        'handwritten-digit-recognition',
        'auto-price-prediction',
        'fifa20-clustering'
    ];

<<<<<<< Updated upstream
=======
    // --- Fetch Logic ---
>>>>>>> Stashed changes
    async function fetchRepos() {
        try {
            const response = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`);
            if (!response.ok) throw new Error('Failed to fetch repositories');
<<<<<<< Updated upstream
            
            let repos = await response.json();
            
            // Filter: Exclude forks (unless critical) and pinned repos
            repos = repos.filter(repo => {
                return !repo.fork && !pinnedRepos.includes(repo.name);
            });

            // Sort: Most stars, then most recently updated
            repos.sort((a, b) => {
=======

            let repos = await response.json();

            // Filter out forks and pinned repos
            allRepos = repos.filter(repo => {
                return !repo.fork && !pinnedRepos.includes(repo.name);
            });

            // Sort: Stars then Updated
            allRepos.sort((a, b) => {
>>>>>>> Stashed changes
                if (b.stargazers_count !== a.stargazers_count) {
                    return b.stargazers_count - a.stargazers_count;
                }
                return new Date(b.updated_at) - new Date(a.updated_at);
            });

<<<<<<< Updated upstream
            renderRepos(repos);
=======
            // Initial Render (All)
            renderRepos(allRepos);
>>>>>>> Stashed changes
        } catch (error) {
            console.error('Error fetching repos:', error);
            loadingElement.textContent = 'Failed to load repositories. Please check GitHub directly.';
        }
    }

<<<<<<< Updated upstream
    function renderRepos(repos) {
        loadingElement.style.display = 'none';
        
        if (repos.length === 0) {
            repoContainer.innerHTML = '<p>No additional public repositories found.</p>';
=======
    // --- Render Logic ---
    function renderRepos(repos) {
        loadingElement.style.display = 'none';
        repoContainer.innerHTML = '';

        if (repos.length === 0) {
            repoContainer.innerHTML = '<p>No repositories found for this category.</p>';
>>>>>>> Stashed changes
            return;
        }

        repos.forEach(repo => {
            const li = document.createElement('li');
            li.className = 'project-item';
<<<<<<< Updated upstream
            
            const description = repo.description || 'No description available.';
            const language = repo.language ? `<span class="tech-tag">${repo.language}</span>` : '';
            const stars = repo.stargazers_count > 0 ? ` • ⭐ ${repo.stargazers_count}` : '';
            
=======

            // Smart Categorization / Tech Stack
            const language = repo.language || 'Research';
            const stars = repo.stargazers_count > 0 ? ` • ⭐ ${repo.stargazers_count}` : '';
            const description = repo.description || 'A specialized research implementation.';

>>>>>>> Stashed changes
            li.innerHTML = `
                <h3 class="project-title">
                    <a href="${repo.html_url}" target="_blank">${formatTitle(repo.name)}</a>
                </h3>
                <div class="project-meta">
<<<<<<< Updated upstream
                    ${language}${stars} • Updated: ${new Date(repo.updated_at).toLocaleDateString()}
                </div>
                <p class="project-description">${description}</p>
            `;
            
            repoContainer.appendChild(li);
        });
    }

=======
                    <span class="tech-tag">${language}</span>${stars}
                </div>
                <p class="project-description">${description}</p>
                <button class="view-details-btn" data-repo="${repo.name}">
                    View Details <i class="fas fa-arrow-right"></i>
                </button>
            `;

            repoContainer.appendChild(li);
        });

        // Attach Event Listeners to new buttons
        document.querySelectorAll('.view-details-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const repoName = e.target.closest('button').dataset.repo;
                openReadmeModal(repoName);
            });
        });
    }

    // --- Smart Filtering Logic ---
    function filterRepos(category) {
        if (category === 'all') {
            renderRepos(allRepos);
            return;
        }

        const filtered = allRepos.filter(repo => {
            const lang = (repo.language || '').toLowerCase();
            const topics = (repo.topics || []).join(' ').toLowerCase();
            const name = repo.name.toLowerCase();
            const desc = (repo.description || '').toLowerCase();

            const text = `${lang} ${topics} ${name} ${desc}`;

            if (category === 'ai') {
                return text.includes('python') || text.includes('learning') || text.includes('data') || text.includes('ai') || text.includes('neural') || text.includes('tensorflow') || text.includes('keras') || text.includes('pandas');
            } else if (category === 'web') {
                return text.includes('javascript') || text.includes('html') || text.includes('css') || text.includes('react') || text.includes('web') || text.includes('node') || text.includes('frontend');
            } else if (category === 'research') {
                // Research is the fallback for anything that isn't clearly web, or explicitly tagged research
                return text.includes('research') || text.includes('paper') || (!text.includes('javascript') && !text.includes('css') && !text.includes('html'));
            }
            return true;
        });

        renderRepos(filtered);
    }

    // --- Deep Doc Engine (README Fetcher) ---
    async function openReadmeModal(repoName) {
        modal.classList.add('active');
        modalBody.innerHTML = '<div style="text-align:center; padding: 2rem;">Loading documentation...</div>';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling

        try {
            // Fetch README from GitHub API
            const response = await fetch(`https://api.github.com/repos/${username}/${repoName}/readme`);
            if (!response.ok) throw new Error('README not found');

            const data = await response.json();
            // Decode Base64 content
            const rawMarkdown = atob(data.content);

            // Parse and Sanitize
            const htmlContent = DOMPurify.sanitize(marked.parse(rawMarkdown));

            modalBody.innerHTML = htmlContent;

            // Apply Syntax Highlighting
            modalBody.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });

        } catch (error) {
            console.error('Error fetching README:', error);
            modalBody.innerHTML = `
                <div style="text-align:center; padding: 2rem;">
                    <h3>Documentation Unavailable</h3>
                    <p>Could not load README.md for this repository.</p>
                    <a href="https://github.com/${username}/${repoName}" target="_blank" style="color: var(--accent-color)">View on GitHub &rarr;</a>
                </div>
            `;
        }
    }

    // --- Event Listeners ---

    // Filter Buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update UI
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Filter Data
            filterRepos(btn.dataset.filter);
        });
    });

    // Modal Close
    closeModal.addEventListener('click', () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    });

    // Close modal on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Helpers
>>>>>>> Stashed changes
    function formatTitle(str) {
        return str.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

<<<<<<< Updated upstream
=======
    // Init
>>>>>>> Stashed changes
    fetchRepos();
});
