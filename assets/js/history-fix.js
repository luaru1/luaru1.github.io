window.addEventListener("hashchange", () => {
  const targetId = location.hash.substring(1);
  const target = document.getElementById(targetId);
  if (target) {
    target.scrollIntoView({ behavior: "smooth" });
  }
});