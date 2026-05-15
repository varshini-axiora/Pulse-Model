const API_BASE = "http://localhost:8000";

const rawInput = document.getElementById('rawInput');
const generateBtn = document.getElementById('generateBtn');
const statusContainer = document.getElementById('statusContainer');
const resultContainer = document.getElementById('resultContainer');
const questionsList = document.getElementById('questionsList');

let lastGeneratedSurvey = null;

generateBtn.addEventListener('click', async () => {
    const text = rawInput.value.trim();
    if (text.length < 10) {
        alert("Please enter at least 10 characters.");
        return;
    }

    resetUI();
    generateBtn.disabled = true;
    statusContainer.classList.remove('hidden');

    try {
        updateStatus('status-cleaning', 'active');
        
        const response = await fetch(`${API_BASE}/generate-survey`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_text: text })
        });

        if (!response.ok) throw new Error("Failed to generate survey");

        const data = await response.json();
        lastGeneratedSurvey = data;

        // Simulate status updates for better UX (since the real API call is one chunk)
        updateStatus('status-cleaning', 'done');
        updateStatus('status-analyzing', 'active');
        await sleep(800);
        updateStatus('status-analyzing', 'done');
        updateStatus('status-generating', 'active');
        await sleep(800);
        updateStatus('status-generating', 'done');
        updateStatus('status-validating', 'active');
        await sleep(800);
        updateStatus('status-validating', 'done');

        renderSurvey(data);
        
    } catch (err) {
        alert("Error: " + err.message);
        statusContainer.classList.add('hidden');
    } finally {
        generateBtn.disabled = false;
    }
});

function updateStatus(id, state) {
    const el = document.getElementById(id);
    el.classList.remove('active', 'done');
    if (state) el.classList.add(state);
}

function renderSurvey(data) {
    statusContainer.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    
    document.getElementById('surveyTitle').textContent = data.title;
    document.getElementById('surveyDescription').textContent = data.description;
    
    questionsList.innerHTML = '';
    data.questions.forEach((q, i) => {
        const item = document.createElement('div');
        item.className = 'question-item';
        
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {
            optionsHtml = `
                <div class="options-list">
                    ${q.options.map(opt => `<div class="option">${opt}</div>`).join('')}
                </div>
            `;
        }

        item.innerHTML = `
            <span class="question-type">${q.type.replace('_', ' ')}</span>
            <div class="question-text">${i + 1}. ${q.question}</div>
            ${optionsHtml}
        `;
        questionsList.appendChild(item);
    });
}

function resetUI() {
    resultContainer.classList.add('hidden');
    statusContainer.classList.add('hidden');
    document.querySelectorAll('.status-item').forEach(item => {
        item.classList.remove('active', 'done');
    });
}

function copyJSON() {
    if (!lastGeneratedSurvey) return;
    navigator.clipboard.writeText(JSON.stringify(lastGeneratedSurvey, null, 2));
    alert("JSON copied to clipboard!");
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
