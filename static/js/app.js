
document.addEventListener('DOMContentLoaded', async () => {
    let fullData = [];
    let gdpChart, populationTrendChart, populationBarChart;

    async function initialize() {
        fetch('/api/v1/data/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Not authenticated');
                }
                return response.json();
            })
            .then(data => {
                fullData = data;
                populateFilters();

                updateGdpChart(document.getElementById('gdp-year-filter').value, null);
                updatePopulationTrendChart('India');
                updatePopulationBarChart(document.getElementById('population-year-filter').value);

                setupEventListeners();
            })
            .catch(error => {
                console.error("Authentication error:", error);
                window.location.href = '/login/';
            });
    }

    function populateFilters() {
        const years = [...new Set(fullData.map(item => item.year))].sort((a, b) => b - a);
        const countries = [...new Set(fullData.map(item => item.country))].sort();

        const yearSelectors = ['gdp-year-filter', 'population-year-filter'];
        const countrySelectors = ['gdp-country-filter', 'population-country-filter'];

        yearSelectors.forEach(id => {
            const select = document.getElementById(id);
            select.innerHTML = `<option value="">-- Select Year --</option>`;
            years.forEach(year => select.innerHTML += `<option value="${year}">${year}</option>`);
        });

        countrySelectors.forEach(id => {
            const select = document.getElementById(id);
            select.innerHTML = `<option value="">-- Select Country --</option>`;
            countries.forEach(country => select.innerHTML += `<option value="${country}">${country}</option>`);
        });

        document.getElementById('gdp-year-filter').value = "2022";
        document.getElementById('population-country-filter').value = "India";
        document.getElementById('population-year-filter').value = "2022";
    }

    function updateGdpChart(year, country) {
        const titleEl = document.getElementById('gdp-chart-title');
        const ctx = document.getElementById('gdpChart').getContext('2d');
        if (gdpChart) gdpChart.destroy();

        const gdpData = fullData.filter(d => d.series === 'GDP (current US$)');

        if (country) {
            titleEl.textContent = `GDP Trend for ${country} (Last 10 Years)`;
            const countryData = gdpData.filter(d => d.country === country).sort((a, b) => b.year - a.year).slice(0, 10);
            gdpChart = new Chart(ctx, { type: 'bar', data: { labels: countryData.map(d => d.year).reverse(), datasets: [{ label: 'GDP (US$)', data: countryData.map(d => d.value).reverse(), backgroundColor: '#36A2EB' }] }, options: { responsive: true, maintainAspectRatio: false } });
        } else if (year) {
            titleEl.textContent = `Top 10 GDP Share (${year})`;
            const yearData = gdpData.filter(d => d.year == year).sort((a, b) => b.value - a.value).slice(0, 10);
            gdpChart = new Chart(ctx, { type: 'pie', data: { labels: yearData.map(d => d.country), datasets: [{ data: yearData.map(d => d.value), backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#E7E9ED', '#8D5B4C', '#586776'] }] }, options: { responsive: true, maintainAspectRatio: false } });
        }
    }

    function updatePopulationTrendChart(country) {
        const titleEl = document.getElementById('population-trend-title');
        titleEl.textContent = `Population Trend for ${country}`;
        const popData = fullData.filter(d => d.series === 'Population, total' && d.country === country);

        const ctx = document.getElementById('populationTrendChart').getContext('2d');
        if (populationTrendChart) populationTrendChart.destroy();
        populationTrendChart = new Chart(ctx, { type: 'line', data: { labels: popData.map(d => d.year), datasets: [{ label: 'Population', data: popData.map(d => d.value), borderColor: '#FF6384', tension: 0.1 }] }, options: { responsive: true, maintainAspectRatio: false } });
    }

    function updatePopulationBarChart(year) {
        const titleEl = document.getElementById('population-bar-title');
        titleEl.textContent = `Top 10 Most Populous Countries (${year})`;
        const popData = fullData.filter(d => d.series === 'Population, total' && d.year == year).sort((a, b) => b.value - a.value).slice(0, 10);

        const ctx = document.getElementById('populationBarChart').getContext('2d');
        if (populationBarChart) populationBarChart.destroy();
        populationBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: popData.map(d => d.country).reverse(),
                datasets: [{ label: 'Population', data: popData.map(d => d.value).reverse(), backgroundColor: '#9966FF' }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    function setupEventListeners() {
        const gdpYearFilter = document.getElementById('gdp-year-filter');
        const gdpCountryFilter = document.getElementById('gdp-country-filter');
        const popCountryFilter = document.getElementById('population-country-filter');
        const popYearFilter = document.getElementById('population-year-filter');

        gdpYearFilter.addEventListener('change', () => { gdpCountryFilter.value = ""; updateGdpChart(gdpYearFilter.value, null); });
        gdpCountryFilter.addEventListener('change', () => { gdpYearFilter.value = ""; updateGdpChart(null, gdpCountryFilter.value); });
        popCountryFilter.addEventListener('change', () => { updatePopulationTrendChart(popCountryFilter.value); });
        popYearFilter.addEventListener('change', () => { updatePopulationBarChart(popYearFilter.value); });
    }

    initialize();
});