(() => {
  const { apiGet, apiPost, apiPut, showToast, draft, clearDraft, escapeHtml, titleCase } = HomeHub;

  const STEP_NAMES = [
    "Home Profile", "Rooms", "Furniture", "Appliances",
    "Lifestyle", "Energy", "Maintenance", "Security", "Review",
  ];

  const GOALS = [
    "improve_organization", "use_space_better", "reduce_energy_waste", "improve_comfort",
    "plan_maintenance", "improve_security_awareness", "prepare_for_renovation",
    "make_more_accessible", "create_calmer_environment", "track_improvements",
  ];

  const ROOM_TYPES = [
    "living_room", "bedroom", "kitchen", "bathroom", "dining_room", "home_office", "study",
    "balcony", "hallway", "storage_room", "laundry_room", "guest_room", "kids_room",
    "outdoor_area", "other",
  ];

  const FURNITURE_CATEGORIES = [
    "sofa", "bed", "desk", "chair", "dining_table", "wardrobe", "cabinet", "bookshelf",
    "tv_unit", "coffee_table", "storage_box", "dresser", "kitchen_unit", "other",
  ];

  const APPLIANCE_CATEGORIES = [
    "refrigerator", "air_conditioner", "fan", "washing_machine", "dryer", "water_heater",
    "oven", "microwave", "television", "computer", "lighting", "water_pump", "other",
  ];

  const MAINTENANCE_CATEGORIES = [
    "electrical", "plumbing", "hvac", "roof", "walls_and_paint", "windows_and_doors",
    "appliances", "pest_control", "water_systems", "safety_equipment", "furniture",
    "outdoor_areas", "other",
  ];

  let state = draft("wizardState") || { step: 0, homeId: null, profile: {}, goals: [] };
  let currentHome = null;

  function saveState() {
    draft("wizardState", state);
  }

  function optionList(values, selected) {
    return values
      .map((v) => `<option value="${v}" ${v === selected ? "selected" : ""}>${titleCase(v)}</option>`)
      .join("");
  }

  function renderProgress() {
    const bar = document.getElementById("wizard-progress");
    bar.innerHTML = STEP_NAMES.map((name, i) => {
      const cls = i === state.step ? "is-active" : i < state.step ? "is-complete" : "";
      return `<li class="progress-step ${cls}"><span class="dot"></span><span>${i + 1}. ${name}</span></li>`;
    }).join("");
  }

  function stepContent() {
    switch (state.step) {
      case 0: return stepHomeProfile();
      case 1: return stepRooms();
      case 2: return stepFurniture();
      case 3: return stepAppliances();
      case 4: return stepLifestyle();
      case 5: return stepEnergy();
      case 6: return stepMaintenance();
      case 7: return stepSecurity();
      case 8: return stepReview();
      default: return "";
    }
  }

  function stepHomeProfile() {
    const p = state.profile;
    return `
      <h2 class="font-display text-2xl mb-1">Tell us about your home</h2>
      <p class="text-sm text-charcoal/60 mb-6">Broad details only — no exact address needed.</p>
      <div class="grid sm:grid-cols-2 gap-5">
        <label class="block">
          <span class="text-sm font-medium">Home name</span>
          <input required name="name" value="${escapeHtml(p.name || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5" placeholder="e.g. The Alvi Residence">
        </label>
        <label class="block">
          <span class="text-sm font-medium">Home type</span>
          <select name="home_type" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
            ${optionList(["apartment","house","villa","studio","townhouse","shared_home","office_home","other"], p.home_type)}
          </select>
        </label>
        <label class="block">
          <span class="text-sm font-medium">Climate zone / location</span>
          <input name="climate_zone_or_location" value="${escapeHtml(p.climate_zone_or_location || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5" placeholder="e.g. Hot, coastal">
        </label>
        <label class="block">
          <span class="text-sm font-medium">Residents</span>
          <input type="number" min="1" name="resident_count" value="${p.resident_count || 1}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
        </label>
        <label class="block">
          <span class="text-sm font-medium">Floors</span>
          <input type="number" min="1" name="floor_count" value="${p.floor_count || 1}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
        </label>
        <label class="block">
          <span class="text-sm font-medium">Approx. total area (sqm)</span>
          <input type="number" min="0" name="approximate_total_area_sqm" value="${p.approximate_total_area_sqm || ""}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
        </label>
        <label class="block sm:col-span-2">
          <span class="text-sm font-medium">Ownership</span>
          <select name="ownership_status" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
            ${optionList(["owned","rented","shared","other"], p.ownership_status)}
          </select>
        </label>
      </div>
      <fieldset class="mt-6">
        <legend class="text-sm font-medium mb-2">Main goals (select any that apply)</legend>
        <div class="flex flex-wrap gap-2">
          ${GOALS.map((g) => `
            <label class="flex items-center gap-1.5 border border-taupe rounded-full px-3 py-1.5 text-sm cursor-pointer has-[:checked]:bg-olive has-[:checked]:text-ivory has-[:checked]:border-olive">
              <input type="checkbox" name="goal" value="${g}" class="sr-only" ${state.goals.includes(g) ? "checked" : ""}>
              ${titleCase(g)}
            </label>`).join("")}
        </div>
      </fieldset>`;
  }

  function stepRooms() {
    const rooms = currentHome?.rooms || [];
    return `
      <h2 class="font-display text-2xl mb-1">Add your rooms</h2>
      <p class="text-sm text-charcoal/60 mb-6">Add at least one room. You can add furniture and appliances next.</p>
      <div id="room-list" class="space-y-2 mb-6">
        ${rooms.length ? rooms.map((r) => `
          <div class="flex items-center justify-between border border-taupe/60 rounded-lg px-4 py-3">
            <div>
              <p class="font-medium">${escapeHtml(r.name)}</p>
              <p class="text-xs text-charcoal/50">${titleCase(r.room_type)} · ${r.length_m}m × ${r.width_m}m</p>
            </div>
            <button type="button" class="text-xs text-terracotta hover:underline" data-remove-room="${r.id}">Remove</button>
          </div>`).join("") : `<p class="text-sm text-charcoal/50 empty-hint">No rooms added yet.</p>`}
      </div>
      <div class="grid sm:grid-cols-4 gap-3 items-end bg-stone/50 rounded-lg p-4">
        <label class="block sm:col-span-2"><span class="text-xs font-medium">Room name</span>
          <input id="new-room-name" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2" placeholder="Living Room"></label>
        <label class="block"><span class="text-xs font-medium">Type</span>
          <select id="new-room-type" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2">${optionList(ROOM_TYPES)}</select></label>
        <label class="block"><span class="text-xs font-medium">Length (m)</span>
          <input id="new-room-length" type="number" step="0.1" min="0.1" value="4" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <label class="block"><span class="text-xs font-medium">Width (m)</span>
          <input id="new-room-width" type="number" step="0.1" min="0.1" value="3" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <button type="button" id="add-room-btn" class="sm:col-span-1 bg-charcoal text-ivory rounded-lg px-4 py-2 text-sm font-medium hover:bg-olive">Add Room</button>
      </div>`;
  }

  function roomOptions() {
    const rooms = currentHome?.rooms || [];
    if (!rooms.length) return `<option value="">No rooms yet — go back to add one</option>`;
    return rooms.map((r) => `<option value="${r.id}">${escapeHtml(r.name)}</option>`).join("");
  }

  function stepFurniture() {
    const rooms = currentHome?.rooms || [];
    return `
      <h2 class="font-display text-2xl mb-1">Add furniture</h2>
      <p class="text-sm text-charcoal/60 mb-6">Optional but improves space-planning recommendations.</p>
      <label class="block mb-4"><span class="text-sm font-medium">Room</span>
        <select id="furniture-room-select" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${roomOptions()}</select></label>
      <div id="furniture-list" class="space-y-2 mb-6"></div>
      <div class="grid sm:grid-cols-4 gap-3 items-end bg-stone/50 rounded-lg p-4">
        <label class="block sm:col-span-1"><span class="text-xs font-medium">Name</span>
          <input id="new-furn-name" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2" placeholder="Sofa"></label>
        <label class="block"><span class="text-xs font-medium">Category</span>
          <select id="new-furn-category" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2">${optionList(FURNITURE_CATEGORIES)}</select></label>
        <label class="block"><span class="text-xs font-medium">Width (cm)</span>
          <input id="new-furn-width" type="number" min="1" value="180" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <label class="block"><span class="text-xs font-medium">Depth (cm)</span>
          <input id="new-furn-depth" type="number" min="1" value="80" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <button type="button" id="add-furniture-btn" class="bg-charcoal text-ivory rounded-lg px-4 py-2 text-sm font-medium hover:bg-olive">Add</button>
      </div>
      <p class="text-xs text-charcoal/50 mt-2">${rooms.length ? "" : "Add a room in the previous step first."}</p>`;
  }

  function stepAppliances() {
    const rooms = currentHome?.rooms || [];
    return `
      <h2 class="font-display text-2xl mb-1">Add appliances</h2>
      <p class="text-sm text-charcoal/60 mb-6">Optional — helps with energy and maintenance insights.</p>
      <label class="block mb-4"><span class="text-sm font-medium">Room</span>
        <select id="appliance-room-select" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${roomOptions()}</select></label>
      <div id="appliance-list" class="space-y-2 mb-6"></div>
      <div class="grid sm:grid-cols-4 gap-3 items-end bg-stone/50 rounded-lg p-4">
        <label class="block"><span class="text-xs font-medium">Name</span>
          <input id="new-appl-name" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2" placeholder="Refrigerator"></label>
        <label class="block"><span class="text-xs font-medium">Category</span>
          <select id="new-appl-category" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2">${optionList(APPLIANCE_CATEGORIES)}</select></label>
        <label class="block"><span class="text-xs font-medium">Age (years)</span>
          <input id="new-appl-age" type="number" min="0" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <label class="block"><span class="text-xs font-medium">Power (W, if known)</span>
          <input id="new-appl-watts" type="number" min="0" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"></label>
        <button type="button" id="add-appliance-btn" class="bg-charcoal text-ivory rounded-lg px-4 py-2 text-sm font-medium hover:bg-olive">Add</button>
      </div>
      <p class="text-xs text-charcoal/50 mt-2">${rooms.length ? "" : "Add a room in the previous step first."}</p>`;
  }

  function stepLifestyle() {
    const l = currentHome?.lifestyle || {};
    return `
      <h2 class="font-display text-2xl mb-1">Lifestyle &amp; preferences</h2>
      <p class="text-sm text-charcoal/60 mb-6">Helps tailor recommendations to how you actually live.</p>
      <div class="grid sm:grid-cols-2 gap-4">
        ${[
          ["works_from_home", "I work from home"],
          ["hosts_guests_often", "I host guests often"],
          ["has_children", "I have children at home"],
          ["has_pets", "I have pets"],
          ["prefers_open_spaces", "I prefer open spaces over more storage"],
          ["prefers_decorative_interiors", "I prefer decorative over minimal interiors"],
          ["has_accessibility_considerations", "I have accessibility considerations"],
          ["prefers_low_cost_changes", "I prefer low-cost changes over larger projects"],
        ].map(([key, label]) => `
          <label class="flex items-center gap-2 text-sm">
            <input type="checkbox" name="${key}" ${l[key] ? "checked" : ""} class="rounded border-taupe">
            ${label}
          </label>`).join("")}
      </div>
      <label class="block mt-5"><span class="text-sm font-medium">Preferred home style</span>
        <select name="preferred_style" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
          ${optionList(["minimal","modern","warm_contemporary","traditional","japandi_inspired","industrial","classic","eclectic","natural","functional","undecided"], l.preferred_style)}
        </select></label>
      <label class="block mt-4"><span class="text-sm font-medium">Top priority</span>
        <select name="top_priority" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
          ${optionList(["comfort","efficiency","aesthetics","practicality"], l.top_priority)}
        </select></label>
      <label class="block mt-4"><span class="text-sm font-medium">Accessibility notes (optional)</span>
        <textarea name="accessibility_notes" rows="2" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${escapeHtml(l.accessibility_notes || "")}</textarea></label>`;
  }

  function stepEnergy() {
    const e = currentHome?.energy || {};
    return `
      <h2 class="font-display text-2xl mb-1">Energy profile</h2>
      <p class="text-sm text-charcoal/60 mb-6">Leave anything blank if you don't know it — estimates will be clearly labeled.</p>
      <div class="grid sm:grid-cols-2 gap-5">
        <label class="block"><span class="text-sm font-medium">Provider / tariff</span>
          <input name="provider_or_tariff" value="${escapeHtml(e.provider_or_tariff || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        <label class="block"><span class="text-sm font-medium">Approx. monthly bill</span>
          <input type="number" min="0" name="approximate_monthly_bill" value="${e.approximate_monthly_bill || ""}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        <label class="block"><span class="text-sm font-medium">Currency</span>
          <input name="currency" value="${escapeHtml(e.currency || "USD")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        <label class="block"><span class="text-sm font-medium">Main cooling method</span>
          <input name="main_cooling_method" value="${escapeHtml(e.main_cooling_method || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        <label class="block"><span class="text-sm font-medium">Main heating method</span>
          <input name="main_heating_method" value="${escapeHtml(e.main_heating_method || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
        <label class="block"><span class="text-sm font-medium">Lighting type</span>
          <input name="lighting_type" value="${escapeHtml(e.lighting_type || "")}" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
      </div>
      <div class="flex gap-6 mt-5">
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" name="solar_available" ${e.solar_available ? "checked" : ""}> Solar available</label>
        <label class="flex items-center gap-2 text-sm"><input type="checkbox" name="backup_power_available" ${e.backup_power_available ? "checked" : ""}> Backup power available</label>
      </div>
      <label class="block mt-4"><span class="text-sm font-medium">Energy concerns (optional)</span>
        <textarea name="energy_concerns" rows="2" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${escapeHtml(e.energy_concerns || "")}</textarea></label>`;
  }

  function stepMaintenance() {
    const rooms = currentHome?.rooms || [];
    return `
      <h2 class="font-display text-2xl mb-1">Maintenance</h2>
      <p class="text-sm text-charcoal/60 mb-6">Optional — add anything you're already tracking.</p>
      <div id="maintenance-list" class="space-y-2 mb-6"></div>
      <div class="grid sm:grid-cols-4 gap-3 items-end bg-stone/50 rounded-lg p-4">
        <label class="block"><span class="text-xs font-medium">Title</span>
          <input id="new-maint-title" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2" placeholder="Check water heater"></label>
        <label class="block"><span class="text-xs font-medium">Category</span>
          <select id="new-maint-category" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2">${optionList(MAINTENANCE_CATEGORIES)}</select></label>
        <label class="block"><span class="text-xs font-medium">Room (optional)</span>
          <select id="new-maint-room" class="mt-1 w-full border border-taupe rounded-lg px-3 py-2"><option value="">— None —</option>${roomOptions()}</select></label>
        <button type="button" id="add-maintenance-btn" class="bg-charcoal text-ivory rounded-lg px-4 py-2 text-sm font-medium hover:bg-olive">Add</button>
      </div>`;
  }

  function stepSecurity() {
    const s = currentHome?.security || {};
    return `
      <h2 class="font-display text-2xl mb-1">Security awareness</h2>
      <p class="text-sm text-charcoal/60 mb-4 max-w-lg">This feature provides general home-safety guidance. It is not a professional security assessment or emergency service. Never share passwords or access codes here.</p>
      <div class="grid sm:grid-cols-2 gap-3">
        ${[
          ["door_locks_present", "Door locks present"],
          ["window_locks_present", "Window locks present"],
          ["outdoor_lighting", "Outdoor lighting present"],
          ["smoke_alarms", "Smoke alarms installed"],
          ["carbon_monoxide_alarms", "Carbon monoxide alarms installed"],
          ["emergency_exits_clear", "Emergency exits are kept clear"],
          ["first_aid_kit_available", "First-aid kit available"],
          ["fire_extinguisher_available", "Fire extinguisher available"],
          ["backup_communication_plan", "Backup communication plan exists"],
        ].map(([key, label]) => `
          <label class="flex items-center gap-2 text-sm">
            <input type="checkbox" name="${key}" ${s[key] ? "checked" : ""} class="rounded border-taupe"> ${label}
          </label>`).join("")}
      </div>
      <label class="block mt-4"><span class="text-sm font-medium">Emergency notes (optional)</span>
        <textarea name="important_emergency_notes" rows="2" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">${escapeHtml(s.important_emergency_notes || "")}</textarea></label>`;
  }

  function stepReview() {
    const h = currentHome;
    if (!h) return `<p>Loading…</p>`;
    return `
      <h2 class="font-display text-2xl mb-1">Review your home</h2>
      <p class="text-sm text-charcoal/60 mb-6">Everything looks good? Finish setup to unlock your dashboard and run your first analysis.</p>
      <dl class="grid sm:grid-cols-2 gap-4 text-sm">
        <div><dt class="text-charcoal/50">Name</dt><dd class="font-medium">${escapeHtml(h.name)}</dd></div>
        <div><dt class="text-charcoal/50">Type</dt><dd class="font-medium">${titleCase(h.home_type)}</dd></div>
        <div><dt class="text-charcoal/50">Rooms</dt><dd class="font-medium">${(h.rooms || []).length}</dd></div>
        <div><dt class="text-charcoal/50">Residents</dt><dd class="font-medium">${h.resident_count}</dd></div>
        <div><dt class="text-charcoal/50">Goals</dt><dd class="font-medium">${(h.main_goals || []).map(titleCase).join(", ") || "None set"}</dd></div>
      </dl>`;
  }

  function bindStepEvents() {
    if (state.step === 1) {
      document.getElementById("add-room-btn")?.addEventListener("click", onAddRoom);
      document.querySelectorAll("[data-remove-room]").forEach((btn) =>
        btn.addEventListener("click", () => onRemoveRoom(btn.dataset.removeRoom))
      );
    }
    if (state.step === 2) {
      document.getElementById("add-furniture-btn")?.addEventListener("click", onAddFurniture);
      renderFurnitureList();
      document.getElementById("furniture-room-select")?.addEventListener("change", renderFurnitureList);
    }
    if (state.step === 3) {
      document.getElementById("add-appliance-btn")?.addEventListener("click", onAddAppliance);
      renderApplianceList();
      document.getElementById("appliance-room-select")?.addEventListener("change", renderApplianceList);
    }
    if (state.step === 6) {
      document.getElementById("add-maintenance-btn")?.addEventListener("click", onAddMaintenance);
      renderMaintenanceList();
    }
  }

  function renderFurnitureList() {
    const roomId = document.getElementById("furniture-room-select")?.value;
    const room = (currentHome?.rooms || []).find((r) => r.id === roomId);
    const list = document.getElementById("furniture-list");
    if (!list) return;
    const items = room?.furniture || [];
    list.innerHTML = items.length
      ? items.map((f) => `<div class="flex justify-between border border-taupe/50 rounded-lg px-3 py-2 text-sm"><span>${escapeHtml(f.name)} · ${titleCase(f.category)}</span><span class="text-charcoal/50">${f.width}×${f.depth}cm</span></div>`).join("")
      : `<p class="text-sm text-charcoal/50">No furniture in this room yet.</p>`;
  }

  function renderApplianceList() {
    const roomId = document.getElementById("appliance-room-select")?.value;
    const room = (currentHome?.rooms || []).find((r) => r.id === roomId);
    const list = document.getElementById("appliance-list");
    if (!list) return;
    const items = room?.appliances || [];
    list.innerHTML = items.length
      ? items.map((a) => `<div class="flex justify-between border border-taupe/50 rounded-lg px-3 py-2 text-sm"><span>${escapeHtml(a.name)} · ${titleCase(a.category)}</span><span class="text-charcoal/50">${a.estimated_power_watts ? a.estimated_power_watts + "W" : "—"}</span></div>`).join("")
      : `<p class="text-sm text-charcoal/50">No appliances in this room yet.</p>`;
  }

  async function renderMaintenanceList() {
    const list = document.getElementById("maintenance-list");
    if (!list) return;
    try {
      const items = await apiGet(`/api/maintenance?home_id=${state.homeId}`);
      list.innerHTML = items.length
        ? items.map((m) => `<div class="flex justify-between border border-taupe/50 rounded-lg px-3 py-2 text-sm"><span>${escapeHtml(m.title)} · ${titleCase(m.category)}</span><span class="text-charcoal/50">${titleCase(m.status)}</span></div>`).join("")
        : `<p class="text-sm text-charcoal/50">No maintenance items yet.</p>`;
    } catch (err) {
      list.innerHTML = `<p class="text-sm text-terracotta">${err.message}</p>`;
    }
  }

  async function onAddRoom() {
    const name = document.getElementById("new-room-name").value.trim();
    if (!name) return showToast("Enter a room name.", "warning");
    try {
      await apiPost("/api/rooms", {
        home_id: state.homeId,
        name,
        room_type: document.getElementById("new-room-type").value,
        length_m: parseFloat(document.getElementById("new-room-length").value) || 1,
        width_m: parseFloat(document.getElementById("new-room-width").value) || 1,
      });
      currentHome = await apiGet(`/api/home?home_id=${state.homeId}`);
      showToast("Room added", "success");
      renderStep();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function onRemoveRoom(roomId) {
    try {
      await HomeHub.apiDelete(`/api/rooms/${roomId}`);
      currentHome = await apiGet(`/api/home?home_id=${state.homeId}`);
      renderStep();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function onAddFurniture() {
    const roomId = document.getElementById("furniture-room-select").value;
    if (!roomId) return showToast("Add a room first.", "warning");
    const name = document.getElementById("new-furn-name").value.trim();
    if (!name) return showToast("Enter a furniture name.", "warning");
    try {
      await apiPost(`/api/rooms/${roomId}/furniture`, {
        name,
        category: document.getElementById("new-furn-category").value,
        width: parseFloat(document.getElementById("new-furn-width").value) || 50,
        depth: parseFloat(document.getElementById("new-furn-depth").value) || 50,
      });
      currentHome = await apiGet(`/api/home?home_id=${state.homeId}`);
      showToast("Furniture added", "success");
      renderStep();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function onAddAppliance() {
    const roomId = document.getElementById("appliance-room-select").value;
    if (!roomId) return showToast("Add a room first.", "warning");
    const name = document.getElementById("new-appl-name").value.trim();
    if (!name) return showToast("Enter an appliance name.", "warning");
    try {
      await apiPost(`/api/rooms/${roomId}/appliances`, {
        name,
        category: document.getElementById("new-appl-category").value,
        approximate_age_years: parseFloat(document.getElementById("new-appl-age").value) || null,
        estimated_power_watts: parseFloat(document.getElementById("new-appl-watts").value) || null,
      });
      currentHome = await apiGet(`/api/home?home_id=${state.homeId}`);
      showToast("Appliance added", "success");
      renderStep();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function onAddMaintenance() {
    const title = document.getElementById("new-maint-title").value.trim();
    if (!title) return showToast("Enter a title.", "warning");
    try {
      await apiPost("/api/maintenance", {
        home_id: state.homeId,
        title,
        category: document.getElementById("new-maint-category").value,
        room_id: document.getElementById("new-maint-room").value || null,
      });
      showToast("Maintenance item added", "success");
      document.getElementById("new-maint-title").value = "";
      renderMaintenanceList();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  function collectFormValues() {
    const form = document.getElementById("wizard-form");
    const data = {};
    form.querySelectorAll("input, select, textarea").forEach((el) => {
      if (!el.name) return;
      if (el.type === "checkbox") data[el.name] = el.checked;
      else if (el.type === "radio") { if (el.checked) data[el.name] = el.value; }
      else data[el.name] = el.value;
    });
    data.goal = Array.from(form.querySelectorAll('input[name="goal"]:checked')).map((el) => el.value);
    return data;
  }

  async function saveCurrentStep() {
    const values = collectFormValues();
    if (state.step === 0) {
      state.profile = {
        name: values.name,
        home_type: values.home_type,
        climate_zone_or_location: values.climate_zone_or_location || null,
        resident_count: parseInt(values.resident_count, 10) || 1,
        floor_count: parseInt(values.floor_count, 10) || 1,
        approximate_total_area_sqm: values.approximate_total_area_sqm ? parseFloat(values.approximate_total_area_sqm) : null,
        ownership_status: values.ownership_status,
      };
      state.goals = values.goal || [];
      if (!state.profile.name) throw new Error("Home name is required.");
      if (!state.homeId) {
        const home = await apiPost("/api/home", { ...state.profile, main_goals: state.goals });
        state.homeId = home.id;
        currentHome = home;
      } else {
        currentHome = await apiPut(`/api/home/${state.homeId}`, { ...state.profile, main_goals: state.goals });
      }
      saveState();
    } else if (state.step === 4) {
      currentHome = await apiPut(`/api/home/${state.homeId}`, {
        lifestyle: {
          works_from_home: !!values.works_from_home,
          hosts_guests_often: !!values.hosts_guests_often,
          has_children: !!values.has_children,
          has_pets: !!values.has_pets,
          prefers_open_spaces: !!values.prefers_open_spaces,
          prefers_decorative_interiors: !!values.prefers_decorative_interiors,
          has_accessibility_considerations: !!values.has_accessibility_considerations,
          prefers_low_cost_changes: !!values.prefers_low_cost_changes,
          preferred_style: values.preferred_style,
          top_priority: values.top_priority,
          accessibility_notes: values.accessibility_notes || null,
        },
      });
    } else if (state.step === 5) {
      currentHome = await apiPut(`/api/home/${state.homeId}`, {
        energy: {
          provider_or_tariff: values.provider_or_tariff || null,
          approximate_monthly_bill: values.approximate_monthly_bill ? parseFloat(values.approximate_monthly_bill) : null,
          currency: values.currency || "USD",
          main_cooling_method: values.main_cooling_method || null,
          main_heating_method: values.main_heating_method || null,
          lighting_type: values.lighting_type || null,
          solar_available: !!values.solar_available,
          backup_power_available: !!values.backup_power_available,
          energy_concerns: values.energy_concerns || null,
        },
      });
    } else if (state.step === 7) {
      currentHome = await apiPut(`/api/home/${state.homeId}`, {
        security: {
          door_locks_present: !!values.door_locks_present,
          window_locks_present: !!values.window_locks_present,
          outdoor_lighting: !!values.outdoor_lighting,
          smoke_alarms: !!values.smoke_alarms,
          carbon_monoxide_alarms: !!values.carbon_monoxide_alarms,
          emergency_exits_clear: !!values.emergency_exits_clear,
          first_aid_kit_available: !!values.first_aid_kit_available,
          fire_extinguisher_available: !!values.fire_extinguisher_available,
          backup_communication_plan: !!values.backup_communication_plan,
          important_emergency_notes: values.important_emergency_notes || null,
        },
      });
    }
  }

  function renderStep() {
    renderProgress();
    document.getElementById("wizard-step-content").innerHTML = stepContent();
    document.getElementById("wizard-back").disabled = state.step === 0;
    document.getElementById("wizard-next").textContent = state.step === STEP_NAMES.length - 1 ? "Finish Setup" : "Continue";
    bindStepEvents();
  }

  async function onNext() {
    const nextBtn = document.getElementById("wizard-next");
    nextBtn.disabled = true;
    try {
      await saveCurrentStep();
      if (state.step === STEP_NAMES.length - 1) {
        await apiPut(`/api/home/${state.homeId}`, { setup_completed: true });
        clearDraft("wizardState");
        showToast("Home setup complete", "success");
        window.location.reload();
        return;
      }
      state.step += 1;
      saveState();
      renderStep();
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      nextBtn.disabled = false;
    }
  }

  function onBack() {
    if (state.step === 0) return;
    state.step -= 1;
    saveState();
    renderStep();
  }

  function renderFloorPlan() {
    const svg = document.getElementById("floorplan-svg");
    const rooms = currentHome?.rooms || [];
    if (!svg) return;
    if (!rooms.length) {
      svg.innerHTML = `<text x="20" y="40" font-family="Inter" font-size="14" fill="#8a8172">No rooms yet — add one from the Rooms page.</text>`;
      return;
    }
    const cols = Math.ceil(Math.sqrt(rooms.length));
    const cellW = 580 / cols;
    const scale = 28;
    let svgContent = "";
    rooms.forEach((room, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const x = 10 + col * cellW;
      const y = 10 + row * 130;
      const w = Math.min(cellW - 14, room.length_m * scale);
      const h = Math.min(110, room.width_m * scale);
      const isPriority = room.priority === "high" || room.priority === "urgent_attention";
      svgContent += `
        <g class="floor-plan-room ${isPriority ? 'is-priority' : ''}" data-room-id="${room.id}">
          <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${isPriority ? '#C1694F0d' : '#6B76540d'}" stroke="${isPriority ? '#C1694F' : '#6B7654'}" stroke-width="1.5" rx="3"/>
          <text x="${x + 8}" y="${y + 16}" font-family="IBM Plex Mono" font-size="10" fill="#2B2620">${escapeHtml(room.name)}</text>
          <text x="${x + 8}" y="${y + h - 8}" font-family="IBM Plex Mono" font-size="9" fill="#6b6252">${room.length_m}m × ${room.width_m}m</text>
        </g>`;
    });
    svg.innerHTML = svgContent;
    svg.querySelectorAll("[data-room-id]").forEach((el) => {
      el.addEventListener("click", () => (window.location.href = `/rooms/${el.dataset.roomId}`));
    });
  }

  let zoom = 1;
  function bindFloorplanControls() {
    const svg = document.getElementById("floorplan-svg");
    document.getElementById("floorplan-zoom-in")?.addEventListener("click", () => {
      zoom = Math.min(2, zoom + 0.2);
      svg.style.transform = `scale(${zoom})`;
      svg.style.transformOrigin = "top left";
    });
    document.getElementById("floorplan-zoom-out")?.addEventListener("click", () => {
      zoom = Math.max(0.5, zoom - 0.2);
      svg.style.transform = `scale(${zoom})`;
    });
    document.getElementById("floorplan-reset")?.addEventListener("click", () => {
      zoom = 1;
      svg.style.transform = "scale(1)";
    });
  }

  function renderDashboard() {
    document.getElementById("dashboard-home-name").textContent = currentHome.name;
    document.getElementById("dashboard-home-meta").textContent =
      `${titleCase(currentHome.home_type)} · ${currentHome.resident_count} resident(s) · ${(currentHome.rooms || []).length} room(s)`;

    const furnitureCount = (currentHome.rooms || []).reduce((sum, r) => sum + (r.furniture || []).length, 0);
    const applianceCount = (currentHome.rooms || []).reduce((sum, r) => sum + (r.appliances || []).length, 0);
    document.getElementById("dashboard-stats").innerHTML = `
      <div class="flex justify-between"><dt class="text-charcoal/60">Rooms</dt><dd class="font-mono">${(currentHome.rooms || []).length}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Furniture items</dt><dd class="font-mono">${furnitureCount}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Appliances</dt><dd class="font-mono">${applianceCount}</dd></div>
      <div class="flex justify-between"><dt class="text-charcoal/60">Main goals</dt><dd class="font-mono text-right">${(currentHome.main_goals || []).length}</dd></div>`;

    renderFloorPlan();
    bindFloorplanControls();

    document.getElementById("edit-profile-btn").addEventListener("click", () => {
      state = { step: 0, homeId: currentHome.id, profile: currentHome, goals: currentHome.main_goals || [] };
      saveState();
      document.getElementById("dashboard-view").classList.add("hidden");
      document.getElementById("wizard-view").classList.remove("hidden");
      renderStep();
    });
  }

  async function init() {
    document.getElementById("loading-state").classList.remove("hidden");
    try {
      const home = await apiGet("/api/home");
      document.getElementById("loading-state").classList.add("hidden");
      if (home && home.setup_completed) {
        currentHome = home;
        document.getElementById("dashboard-view").classList.remove("hidden");
        renderDashboard();
      } else {
        if (home) {
          state.homeId = home.id;
          state.profile = home;
          state.goals = home.main_goals || [];
          currentHome = home;
          if (state.step === 0) state.step = 1;
        }
        document.getElementById("wizard-view").classList.remove("hidden");
        renderStep();
        document.getElementById("wizard-next").addEventListener("click", onNext);
        document.getElementById("wizard-back").addEventListener("click", onBack);
      }
    } catch (err) {
      document.getElementById("loading-state").textContent = "Couldn't load your home. " + err.message;
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
