// Fetch unique values from backend API endpoints
async function fetchOptions() {
    const response = await fetch('/api/options'); // backend route to return commodities, markets, states
    const data = await response.json();

    return data; // { commodities: [...], markets: [...], states: [...] }
}

function populateSelect(selectElement, options) {
    selectElement.innerHTML = '<option value="all">All</option>'; // reset
    options.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.toLowerCase();
        el.textContent = opt;
        selectElement.appendChild(el);
    });
}

async function initFilters() {
    const { commodities, markets, states } = await fetchOptions();

    populateSelect(document.getElementById('commoditySelect'), commodities);
    populateSelect(document.getElementById('marketSelect'), markets);
    populateSelect(document.getElementById('stateSelect'), states);
}

initFilters();

// Update iframe src on filter
document.getElementById('applyFilters').addEventListener('click', () => {
    const commodity = document.getElementById('commoditySelect').value;
    const market = document.getElementById('marketSelect').value;
    const state = document.getElementById('stateSelect').value;

    const params = `?commodity=${commodity}&market=${market}&state=${state}`;

    document.getElementById('commodityBar').src = "visualizations/commodity_bar.html" + params;
    document.getElementById('marketPie').src = "visualizations/market_pie.html" + params;
    document.getElementById('topCommodityLine').src = "visualizations/top_commodity_line.html" + params;
    document.getElementById('top10Commodities').src = "visualizations/top10_commodities.html" + params;
    document.getElementById('stateMap').src = "visualizations/state_map.html" + params;
    document.getElementById('heatmap').src = "visualizations/market_commodity_heatmap.html" + params;
});
