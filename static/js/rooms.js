(() => {
  const { apiGet, apiPost, apiDelete, showToast, openModal, confirmAction, escapeHtml, titleCase } = HomeHub;

  const ROOM_TYPES = [
    "living_room", "bedroom", "kitchen", "bathroom", "dining_room", "home_office", "study",
    "balcony", "hallway", "storage_room", "laundry_room", "guest_room", "kids_room",
    "outdoor_area", "other",
  ];

  let homeId = null;
  let rooms = [];

  const statusBadge = (room) => {
    const problems = room.current_problems || [];
    if (problems.length) return `<span class="text-xs font-mono bg-amber/15 text-amber px-2 py-0.5 rounded">Needs review</span>`;
    return `<span class="text-xs font-mono bg-olive/15 text-olive px-2 py-0.5 rounded">Ready</span>`;
  };

  function renderRooms() {
    const grid = document.getElementById("rooms-grid");
    const empty = document.getElementById("rooms-empty");
    if (!rooms.length) {
      grid.innerHTML = "";
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");
    grid.innerHTML = rooms.map((room) => `
      <div class="blueprint-frame border border-taupe/60 rounded-xl p-5 flex flex-col ${room.priority === 'high' || room.priority === 'urgent_attention' ? 'ring-1 ring-terracotta/40' : ''}">
        <div class="flex items-start justify-between mb-2">
          <h3 class="font-semibold">${escapeHtml(room.name)}</h3>
          ${statusBadge(room)}
        </div>
        <p class="text-sm text-charcoal/60 mb-1">${titleCase(room.room_type)}</p>
        <p class="text-xs font-mono text-charcoal/50 mb-3">${room.length_m}m × ${room.width_m}m · ${(room.furniture || []).length} furniture · ${(room.appliances || []).length} appliances</p>
        ${(room.current_problems || []).length ? `<p class="text-xs text-terracotta/80 mb-3">${escapeHtml(room.current_problems[0])}</p>` : ""}
        <div class="mt-auto flex items-center gap-2 pt-3 border-t border-taupe/40">
          <a href="/rooms/${room.id}" class="text-sm font-medium text-olive hover:underline">Open →</a>
          <button class="ml-auto text-xs text-charcoal/50 hover:text-charcoal" data-duplicate="${room.id}">Duplicate</button>
          <button class="text-xs text-terracotta hover:underline" data-delete="${room.id}">Delete</button>
        </div>
      </div>`).join("");

    grid.querySelectorAll("[data-duplicate]").forEach((btn) =>
      btn.addEventListener("click", () => duplicateRoom(btn.dataset.duplicate))
    );
    grid.querySelectorAll("[data-delete]").forEach((btn) =>
      btn.addEventListener("click", () => deleteRoom(btn.dataset.delete))
    );
  }

  async function duplicateRoom(roomId) {
    try {
      await apiPost(`/api/rooms/${roomId}/duplicate`);
      showToast("Room duplicated", "success");
      await load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function deleteRoom(roomId) {
    const ok = await confirmAction("This will permanently delete the room and everything in it.");
    if (!ok) return;
    try {
      await apiDelete(`/api/rooms/${roomId}`);
      showToast("Room deleted", "success");
      await load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  function openAddRoomModal() {
    if (!homeId) {
      showToast("Create your home profile first.", "warning");
      window.location.href = "/home";
      return;
    }
    const close = openModal(`
      <form id="add-room-form" class="p-6">
        <h2 class="font-display text-xl mb-4">Add a room</h2>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium">Room name</span>
            <input required name="name" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          <label class="block"><span class="text-sm font-medium">Room type</span>
            <select name="room_type" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
              ${ROOM_TYPES.map((t) => `<option value="${t}">${titleCase(t)}</option>`).join("")}
            </select></label>
          <div class="grid grid-cols-2 gap-4">
            <label class="block"><span class="text-sm font-medium">Length (m)</span>
              <input type="number" step="0.1" min="0.1" name="length_m" value="4" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
            <label class="block"><span class="text-sm font-medium">Width (m)</span>
              <input type="number" step="0.1" min="0.1" name="width_m" value="3" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          </div>
          <label class="block"><span class="text-sm font-medium">Priority</span>
            <select name="priority" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
              <option value="low">Low</option><option value="medium" selected>Medium</option><option value="high">High</option>
            </select></label>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-full text-sm font-medium bg-charcoal text-ivory hover:bg-olive">Add Room</button>
        </div>
      </form>`);
    document.querySelector("[data-cancel]").addEventListener("click", close);
    document.getElementById("add-room-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      try {
        await apiPost("/api/rooms", {
          home_id: homeId,
          name: form.get("name"),
          room_type: form.get("room_type"),
          length_m: parseFloat(form.get("length_m")),
          width_m: parseFloat(form.get("width_m")),
          priority: form.get("priority"),
        });
        close();
        showToast("Room added", "success");
        await load();
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  }

  async function load() {
    try {
      const home = await apiGet("/api/home");
      if (!home) {
        homeId = null;
        rooms = [];
        renderRooms();
        return;
      }
      homeId = home.id;
      rooms = home.rooms || [];
      renderRooms();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("add-room-open").addEventListener("click", openAddRoomModal);
    document.getElementById("add-room-open-empty").addEventListener("click", openAddRoomModal);
    load();
  });
})();
