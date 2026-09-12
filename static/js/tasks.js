(() => {
  const { apiGet, apiPost, apiPut, apiDelete, showToast, openModal, confirmAction, escapeHtml, titleCase } = HomeHub;

  let homeId = null;
  let tasks = [];
  let view = "roadmap";

  function bucketFor(task) {
    if (!task.due_date) {
      if (task.priority === "urgent_attention" || task.priority === "high") return "This Week";
      return "Later";
    }
    const due = new Date(task.due_date);
    const now = new Date();
    const days = (due - now) / 86400000;
    if (days <= 1) return "Today";
    if (days <= 7) return "This Week";
    if (days <= 30) return "This Month";
    return "Later";
  }

  function taskCard(task) {
    return `
      <div class="border border-taupe/60 rounded-lg p-4 bg-white/50 ${task.status === 'completed' ? 'opacity-60' : ''}" data-task-id="${task.id}">
        <div class="flex items-start justify-between mb-1">
          <p class="font-medium text-sm">${escapeHtml(task.title)}</p>
          <button class="text-xs text-terracotta hover:underline" data-delete-task="${task.id}">✕</button>
        </div>
        <p class="text-xs text-charcoal/50 mb-2">${titleCase(task.priority)} · ${titleCase(task.status)}</p>
        ${task.description ? `<p class="text-xs text-charcoal/60 mb-2">${escapeHtml(task.description)}</p>` : ""}
        <div class="flex gap-2 text-xs">
          ${task.status !== "completed" ? `<button class="text-olive hover:underline" data-complete-task="${task.id}">Mark complete</button>` : `<button class="text-charcoal/60 hover:underline" data-reopen-task="${task.id}">Reopen</button>`}
        </div>
      </div>`;
  }

  function renderRoadmap() {
    const buckets = { Today: [], "This Week": [], "This Month": [], Later: [] };
    tasks.filter((t) => t.status !== "archived").forEach((t) => buckets[bucketFor(t)].push(t));
    const container = document.getElementById("roadmap-view");
    container.innerHTML = Object.entries(buckets).map(([name, items]) => `
      <div>
        <h2 class="font-semibold text-sm uppercase tracking-wide text-charcoal/60 mb-3">${name}</h2>
        <div class="space-y-3">${items.map(taskCard).join("") || `<p class="text-xs text-charcoal/40">Nothing here.</p>`}</div>
      </div>`).join("");
    bindTaskActions();
  }

  function renderList() {
    const container = document.getElementById("list-view");
    container.innerHTML = tasks.map((t) => `
      <div class="flex items-center justify-between border border-taupe/50 rounded-lg px-4 py-3" data-task-id="${t.id}">
        <div>
          <p class="font-medium text-sm">${escapeHtml(t.title)}</p>
          <p class="text-xs text-charcoal/50">${titleCase(t.priority)} · ${titleCase(t.status)}${t.room_id ? " · Room" : ""}${t.due_date ? " · Due " + t.due_date : ""}</p>
        </div>
        <div class="flex gap-3 text-xs">
          ${t.status !== "completed" ? `<button class="text-olive hover:underline" data-complete-task="${t.id}">Complete</button>` : `<button class="text-charcoal/60 hover:underline" data-reopen-task="${t.id}">Reopen</button>`}
          <button class="text-terracotta hover:underline" data-delete-task="${t.id}">Delete</button>
        </div>
      </div>`).join("");
    bindTaskActions();
  }

  function bindTaskActions() {
    document.querySelectorAll("[data-complete-task]").forEach((btn) =>
      btn.addEventListener("click", () => updateStatus(btn.dataset.completeTask, "completed"))
    );
    document.querySelectorAll("[data-reopen-task]").forEach((btn) =>
      btn.addEventListener("click", () => updateStatus(btn.dataset.reopenTask, "todo"))
    );
    document.querySelectorAll("[data-delete-task]").forEach((btn) =>
      btn.addEventListener("click", () => deleteTask(btn.dataset.deleteTask))
    );
  }

  async function updateStatus(id, status) {
    try {
      await apiPut(`/api/tasks/${id}`, { status });
      showToast(status === "completed" ? "Task completed" : "Task reopened", "success");
      await load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function deleteTask(id) {
    if (!(await confirmAction("Delete this task?"))) return;
    try {
      await apiDelete(`/api/tasks/${id}`);
      showToast("Task deleted", "success");
      await load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  function renderEmptyState() {
    const empty = document.getElementById("tasks-empty");
    empty.classList.toggle("hidden", tasks.length !== 0);
    document.getElementById("roadmap-view").classList.toggle("hidden", tasks.length === 0 || view !== "roadmap");
    document.getElementById("list-view").classList.toggle("hidden", tasks.length === 0 || view !== "list");
  }

  function openAddTaskModal() {
    if (!homeId) {
      showToast("Create your home profile first.", "warning");
      return;
    }
    const close = openModal(`
      <form id="task-form" class="p-6">
        <h2 class="font-display text-xl mb-4">Add a task</h2>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium">Title</span><input required name="title" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          <label class="block"><span class="text-sm font-medium">Description (optional)</span><textarea name="description" rows="2" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></textarea></label>
          <div class="grid grid-cols-2 gap-4">
            <label class="block"><span class="text-sm font-medium">Priority</span>
              <select name="priority" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5">
                <option value="low">Low</option><option value="medium" selected>Medium</option><option value="high">High</option><option value="urgent_attention">Urgent Attention</option>
              </select></label>
            <label class="block"><span class="text-sm font-medium">Due date (optional)</span><input type="date" name="due_date" class="mt-1.5 w-full border border-taupe rounded-lg px-3 py-2.5"></label>
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Cancel</button>
          <button type="submit" class="px-4 py-2 rounded-full text-sm font-medium bg-charcoal text-ivory hover:bg-olive">Add Task</button>
        </div>
      </form>`);
    document.querySelector("[data-cancel]").addEventListener("click", close);
    document.getElementById("task-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      try {
        await apiPost("/api/tasks", {
          home_id: homeId,
          title: form.get("title"),
          description: form.get("description") || null,
          priority: form.get("priority"),
          due_date: form.get("due_date") || null,
        });
        close();
        showToast("Task added", "success");
        await load();
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  }

  async function load() {
    const home = await apiGet("/api/home");
    if (!home) {
      document.getElementById("tasks-empty").classList.remove("hidden");
      return;
    }
    homeId = home.id;
    tasks = await apiGet(`/api/tasks?home_id=${homeId}`);
    renderEmptyState();
    if (view === "roadmap") renderRoadmap();
    else renderList();
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("add-task-open").addEventListener("click", openAddTaskModal);
    document.querySelectorAll(".view-tab").forEach((tab) =>
      tab.addEventListener("click", () => {
        view = tab.dataset.view;
        document.querySelectorAll(".view-tab").forEach((t) => {
          t.classList.toggle("bg-charcoal", t === tab);
          t.classList.toggle("text-ivory", t === tab);
        });
        renderEmptyState();
        if (view === "roadmap") renderRoadmap();
        else renderList();
      })
    );
    load();
  });
})();
