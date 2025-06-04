// AxiomTradeAPI Documentation JavaScript
// Interactive features and enhancements for GitHub Pages

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavigation();
    initializeCodeHighlighting();
    initializeScrollEffects();
    initializeAnalytics();
    initializeCopyToClipboard();
    initializeSearch();
    initializeThemeToggle();
    initializeFeedback();
    initializeProgressIndicator();
    initializeTableOfContents();
    initializeLazyLoading();
});

// Navigation functionality with enhanced mobile support
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    const currentPath = window.location.pathname;
    
    // Highlight active navigation item
    [...navLinks, ...sidebarLinks].forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath || (linkPath !== '/' && currentPath.includes(linkPath))) {
            link.classList.add('active');
        }
    });
    
    // Mobile menu toggle with animation
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.setAttribute('aria-expanded', mobileMenu.classList.contains('active'));
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                mobileMenu.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // Enhanced smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed header
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Update URL without jumping
                history.pushState(null, null, this.getAttribute('href'));
            }
        });
    });
    
    // Keyboard navigation support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('active')) {
            mobileMenu.classList.remove('active');
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
        }
    });
}

// Dark/Light theme toggle
function initializeThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Get saved theme or default to system preference
    let currentTheme = localStorage.getItem('theme');
    if (!currentTheme) {
        currentTheme = prefersDark.matches ? 'dark' : 'light';
    }
    
    // Apply theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            currentTheme = newTheme;
            
            // Update toggle icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        });
    }
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            currentTheme = newTheme;
        }
    });
}

// Reading progress indicator
function initializeProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.innerHTML = '<div class="progress-fill"></div>';
    document.body.appendChild(progressBar);
    
    const progressFill = progressBar.querySelector('.progress-fill');
    
    function updateProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        progressFill.style.width = Math.min(scrollPercent, 100) + '%';
    }
    
    window.addEventListener('scroll', updateProgress);
    updateProgress(); // Initial call
}

// Enhanced Table of Contents with active section highlighting
function initializeTableOfContents() {
    const tocLinks = document.querySelectorAll('.toc-link');
    const headings = document.querySelectorAll('h2, h3, h4, h5, h6');
    
    if (tocLinks.length === 0 || headings.length === 0) return;
    
    let activeHeading = null;
    
    function updateActiveTocLink() {
        let current = null;
        
        headings.forEach(heading => {
            const rect = heading.getBoundingClientRect();
            if (rect.top <= 100) {
                current = heading;
            }
        });
        
        if (current !== activeHeading) {
            // Remove active class from all links
            tocLinks.forEach(link => link.classList.remove('active'));
            
            // Add active class to current link
            if (current) {
                const activeLink = document.querySelector(`.toc-link[href="#${current.id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
            
            activeHeading = current;
        }
    }
    
    window.addEventListener('scroll', updateProgress);
    updateActiveTocLink(); // Initial call
}

// Lazy loading for images and content
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
        
        // Lazy load code blocks for better performance
        const codeObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const codeBlock = entry.target;
                    if (window.Prism) {
                        Prism.highlightElement(codeBlock.querySelector('code'));
                    }
                    observer.unobserve(codeBlock);
                }
            });
        });
        
        document.querySelectorAll('.code-block').forEach(block => {
            codeObserver.observe(block);
        });
    }
}

// Code syntax highlighting and copy functionality
function initializeCodeHighlighting() {
    // Add copy buttons to code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const pre = block.parentElement;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-btn';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'Copy to clipboard';
        
        // Position button
        pre.style.position = 'relative';
        copyButton.style.position = 'absolute';
        copyButton.style.top = '0.5rem';
        copyButton.style.right = '0.5rem';
        copyButton.style.background = 'rgba(255, 255, 255, 0.1)';
        copyButton.style.border = 'none';
        copyButton.style.color = 'white';
        copyButton.style.padding = '0.5rem';
        copyButton.style.borderRadius = '0.25rem';
        copyButton.style.cursor = 'pointer';
        copyButton.style.opacity = '0.7';
        copyButton.style.transition = 'opacity 0.2s';
        
        copyButton.addEventListener('mouseenter', () => {
            copyButton.style.opacity = '1';
        });
        
        copyButton.addEventListener('mouseleave', () => {
            copyButton.style.opacity = '0.7';
        });
        
        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent).then(() => {
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                copyButton.style.color = '#10b981';
                
                setTimeout(() => {
                    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                    copyButton.style.color = 'white';
                }, 2000);
            });
        });
        
        pre.appendChild(copyButton);
    });
}

// Copy to clipboard functionality
function initializeCopyToClipboard() {
    // Add copy functionality to installation commands
    const installCommands = document.querySelectorAll('.install-command');
    
    installCommands.forEach(command => {
        command.addEventListener('click', function() {
            const text = this.textContent.trim();
            navigator.clipboard.writeText(text).then(() => {
                // Show feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                this.style.color = '#10b981';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.color = '';
                }, 2000);
            });
        });
    });
}

// Scroll effects and animations
function initializeScrollEffects() {
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Fade in animations on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe feature cards and strategy cards
    document.querySelectorAll('.feature-card, .strategy-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Add CSS for fade-in effect
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
    
    // Stagger animation for grid items
    const grids = document.querySelectorAll('.features-grid, .strategies-grid');
    grids.forEach(grid => {
        const items = grid.querySelectorAll('.feature-card, .strategy-card');
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
        });
    });
}

// Analytics and tracking
function initializeAnalytics() {
    // Track button clicks
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            const href = this.getAttribute('href');
            
            // Track with Google Analytics if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'click', {
                    event_category: 'Button',
                    event_label: buttonText,
                    value: href
                });
            }
            
            // Track chipa.tech link clicks
            if (href && href.includes('chipa.tech')) {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        event_category: 'External Link',
                        event_label: 'chipa.tech',
                        value: href
                    });
                }
            }
        });
    });
    
    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', () => {
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent > maxScroll && scrollPercent % 25 === 0) {
            maxScroll = scrollPercent;
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'scroll', {
                    event_category: 'Engagement',
                    event_label: `${scrollPercent}%`,
                    value: scrollPercent
                });
            }
        }
    });
    
    // Track time on page
    const startTime = Date.now();
    
    window.addEventListener('beforeunload', () => {
        const timeOnPage = Math.round((Date.now() - startTime) / 1000);
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'timing_complete', {
                name: 'page_view_duration',
                value: timeOnPage
            });
        }
    });
}

// Enhanced feedback system
function initializeFeedback() {
    const feedbackButtons = document.querySelectorAll('.feedback-btn');
    
    feedbackButtons.forEach(button => {
        button.addEventListener('click', function() {
            const type = this.classList.contains('positive') ? 'positive' : 'negative';
            const page = window.location.pathname;
            
            // Send feedback to analytics (if available)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'feedback', {
                    'feedback_type': type,
                    'page_path': page
                });
            }
            
            // Show thank you message
            const feedbackCard = this.closest('.feedback-card');
            const message = type === 'positive' 
                ? 'Thank you for your feedback! 🎉' 
                : 'Thank you! We\'ll work on improving this content. 💪';
            
            feedbackCard.innerHTML = `
                <div class="feedback-success">
                    <i class="fas fa-check-circle"></i>
                    <p>${message}</p>
                </div>
            `;
            
            // Optional: Show additional feedback form for negative feedback
            if (type === 'negative') {
                setTimeout(() => {
                    const additionalFeedback = document.createElement('div');
                    additionalFeedback.className = 'additional-feedback';
                    additionalFeedback.innerHTML = `
                        <p>Help us improve by telling us what went wrong:</p>
                        <textarea placeholder="What could we do better?" class="feedback-textarea"></textarea>
                        <button class="btn btn-sm btn-primary" onclick="submitDetailedFeedback()">Send Feedback</button>
                    `;
                    feedbackCard.appendChild(additionalFeedback);
                }, 2000);
            }
        });
    });
}

// Submit detailed feedback
window.submitDetailedFeedback = function() {
    const textarea = document.querySelector('.feedback-textarea');
    const feedback = textarea.value.trim();
    
    if (feedback) {
        // In a real implementation, this would send to your backend
        console.log('Detailed feedback:', feedback);
        
        // Send to analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'detailed_feedback', {
                'feedback_text': feedback,
                'page_path': window.location.pathname
            });
        }
        
        // Show success message
        const additionalFeedback = document.querySelector('.additional-feedback');
        additionalFeedback.innerHTML = `
            <div class="feedback-success">
                <i class="fas fa-check-circle"></i>
                <p>Thank you for the detailed feedback! We really appreciate it.</p>
            </div>
        `;
    }
};

// Advanced search functionality
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    const searchOverlay = document.querySelector('.search-overlay');
    
    if (!searchInput) return;
    
    let searchIndex = [];
    let searchTimeout;
    
    // Build search index from page content
    function buildSearchIndex() {
        const content = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, .api-description, .feature-description');
        searchIndex = [];
        
        content.forEach((element, index) => {
            const text = element.textContent.trim();
            const heading = element.closest('section')?.querySelector('h1, h2, h3')?.textContent || '';
            
            if (text.length > 10) {
                searchIndex.push({
                    id: index,
                    text: text,
                    heading: heading,
                    element: element,
                    url: window.location.pathname + '#' + (element.id || 'section-' + index)
                });
            }
        });
    }
    
    // Perform search
    function performSearch(query) {
        if (!query || query.length < 2) {
            return [];
        }
        
        const results = searchIndex
            .filter(item => 
                item.text.toLowerCase().includes(query.toLowerCase()) ||
                item.heading.toLowerCase().includes(query.toLowerCase())
            )
            .slice(0, 10)
            .map(item => ({
                ...item,
                relevance: calculateRelevance(item, query)
            }))
            .sort((a, b) => b.relevance - a.relevance);
        
        return results;
    }
    
    // Calculate search relevance score
    function calculateRelevance(item, query) {
        const queryLower = query.toLowerCase();
        const textLower = item.text.toLowerCase();
        const headingLower = item.heading.toLowerCase();
        
        let score = 0;
        
        // Exact matches in heading get highest score
        if (headingLower.includes(queryLower)) score += 10;
        
        // Exact matches in text
        if (textLower.includes(queryLower)) score += 5;
        
        // Word boundary matches
        const words = queryLower.split(' ');
        words.forEach(word => {
            if (new RegExp('\\b' + word + '\\b').test(textLower)) score += 3;
            if (new RegExp('\\b' + word + '\\b').test(headingLower)) score += 6;
        });
        
        return score;
    }
    
    // Display search results
    function displaySearchResults(results) {
        if (!searchResults) return;
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No results found</div>';
            return;
        }
        
        const resultsHTML = results.map(result => `
            <div class="search-result-item" onclick="scrollToResult('${result.element.id || 'section-' + result.id}')">
                <h4>${result.heading}</h4>
                <p>${highlightSearchTerm(result.text.substring(0, 150) + '...', searchInput.value)}</p>
            </div>
        `).join('');
        
        searchResults.innerHTML = resultsHTML;
    }
    
    // Highlight search terms in text
    function highlightSearchTerm(text, term) {
        const regex = new RegExp(`(${term})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    // Scroll to search result
    window.scrollToResult = function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            element.classList.add('highlight');
            setTimeout(() => element.classList.remove('highlight'), 2000);
        }
        
        // Close search overlay
        if (searchOverlay) {
            searchOverlay.classList.remove('active');
        }
    };
    
    // Search input event listeners
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        searchTimeout = setTimeout(() => {
            if (query.length >= 2) {
                const results = performSearch(query);
                displaySearchResults(results);
                
                if (searchOverlay) {
                    searchOverlay.classList.add('active');
                }
            } else {
                if (searchOverlay) {
                    searchOverlay.classList.remove('active');
                }
            }
        }, 300);
    });
    
    // Close search on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('active')) {
            searchOverlay.classList.remove('active');
            searchInput.value = '';
        }
    });
    
    // Initialize search index
    buildSearchIndex();
}

// Performance monitoring
function initializePerformanceMonitoring() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                
                // Send performance data to analytics
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'page_load_time', {
                        'load_time': loadTime,
                        'page_path': window.location.pathname
                    });
                }
                
                // Show performance warning if slow
                if (loadTime > 3000) {
                    console.warn('Page load time is slow:', loadTime + 'ms');
                }
            }, 1000);
        });
    }
}

// Initialize performance monitoring
initializePerformanceMonitoring();

// Service Worker registration for offline support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Notification system for updates
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, duration);
}

// Export functions for external use
window.AxiomDocs = {
    showNotification,
    scrollToResult: window.scrollToResult,
    submitDetailedFeedback: window.submitDetailedFeedback
};
