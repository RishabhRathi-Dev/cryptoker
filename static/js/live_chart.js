document.addEventListener('DOMContentLoaded', function() {
    // Create the initial empty chart
    let chart;

    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: currencyData.map(entry => entry.currency),
            datasets: [{
                label: 'Price',
                data: currencyData.map(entry => entry.price),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                borderRadius: 5,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'category', // Use 'category' type for the x-axis to display cryptocurrency names
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Function to update the chart data with live data
    const updateChartData = async () => {
        try {
            // Fetch live data for selected cryptocurrencies from the Binance API
            const base_url = "https://api.binance.com/api/v3/ticker/price?symbol=";
            for (const currency of selectedCryptos) {
                const response = await fetch(base_url + currency);
                const data = await response.json();
                const updatedCurrencyData = { currency, price: parseFloat(data['price']) };

                // Update the currencyData with the latest price
                const index = currencyData.findIndex(entry => entry.currency === currency);
                if (index !== -1) {
                    currencyData[index] = updatedCurrencyData;
                }
            }

            // Update the chart with new data
            chart.data.labels = currencyData.map(entry => entry.currency);
            chart.data.datasets[0].data = currencyData.map(entry => entry.price);
            chart.update();
        } catch (error) {
            console.error('Error fetching or updating cryptocurrency data:', error);
        }
    };

    // Call the updateChartData function every 10 seconds (10000 milliseconds) for live updates
    setInterval(updateChartData, 10000);

    // Handle form submission to save preferences
    const cryptoForm = document.getElementById('cryptoForm');
    cryptoForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(cryptoForm);
        const selectedCryptos = [];
        for (const entry of formData.entries()) {
            if (entry[0] === 'cryptos') {
                selectedCryptos.push(entry[1]);
            }
        }

        // Save the selected cryptocurrencies in the server-side database
        try {
            const response = await fetch('/save_cryptos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ selectedCryptos })
            });
            const data = await response.json();
            if (data.success) {
                console.log('Cryptocurrency preferences saved successfully!');
                location.reload();
            } else {
                console.error('Failed to save cryptocurrency preferences.');
            }
        } catch (error) {
            console.error('Error saving cryptocurrency preferences:', error);
        }
    });
});
