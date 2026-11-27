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

/* ---------- Hero Apple Fluted Glass Louvers + Jet-Vented Stand-Fan Steam ---------- */
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
  let slatCount = 28;
  let steamParticles = [];
  let rafId = 0;
  let isHeroInView = true;
  let lastTime = 0;
  let simTime = 0;
  let steamSpawnAcc = 0;

  // Pre-rendered soft volumetric white steam puff sprite
  const puffSize = 128;
  const puffCanvas = document.createElement("canvas");
  puffCanvas.width = puffSize;
  puffCanvas.height = puffSize;
  const pCtx = puffCanvas.getContext("2d");
  const puffGrad = pCtx.createRadialGradient(
    puffSize * 0.5, puffSize * 0.5, puffSize * 0.02,
    puffSize * 0.5, puffSize * 0.5, puffSize * 0.5
  );
  puffGrad.addColorStop(0, "rgba(255, 255, 255, 0.96)");
  puffGrad.addColorStop(0.28, "rgba(246, 250, 255, 0.64)");
  puffGrad.addColorStop(0.62, "rgba(222, 236, 255, 0.22)");
  puffGrad.addColorStop(1, "rgba(222, 236, 255, 0)");
  pCtx.fillStyle = puffGrad;
  pCtx.fillRect(0, 0, puffSize, puffSize);

  function easeInOutSine(x) {
    return -(Math.cos(Math.PI * Math.max(0, Math.min(1, x))) - 1) / 2;
  }

  // Smooth crack-open & close cycle (~6.8s)
  function getCycleState(time) {
    const period = 6.8;
    const u = (time % period) / period;
    let open = 0;
    let venting = 0;

    if (u < 0.36) {
      const p = u / 0.36;
      open = easeInOutSine(p);
      venting = Math.sin(p * Math.PI) * (0.5 + 0.5 * open);
    } else if (u < 0.50) {
      open = 1;
      venting = 0.55 * (1 - (u - 0.36) / 0.14);
    } else if (u < 0.86) {
      const p = (u - 0.50) / 0.36;
      open = 1 - easeInOutSine(p);
      venting = 0;
    } else {
      open = 0;
      venting = 0;
    }
    return { open, venting };
  }

  function getLocalOpen(index, open) {
    const tNorm = index / Math.max(1, slatCount - 1);
    const waveOffset = Math.sin(tNorm * Math.PI) * 0.10;
    return Math.max(0, Math.min(1, open * 1.10 - waveOffset));
  }

  function buildScene() {
    const rect = heroSection.getBoundingClientRect();
    width = Math.max(1, rect.width);
    height = Math.max(1, rect.height);
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    slatCount = width <= 768 ? 18 : 30;
    steamParticles = [];
  }

  function spawnSteamBurst(count, open) {
    const isMobile = width <= 768;
    const maxParticles = isMobile ? 85 : 150;
    const slatW = width / slatCount;

    for (let i = 0; i < count; i++) {
      if (steamParticles.length >= maxParticles) break;
      const idx = Math.floor(Math.random() * slatCount);
      const localOpen = getLocalOpen(idx, open);
      if (localOpen < 0.10) continue;

      // Slats hinge on their RIGHT edge & crack open on their LEFT edge -> jet shoots LEFT!
      const slitX = idx * slatW + 4;
      const spawnY = height * (0.14 + Math.random() * 0.78);

      steamParticles.push({
        x: slitX,
        y: spawnY,
        // Fast pressurized jet exhaust to the left, then fan-turbulence slows & swirls it
        vx: -((isMobile ? 120 : 175) + Math.random() * (isMobile ? 80 : 120)),
        vy: (Math.random() - 0.62) * 32,
        size: (isMobile ? 22 : 30) + Math.random() * 18,
        grow: (isMobile ? 3.2 : 4.0) + Math.random() * 1.4,
        maxAlpha: 0.30 + Math.random() * 0.22,
        seed: Math.random() * Math.PI * 2,
        spin: (Math.random() - 0.5) * 2.2,
        age: 0,
        life: 1.6 + Math.random() * 1.3
      });
    }
  }

  function updateSteam(dt, time) {
    for (let i = steamParticles.length - 1; i >= 0; i--) {
      const p = steamParticles[i];
      p.age += dt;
      if (p.age >= p.life || p.x < -p.size * 3 || p.y < -p.size * 3) {
        steamParticles.splice(i, 1);
        continue;
      }
      const progress = p.age / p.life;

      // Jet phase (0..0.25): fast linear jet out of the glass slit
      // Fan-wind phase (0.25..1.0): air drag + stand-fan swirling turbulence & upward billow
      if (progress > 0.22) {
        p.vx *= 1 - 1.35 * dt; // jet decelerates into ambient fan air
        p.vy -= 42 * dt;       // hot steam rises as it slows
        const fanSwirlY = Math.sin(time * 3.6 + p.seed + p.x * 0.014) * 58;
        const fanSwirlX = Math.cos(time * 2.8 + p.seed + p.y * 0.012) * 24;
        p.x += (p.vx + fanSwirlX) * dt;
        p.y += (p.vy + fanSwirlY) * dt;
      } else {
        p.x += p.vx * dt;
        p.y += p.vy * dt;
      }
    }
  }

  function drawSteamLayer(frontPass) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";

    for (let i = 0; i < steamParticles.length; i++) {
      const p = steamParticles[i];
      const progress = p.age / p.life;
      // Young jet (progress <= 0.24) renders BEHIND the glass fins (emerging from inside!)
      // Expanded fan-swirled clouds (progress > 0.24) render IN FRONT of the glass!
      const isFront = progress > 0.24;
      if (isFront !== frontPass) continue;

      const fadeIn = Math.min(1, progress / 0.08);
      const fadeOut = Math.pow(1 - progress, 1.35);
      const alpha = p.maxAlpha * fadeIn * fadeOut;
      if (alpha <= 0.005) continue;

      const curSize = p.size * (0.55 + progress * p.grow);
      // Jet is stretched horizontally at birth, then relaxes into round billowing fan clouds
      const jetFactor = Math.max(0, 1 - progress / 0.35);
      const scaleX = 1 + jetFactor * 1.45;
      const scaleY = 1 - jetFactor * 0.38;
      const angle = Math.atan2(p.vy, p.vx) * jetFactor + p.spin * progress * (1 - jetFactor);

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(angle);
      ctx.scale(scaleX, scaleY);
      ctx.globalAlpha = alpha;
      ctx.drawImage(puffCanvas, -curSize * 0.5, -curSize * 0.5, curSize, curSize);
      ctx.restore();
    }

    ctx.restore();
  }

  function drawFlutedGlass(open, time) {
    const slatW = width / slatCount;

    // Bright pressurized steam glow INSIDE behind the open left slits
    if (open > 0.08) {
      ctx.save();
      ctx.globalCompositeOperation = "screen";
      for (let i = 0; i < slatCount; i++) {
        const localOpen = getLocalOpen(i, open);
        if (localOpen < 0.08) continue;
        const slitX = i * slatW;
        const gapW = slatW * localOpen * 0.24;
        ctx.fillStyle = `rgba(235, 246, 255, ${0.24 * localOpen})`;
        ctx.fillRect(slitX, 0, Math.max(3, gapW), height);
      }
      ctx.restore();
    }

    for (let i = 0; i < slatCount; i++) {
      const tNorm = i / Math.max(1, slatCount - 1);
      const localOpen = getLocalOpen(i, open);

      // Slats anchor on their RIGHT edge & crack open ~24% on their LEFT edge
      const faceW = slatW * (1 - localOpen * 0.24);
      const xRight = (i + 1) * slatW;
      const xLeft = xRight - faceW;

      const wavePhase = Math.sin(tNorm * 4.2 + time * 0.35);
      const yShift = height * (0.38 + wavePhase * 0.16);

      const vGrad = ctx.createLinearGradient(0, 0, 0, height);
      const coralAlpha = 0.14 * Math.max(0, 1 - tNorm * 1.55);
      const bluePos = Math.max(0.18, Math.min(0.65, yShift / height));
      vGrad.addColorStop(0, `rgba(255, 92, 68, ${coralAlpha})`);
      vGrad.addColorStop(bluePos, `rgba(41, 151, 255, ${0.22 + 0.06 * (1 - localOpen)})`);
      vGrad.addColorStop(Math.min(0.88, bluePos + 0.24), "rgba(138, 68, 226, 0.18)");
      vGrad.addColorStop(1, "rgba(24, 32, 58, 0.22)");

      ctx.fillStyle = vGrad;
      ctx.fillRect(xLeft, 0, faceW, height);

      const hGrad = ctx.createLinearGradient(xLeft, 0, xRight, 0);
      hGrad.addColorStop(0, `rgba(255, 255, 255, ${0.26 + localOpen * 0.16})`);
      hGrad.addColorStop(0.16, "rgba(185, 228, 255, 0.10)");
      hGrad.addColorStop(0.55, "rgba(255, 255, 255, 0.01)");
      hGrad.addColorStop(0.88, "rgba(0, 0, 0, 0.28)");
      hGrad.addColorStop(1, "rgba(0, 0, 0, 0.42)");

      ctx.fillStyle = hGrad;
      ctx.fillRect(xLeft, 0, faceW, height);

      // Crisp glass highlight on the opening LEFT edge
      ctx.fillStyle = `rgba(255, 255, 255, ${0.24 + localOpen * 0.20})`;
      ctx.fillRect(xLeft, 0, 1.2, height);
    }

    const vigTop = ctx.createLinearGradient(0, 0, 0, height * 0.18);
    vigTop.addColorStop(0, "rgba(0, 0, 0, 0.45)");
    vigTop.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = vigTop;
    ctx.fillRect(0, 0, width, height * 0.18);
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

    const { open, venting } = getCycleState(simTime);

    if (venting > 0.04) {
      const spawnRate = (width <= 768 ? 48 : 78) * venting;
      steamSpawnAcc += spawnRate * dt;
      const toSpawn = Math.floor(steamSpawnAcc);
      if (toSpawn > 0) {
        steamSpawnAcc -= toSpawn;
        spawnSteamBurst(toSpawn, open);
      }
    }

    updateSteam(dt, simTime);

    ctx.clearRect(0, 0, width, height);
    // 1. Jet steam emerging from INSIDE behind the glass slits
    drawSteamLayer(false);
    // 2. Fluted glass louvers
    drawFlutedGlass(open, simTime);
    // 3. Escaped steam caught in the stand-fan breeze & billowing outward
    drawSteamLayer(true);

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
