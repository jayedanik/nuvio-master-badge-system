const RAW_BASE = "https://raw.githubusercontent.com/jayedanik/nuvio-master-badge-system/main/";

const THEME_GLOWS = {
  "gta6-vice-sunset": ["#ff3e9d", "#ff9e44"],
  "washi-tape": ["#d97706", "#16a34a"],
  "liquid-glass": ["#2997ff", "#a855f7"],
  "manga-halftone": ["#ef4444", "#facc15"],
  "holo-prism": ["#38bdf8", "#ec4899"],
  "stained-glass": ["#e11d48", "#38bdf8"],
  "comic-bubble": ["#38bdf8", "#facc15"],
  "zine-cutout": ["#facc15", "#ec4899"],
  "matrix-terminal": ["#22c55e", "#10b981"],
  "sticky-note": ["#facc15", "#fb923c"],
  "bauhaus-split": ["#f59e0b", "#3b82f6"],
  "titanium-chrome": ["#94a3b8", "#e2e8f0"],
  "live-tv-broadcast": ["#ef4444", "#f97316"],
  "enamel-pins": ["#fbbf24", "#7c3aed"],
  "criterion-leather": ["#d97706", "#78350f"],
  "cinema-ticket": ["#f59e0b", "#b45309"],
  "clapperboard": ["#e2e8f0", "#475569"],
  "vhs-tape": ["#f97316", "#ec4899"],
  "neotokyo-tag": ["#06b6d4", "#f43f5e"],
  "audiophile-vfd": ["#22d3ee", "#0284c7"],
  "gmk-keycaps": ["#94a3b8", "#38bdf8"],
  "rgb-keycaps": ["#ec4899", "#22d3ee"],
  "studio-markers": ["#3b82f6", "#60a5fa"],
  "pristine": ["#38bdf8", "#a855f7"]
};

const THEMES = [
  { id: "gta6-vice-sunset", name: "GTA 6 Vice City Sunset", cat: "pop", json: "gta6-vice-sunset.json", dir: "themes/gta6-vice-sunset/badges", desc: "Miami sunset skies with glowing sun discs, palm silhouettes & heavy stroked GTA typography." },
  { id: "washi-tape", name: "Artisan Japanese Washi Tape", cat: "craft", json: "washi-tape.json", dir: "themes/washi-tape/badges", desc: "Handmade mulberry fiber paper rolls with deckled torn edges, gold leaf hot-stamping & 3D drop shadows." },
  { id: "liquid-glass", name: "Apple VisionOS Liquid Glass", cat: "tech", json: "liquid-glass.json", dir: "themes/liquid-glass/badges", desc: "WWDC25 droplet optics with 3D convex liquid meniscus curvature, caustic refraction & smoked translucent core." },
  { id: "manga-halftone", name: "Anime / Manga Halftone Ink", cat: "pop", json: "manga-halftone.json", dir: "themes/manga-halftone/badges", desc: "Bold Japanese manga ink panels with Ben-Day halftone dots, hard offset shadows & vibrant accent bars." },
  { id: "holo-prism", name: "Iridescent Holographic Prism", cat: "tech", json: "holo-prism.json", dir: "themes/holo-prism/badges", desc: "Dark obsidian glass cores framed by rainbow holographic foil rims & iridescent prism shimmer." },
  { id: "stained-glass", name: "Stained Glass Mosaic", cat: "craft", json: "stained-glass.json", dir: "themes/stained-glass/badges", desc: "Jewel-toned cathedral stained glass shards framed by bold black lead-came lines." },
  { id: "comic-bubble", name: "Comic Book Speech Bubble", cat: "pop", json: "comic-bubble.json", dir: "themes/comic-bubble/badges", desc: "Pop comic speech bubbles with tails, thick black ink outlines & hard offset shadows." },
  { id: "zine-cutout", name: "Streetwear Zine Cutout", cat: "pop", json: "zine-cutout.json", dir: "themes/zine-cutout/badges", desc: "Tilted punk streetwear paper-cut collage strips with highlighter pop colors & brutalist ink." },
  { id: "matrix-terminal", name: "Matrix Terminal >_", cat: "pop", json: "matrix-terminal.json", dir: "themes/matrix-terminal/badges", desc: "Phosphor-green hacker console frames with >_ command prompt prefixes." },
  { id: "sticky-note", name: "Peeled Sticky Note", cat: "craft", json: "sticky-note.json", dir: "themes/sticky-note/badges", desc: "Post-It paper sticky notes with folded bottom-right corner flaps & crisp ink." },
  { id: "bauhaus-split", name: "Swiss Bauhaus Split-Block", cat: "tech", json: "bauhaus-split.json", dir: "themes/bauhaus-split/badges", desc: "Matte cream hardware blocks with solid Swiss Bauhaus color-blocks & geometric punch-dots." },
  { id: "titanium-chrome", name: "Brushed Titanium / Chrome Pill", cat: "tech", json: "titanium-chrome.json", dir: "themes/titanium-chrome/badges", desc: "Machined silver-chrome metallic capsules with specular sheen & engraved dark ink lettering." },
  { id: "live-tv-broadcast", name: "Live TV & Sports Broadcast", cat: "minimal", json: "live-tv-broadcast.json", dir: "themes/live-tv-broadcast/badges", desc: "Dedicated zero-background borderless broadcast typography curated for Live TV, IPTV & Sports streams." },
  { id: "enamel-pins", name: "Cloisonné Enamel & Gold Pins", cat: "craft", json: "enamel-pins.json", dir: "themes/enamel-pins/badges", desc: "Jewelry-grade cast brass bezel with cloisonné enamel fill & Roman engraving." },
  { id: "criterion-leather", name: "Criterion Archival Leather", cat: "craft", json: "criterion-leather.json", dir: "themes/criterion-leather/badges", desc: "Gilded archival Moroccan leather bookbinding with gold leaf hot-stamping." },
  { id: "cinema-ticket", name: "Golden Age Cinema Ticket", cat: "craft", json: "cinema-ticket.json", dir: "themes/cinema-ticket/badges", desc: "Perforated vintage admission ticket stubs with starburst punches." },
  { id: "clapperboard", name: "Hollywood Director Clapperboard", cat: "craft", json: "clapperboard.json", dir: "themes/clapperboard/badges", desc: "Matte slate chalkboard with diagonal sound-sync chevrons." },
  { id: "vhs-tape", name: "1980s Retro VHS Tape", cat: "craft", json: "vhs-tape.json", dir: "themes/vhs-tape/badges", desc: "Aged matte paper cassette label with 80s rainbow stripes & barcodes." },
  { id: "neotokyo-tag", name: "NeoTokyo Cyberpunk Asset Tag", cat: "pop", json: "neotokyo-tag.json", dir: "themes/neotokyo-tag/badges", desc: "Weathered industrial machinery asset tag with stencil legends." },
  { id: "audiophile-vfd", name: "Hi-Fi Vacuum Tube VFD", cat: "tech", json: "audiophile-vfd.json", dir: "themes/audiophile-vfd/badges", desc: "Cyan phosphor vacuum tube instrument monospace display." },
  { id: "gmk-keycaps", name: "GMK Custom Mechanical Keycaps", cat: "tech", json: "gmk-keycaps.json", dir: "themes/gmk-keycaps/badges", desc: "Double-shot PBT spherical Cherry profile DIN standard keycaps." },
  { id: "rgb-keycaps", name: "Cyberpunk RGB Keycaps", cat: "tech", json: "rgb-keycaps.json", dir: "themes/rgb-keycaps/badges", desc: "Translucent pudding keycaps with neon RGB underglow." },
  { id: "studio-markers", name: "StreamBridge Studio Markers", cat: "tech", json: "studio-markers.json", dir: "themes/studio-markers/badges", desc: "Condensed technical studio monitor markers with crisp edge framing." },
  { id: "pristine", name: "Pristine Master (Default)", cat: "minimal", json: "badges.json", dir: "badges", desc: "Clean OLED floating vector sans-serif master badges with zero background." }
];

const FLAGSHIPS = [
  { idx: 0, tab: "GTA 6 Vice Sunset", kicker: "NEW DROP • VICE CITY EDITION" },
  { idx: 2, tab: "VisionOS Liquid Glass", kicker: "SPATIAL OPTICS • WWDC25" },
  { idx: 1, tab: "Japanese Washi Tape", kicker: "ARTISAN CRAFT • MULBERRY FIBER" },
  { idx: 3, tab: "Anime / Manga Ink", kicker: "POP CULTURE • BEN-DAY HALFTONE" }
];

const LIVE_TITLES = [
  {
    title: "Superman",
    meta: "2025 · 2160p UHD BluRay REMUX · Real-Debrid · 72.1 GB",
    release: "Superman.2025.2160p.UHD.BluRay.REMUX.DV.TrueHD.7.1.Atmos.IMAX.HEVC.10bit.MKV",
    badges: ["4k", "remux", "dolby-vision", "dolby-atmos", "warnerbros", "english-flag"]
  },
  {
    title: "Avatar: Fire and Ash",
    meta: "2025 · 2160p IMAX UHD REMUX · Real-Debrid · 84.0 GB",
    release: "Avatar.Fire.and.Ash.2025.2160p.UHD.BluRay.REMUX.DV.Atmos.IMAX.HEVC.MKV",
    badges: ["4k", "remux", "dolby-vision", "dolby-atmos", "imax", "english-flag"]
  },
  {
    title: "Mission: Impossible – The Final Reckoning",
    meta: "2025 · 2160p UHD REMUX · TorBox · 78.6 GB",
    release: "Mission.Impossible.The.Final.Reckoning.2025.2160p.UHD.REMUX.HDR10Plus.Atmos.IMAX.MKV",
    badges: ["4k", "remux", "hdr10plus", "dolby-atmos", "paramount_studio", "english-flag"]
  },
  {
    title: "Severance · S02E10",
    meta: "2025 · 2160p ATVP WEB-DL · Real-Debrid · 6.4 GB",
    release: "Severance.S02E10.2025.2160p.ATVP.WEB-DL.DDP5.1.Atmos.DV.H265.English.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "appletv", "english-flag"]
  },
  {
    title: "The Fantastic Four: First Steps",
    meta: "2025 · 2160p DSNP WEB-DL · TorBox · 18.4 GB",
    release: "The.Fantastic.Four.First.Steps.2025.2160p.DSNP.WEB-DL.DV.Atmos.IMAX.H265.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "disney", "english-flag"]
  },
  {
    title: "Solo Leveling · S02E13",
    meta: "2025 · 1080p CR WEB-DL · Dual-Audio · 1.8 GB",
    release: "[SubsPlease] Solo Leveling S2 - 13 (2025) (1080p) [Dual-Audio] [Crunchyroll] [AV1].mkv",
    badges: ["1080p", "web-dl", "av1", "dual", "crunchyroll", "english-flag"]
  },
  {
    title: "Andor · S02E12",
    meta: "2025 · 2160p DSNP WEB-DL · Real-Debrid · 5.8 GB",
    release: "Andor.S02E12.2025.2160p.DSNP.WEB-DL.DV.Atmos.H265.English.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "cached", "english-flag"]
  },
  {
    title: "Formula 1 · Monaco Grand Prix",
    meta: "2026 · Live Sports Feed · 1080p 60 FPS",
    release: "F1.Grand.Prix.2026.Live.1080p.60fps.HDTV.AAC.English.TS",
    badges: ["live", "1080p", "60fps", "hevc", "cached", "english-flag"]
  }
];

function getBadgesForTheme(theme, titleObj) {
  if (theme.id === "live-tv-broadcast") {
    return ["live", "4k", "1080p", "60fps", "hevc", "english-flag"];
  }
  return titleObj.badges;
}

const TIER_SAMPLES = [
  "4k", "remux", "dolby-vision", "dolby-atmos", "imax", "cached", "live",
  "1080p", "web-dl", "bluray", "hdr10plus", "truehd", "5.1", "av1",
  "netflix", "appletv", "hulu", "crunchyroll", "warnerbros", "universal", "a24", "ghibli",
  "bangladesh-flag", "english-flag", "japanese", "korean"
];
const CAT_LABELS = { pop: "Pop Culture", craft: "Physical & Craft", tech: "Hardware & Tech", minimal: "Minimal" };

const gridEl = document.getElementById("theme-grid");
const emptyEl = document.getElementById("empty-state");
const searchEl = document.getElementById("hero-search");
const sortEl = document.getElementById("sort-select");
const savedCountEl = document.getElementById("saved-count");

const simLayer0 = document.getElementById("cinema-layer-0");
const simLayer1 = document.getElementById("cinema-layer-1");
const simMovieTitleEl = document.getElementById("sim-movie-title");
const simMovieMetaEl = document.getElementById("sim-movie-meta");
const simActiveNameEl = document.getElementById("sim-active-name");
const simCounterEl = document.getElementById("sim-counter");
const simCopyBtn = document.getElementById("sim-copy-btn");
const simInspectBtn = document.getElementById("sim-inspect-btn");
const simAutoBtn = document.getElementById("sim-auto-btn");
const simPrevBtn = document.getElementById("sim-prev-btn");
const simNextBtn = document.getElementById("sim-next-btn");
const cinemaFrameEl = document.querySelector(".cinema-frame");

const flagTabsEl = document.getElementById("flagship-tabs");
const flagStageEl = document.getElementById("flagship-stage");

const dialogEl = document.getElementById("inspector-dialog");
const dlgTitle = document.getElementById("dlg-title");
const dlgCat = document.getElementById("dlg-cat");
const dlgImg = document.getElementById("dlg-img");
const dlgDesc = document.getElementById("dlg-desc");
const dlgUrl = document.getElementById("dlg-url");
const dlgCopy = document.getElementById("dlg-copy");
const releaseInput = document.getElementById("release-input");
const testerCount = document.getElementById("tester-count");
const testerBadges = document.getElementById("tester-badges");
const tierSampleGrid = document.getElementById("tier-sample-grid");
const manifestStats = document.getElementById("manifest-stats");

let activeCategory = "all";
let simThemeId = THEMES[0].id;
let currentDialogIndex = 0;
const manifestCache = new Map();
const savedIds = new Set(JSON.parse(localStorage.getItem("nuvio_saved_themes") || "[]"));

function updateSavedCount() { savedCountEl.textContent = savedIds.size; }

function copyUrl(url, btn) {
  navigator.clipboard.writeText(url).then(() => {
    const orig = btn.textContent;
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(() => { btn.textContent = orig; btn.classList.remove("copied"); }, 1500);
  });
}

let activeFlagshipIdx = 0;
let flagHoverPaused = false;
let flagTimer = null;

function flagSlideHtml(f) {
  const t = THEMES[f.idx];
  const url = RAW_BASE + t.json;
  return `
    <div class="flag-media" data-open="${f.idx}">
      <img src="previews/preview-${t.id}.jpg" alt="${t.name}" decoding="async" />
    </div>
    <div class="flag-info">
      <span class="flag-kicker">${f.kicker}</span>
      <h3>${t.name}</h3>
      <p>${t.desc}</p>
      <div class="flag-actions">
        <button type="button" class="btn btn-blue btn-sm" data-copy="${url}">Copy JSON URL</button>
        <button type="button" class="btn btn-outline-dark btn-sm" data-open="${f.idx}">Inspect 4K &amp; Regex ›</button>
      </div>
    </div>
  `;
}

function buildFlagshipSlidesOnce() {
  flagStageEl.innerHTML = FLAGSHIPS.map((f, i) =>
    `<div class="flag-slide ${i === 0 ? "layer-front" : "layer-back"}" data-flag-slide="${i}">${flagSlideHtml(f)}</div>`
  ).join("");
}

function renderFlagship(flagIdx) {
  activeFlagshipIdx = (flagIdx + FLAGSHIPS.length) % FLAGSHIPS.length;
  flagTabsEl.querySelectorAll(".flag-tab").forEach((b, i) => b.classList.toggle("active", i === activeFlagshipIdx));
  flagStageEl.querySelectorAll(".flag-slide").forEach((slide, i) => {
    const isAct = i === activeFlagshipIdx;
    slide.classList.toggle("layer-front", isAct);
    slide.classList.toggle("layer-back", !isAct);
  });
}

function resetFlagTimer() {
  if (flagTimer) clearInterval(flagTimer);
  flagTimer = setInterval(() => {
    if (!flagHoverPaused && flagVisible && !dialogEl.open) renderFlagship(activeFlagshipIdx + 1);
  }, 4000);
}

function initFlagships() {
  buildFlagshipSlidesOnce();
  flagTabsEl.innerHTML = FLAGSHIPS.map((f, i) =>
    `<button type="button" class="flag-tab${i === 0 ? " active" : ""}" data-flag="${i}">${f.tab}</button>`
  ).join("");
  flagTabsEl.addEventListener("click", (e) => {
    const tab = e.target.closest(".flag-tab");
    if (tab) {
      renderFlagship(Number(tab.dataset.flag));
      resetFlagTimer();
    }
  });
  flagStageEl.addEventListener("mouseenter", () => { flagHoverPaused = true; });
  flagStageEl.addEventListener("mouseleave", () => { flagHoverPaused = false; });
  resetFlagTimer();
}

let autoShuffleEnabled = true;
let simHoverPaused = false;
let simTimer = null;

function preloadThemeBadges(theme, titleObj) {
  const list = getBadgesForTheme(theme, titleObj);
  return Promise.all(list.map((b) => new Promise((resolve) => {
    const img = new Image();
    img.onload = () => (img.decode ? img.decode().then(resolve, resolve) : resolve());
    img.onerror = resolve;
    img.src = `${theme.dir}/${b}.webp`;
  })));
}

let simRenderSeq = 0;
let frontLayerIdx = 0;

function buildSimRowsOnce() {
  simLayer0.innerHTML = "";
  simLayer1.innerHTML = "";
}

async function renderSimulator(themeId, animate = true) {
  const seq = ++simRenderSeq;
  simThemeId = themeId;
  const idx = THEMES.findIndex((x) => x.id === themeId);
  const safeIdx = idx >= 0 ? idx : 0;
  const t = THEMES[safeIdx];
  const titleObj = LIVE_TITLES[safeIdx % LIVE_TITLES.length];

  simActiveNameEl.textContent = t.name;
  simCounterEl.textContent = `${safeIdx + 1} / ${THEMES.length}`;
  simMovieTitleEl.textContent = titleObj.title;
  simMovieMetaEl.textContent = titleObj.meta;
  if (cinemaFrameEl) {
    const [g1, g2] = THEME_GLOWS[t.id] || [t.accent, "#2997ff"];
    cinemaFrameEl.style.setProperty("--glow-1", g1);
    cinemaFrameEl.style.setProperty("--glow-2", g2);
  }

  simCopyBtn.onclick = () => copyUrl(RAW_BASE + t.json, simCopyBtn);
  simInspectBtn.onclick = () => openDialog(safeIdx, titleObj.release);

  await preloadThemeBadges(t, titleObj);
  if (seq !== simRenderSeq) return;

  const layers = [simLayer0, simLayer1];
  const badgeList = getBadgesForTheme(t, titleObj);
  const badgesHtml = badgeList.map((b) => `<img src="${t.dir}/${b}.webp" alt="${b}" />`).join("");

  if (!animate) {
    layers[frontLayerIdx].innerHTML = badgesHtml;
  } else {
    const nextLayerIdx = 1 - frontLayerIdx;
    layers[nextLayerIdx].innerHTML = badgesHtml;

    requestAnimationFrame(() => {
      layers[frontLayerIdx].classList.remove("layer-front");
      layers[frontLayerIdx].classList.add("layer-back");
      layers[nextLayerIdx].classList.remove("layer-back");
      layers[nextLayerIdx].classList.add("layer-front");
      frontLayerIdx = nextLayerIdx;
    });
  }

  const nextIdx = (safeIdx + 1) % THEMES.length;
  preloadThemeBadges(THEMES[nextIdx], LIVE_TITLES[nextIdx % LIVE_TITLES.length]);
}

let heroVisible = true;
let flagVisible = true;

function stepSimulator() {
  if (!autoShuffleEnabled || simHoverPaused || !heroVisible || dialogEl.open) return;
  const curIdx = THEMES.findIndex((x) => x.id === simThemeId);
  const nextIdx = (curIdx + 1) % THEMES.length;
  renderSimulator(THEMES[nextIdx].id, true);
}

function resetSimTimer() {
  if (simTimer) clearInterval(simTimer);
  simTimer = setInterval(stepSimulator, 3000);
}

function initSimChips() {
  simAutoBtn.addEventListener("click", () => {
    autoShuffleEnabled = !autoShuffleEnabled;
    simAutoBtn.textContent = autoShuffleEnabled ? "Auto: On" : "Auto: Off";
    simAutoBtn.setAttribute("aria-pressed", String(autoShuffleEnabled));
    if (autoShuffleEnabled) resetSimTimer();
  });
  simPrevBtn.addEventListener("click", () => {
    const cur = THEMES.findIndex((x) => x.id === simThemeId);
    renderSimulator(THEMES[(cur - 1 + THEMES.length) % THEMES.length].id, true);
    resetSimTimer();
  });
  simNextBtn.addEventListener("click", () => {
    const cur = THEMES.findIndex((x) => x.id === simThemeId);
    renderSimulator(THEMES[(cur + 1) % THEMES.length].id, true);
    resetSimTimer();
  });
  cinemaFrameEl.addEventListener("mouseenter", () => { simHoverPaused = true; });
  cinemaFrameEl.addEventListener("mouseleave", () => { simHoverPaused = false; });
  resetSimTimer();
}

function renderGrid() {
  const q = searchEl.value.trim().toLowerCase();
  let list = THEMES.filter((t) => {
    const matchCat = activeCategory === "all" || (activeCategory === "saved" ? savedIds.has(t.id) : t.cat === activeCategory);
    const matchQ = !q || t.name.toLowerCase().includes(q) || t.desc.toLowerCase().includes(q) || t.id.includes(q);
    return matchCat && matchQ;
  });
  if (sortEl.value === "az") list = [...list].sort((a, b) => a.name.localeCompare(b.name));

  gridEl.innerHTML = list.map((t, i) => {
    const idx = THEMES.indexOf(t);
    const jsonUrl = RAW_BASE + t.json;
    const isSaved = savedIds.has(t.id);
    const delay = (i % 3) * 70;
    return `
      <article class="theme-card scroll-card" style="transition-delay:${delay}ms">
        <div class="card-media">
          <button type="button" class="card-thumb-btn" data-open="${idx}" aria-label="Inspect ${t.name}">
            <img src="previews/preview-${t.id}.jpg" alt="${t.name} 4K preview" loading="lazy" decoding="async" />
          </button>
        </div>
        <div class="card-body">
          <div class="card-meta-row">
            <span class="card-cat-label">${CAT_LABELS[t.cat]}</span>
            <button type="button" class="fav-btn${isSaved ? " saved" : ""}" data-fav="${t.id}" aria-label="Save ${t.name}" title="Save theme">${isSaved ? "★" : "☆"}</button>
          </div>
          <h3 class="card-title">${t.name}</h3>
          <p class="card-desc">${t.desc}</p>
          <div class="card-actions">
            <button type="button" class="btn btn-dark btn-sm" data-copy="${jsonUrl}">Copy URL</button>
            <button type="button" class="btn btn-outline-dark btn-sm" data-open="${idx}">Inspect ›</button>
          </div>
        </div>
      </article>
    `;
  }).join("");

  emptyEl.hidden = list.length > 0;
  observeScrollItems();
}

async function getManifest(theme) {
  if (manifestCache.has(theme.id)) return manifestCache.get(theme.id);
  const res = await fetch(theme.json);
  const data = await res.json();
  manifestCache.set(theme.id, data);
  return data;
}

function filenameFromImageUrl(url) {
  const parts = url.split("/");
  return parts[parts.length - 1];
}

async function runReleaseTester(theme) {
  const text = releaseInput.value || "";
  tierSampleGrid.innerHTML = TIER_SAMPLES.map((b) => `<img src="${theme.dir}/${b}.webp" alt="${b}" loading="lazy" />`).join("");

  try {
    const data = await getManifest(theme);
    const filters = (data.filters || []).filter((f) => f.enabled !== false);
    manifestStats.textContent = `${filters.length} active regex rules`;

    const matched = [];
    const seenImgs = new Set();
    for (const f of filters) {
      if (!f.pattern || !f.imageURL) continue;
      try {
        const cleanPattern = f.pattern.replace(/\(\?i\)/g, "");
        const rx = new RegExp(cleanPattern, "i");
        if (rx.test(text)) {
          const fname = filenameFromImageUrl(f.imageURL);
          if (!seenImgs.has(fname)) {
            seenImgs.add(fname);
            matched.push({ name: f.name || fname, fname });
          }
        }
      } catch (_) {}
    }

    testerCount.textContent = `${matched.length} badge${matched.length === 1 ? "" : "s"} matched this release:`;
    testerBadges.innerHTML = matched.length
      ? matched.map((m) => `<img src="${theme.dir}/${m.fname}" alt="${m.name}" title="${m.name}" />`).join("")
      : `<span style="color:#a1a1a6;font-size:0.84rem;">No badges matched. Try adding 4K, REMUX, Atmos, or Netflix.</span>`;
  } catch (err) {
    testerCount.textContent = "Run via a local server or GitHub Pages to load live JSON rules.";
    testerBadges.innerHTML = "";
  }
}

function openDialog(idx, customRelease) {
  currentDialogIndex = (idx + THEMES.length) % THEMES.length;
  const t = THEMES[currentDialogIndex];
  const titleObj = LIVE_TITLES[currentDialogIndex % LIVE_TITLES.length];
  releaseInput.value = customRelease || titleObj.release;
  dlgCat.textContent = CAT_LABELS[t.cat];
  dlgTitle.textContent = t.name;
  dlgImg.src = `previews/preview-${t.id}.jpg`;
  dlgImg.alt = `${t.name} 4K preview`;
  dlgDesc.textContent = t.desc;
  const url = RAW_BASE + t.json;
  dlgUrl.textContent = url;
  dlgCopy.onclick = () => copyUrl(url, dlgCopy);

  history.replaceState(null, "", `#theme=${t.id}`);
  runReleaseTester(t);
  if (!dialogEl.open) dialogEl.showModal();
}

document.querySelectorAll(".filter-pills .pill").forEach((pill) => {
  pill.addEventListener("click", () => {
    document.querySelectorAll(".filter-pills .pill").forEach((p) => p.classList.remove("active"));
    pill.classList.add("active");
    activeCategory = pill.dataset.cat;
    renderGrid();
  });
});

searchEl.addEventListener("input", renderGrid);
sortEl.addEventListener("change", renderGrid);

document.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT" && !dialogEl.open) {
    e.preventDefault();
    searchEl.focus();
  }
});

document.body.addEventListener("click", (e) => {
  const favBtn = e.target.closest("[data-fav]");
  if (favBtn) {
    const id = favBtn.dataset.fav;
    if (savedIds.has(id)) savedIds.delete(id);
    else savedIds.add(id);
    localStorage.setItem("nuvio_saved_themes", JSON.stringify([...savedIds]));
    updateSavedCount();
    renderGrid();
    return;
  }
  const copyBtn = e.target.closest("[data-copy]");
  if (copyBtn) { copyUrl(copyBtn.dataset.copy, copyBtn); return; }
  const openBtn = e.target.closest("[data-open]");
  if (openBtn && !openBtn.closest(".inspector-dialog")) openDialog(Number(openBtn.dataset.open));
});

document.querySelectorAll(".dlg-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".dlg-tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    const target = tab.dataset.tab;
    document.getElementById("tab-showcase").hidden = target !== "showcase";
    document.getElementById("tab-tester").hidden = target !== "tester";
  });
});

releaseInput.addEventListener("input", () => runReleaseTester(THEMES[currentDialogIndex]));
document.querySelectorAll(".preset-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    releaseInput.value = chip.dataset.preset;
    runReleaseTester(THEMES[currentDialogIndex]);
  });
});

document.getElementById("dlg-close").addEventListener("click", () => dialogEl.close());
document.getElementById("dlg-prev").addEventListener("click", () => openDialog(currentDialogIndex - 1));
document.getElementById("dlg-next").addEventListener("click", () => openDialog(currentDialogIndex + 1));
dialogEl.addEventListener("click", (e) => { if (e.target === dialogEl) dialogEl.close(); });
dialogEl.addEventListener("close", () => { if (location.hash.startsWith("#theme=")) history.replaceState(null, "", location.pathname); });
dialogEl.addEventListener("keydown", (e) => {
  if (document.activeElement === releaseInput) return;
  if (e.key === "ArrowLeft") openDialog(currentDialogIndex - 1);
  if (e.key === "ArrowRight") openDialog(currentDialogIndex + 1);
});

const io = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("visible"); io.unobserve(en.target); }
  });
}, { threshold: 0.05, rootMargin: "60px 0px" });

// Pause off-screen auto-shuffles so background image decoding never hiccups scroll
const visObserver = new IntersectionObserver((entries) => {
  entries.forEach((en) => {
    if (en.target === cinemaFrameEl) heroVisible = en.isIntersecting;
    if (en.target === flagStageEl) flagVisible = en.isIntersecting;
  });
}, { threshold: 0.05 });
if (cinemaFrameEl) visObserver.observe(cinemaFrameEl);
if (flagStageEl) visObserver.observe(flagStageEl);

function observeScrollItems() {
  document.querySelectorAll(".reveal, .spec-tile, .step-card, .faq-item, .scroll-card").forEach((el, i) => {
    if (!el.classList.contains("scroll-card") && !el.classList.contains("reveal")) {
      el.classList.add("scroll-card");
      el.style.transitionDelay = `${(i % 4) * 60}ms`;
    }
    if (!el.classList.contains("visible")) io.observe(el);
  });
}

// Smooth Hero Scroll Parallax (desktop only, stops past hero)
const heroTitleEl = document.querySelector(".hero-title");
const heroAuraEl = document.querySelector(".hero-aura");
let scrollTicking = false;
let lastHeroReset = false;
window.addEventListener("scroll", () => {
  if (window.innerWidth <= 768) return;
  if (window.scrollY > 560) {
    if (!lastHeroReset) { lastHeroReset = true; }
    return;
  }
  lastHeroReset = false;
  if (scrollTicking) return;
  scrollTicking = true;
  requestAnimationFrame(() => {
    const y = Math.min(window.scrollY, 500);
    if (heroTitleEl) {
      heroTitleEl.style.transform = `translateY(${y * 0.14}px)`;
      heroTitleEl.style.opacity = String(Math.max(0.25, 1 - y / 460));
    }
    if (heroAuraEl) {
      heroAuraEl.style.transform = `translateX(-50%) translateY(${y * 0.25}px) scale(${1 + y * 0.0006})`;
    }
    scrollTicking = false;
  });
}, { passive: true });

observeScrollItems();

updateSavedCount();
buildSimRowsOnce();
initSimChips();
renderSimulator(THEMES[0].id, false);
initFlagships();
renderGrid();

if (location.hash.startsWith("#theme=")) {
  const id = location.hash.slice(7);
  const idx = THEMES.findIndex((t) => t.id === id);
  if (idx >= 0) openDialog(idx);
}

/* ---------- Hero Apple Fluted Glass Louvers + Fin-Slit Masked FBM Steam ---------- */
(function initHeroAotAtmosphere() {
  const canvas = document.getElementById("hero-aot-canvas");
  const heroSection = document.querySelector(".hero");
  if (!canvas || !heroSection) return;
  const ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let width = 0;
  let height = 0;
  let dpr = 1;
  let slatCount = 26;
  let rafId = 0;
  let isHeroInView = true;
  let lastTime = 0;
  let simTime = 0;

  // Offscreen half-res mask buffer so steam ONLY originates from each open fin slit & sweeps left
  const plumeCanvas = document.createElement("canvas");
  const plumeCtx = plumeCanvas.getContext("2d", { alpha: true });

  // Build seamlessly tileable 256x256 FBM steam texture once at init
  function createTileableFbmTexture(seedOffset, gridPeriod) {
    const size = 256;
    const off = document.createElement("canvas");
    off.width = size;
    off.height = size;
    const oCtx = off.getContext("2d");
    const img = oCtx.createImageData(size, size);
    const data = img.data;

    function hash(x, y, per) {
      const wx = ((x % per) + per) % per;
      const wy = ((y % per) + per) % per;
      const n = Math.sin(wx * 127.1 + wy * 311.7 + seedOffset * 74.7) * 43758.5453;
      return n - Math.floor(n);
    }
    function smoothNoise(x, y, per) {
      const ix = Math.floor(x);
      const iy = Math.floor(y);
      const fx = x - ix;
      const fy = y - iy;
      const ux = fx * fx * (3 - 2 * fx);
      const uy = fy * fy * (3 - 2 * fy);
      const a = hash(ix, iy, per);
      const b = hash(ix + 1, iy, per);
      const c = hash(ix, iy + 1, per);
      const d = hash(ix + 1, iy + 1, per);
      return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
    }
    function fbm(x, y, basePer) {
      let val = 0;
      let amp = 0.5;
      let freq = 1;
      for (let o = 0; o < 4; o++) {
        val += amp * smoothNoise(x * freq, y * freq, basePer * freq);
        freq *= 2;
        amp *= 0.5;
      }
      return val;
    }

    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const nx = (x / size) * gridPeriod;
        const ny = (y / size) * gridPeriod;
        const warpX = fbm(nx + 1.3, ny + 2.7, gridPeriod);
        const warpY = fbm(nx + 4.1, ny + 0.9, gridPeriod);
        const n = fbm(nx + warpX * 1.1, ny + warpY * 1.1, gridPeriod);
        const density = Math.max(0, Math.min(1, (n - 0.14) * 2.1));
        const alpha = Math.round(density * 255);

        const p = (y * size + x) * 4;
        data[p] = 246;
        data[p + 1] = 250;
        data[p + 2] = 255;
        data[p + 3] = alpha;
      }
    }
    oCtx.putImageData(img, 0, 0);
    return off;
  }

  const steamTex = createTileableFbmTexture(5, 5);
  const steamPattern = plumeCtx ? plumeCtx.createPattern(steamTex, "repeat") : null;

  function smoothstep(edge0, edge1, x) {
    const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
    return t * t * (3 - 2 * t);
  }

  // Pure continuous zero-delay cosine wave (no stalls, no clamping kinks)
  function getCycleState(time) {
    const period = 6.2;
    const open = 0.5 - 0.5 * Math.cos((time / period) * Math.PI * 2);
    return { open, steam: 1, time };
  }

  function getLocalOpen(index, _open, time) {
    const period = 6.2;
    const tNorm = index / Math.max(1, slatCount - 1);
    // Silky travelling cosine wave across all fins — zero delay, zero hard stops
    const phase = (time / period) * Math.PI * 2 - tNorm * 1.4;
    return 0.5 - 0.5 * Math.cos(phase);
  }

  function buildScene() {
    const rect = heroSection.getBoundingClientRect();
    width = Math.max(1, rect.width);
    height = Math.max(1, rect.height);
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Half-res plume mask buffer for ultra-fast smooth compositing
    plumeCanvas.width = Math.max(1, Math.round(width * 0.5));
    plumeCanvas.height = Math.max(1, Math.round(height * 0.5));

    slatCount = width <= 768 ? 16 : 26;
  }

  // Render FBM steam strictly masked to plumes originating from each open fin slit & sweeping left
  function drawFinSlitSteam(open, steam, time) {
    if (!plumeCtx || !steamPattern) return;

    const pw = plumeCanvas.width;
    const ph = plumeCanvas.height;
    const sx = pw / width;
    const slatW = pw / slatCount;
    const reach = slatW * (1.4 + 1.1 * steam);

    plumeCtx.globalCompositeOperation = "source-over";
    plumeCtx.clearRect(0, 0, pw, ph);

    // 1. Paint exact plume emission masks anchored at every open fin slit, fading left
    for (let i = 0; i < slatCount; i++) {
      const localOpen = getLocalOpen(i, open, time);
      if (localOpen <= 0.01) continue;

      const slitX = i * slatW + slatW * localOpen * 0.14;
      const leftX = slitX - reach;
      const g = plumeCtx.createLinearGradient(leftX, 0, slitX + 2, 0);
      g.addColorStop(0, "rgba(255, 255, 255, 0)");
      g.addColorStop(0.55, `rgba(255, 255, 255, ${0.46 * localOpen * steam})`);
      g.addColorStop(0.92, `rgba(255, 255, 255, ${0.95 * localOpen * steam})`);
      g.addColorStop(1, "rgba(255, 255, 255, 0)");

      plumeCtx.fillStyle = g;
      plumeCtx.fillRect(leftX, 0, reach + 3, ph);
    }

    // Soft top & bottom vertical fade
    plumeCtx.globalCompositeOperation = "destination-in";
    const vMask = plumeCtx.createLinearGradient(0, 0, 0, ph);
    vMask.addColorStop(0, "rgba(255, 255, 255, 0)");
    vMask.addColorStop(0.18, "rgba(255, 255, 255, 0.70)");
    vMask.addColorStop(0.65, "rgba(255, 255, 255, 1)");
    vMask.addColorStop(0.95, "rgba(255, 255, 255, 0.40)");
    vMask.addColorStop(1, "rgba(255, 255, 255, 0)");
    plumeCtx.fillStyle = vMask;
    plumeCtx.fillRect(0, 0, pw, ph);

    // 2. Single fillRect with repeating CanvasPattern so source-in covers the ENTIRE canvas!
    plumeCtx.globalCompositeOperation = "source-in";
    const scale = (width <= 768 ? 140 : 190) * sx / 256;
    const ox = -((time * 68 * sx) % (256 * scale));
    const oy = -((time * 24 * sx) % (256 * scale));
    plumeCtx.save();
    plumeCtx.translate(ox, oy);
    plumeCtx.scale(scale, scale);
    plumeCtx.fillStyle = steamPattern;
    plumeCtx.fillRect(-ox / scale, -oy / scale, pw / scale + 256, ph / scale + 256);
    plumeCtx.restore();

    // 3. Composite onto main hero canvas (light, refined, never overpowering)
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    ctx.globalAlpha = 0.06;
    ctx.drawImage(plumeCanvas, 0, 0, width, height);
    ctx.restore();
  }

  function drawFlutedGlass(open, time) {
    const slatW = width / slatCount;

    for (let i = 0; i < slatCount; i++) {
      const tNorm = i / Math.max(1, slatCount - 1);
      const localOpen = getLocalOpen(i, open, time);

      // When localOpen === 0, faceW === slatW (100% sealed shut, zero gap)
      const faceW = slatW * (1 - localOpen * 0.24);
      const xRight = (i + 1) * slatW;
      const xLeft = xRight - faceW;

      const wavePhase = Math.sin(tNorm * 4.2 + time * 0.35);
      const yShift = height * (0.38 + wavePhase * 0.16);

      const vGrad = ctx.createLinearGradient(0, 0, 0, height);
      const coralAlpha = 0.14 * Math.max(0, 1 - tNorm * 1.55);
      const bluePos = Math.max(0.18, Math.min(0.65, yShift / height));
      vGrad.addColorStop(0, `rgba(255, 92, 68, ${coralAlpha})`);
      vGrad.addColorStop(bluePos, `rgba(28, 108, 210, ${0.30 + 0.08 * (1 - localOpen)})`);
      vGrad.addColorStop(Math.min(0.88, bluePos + 0.24), "rgba(92, 44, 165, 0.26)");
      vGrad.addColorStop(1, "rgba(12, 16, 30, 0.32)");

      ctx.fillStyle = vGrad;
      ctx.fillRect(xLeft, 0, faceW, height);

      const hGrad = ctx.createLinearGradient(xLeft, 0, xRight, 0);
      hGrad.addColorStop(0, `rgba(255, 255, 255, ${0.22 + localOpen * 0.16})`);
      hGrad.addColorStop(0.16, "rgba(185, 228, 255, 0.10)");
      hGrad.addColorStop(0.55, "rgba(10, 14, 24, 0.18)");
      hGrad.addColorStop(0.88, "rgba(0, 0, 0, 0.36)");
      hGrad.addColorStop(1, "rgba(0, 0, 0, 0.50)");

      ctx.fillStyle = hGrad;
      ctx.fillRect(xLeft, 0, faceW, height);

      ctx.fillStyle = `rgba(255, 255, 255, ${0.22 + localOpen * 0.18})`;
      ctx.fillRect(xLeft, 0, 1.1, height);
    }

    const vigTop = ctx.createLinearGradient(0, 0, 0, height * 0.16);
    vigTop.addColorStop(0, "rgba(0, 0, 0, 0.42)");
    vigTop.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = vigTop;
    ctx.fillRect(0, 0, width, height * 0.16);
  }

  function frame(now) {
    if (!isHeroInView || document.hidden) {
      rafId = 0;
      return;
    }
    if (!lastTime) lastTime = now;
    const dt = Math.min(0.05, (now - lastTime) / 1000);
    lastTime = now;
    simTime += dt;

    const { open, steam } = getCycleState(simTime);

    ctx.clearRect(0, 0, width, height);
    drawFlutedGlass(open, simTime);
    drawFinSlitSteam(open, steam, simTime);

    rafId = requestAnimationFrame(frame);
  }

  function startLoop() {
    if (reducedMotion) {
      ctx.clearRect(0, 0, width, height);
      drawFlutedGlass(0.35, 0.8);
      return;
    }
    if (!rafId && isHeroInView && !document.hidden) {
      lastTime = 0;
      rafId = requestAnimationFrame(frame);
    }
  }

  function stopLoop() {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  const ro = new ResizeObserver(() => {
    buildScene();
    if (reducedMotion) startLoop();
  });
  ro.observe(heroSection);

  const aotIo = new IntersectionObserver((entries) => {
    isHeroInView = entries[0].isIntersecting;
    if (isHeroInView) startLoop();
    else stopLoop();
  }, { threshold: 0.01 });
  aotIo.observe(heroSection);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopLoop();
    else if (isHeroInView) startLoop();
  });

  buildScene();
  startLoop();
})();
