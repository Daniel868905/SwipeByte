export function installLogoutIntercept(base="/api/v1/users") {
  document.addEventListener("click", (ev) => {
    const a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    const href = a.getAttribute("href") || "";
    const url = new URL(href, window.location.origin);
    if (url.pathname === "/logout" || url.pathname === "/logout/") {
      ev.preventDefault();
      const token = localStorage.getItem("token") || sessionStorage.getItem("token") || "";
      fetch(`${base}/logout/`, {
        method: "POST",
        headers: token ? { Authorization: `Token ${token}` } : {},
      }).finally(() => {
        localStorage.removeItem("token");
        sessionStorage.removeItem("token");
        window.location.href = "/";
      });
    }
  }, true);
}
