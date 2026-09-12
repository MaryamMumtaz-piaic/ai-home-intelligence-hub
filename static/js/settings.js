(() => {
  const { apiGet, apiDelete, showToast, confirmAction } = HomeHub;
  let home = null;

  async function downloadJson() {
    if (!home) {
      showToast("No home profile to export yet.", "warning");
      return;
    }
    const blob = new Blob([JSON.stringify(home, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${(home.name || "home").replace(/\s+/g, "-").toLowerCase()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    showToast("Home profile downloaded", "success");
  }

  async function deleteHome() {
    if (!home) return;
    const ok = await confirmAction("This permanently deletes your home profile and everything in it. This cannot be undone.");
    if (!ok) return;
    try {
      await apiDelete(`/api/home/${home.id}`);
      showToast("Home profile deleted", "success");
      window.location.href = "/";
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  document.addEventListener("DOMContentLoaded", async () => {
    home = await apiGet("/api/home");
    document.getElementById("download-json").addEventListener("click", downloadJson);
    document.getElementById("delete-home-btn").addEventListener("click", deleteHome);
  });
})();
