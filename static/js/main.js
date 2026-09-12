/* Shared utilities used across every page: API fetch wrapper, toasts, modals, nav. */

const HomeHub = (() => {
  async function request(method, path, body) {
    const opts = { method, headers: {} };
    if (body !== undefined) {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    let res;
    try {
      res = await fetch(path, opts);
    } catch (err) {
      throw new Error("Network error. Check your connection and try again.");
    }
    if (res.status === 204) return null;
    let data = null;
    try {
      data = await res.json();
    } catch (err) {
      data = null;
    }
    if (!res.ok) {
      const detail = (data && (data.detail || data.message)) || `Request failed (${res.status}).`;
      const message = typeof detail === "string" ? detail : JSON.stringify(detail);
      throw new Error(message);
    }
    return data;
  }

  const apiGet = (path) => request("GET", path);
  const apiPost = (path, body) => request("POST", path, body ?? {});
  const apiPut = (path, body) => request("PUT", path, body ?? {});
  const apiDelete = (path) => request("DELETE", path);

  function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const colors = {
      info: "bg-charcoal text-ivory",
      success: "bg-olive text-ivory",
      error: "bg-terracotta text-ivory",
      warning: "bg-amber text-ivory",
    };
    const el = document.createElement("div");
    el.className = `toast rounded-lg shadow-lg px-4 py-3 text-sm font-medium ${colors[type] || colors.info}`;
    el.setAttribute("role", "status");
    el.textContent = message;
    container.appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transition = "opacity 0.3s ease";
      setTimeout(() => el.remove(), 300);
    }, 3800);
  }

  function openModal(html, { onClose } = {}) {
    const root = document.getElementById("modal-root");
    root.innerHTML = `
      <div class="modal-backdrop fixed inset-0 bg-charcoal/40 z-50 flex items-end sm:items-center justify-center p-0 sm:p-6" data-modal-backdrop>
        <div class="bg-ivory w-full sm:max-w-lg sm:rounded-2xl rounded-t-2xl shadow-xl max-h-[92vh] overflow-y-auto" role="dialog" aria-modal="true" data-modal-panel>
          ${html}
        </div>
      </div>`;
    const backdrop = root.querySelector("[data-modal-backdrop]");
    const close = () => {
      root.innerHTML = "";
      document.removeEventListener("keydown", escHandler);
      if (onClose) onClose();
    };
    const escHandler = (e) => {
      if (e.key === "Escape") close();
    };
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) close();
    });
    document.addEventListener("keydown", escHandler);
    const focusable = root.querySelector("input, textarea, select, button");
    if (focusable) focusable.focus();
    return close;
  }

  function confirmAction(message) {
    return new Promise((resolve) => {
      const close = openModal(`
        <div class="p-6">
          <h2 class="font-display text-xl mb-2">Are you sure?</h2>
          <p class="text-sm text-charcoal/70 mb-6">${message}</p>
          <div class="flex justify-end gap-3">
            <button type="button" class="px-4 py-2 rounded-full text-sm font-medium border border-taupe hover:bg-stone" data-cancel>Cancel</button>
            <button type="button" class="px-4 py-2 rounded-full text-sm font-medium bg-terracotta text-ivory hover:opacity-90" data-confirm>Delete</button>
          </div>
        </div>`);
      document.querySelector("[data-cancel]").addEventListener("click", () => {
        close();
        resolve(false);
      });
      document.querySelector("[data-confirm]").addEventListener("click", () => {
        close();
        resolve(true);
      });
    });
  }

  function initNav() {
    const btn = document.getElementById("mobile-menu-btn");
    const menu = document.getElementById("mobile-menu");
    if (btn && menu) {
      btn.addEventListener("click", () => {
        const isOpen = !menu.classList.contains("hidden");
        menu.classList.toggle("hidden");
        btn.setAttribute("aria-expanded", String(!isOpen));
      });
    }
    const header = document.getElementById("site-header");
    if (header) {
      const scrolledClasses = (header.dataset.scrolledClass || "").split(" ").filter(Boolean);
      const onScroll = () => {
        const scrolled = window.scrollY > 8;
        scrolledClasses.forEach((c) => header.classList.toggle(c, scrolled));
      };
      document.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  }

  function draft(key, value) {
    if (value === undefined) {
      const raw = localStorage.getItem(`aihh:${key}`);
      return raw ? JSON.parse(raw) : null;
    }
    localStorage.setItem(`aihh:${key}`, JSON.stringify(value));
  }

  function clearDraft(key) {
    localStorage.removeItem(`aihh:${key}`);
  }

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function titleCase(str) {
    return (str || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  }

  document.addEventListener("DOMContentLoaded", initNav);

  return { apiGet, apiPost, apiPut, apiDelete, showToast, openModal, confirmAction, draft, clearDraft, escapeHtml, titleCase };
})();
