document.addEventListener('DOMContentLoaded', () => {
    // FAQ Toggle
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        item.querySelector('.faq-question').addEventListener('click', () => {
            item.classList.toggle('active');
        });
    });

    // Blog Loader (for blog.html)
    const blogGrid = document.querySelector('.blog-grid');
    if (blogGrid) {
        loadBlogPosts();
    }
});

async function loadBlogPosts() {
    try {
        const response = await fetch('blog.json');
        if (!response.ok) throw new Error('Failed to load blog posts');
        const posts = await response.json();

        const blogGrid = document.querySelector('.blog-grid');
        blogGrid.innerHTML = ''; // Clear loading state

        posts.forEach(post => {
            const article = document.createElement('article');
            article.className = 'blog-card';
            article.innerHTML = `
                <div class="blog-img">
                    <i class="fas fa-cube fa-3x"></i> <!-- Placeholder Icon -->
                </div>
                <div class="blog-content">
                    <span class="blog-date">${post.date}</span>
                    <h3><a href="${post.url}">${post.title}</a></h3>
                    <p>${post.excerpt}</p>
                    <a href="${post.url}" class="read-more">Read Article &rarr;</a>
                </div>
            `;
            blogGrid.appendChild(article);
        });
    } catch (error) {
        console.error('Error loading blogs:', error);
        // Optional: specific error handling in UI
    }
}
