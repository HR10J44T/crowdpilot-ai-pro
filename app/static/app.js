async function postJSON(url, body = {}) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  return res.json();
}

const simulateBtn = document.getElementById('simulate-btn');
if (simulateBtn) {
  simulateBtn.addEventListener('click', async () => {
    simulateBtn.disabled = true;
    simulateBtn.textContent = 'Refreshing...';
    try {
      await postJSON('/api/simulate', {});
      window.location.reload();
    } catch (e) {
      console.error(e);
      simulateBtn.textContent = 'Try again';
      simulateBtn.disabled = false;
    }
  });
}

const alertForm = document.getElementById('alert-form');
if (alertForm) {
  alertForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(alertForm);
    await postJSON('/api/alerts', Object.fromEntries(formData.entries()));
    window.location.reload();
  });
}
