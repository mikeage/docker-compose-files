const params = new URLSearchParams(location.search);
const filename = params.get("img");

const nameEl = document.getElementById("name");
const openOriginalBtn = document.getElementById("openOriginal");

if (!filename) {
  nameEl.textContent = "Missing ?img=";
  throw new Error("Missing img parameter");
}

nameEl.textContent = filename;

async function loadManifest() {
  const res = await fetch("/manifest.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed manifest: ${res.status}`);
  return res.json();
}

function initOsd(item) {
  if (!item?.dzi) {
    throw new Error("This image does not have Deep Zoom tiles.");
  }

  openOriginalBtn.addEventListener("click", () => {
    window.open(item.url, "_blank", "noopener,noreferrer");
  });

  OpenSeadragon({
    id: "osd",
    prefixUrl: "https://unpkg.com/openseadragon@4/build/openseadragon/images/",
    tileSources: item.dzi,
    showNavigator: true,
    navigatorPosition: "BOTTOM_RIGHT",
    animationTime: 0.25,
    blendTime: 0.1,
    maxZoomPixelRatio: 2,
    minZoomImageRatio: 0.9,
    zoomPerScroll: 1.2,
    gestureSettingsMouse: {
      clickToZoom: true,
      dblClickToZoom: true,
      flickEnabled: true,
      scrollToZoom: true
    }
  });
}

(async () => {
  const manifest = await loadManifest();
  const item = (manifest.items || []).find(x => x.filename === filename);

  if (!item) {
    nameEl.textContent = `Not found: ${filename}`;
    openOriginalBtn.disabled = true;
    return;
  }

  initOsd(item);
})().catch((e) => {
  console.error(e);
  nameEl.textContent = `Error: ${e.message}`;
  openOriginalBtn.disabled = true;
});

