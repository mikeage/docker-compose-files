import express from "express";
import fs from "fs";
import fsp from "fs/promises";
import path from "path";
import { execFile } from "child_process";
import sharp from "sharp";

const IMAGES_DIR = process.env.IMAGES_DIR || "/app/images";
const DATA_DIR = process.env.DATA_DIR || "/app/data";
const PORT = Number(process.env.PORT || 8080);

const THUMB_MAX = Number(process.env.THUMB_MAX || 320);
const MTIME_TOLERANCE_MS = Number(process.env.MTIME_TOLERANCE_MS || 2000);

const THUMBS_DIR = path.join(DATA_DIR, "thumbs");
const TILES_DIR = path.join(DATA_DIR, "tiles");
const MANIFEST_PATH = path.join(DATA_DIR, "manifest.json");

function isPng(name) {
  return name.toLowerCase().endsWith(".png");
}

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    execFile(cmd, args, { ...opts }, (err, stdout, stderr) => {
      if (err) {
        err.stdout = stdout;
        err.stderr = stderr;
        reject(err);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

async function ensureDirs() {
  await fsp.mkdir(DATA_DIR, { recursive: true });
  await fsp.mkdir(THUMBS_DIR, { recursive: true });
  await fsp.mkdir(TILES_DIR, { recursive: true });
}

async function listImagesWithStats() {
  const entries = await fsp.readdir(IMAGES_DIR, { withFileTypes: true });
  const files = entries
    .filter((e) => e.isFile() && isPng(e.name))
    .map((e) => e.name)
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

  const out = [];
  for (const name of files) {
    const p = path.join(IMAGES_DIR, name);
    const st = await fsp.stat(p);
    out.push({ name, path: p, mtimeMs: st.mtimeMs, size: st.size });
  }
  return out;
}

async function fileExists(p) {
  try {
    await fsp.access(p, fs.constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function getPngSizeViaVipsHeader(filePath) {
  const { stdout } = await run("vipsheader", ["-a", filePath]);

  let w = 0;
  let h = 0;
  for (const line of stdout.split("\n")) {
    const mW = line.match(/^\s*width:\s*(\d+)\s*$/i);
    const mH = line.match(/^\s*height:\s*(\d+)\s*$/i);
    if (mW) w = Number(mW[1]);
    if (mH) h = Number(mH[1]);
  }
  if (!w || !h) throw new Error("Unable to parse width/height from vipsheader");
  return { w, h };
}

function safeIdFromFilename(filename) {
  const base = filename.replace(/\.png$/i, "");
  return base.replace(/[^a-zA-Z0-9._-]+/g, "_");
}

async function ensureThumbnail(srcPath, srcMtimeMs, filename) {
  const thumbName = filename.replace(/\.png$/i, ".jpg");
  const thumbPath = path.join(THUMBS_DIR, thumbName);

  if (await fileExists(thumbPath)) {
    const st = await fsp.stat(thumbPath);
    const delta = st.mtimeMs - srcMtimeMs;

    console.log(
      `[thumb] check   ${filename}: srcMtime=${srcMtimeMs}, thumbMtime=${st.mtimeMs}, delta=${delta}ms`
    );

    if (st.mtimeMs >= srcMtimeMs - MTIME_TOLERANCE_MS) {
      console.log(`[thumb] reuse   ${filename} (within tolerance ${MTIME_TOLERANCE_MS}ms)`);
      return { thumbName, thumbPath, rebuilt: false };
    }

    console.log(
      `[thumb] rebuild ${filename} (thumb older than src beyond tolerance: delta=${delta}ms)`
    );
  } else {
    console.log(`[thumb] missing ${filename}, generating new thumbnail`);
  }

  // vips CLI compatibility approach:
  // 1) vips thumbnail INPUT TEMP.v --size both
  // 2) vips jpegsave TEMP.v OUTPUT.jpg --Q 82 --strip
  const tmpVips = path.join(THUMBS_DIR, `.${thumbName}.${process.pid}.v`);

  try {
    console.log(`[thumb] vips thumbnail+save ${filename} -> ${thumbName} (max=${THUMB_MAX})`);

    // create a small vips native temporary file
    await run("vips", [
      "thumbnail",
      srcPath,
      tmpVips,
      String(THUMB_MAX),
      "--size",
      "both"
    ]);

    // write jpeg with quality + strip metadata
    await run("vips", [
      "jpegsave",
      tmpVips,
      thumbPath,
      "--Q",
      "82",
      "--strip"
    ]);
  } catch (e) {
    console.warn(
      `[thumb] vips thumb pipeline failed for ${filename}, falling back to sharp: ${e?.message || e}`
    );
    await sharp(srcPath, { limitInputPixels: false })
      .resize({
        width: THUMB_MAX,
        height: THUMB_MAX,
        fit: "inside",
        withoutEnlargement: true
      })
      .jpeg({ quality: 82, mozjpeg: true })
      .toFile(thumbPath);
  } finally {
    await fsp.rm(tmpVips, { force: true }).catch(() => {});
  }

  try {
    const d = new Date(srcMtimeMs);
    await fsp.utimes(thumbPath, d, d);
    const stAfter = await fsp.stat(thumbPath);
    console.log(
      `[thumb] wrote   ${filename}: srcMtime=${srcMtimeMs}, thumbMtime=${stAfter.mtimeMs}, delta=${stAfter.mtimeMs - srcMtimeMs}ms`
    );
  } catch (e) {
    console.warn(`[thumb] utimes failed for ${filename}: ${e?.message || e}`);
  }

  return { thumbName, thumbPath, rebuilt: true };
}

async function removeDeepZoomOutputs(tileBasePath) {
  const dziPath = `${tileBasePath}.dzi`;
  const filesDir = `${tileBasePath}_files`;
  await fsp.rm(dziPath, { force: true }).catch(() => {});
  await fsp.rm(filesDir, { recursive: true, force: true }).catch(() => {});
}

async function ensureDeepZoomTiles(srcPath, srcMtimeMs, tileId, filename) {
  const tileBasePath = path.join(TILES_DIR, tileId);
  const dziPath = `${tileBasePath}.dzi`;

  if (await fileExists(dziPath)) {
    const st = await fsp.stat(dziPath);
    const delta = st.mtimeMs - srcMtimeMs;

    console.log(
      `[dzi]   check   ${filename}: srcMtime=${srcMtimeMs}, dziMtime=${st.mtimeMs}, delta=${delta}ms`
    );

    if (st.mtimeMs >= srcMtimeMs - MTIME_TOLERANCE_MS) {
      console.log(`[dzi]   reuse   ${filename} (within tolerance ${MTIME_TOLERANCE_MS}ms)`);
      return { dziUrl: `/tiles/${encodeURIComponent(tileId)}.dzi`, rebuilt: false };
    }

    console.log(
      `[dzi]   rebuild ${filename} (dzi older than src beyond tolerance: delta=${delta}ms)`
    );
  } else {
    console.log(`[dzi]   missing ${filename}, generating new Deep Zoom tiles`);
  }

  await removeDeepZoomOutputs(tileBasePath);

  console.log(
    `[dzi]   dzsave  ${filename} -> base=${tileBasePath} (tile-size=256, overlap=1)`
  );
  await run("vips", [
    "dzsave",
    srcPath,
    tileBasePath,
    "--tile-size",
    "256",
    "--overlap",
    "1",
    "--suffix",
    ".jpg[Q=85]"
  ]);

  try {
    const d = new Date(srcMtimeMs);
    await fsp.utimes(dziPath, d, d);
    const stAfter = await fsp.stat(dziPath);
    console.log(
      `[dzi]   wrote   ${filename}: srcMtime=${srcMtimeMs}, dziMtime=${stAfter.mtimeMs}, delta=${stAfter.mtimeMs - srcMtimeMs}ms`
    );
  } catch (e) {
    console.warn(`[dzi]   utimes failed for ${filename}: ${e?.message || e}`);
  }

  return { dziUrl: `/tiles/${encodeURIComponent(tileId)}.dzi`, rebuilt: true };
}

async function buildManifest() {
  console.log("============================================================");
  console.log("buildManifest: starting (mode=all-deepzoom)");
  console.log(`  IMAGES_DIR=${IMAGES_DIR}`);
  console.log(`  DATA_DIR=${DATA_DIR}`);
  console.log(`  THUMB_MAX=${THUMB_MAX}`);
  console.log(`  MTIME_TOLERANCE_MS=${MTIME_TOLERANCE_MS}`);

  await ensureDirs();

  const images = await listImagesWithStats();
  console.log(`buildManifest: found ${images.length} PNG file(s) in images dir`);

  const items = [];
  let thumbsRebuilt = 0;
  let tilesRebuilt = 0;

  for (const img of images) {
    const filename = img.name;
    const srcPath = img.path;

    console.log("------------------------------------------------------------");
    console.log(`Image: ${filename} (mtimeMs=${img.mtimeMs}, size=${img.size} bytes)`);

    let w, h;
    try {
      ({ w, h } = await getPngSizeViaVipsHeader(srcPath));
      console.log(`  Dimensions: ${w} x ${h}`);
    } catch (e) {
      console.warn(`  Skipping unreadable image: ${filename} (${e?.message || e})`);
      continue;
    }

    const pixels = w * h;
    console.log(`  Pixels: ${pixels} (${Math.round(pixels / 1_000_000)} MP)`);

    const t = await ensureThumbnail(srcPath, img.mtimeMs, filename);
    if (t.rebuilt) thumbsRebuilt++;

    const tileId = safeIdFromFilename(filename);
    const dz = await ensureDeepZoomTiles(srcPath, img.mtimeMs, tileId, filename);
    if (dz.rebuilt) tilesRebuilt++;

    items.push({
      filename,
      url: `/images/${encodeURIComponent(filename)}`,
      thumb: `/thumbs/${encodeURIComponent(t.thumbName)}`,
      w,
      h,
      pixels,
      mtimeMs: img.mtimeMs,
      size: img.size,
      type: "deepzoom",
      tileId,
      dzi: dz.dziUrl,
      view: `/viewer.html?img=${encodeURIComponent(filename)}`
    });

    console.log(`  Manifest entry: type=deepzoom, tileId=${tileId}, dzi=${dz.dziUrl}`);
  }

  const manifest = {
    generatedAt: new Date().toISOString(),
    thresholds: { mode: "all-deepzoom" },
    counts: { total: items.length, thumbsRebuilt, tilesRebuilt },
    items
  };

  await fsp.writeFile(MANIFEST_PATH, JSON.stringify(manifest, null, 2));
  console.log(`buildManifest: wrote manifest ${MANIFEST_PATH}`);
  console.log(`buildManifest: total=${items.length}, thumbsRebuilt=${thumbsRebuilt}, tilesRebuilt=${tilesRebuilt}`);
  console.log("============================================================");
}

let server;

async function main() {
  await buildManifest();

  const app = express();

  app.use("/", express.static(path.join("/app", "public"), { extensions: ["html"] }));

  app.get("/manifest.json", async (_req, res) => {
    try {
      const data = await fsp.readFile(MANIFEST_PATH, "utf-8");
      res.type("json").send(data);
    } catch {
      res.status(500).json({ error: "manifest missing" });
    }
  });

  app.use("/thumbs", express.static(THUMBS_DIR, { maxAge: "7d", immutable: true }));
  app.use("/tiles", express.static(TILES_DIR, { maxAge: "7d", immutable: true }));
  app.use("/images", express.static(IMAGES_DIR, { maxAge: "1d" }));

  app.post("/rebuild", async (_req, res) => {
    try {
      await buildManifest();
      res.json({ ok: true });
    } catch (e) {
      res.status(500).json({ ok: false, error: e?.message || String(e) });
    }
  });

  server = app.listen(PORT, "0.0.0.0", () => {
    console.log(`Gallery running on http://0.0.0.0:${PORT}`);
  });
}

function gracefulShutdown(signal) {
  console.log(`Received ${signal}, shutting down HTTP server...`);
  if (!server) {
    process.exit(0);
    return;
  }
  server.close(() => {
    console.log("HTTP server closed, exiting.");
    process.exit(0);
  });
  setTimeout(() => {
    console.warn("Force exit after timeout.");
    process.exit(0);
  }, 5000).unref();
}

process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
process.on("SIGINT", () => gracefulShutdown("SIGINT"));

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
