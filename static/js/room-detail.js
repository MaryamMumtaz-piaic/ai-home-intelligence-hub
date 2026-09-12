(() => {
  const { apiGet, apiPost, apiDelete, showToast, openModal, confirmAction, escapeHtml, titleCase } = HomeHub;

  const roomId = document.querySelector("[data-room-id]").dataset.roomId;
  let room = null;

  const FURNITURE_CATEGORIES = ["sofa","bed","desk","chair","dining_table","wardrobe","cabinet","bookshelf","tv_unit","coffee_table","storage_box","dresser","kitchen_unit","other"];
  const APPLIANCE_CATEGORIES = ["refrigerator","air_conditioner","fan","washing_machine","dryer","water_heater","oven","microwave","television","computer","lighting","water_pump","other"];

  function renderSvg() {
    const svg = document.getElementById("room-svg");
    const scale = Math.min(360 / room.length_m, 180 / room.width_m);
    const w = room.length_m * scale;
    const h = room.width_m * scale;
    const ox = (400 - w) / 2;
    const oy = (220 - h) / 2;
    let furniture = "";
    (room.furniture || []).forEach((f, i) => {
      const fw = Math.min(w * 0.4, (f.width / 100) * scale);
      const fh = Math.min(h * 0.4, (f.depth / 100) * scale);
      const fx = ox + (f.position?.x || (10 + i * 15)) / 100 * (w - fw);
      const fy = oy + (f.position?.y || 10) / 100 * (h - fh);
      furniture += `<rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" fill="#C1694F22" stroke="#C1694F" stroke-width="1"/>
        <text x="${fx + 3}" y="${fy + 11}" font-size="8" font-family="IBM Plex Mono" fill="#8a4732">${escapeHtml(f.name)}</text>`;
    });
    svg.innerHTML = `
      <rect x="${ox}" y="${oy}" width="${w}" height="${h}" fill="#6B76540d" stroke="#6B7654" stroke-width="1.5"/>
      ${furniture}
      <text x="${ox + 4}" y="${oy - 6}" font-size="9" font-family="IBM Plex Mono" fill="#6b6252">${room.length_m}m × ${room.width_m}m</text>`;
  }

  function renderDetails() {
    document.getElementById("room-type-label").textContent = "Room";
    document.getElementById("room-name").textContent = room.name;
    document.getElementById("room-dims").textContent = `${titleCase(room.room_type)} · ${room.length_m}m × ${room.width_m}m · ${room.ceiling_height_m}m ceiling`;
    document.getElementById("room-details").innerHTML = `
      <div class="flex justify-between"><dt class="text-charcoal/60">Natural light</dt><dd>${titleCase(room.natural_light)}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Windows</dt><dd>${room.window_count}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Doors</dt><dd>${room.door_count}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Priority</dt><dd>${titleCase(room.priority)}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Purpose</dt><dd class="text-right max-w-[60%]">${escapeHtml(room.primary_purpose || "—")}</dd></div>`;

    document.getElementById("furniture-items").innerHTML = (room.furniture || []).length
      ? room.furniture.map((f) => `
        <div class="flex items-center justify-between border border-taupe/50 rounded-lg px-4 py-3">
          <div><p class="font-medium text-sm">${escapeHtml(f.name)}</p><p class="text-xs text-charcoal/50">${titleCase(f.category)} · ${f.width}×${f.depth}cm</p></div>
          <button class="text-xs text-terracotta hover:underline" data-del-furniture="${f.id}">Remove</button>
        </div>`).join("")
      : `<p class="text-sm text-charcoal/50">No furniture yet.</p>`;

    document.getElementById("appliance-items").innerHTML = (room.appliances || []).length
      ? room.appliances.map((a) => `
        <div class="flex items-center justify-between border border-taupe/50 rounded-lg px-4 py-3">
          <div><p class="font-medium text-sm">${escapeHtml(a.name)}</p><p class="text-xs text-charcoal/50">${titleCase(a.category)}${a.estimated_power_watts ? " · " + a.estimated_power_watts + "W" : ""}</p></div>
          <button class="text-xs text-terracotta hover:underline" data-del-appliance="${a.id}">Remove</button>
        </div>`).join("")
      : `<p class="text-sm text-charcoal/50">No appliances yet.</p>`;

    document.querySelectorAll("[data-del-furniture]").forEach((btn) =>
      btn.addEventListener("click", async () => {
        if (!(await confirmAction("Remove this furniture item?"))) return;
        await apiDelete(`/api/rooms/${roomId}/furniture/${btn.dataset.delFurniture}`);
        await load();
      })
    );
    document.querySelectorAll("[data-del-appliance]").forEach((btn) =>
      btn.addEventListener("click", async () => {
        if (!(await confirmAction("Remove this appliance?"))) return;
        await apiDelete(`/api/rooms/${roomId}/appliances/${btn.dataset.delAppliance}`);
        await load();
      })
    );

    renderSvg();
  }

  function openAddFurniture() {
    const close = openModal(`
      <form id="furn-form" class="p-6">
        <h2 class="font-display text-xl mb-4">Add furniture</h2>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium">Name</span><input required name="name" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          <label class="block"><span class="text-sm font-medium">Category</span>
            <select name="category" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${FURNITURE_CATEGORIES.map((c) => `<option value="${c}">${titleCase(c)}</option>`).join("")}</select></label>
          <div class="grid grid-cols-2 gap-4">
            <label class="block"><span class="text-sm font-medium">Width (cm)</span><input type="number" name="width" value="100" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
            <label class="block"><span class="text-sm font-medium">Depth (cm)</span><input type="number" name="depth" value="60" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-full text-sm font-medium bg-charcoal text-ivory hover:bg-olive">Add</button>
        </div>
      </form>`);
    document.querySelector("[data-cancel]").addEventListener("click", close);
    document.getElementById("furn-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      try {
        await apiPost(`/api/rooms/${roomId}/furniture`, {
          name: form.get("name"), category: form.get("category"),
          width: parseFloat(form.get("width")), depth: parseFloat(form.get("depth")),
        });
        close();
        showToast("Furniture added", "success");
        await load();
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  }

  function openAddAppliance() {
    const close = openModal(`
      <form id="appl-form" class="p-6">
        <h2 class="font-display text-xl mb-4">Add appliance</h2>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium">Name</span><input required name="name" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          <label class="block"><span class="text-sm font-medium">Category</span>
            <select name="category" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${APPLIANCE_CATEGORIES.map((c) => `<option value="${c}">${titleCase(c)}</option>`).join("")}</select></label>
          <label class="block"><span class="text-sm font-medium">Estimated power (W, optional)</span><input type="number" name="watts" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-full text-sm font-medium bg-charcoal text-ivory hover:bg-olive">Add</button>
        </div>
      </form>`);
    document.querySelector("[data-cancel]").addEventListener("click", close);
    document.getElementById("appl-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      try {
        await apiPost(`/api/rooms/${roomId}/appliances`, {
          name: form.get("name"), category: form.get("category"),
          estimated_power_watts: form.get("watts") ? parseFloat(form.get("watts")) : null,
        });
        close();
        showToast("Appliance added", "success");
        await load();
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  }

  async function analyzeRoom() {
    const home = await apiGet("/api/home");
    if (!home) return;
    const btn = document.getElementById("analyze-room-btn");
    btn.disabled = true;
    btn.textContent = "Analyzing…";
    try {
      const result = await apiPost("/api/ai/analyze-room", { home_id: home.id, room_id: roomId });
      const box = document.getElementById("ai-observations");
      box.classList.remove("hidden");
      document.getElementById("ai-observations-text").textContent = result.observations || "No observations available.";
      document.getElementById("ai-room-recs").innerHTML = (result.recommendations || []).map((r) => `
        <div class="border border-taupe/50 rounded-lg p-4">
          <p class="text-xs font-mono uppercase text-charcoal/50 mb-1">${titleCase(r.category)} · ${titleCase(r.priority)}</p>
          <p class="font-medium text-sm mb-1">${escapeHtml(r.title)}</p>
          <p class="text-xs text-charcoal/60">${escapeHtml(r.recommended_action)}</p>
        </div>`).join("") || `<p class="text-sm text-charcoal/50">No specific recommendations this time.</p>`;
      if (!result.succeeded) showToast("Analysis is partial: " + (result.error || "AI service unavailable."), "warning");
      else showToast("Room analysis complete", "success");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      btn.disabled = false;
      btn.textContent = "Analyze Room";
    }
  }

  const SCENARIO_TYPES = [
    "move_furniture", "add_storage", "remove_furniture_item", "create_home_office_zone",
    "replace_lighting", "reduce_appliance_usage", "add_maintenance_task", "reorganize_room",
    "improve_entryway_organization",
  ];

  function openScenarioModal() {
    const close = openModal(`
      <form id="scenario-form" class="p-6">
        <h2 class="font-display text-xl mb-1">Compare a what-if scenario</h2>
        <p class="text-xs text-charcoal/50 mb-4">A planning simulation based on your data — not an exact architectural or engineering simulation.</p>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium">Scenario type</span>
            <select name="scenario_type" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${SCENARIO_TYPES.map((s) => `<option value="${s}">${titleCase(s)}</option>`).join("")}</select></label>
          <label class="block"><span class="text-sm font-medium">Describe the change</span>
            <textarea required name="description" rows="3" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5" placeholder="e.g. Move the sofa to the opposite wall and add a bookshelf."></textarea></label>
        </div>
        <div id="scenario-result" class="hidden mt-5 border-t border-taupe/50 pt-4 text-sm space-y-3"></div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Close</button>
          <button type="submit" class="px-4 py-2 rounded-full text-sm font-medium bg-charcoal text-ivory hover:bg-olive">Compare</button>
        </div>
      </form>`);
    document.querySelector("[data-cancel]").addEventListener("click", close);
    document.getElementById("scenario-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const home = await apiGet("/api/home");
      if (!home) return;
      const form = new FormData(e.target);
      const submitBtn = e.target.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = "Comparing…";
      try {
        const result = await apiPost("/api/ai/compare-scenario", {
          home_id: home.id, room_id: roomId,
          scenario_type: form.get("scenario_type"),
          description: form.get("description"),
        });
        const box = document.getElementById("scenario-result");
        box.classList.remove("hidden");
        box.innerHTML = `
          <div><p class="font-medium mb-1">Current state</p><p class="text-charcoal/70">${escapeHtml(result.current_state_summary)}</p></div>
          <div><p class="font-medium mb-1">Proposed change</p><p class="text-charcoal/70">${escapeHtml(result.proposed_change_summary)}</p></div>
          ${result.potential_benefits?.length ? `<div><p class="font-medium mb-1">Potential benefits</p><ul class="text-charcoal/70 list-disc pl-5">${result.potential_benefits.map((b) => `<li>${escapeHtml(b)}</li>`).join("")}</ul></div>` : ""}
          ${result.possible_trade_offs?.length ? `<div><p class="font-medium mb-1">Possible trade-offs</p><ul class="text-charcoal/70 list-disc pl-5">${result.possible_trade_offs.map((b) => `<li>${escapeHtml(b)}</li>`).join("")}</ul></div>` : ""}
          <p class="text-xs text-charcoal/50">Estimated effort: ${escapeHtml(result.estimated_effort)}</p>
          <p class="text-xs text-charcoal/40">${escapeHtml(result.disclaimer || "This is a planning simulation, not an exact architectural or engineering simulation.")}</p>`;
      } catch (err) {
        showToast(err.message, "error");
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Compare";
      }
    });
  }

  async function load() {
    try {
      room = await apiGet(`/api/rooms/${roomId}`);
      document.getElementById("room-loading").classList.add("hidden");
      document.getElementById("room-content").classList.remove("hidden");
      renderDetails();
    } catch (err) {
      document.getElementById("room-loading").textContent = "Room not found.";
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("add-furniture-open")?.addEventListener("click", openAddFurniture);
    document.getElementById("add-appliance-open")?.addEventListener("click", openAddAppliance);
    document.getElementById("analyze-room-btn")?.addEventListener("click", analyzeRoom);
    document.getElementById("compare-scenario-btn")?.addEventListener("click", openScenarioModal);
    load();
  });
})();
