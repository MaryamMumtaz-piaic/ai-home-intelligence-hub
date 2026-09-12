(() => {
  const { apiGet, apiPost, showToast, escapeHtml, titleCase } = HomeHub;

  let homeId = null;
  let all = [];

  const priorityColor = { urgent_attention: "bg-terracotta/15 text-terracotta", high: "bg-amber/15 text-amber", medium: "bg-dusty/15 text-dusty", low: "bg-stone text-charcoal/60" };
  const effortWeight = { low: 0, medium: 1, high: 2 };
  const costWeight = { none: 0, low: 1, medium: 2, high: 3 };
  const priorityWeight = { urgent_attention: 3, high: 2, medium: 1, low: 0 };

  function applyFiltersAndSort() {
    const category = document.getElementById("filter-category").value;
    const priority = document.getElementById("filter-priority").value;
    const status = document.getElementById("filter-status").value;
    const sortBy = document.getElementById("sort-by").value;

    let list = all.filter((r) =>
      (!category || r.category === category) &&
      (!priority || r.priority === priority) &&
      (!status || r.status === status)
    );

    list = [...list].sort((a, b) => {
      if (sortBy === "priority") return priorityWeight[b.priority] - priorityWeight[a.priority];
      if (sortBy === "effort") return effortWeight[a.effort] - effortWeight[b.effort];
      if (sortBy === "cost") return costWeight[a.estimated_cost?.type || "none"] - costWeight[b.estimated_cost?.type || "none"];
      if (sortBy === "room") return (a.room_name || "").localeCompare(b.room_name || "");
      if (sortBy === "newest") return (b.created_at || "").localeCompare(a.created_at || "");
      return 0;
    });

    render(list);
  }

  function render(list) {
    const grid = document.getElementById("recs-grid");
    const empty = document.getElementById("recs-empty");
    if (!list.length) {
      grid.innerHTML = "";
      empty.classList.toggle("hidden", all.length !== 0);
      grid.classList.toggle("hidden", all.length === 0);
      if (all.length) grid.innerHTML = `<p class="text-sm text-charcoal/50 sm:col-span-2 py-10 text-center">No recommendations match your filters.</p>`;
      return;
    }
    empty.classList.add("hidden");
    grid.innerHTML = list.map((r) => `
      <div class="border border-taupe/60 rounded-xl p-5 flex flex-col ${r.status === 'dismissed' || r.status === 'completed' ? 'opacity-60' : ''}">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-mono uppercase px-2 py-0.5 rounded ${priorityColor[r.priority] || ''}">${titleCase(r.priority)}</span>
          <span class="text-xs text-charcoal/50">${titleCase(r.category)}${r.room_name ? " · " + escapeHtml(r.room_name) : ""}</span>
        </div>
        <h3 class="font-semibold mb-1">${escapeHtml(r.title)}</h3>
        <p class="text-sm text-charcoal/70 mb-2">${escapeHtml(r.why_it_matters)}</p>
        <p class="text-sm text-charcoal/80 mb-2"><strong>Action:</strong> ${escapeHtml(r.recommended_action)}</p>
        <p class="text-xs text-charcoal/50 mb-3">${escapeHtml(r.expected_benefit)}</p>
        <div class="flex flex-wrap gap-2 text-xs text-charcoal/50 mb-4">
          <span>Effort: ${titleCase(r.effort)}</span>
          <span>·</span>
          <span>Cost: ${titleCase(r.estimated_cost?.type || "none")}${r.estimated_cost?.is_estimate ? " (estimate)" : ""}</span>
          <span>·</span>
          <span>Confidence: ${titleCase(r.confidence)}</span>
          ${r.requires_professional_assessment ? '<span>· Requires professional assessment</span>' : ""}
        </div>
        <div class="mt-auto flex flex-wrap gap-2 pt-3 border-t border-taupe/40 text-xs">
          <button class="px-3 py-1.5 rounded-full border border-taupe hover:bg-stone" data-action="save" data-id="${r.id}">Save</button>
          <button class="px-3 py-1.5 rounded-full border border-taupe hover:bg-stone" data-action="complete" data-id="${r.id}">Complete</button>
          <button class="px-3 py-1.5 rounded-full border border-taupe hover:bg-stone" data-action="dismiss" data-id="${r.id}">Dismiss</button>
          <button class="px-3 py-1.5 rounded-full border border-taupe hover:bg-stone ml-auto" data-action="copy" data-id="${r.id}">Copy</button>
          <button class="px-3 py-1.5 rounded-full bg-charcoal text-ivory hover:bg-olive" data-action="task" data-id="${r.id}">Add to Tasks</button>
        </div>
      </div>`).join("");

    grid.querySelectorAll("[data-action]").forEach((btn) =>
      btn.addEventListener("click", () => handleAction(btn.dataset.action, btn.dataset.id))
    );
  }

  async function handleAction(action, id) {
    const rec = all.find((r) => r.id === id);
    if (!rec) return;
    try {
      if (action === "save") {
        await apiPost(`/api/recommendations/${id}/save`);
        rec.status = "saved";
        showToast("Recommendation saved", "success");
      } else if (action === "complete") {
        await apiPost(`/api/recommendations/${id}/complete`);
        rec.status = "completed";
        showToast("Marked as completed", "success");
      } else if (action === "dismiss") {
        await apiPost(`/api/recommendations/${id}/dismiss`);
        rec.status = "dismissed";
        showToast("Recommendation dismissed", "info");
      } else if (action === "copy") {
        await navigator.clipboard.writeText(`${rec.title}\n${rec.recommended_action}`);
        showToast("Copied to clipboard", "success");
      } else if (action === "task") {
        await apiPost("/api/tasks", {
          home_id: homeId,
          title: rec.title,
          description: rec.recommended_action,
          room_id: rec.room_id,
          priority: rec.priority === "urgent_attention" ? "urgent_attention" : rec.priority,
          source_recommendation_id: rec.id,
        });
        showToast("Added to tasks", "success");
      }
      applyFiltersAndSort();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function load() {
    const home = await apiGet("/api/home");
    if (!home) {
      document.getElementById("recs-empty").classList.remove("hidden");
      return;
    }
    homeId = home.id;
    all = await apiGet(`/api/recommendations?home_id=${homeId}`);
    applyFiltersAndSort();
  }

  document.addEventListener("DOMContentLoaded", () => {
    ["filter-category", "filter-priority", "filter-status", "sort-by"].forEach((id) =>
      document.getElementById(id).addEventListener("change", applyFiltersAndSort)
    );
    load();
  });
})();
