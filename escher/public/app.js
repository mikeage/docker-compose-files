const grid = document.getElementById("grid");
const statusEl = document.getElementById("status");
const filterEl = document.getElementById("filter");
const reloadBtn = document.getElementById("reload");

let allItems = [];

function setStatus(msg) {
  statusEl.textContent = msg;
}

function clearGrid() {
  grid.innerHTML = "";
}

function render(items) {
  clearGrid();

  if (!items.length) {
    setStatus("No images match.");
    return;
  }

  setStatus(`${items.length} image(s)`);

  for (const item of items) {
    const tile = document.createElement("div");
    tile.className = "tile";

    const a = document.createElement("a");
    a.href = `/viewer.html?img=${encodeURIComponent(item.filename)}`;
    a.dataset.filename = item.filename;

    const img = document.createElement("img");
    img.className = "thumb";
    img.loading = "lazy";
    img.src = item.thumb;
    img.alt = item.filename;

    const cap = document.createElement("div");
    cap.className = "caption";

    const mp = item.pixels ? Math.round(item.pixels / 1_000_000) : 0;
    cap.textContent = item.filename;

    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = `${mp} MP · Deep Zoom`;

    cap.appendChild(badge);

    a.appendChild(img);
    tile.appendChild(a);
    tile.appendChild(cap);
    grid.appendChild(tile);
  }
}

async function loadManifest() {
  setStatus("Loading…");
  const res = await fetch("/manifest.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed manifest: ${res.status}`);
  const data = await res.json();
  allItems = data.items || [];
  applyFilter();
}

function applyFilter() {
  const q = (filterEl.value || "").trim().toLowerCase();
  const items = q
    ? allItems.filter((x) => x.filename.toLowerCase().includes(q))
    : allItems;
  render(items);
}

filterEl.addEventListener("input", () => applyFilter());
reloadBtn.addEventListener("click", async () => { await loadManifest(); });

loadManifest().catch((e) => {
  console.error(e);
  setStatus(`Error: ${e.message}`);
});

