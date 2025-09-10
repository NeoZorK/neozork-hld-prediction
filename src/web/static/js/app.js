// NeoZork Pocket Hedge Fund - Web Interface
class PocketHedgeFundApp {
    constructor() {
        this.apiBase = 'http://localhost:8080/api/v1';
        this.token = localStorage.getItem('auth_token');
        this.currentUser = null;
        this.performanceChart = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuth();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.showSection(link.getAttribute('href').substring(1));
            });
        });

        // Hamburger menu
        document.getElementById('hamburger').addEventListener('click', () => {
            document.getElementById('nav-menu').classList.toggle('active');
            document.getElementById('hamburger').classList.toggle('active');
        });

        // Login form
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });

        // Modal controls
        document.getElementById('close-login').addEventListener('click', () => {
            this.hideModal('login-modal');
        });

        document.getElementById('close-register').addEventListener('click', () => {
            this.hideModal('register-modal');
        });

        document.getElementById('show-register').addEventListener('click', (e) => {
            e.preventDefault();
            this.hideModal('login-modal');
            this.showModal('register-modal');
        });

        document.getElementById('show-login').addEventListener('click', (e) => {
            e.preventDefault();
            this.hideModal('register-modal');
            this.showModal('login-modal');
        });

        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.handleLogout();
        });

        // Refresh buttons
        document.getElementById('refresh-investments').addEventListener('click', () => {
            this.loadInvestments();
        });

        document.getElementById('refresh-portfolio').addEventListener('click', () => {
            this.loadPortfolio();
        });

        document.getElementById('refresh-analytics').addEventListener('click', () => {
            this.loadAnalytics();
        });

        // Close modals on outside click
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideModal(e.target.id);
            }
        });
    }

    checkAuth() {
        if (this.token) {
            this.loadUserData();
            this.hideModal('login-modal');
            this.hideModal('register-modal');
        } else {
            this.showModal('login-modal');
        }
    }

    async loadUserData() {
        try {
            const response = await this.apiCall('/auth/verify', 'POST', {
                token: this.token
            });
            
            if (response.success) {
                this.currentUser = response.user;
                this.loadDashboard();
            } else {
                this.handleLogout();
            }
        } catch (error) {
            console.error('Failed to load user data:', error);
            this.handleLogout();
        }
    }

    async handleLogin() {
        const form = document.getElementById('login-form');
        const formData = new FormData(form);
        
        const loginData = {
            email: formData.get('email'),
            password: formData.get('password')
        };

        try {
            this.showLoading();
            const response = await this.apiCall('/auth/login', 'POST', loginData);
            
            this.token = response.access_token;
            localStorage.setItem('auth_token', this.token);
            this.currentUser = response.user;
            
            this.hideModal('login-modal');
            this.loadDashboard();
            this.showToast('Login successful!', 'success');
            
        } catch (error) {
            this.showToast('Login failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async handleRegister() {
        const form = document.getElementById('register-form');
        const formData = new FormData(form);
        
        const registerData = {
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name'),
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        };

        try {
            this.showLoading();
            const response = await this.apiCall('/auth/register', 'POST', registerData);
            
            this.showToast('Registration successful! Please login.', 'success');
            this.hideModal('register-modal');
            this.showModal('login-modal');
            
        } catch (error) {
            this.showToast('Registration failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    handleLogout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('auth_token');
        this.showModal('login-modal');
        this.showToast('Logged out successfully', 'info');
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        document.getElementById(sectionId).classList.add('active');

        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[href="#${sectionId}"]`).classList.add('active');

        // Load section data
        switch(sectionId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'portfolio':
                this.loadPortfolio();
                break;
            case 'funds':
                this.loadFunds();
                break;
            case 'analytics':
                this.loadAnalytics();
                break;
            case 'profile':
                this.loadProfile();
                break;
        }
    }

    async loadDashboard() {
        try {
            const [portfolioData, investmentsData] = await Promise.all([
                this.apiCall('/returns/portfolio', 'GET'),
                this.apiCall('/investments', 'GET')
            ]);

            this.updateDashboardStats(portfolioData);
            this.updateInvestmentsTable(investmentsData);

        } catch (error) {
            console.error('Failed to load dashboard:', error);
            this.showToast('Failed to load dashboard data', 'error');
        }
    }

    updateDashboardStats(portfolioData) {
        document.getElementById('total-invested').textContent = 
            this.formatCurrency(portfolioData.total_invested);
        document.getElementById('current-value').textContent = 
            this.formatCurrency(portfolioData.total_current_value);
        document.getElementById('total-return').textContent = 
            this.formatCurrency(portfolioData.total_return);
        document.getElementById('return-percentage').textContent = 
            this.formatPercentage(portfolioData.total_return_percentage);
    }

    updateInvestmentsTable(investmentsData) {
        const tbody = document.getElementById('investments-table');
        
        if (investmentsData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No investments found</td></tr>';
            return;
        }

        tbody.innerHTML = investmentsData.map(investment => `
            <tr>
                <td>${investment.fund_name || 'Unknown Fund'}</td>
                <td>${this.formatCurrency(investment.amount)}</td>
                <td>${this.formatCurrency(investment.current_value)}</td>
                <td class="${investment.total_return >= 0 ? 'text-success' : 'text-danger'}">
                    ${this.formatCurrency(investment.total_return)} (${this.formatPercentage(investment.total_return_percentage)})
                </td>
                <td>
                    <span class="badge ${investment.status === 'active' ? 'bg-success' : 'bg-warning'}">
                        ${investment.status}
                    </span>
                </td>
            </tr>
        `).join('');
    }

    async loadPortfolio() {
        try {
            const [portfolioData, allocationsData] = await Promise.all([
                this.apiCall('/returns/portfolio', 'GET'),
                this.apiCall('/portfolio/allocations', 'GET')
            ]);

            this.updatePortfolioSummary(portfolioData);
            this.updateAllocations(allocationsData);

        } catch (error) {
            console.error('Failed to load portfolio:', error);
            this.showToast('Failed to load portfolio data', 'error');
        }
    }

    updatePortfolioSummary(portfolioData) {
        const summaryContainer = document.getElementById('portfolio-summary');
        
        summaryContainer.innerHTML = `
            <div class="portfolio-metric">
                <h3>Total Invested</h3>
                <div class="value">${this.formatCurrency(portfolioData.total_invested)}</div>
            </div>
            <div class="portfolio-metric">
                <h3>Current Value</h3>
                <div class="value">${this.formatCurrency(portfolioData.total_current_value)}</div>
            </div>
            <div class="portfolio-metric">
                <h3>Total Return</h3>
                <div class="value ${portfolioData.total_return >= 0 ? 'text-success' : 'text-danger'}">
                    ${this.formatCurrency(portfolioData.total_return)}
                </div>
            </div>
            <div class="portfolio-metric">
                <h3>Return %</h3>
                <div class="value ${portfolioData.total_return_percentage >= 0 ? 'text-success' : 'text-danger'}">
                    ${this.formatPercentage(portfolioData.total_return_percentage)}
                </div>
            </div>
        `;
    }

    updateAllocations(allocationsData) {
        const container = document.getElementById('allocations-container');
        
        if (allocationsData.length === 0) {
            container.innerHTML = '<div class="loading">No allocations found</div>';
            return;
        }

        container.innerHTML = allocationsData.map(allocation => `
            <div class="allocation-item">
                <h3>${allocation.fund_name}</h3>
                <div class="allocation-details">
                    <div class="allocation-detail">
                        <div class="label">Allocation</div>
                        <div class="value">${this.formatPercentage(allocation.allocation_percentage)}</div>
                    </div>
                    <div class="allocation-detail">
                        <div class="label">Value</div>
                        <div class="value">${this.formatCurrency(allocation.current_value)}</div>
                    </div>
                    <div class="allocation-detail">
                        <div class="label">Return</div>
                        <div class="value ${allocation.return_percentage >= 0 ? 'text-success' : 'text-danger'}">
                            ${this.formatPercentage(allocation.return_percentage)}
                        </div>
                    </div>
                    <div class="allocation-detail">
                        <div class="label">Shares</div>
                        <div class="value">${this.formatNumber(allocation.total_shares)}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async loadFunds() {
        try {
            const fundsData = await this.apiCall('/funds', 'GET');
            this.updateFundsGrid(fundsData);

        } catch (error) {
            console.error('Failed to load funds:', error);
            this.showToast('Failed to load funds data', 'error');
        }
    }

    updateFundsGrid(fundsData) {
        const container = document.getElementById('funds-grid');
        
        if (fundsData.length === 0) {
            container.innerHTML = '<div class="loading">No funds available</div>';
            return;
        }

        container.innerHTML = fundsData.map(fund => `
            <div class="fund-card">
                <div class="fund-header">
                    <div class="fund-name">${fund.name}</div>
                    <div class="fund-type">${fund.fund_type}</div>
                </div>
                <div class="fund-metrics">
                    <div class="fund-metric">
                        <div class="label">Current Value</div>
                        <div class="value">${this.formatCurrency(fund.current_value)}</div>
                    </div>
                    <div class="fund-metric">
                        <div class="label">Initial Capital</div>
                        <div class="value">${this.formatCurrency(fund.initial_capital)}</div>
                    </div>
                    <div class="fund-metric">
                        <div class="label">Return %</div>
                        <div class="value ${fund.total_return_percentage >= 0 ? 'text-success' : 'text-danger'}">
                            ${this.formatPercentage(fund.total_return_percentage)}
                        </div>
                    </div>
                    <div class="fund-metric">
                        <div class="label">Status</div>
                        <div class="value">${fund.status}</div>
                    </div>
                </div>
                <div class="fund-actions">
                    <button class="btn-invest" onclick="app.investInFund('${fund.id}')">
                        Invest Now
                    </button>
                </div>
            </div>
        `).join('');
    }

    async loadAnalytics() {
        try {
            const [riskMetricsData, portfolioData] = await Promise.all([
                this.apiCall('/returns/risk-metrics', 'GET'),
                this.apiCall('/returns/portfolio', 'GET')
            ]);

            this.updateRiskMetrics(riskMetricsData);
            this.updatePerformanceChart(portfolioData);

        } catch (error) {
            console.error('Failed to load analytics:', error);
            this.showToast('Failed to load analytics data', 'error');
        }
    }

    updateRiskMetrics(riskMetricsData) {
        const container = document.getElementById('risk-metrics');
        const metrics = riskMetricsData.risk_metrics;
        
        container.innerHTML = `
            <div class="metric-item">
                <h3>Volatility</h3>
                <div class="value">${this.formatPercentage(metrics.volatility * 100)}</div>
            </div>
            <div class="metric-item">
                <h3>Sharpe Ratio</h3>
                <div class="value">${this.formatNumber(metrics.sharpe_ratio, 2)}</div>
            </div>
            <div class="metric-item">
                <h3>Max Drawdown</h3>
                <div class="value">${this.formatPercentage(metrics.max_drawdown * 100)}</div>
            </div>
            <div class="metric-item">
                <h3>VaR (95%)</h3>
                <div class="value">${this.formatPercentage(metrics.var_95 * 100)}</div>
            </div>
            <div class="metric-item">
                <h3>Beta</h3>
                <div class="value">${this.formatNumber(metrics.beta, 2)}</div>
            </div>
            <div class="metric-item">
                <h3>Diversification</h3>
                <div class="value">${this.formatPercentage(metrics.diversification_ratio * 100)}</div>
            </div>
        `;
    }

    updatePerformanceChart(portfolioData) {
        const ctx = document.getElementById('performance-chart').getContext('2d');
        
        if (this.performanceChart) {
            this.performanceChart.destroy();
        }

        // Mock data for demonstration
        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        const data = [10000, 10200, 10500, 10300, 10700, portfolioData.total_current_value];

        this.performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Portfolio Value',
                    data: data,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    async loadProfile() {
        try {
            const profileData = await this.apiCall('/users/profile', 'GET');
            this.updateProfile(profileData);

        } catch (error) {
            console.error('Failed to load profile:', error);
            this.showToast('Failed to load profile data', 'error');
        }
    }

    updateProfile(profileData) {
        const container = document.getElementById('profile-info');
        
        container.innerHTML = `
            <div class="profile-item">
                <h3>Username</h3>
                <div class="value">${profileData.username || 'N/A'}</div>
            </div>
            <div class="profile-item">
                <h3>Email</h3>
                <div class="value">${profileData.email || 'N/A'}</div>
            </div>
            <div class="profile-item">
                <h3>First Name</h3>
                <div class="value">${profileData.first_name || 'N/A'}</div>
            </div>
            <div class="profile-item">
                <h3>Last Name</h3>
                <div class="value">${profileData.last_name || 'N/A'}</div>
            </div>
            <div class="profile-item">
                <h3>Member Since</h3>
                <div class="value">${profileData.created_at ? new Date(profileData.created_at).toLocaleDateString() : 'N/A'}</div>
            </div>
            <div class="profile-item">
                <h3>Role</h3>
                <div class="value">${profileData.role || 'Investor'}</div>
            </div>
        `;
    }

    async investInFund(fundId) {
        const amount = prompt('Enter investment amount:');
        if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
            this.showToast('Invalid investment amount', 'error');
            return;
        }

        try {
            this.showLoading();
            const response = await this.apiCall(`/investments`, 'POST', {
                fund_id: fundId,
                amount: parseFloat(amount),
                investment_type: 'lump_sum'
            });

            this.showToast('Investment successful!', 'success');
            this.loadDashboard();
            this.loadPortfolio();

        } catch (error) {
            this.showToast('Investment failed: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        const url = `${this.apiBase}${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (this.token) {
            options.headers['Authorization'] = `Bearer ${this.token}`;
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'API request failed');
        }

        return result;
    }

    showModal(modalId) {
        document.getElementById(modalId).style.display = 'block';
    }

    hideModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    showLoading() {
        document.getElementById('loading-overlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? '✓' : 
                    type === 'error' ? '✗' : 
                    type === 'warning' ? '⚠' : 'ℹ';
        
        toast.innerHTML = `
            <span>${icon}</span>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    formatPercentage(value) {
        return `${value.toFixed(2)}%`;
    }

    formatNumber(value, decimals = 0) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(value);
    }
}

// Initialize the application
const app = new PocketHedgeFundApp();
