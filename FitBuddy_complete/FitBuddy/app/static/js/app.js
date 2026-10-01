const $ = (id) => document.getElementById(id);
let currentPlanId = null;

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setMessage(text, error = false) {
  const el = $("formMessage");
  el.textContent = text;
  el.className = error ? "message error" : "message";
}

function renderPlan(data) {
  currentPlanId = data.id;
  const plan = data.plan;

  const days = plan.days.map(day => {
    const exercises = day.exercises.length
      ? day.exercises.map(ex => `
        <div class="exercise">
          <div>
            <strong>${escapeHtml(ex.name)}</strong>
            <small>${escapeHtml(ex.notes)}</small>
          </div>
          <div class="exercise-meta">${escapeHtml(ex.sets)} × ${escapeHtml(ex.reps)}<br>${escapeHtml(ex.rest_seconds)}s rest</div>
        </div>`).join("")
      : `<div class="recovery">No structured workout today. Keep activity light and recover.</div>`;

    return `
      <article class="day">
        <div class="day-head">
          <strong>${escapeHtml(day.day)} · ${escapeHtml(day.focus)}</strong>
          <span>${escapeHtml(day.duration_minutes)} min</span>
        </div>
        ${exercises}
        <div class="recovery"><strong>Recovery:</strong> ${escapeHtml(day.recovery)}</div>
      </article>`;
  }).join("");

  $("results").innerHTML = `
    <div class="plan-header">
      <span class="badge">${escapeHtml(data.source)}</span>
      <span class="badge">${escapeHtml(data.intensity)} intensity</span>
      <h2 style="margin-top:12px">${escapeHtml(plan.title)}</h2>
      <p>${escapeHtml(plan.summary)}</p>
    </div>
    ${days}
    <div class="tip"><strong>Nutrition / recovery tip:</strong><br>${escapeHtml(data.tip)}</div>
    <div class="feedback">
      <h3>Refine this plan</h3>
      <p style="color:var(--muted);font-size:13px">Tell FitBuddy what you want changed, for example: “more focus on cardio” or “include more rest days.”</p>
      <textarea id="feedback" placeholder="What would you like to change?"></textarea>
      <button class="secondary" onclick="submitFeedback()">Regenerate with feedback</button>
    </div>
  `;
}

async function createPlan(event) {
  event.preventDefault();
  setMessage("Generating your plan...");
  const payload = {
    name: $("name").value,
    age: Number($("age").value),
    weight_kg: Number($("weight_kg").value),
    goal: $("goal").value,
    intensity: $("intensity").value,
    experience: $("experience").value,
    equipment: $("equipment").value
  };

  try {
    const response = await fetch("/api/plans", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not create plan.");
    renderPlan(data);
    setMessage(`Plan #${data.id} saved.`);
    loadHistory();
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function submitFeedback() {
  const feedback = $("feedback").value.trim();
  if (!feedback || !currentPlanId) return;

  setMessage("Updating your plan...");
  try {
    const response = await fetch(`/api/plans/${currentPlanId}/feedback`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({feedback})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Could not update plan.");
    renderPlan(data);
    setMessage("Plan updated with your feedback.");
    loadHistory();
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function loadHistory() {
  const container = $("history");
  try {
    const response = await fetch("/api/plans?limit=10");
    const plans = await response.json();
    if (!plans.length) {
      container.innerHTML = `<p style="color:var(--muted)">No saved plans yet.</p>`;
      return;
    }
    container.innerHTML = plans.map(p => `
      <div class="history-item">
        <div>
          <strong>${escapeHtml(p.name)} — ${escapeHtml(p.goal)}</strong>
          <small>Plan #${p.id} · ${escapeHtml(p.source)} · ${new Date(p.updated_at).toLocaleString()}</small>
        </div>
        <button class="secondary" onclick="loadPlan(${p.id})">Open</button>
      </div>
    `).join("");
  } catch {
    container.textContent = "Could not load history.";
  }
}

async function loadPlan(id) {
  const response = await fetch(`/api/plans/${id}`);
  const data = await response.json();
  if (!response.ok) {
    setMessage(data.detail || "Could not load plan.", true);
    return;
  }
  renderPlan(data);
  window.scrollTo({top: 100, behavior: "smooth"});
}

$("planForm").addEventListener("submit", createPlan);
$("refreshHistory").addEventListener("click", loadHistory);
loadHistory();
