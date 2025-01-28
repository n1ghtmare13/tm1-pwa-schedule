const scheduleContainer = document.getElementById('schedule-container');
const substitutionsContainer = document.getElementById('substitutions-container');
const lastUpdateElement = document.getElementById('last-update');

async function fetchData() {
    try {
        const [scheduleResponse, substitutionsResponse] = await Promise.all([
            fetch('schedule.html'),
            fetch('substitutions.html')
        ]);

        const scheduleHTML = await scheduleResponse.text();
        const substitutionsHTML = await substitutionsResponse.text();

        scheduleContainer.innerHTML = '<h2>Plan Lekcji</h2>' + scheduleHTML;
        substitutionsContainer.innerHTML = '<h2>Zastępstwa</h2>' + substitutionsHTML;

        const now = new Date();
        const lastUpdate = now.toLocaleString();
        lastUpdateElement.textContent = `Ostatnia aktualizacja: ${lastUpdate}`;

        localStorage.setItem('lastSchedule', scheduleHTML);
        localStorage.setItem('lastSubstitutions', substitutionsHTML);
        localStorage.setItem('lastUpdateTime', lastUpdate);


    } catch (error) {
        console.error("Błąd pobierania danych:", error);
        loadCachedData();
    }
}

function loadCachedData(){
    const cachedSchedule = localStorage.getItem('lastSchedule');
    const cachedSubstitutions = localStorage.getItem('lastSubstitutions');
    const cachedUpdateTime = localStorage.getItem('lastUpdateTime');

    if (cachedSchedule && cachedSubstitutions && cachedUpdateTime) {
        scheduleContainer.innerHTML = '<h2>Plan Lekcji</h2>' + cachedSchedule;
        substitutionsContainer.innerHTML = '<h2>Zastępstwa</h2>' + cachedSubstitutions;
        lastUpdateElement.textContent = `Ostatnia aktualizacja: ${cachedUpdateTime} (Cache)`;
    } else {
        scheduleContainer.innerHTML = "<p>Brak danych w cache.</p>"
    }
}


fetchData();
