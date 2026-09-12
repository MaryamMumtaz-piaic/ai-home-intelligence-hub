(() => {
  const { apiGet, apiPost, showToast, escapeHtml, titleCase } = HomeHub;

  const STAGES = [
    "Reviewing home profile", "Mapping rooms", "Analyzing space usage",
    "Reviewing organization", "Checking energy opportunities", "Reviewing maintenance",
    "Evaluating safety awareness", "Prioritizing improvements", "Preparing your home intelligence report",
  ];

  let homeId = null;

  function showView(id) {
    ["insights-intro", "progress-view", "error-view", "report-view"].forEach((v) =>
      document.getElementById(v).classList.toggle("hidden", v !== id)
    );
  }

  function renderProgress() {
    const list = document.getElementById("progress-steps");
    list.innerHTML = STAGES.map((s, i) => `<li class="progress-step" data-idx="${i}"><span class="dot"></span><span>${s}</span></li>`).join("");
  }

  function advanceProgress(i) {
    const items = document.querySelectorAll("#progress-steps .progress-step");
    items.forEach((el, idx) => {
      el.classList.toggle("is-active", idx === i);
      el.classList.toggle("is-complete", idx < i);
    });
  }

  async function runAnalysis() {
    const home = await apiGet("/api/home");
    if (!home) {
      document.getElementById("insights-no-home").classList.remove("hidden");
      return;
    }
    homeId = home.id;
    showView("progress-view");
    renderProgress();
    let i = 0;
    const timer = setInterval(() => {
      if (i < STAGES.length - 1) advanceProgress(i++);
    }, 550);
    try {
      const report = await apiPost("/api/ai/analyze-home", { home_id: homeId });
      clearInterval(timer);
      advanceProgress(STAGES.length - 1);
      setTimeout(() => renderReport(report), 300);
    } catch (err) {
      clearInterval(timer);
      showView("error-view");
      document.querySelector("#error-view p").textContent = err.message;
    }
  }

  function scoreColor(score) {
    if (score >= 70) return "text-olive";
    if (score >= 45) return "text-amber";
    return "text-terracotta";
  }

  function renderReport(report) {
    showView("report-view");
    document.getElementById("report-home-name").textContent = report.home_name;
    document.getElementById("report-meta").textContent =
      `${report.room_count} rooms · ${report.furniture_count} furniture · ${report.appliance_count} appliances · ${report.open_task_count} open tasks · ${report.data_completeness_percent}% data complete`;

    const notice = document.getElementById("partial-notice");
    if (report.partial) {
      notice.classList.remove("hidden");
      notice.textContent = "Some sections of this report could not be completed. Showing the available results — try re-analyzing later.";
    } else {
      notice.classList.add("hidden");
    }

    document.getElementById("category-scores").innerHTML = (report.category_scores || []).map((c) => `
      <div class="border border-taupe/60 rounded-xl p-4">
        <p class="text-xs font-mono uppercase text-charcoal/50 mb-1">${escapeHtml(c.label)}</p>
        <p class="font-display text-3xl ${scoreColor(c.score)}">${c.score}</p>
        <p class="text-xs text-charcoal/50 mt-1">AI-generated planning indicator</p>
        <p class="text-xs text-charcoal/60 mt-2">${escapeHtml(c.summary)}</p>
      </div>`).join("");

    document.getElementById("top-actions").innerHTML = (report.top_actions || []).map((t) => `<li class="flex gap-2"><span class="text-terracotta">•</span>${escapeHtml(t)}</li>`).join("") || `<li class="text-charcoal/40">None identified.</li>`;
    document.getElementById("quick-wins").innerHTML = (report.quick_wins || []).map((t) => `<li class="flex gap-2"><span class="text-olive">•</span>${escapeHtml(t)}</li>`).join("") || `<li class="text-charcoal/40">None identified.</li>`;
    document.getElementById("missing-info").innerHTML = (report.missing_information || []).map((t) => `<li class="flex gap-2"><span class="text-amber">•</span>${escapeHtml(t)}</li>`).join("") || `<li class="text-charcoal/40">Nothing missing.</li>`;

    document.getElementById("room-summaries").innerHTML = (report.room_summaries || []).map((r) => `
      <div class="border border-taupe/60 rounded-xl p-5">
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-semibold">${escapeHtml(r.room_name || "Room")}</h3>
          <a href="/rooms/${r.room_id}" class="text-xs text-olive hover:underline">Open →</a>
        </div>
        <p class="text-sm text-charcoal/60 mb-3">${escapeHtml(r.observations)}</p>
        <div class="flex flex-wrap gap-2 text-xs mb-3">
          <span class="bg-stone px-2 py-1 rounded font-mono">Space: ${escapeHtml(r.space_status)}</span>
          <span class="bg-stone px-2 py-1 rounded font-mono">Maintenance: ${escapeHtml(r.maintenance_status)}</span>
          <span class="bg-stone px-2 py-1 rounded font-mono">Organization: ${escapeHtml(r.organization_status)}</span>
        </div>
        ${(r.top_recommendations || []).length ? `<ul class="text-xs text-charcoal/70 space-y-1">${r.top_recommendations.map((t) => `<li>• ${escapeHtml(t)}</li>`).join("")}</ul>` : ""}
      </div>`).join("") || `<p class="text-sm text-charcoal/50">No rooms yet.</p>`;
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("analyze-btn").addEventListener("click", runAnalysis);
    document.getElementById("retry-btn").addEventListener("click", runAnalysis);
    document.getElementById("reanalyze-btn").addEventListener("click", runAnalysis);
    document.getElementById("print-report").addEventListener("click", () => window.print());
  });
})();
