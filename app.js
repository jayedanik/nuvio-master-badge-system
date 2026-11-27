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

/* ---------- Hero Apple Fluted Glass Louvers + Silky FBM Steam (Behind -> Front Left Breeze) ---------- */
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
  let steamParticles = [];
  let rafId = 0;
  let isHeroInView = true;
  let lastTime = 0;
  let simTime = 0;
  let steamSpawnAcc = 0;

  // Build 2 silky FBM-noise steam sprites once at init (authentic organic vapor, zero circles)
  function createFbmSteamSprite(seedOffset) {
    const size = 128;
    const off = document.createElement("canvas");
    off.width = size;
    off.height = size;
    const oCtx = off.getContext("2d");
    const img = oCtx.createImageData(size, size);
    const data = img.data;

    function hash(x, y) {
      const n = Math.sin(x * 127.1 + y * 311.7 + seedOffset * 74.7) * 43758.5453;
      return n - Math.floor(n);
    }
    function smoothNoise(x, y) {
      const ix = Math.floor(x);
      const iy = Math.floor(y);
      const fx = x - ix;
      const fy = y - iy;
      const ux = fx * fx * (3 - 2 * fx);
      const uy = fy * fy * (3 - 2 * fy);
      const a = hash(ix, iy);
      const b = hash(ix + 1, iy);
      const c = hash(ix, iy + 1);
      const d = hash(ix + 1, iy + 1);
      return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
    }
    function fbm(x, y) {
      let val = 0;
      let amp = 0.5;
      let freq = 1;
      for (let o = 0; o < 4; o++) {
        val += amp * smoothNoise(x * freq, y * freq);
        freq *= 2.05;
        amp *= 0.5;
      }
      return val;
    }

    const half = size * 0.5;
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const dx = (x - half) / half;
        const dy = (y - half) / half;
        const r2 = dx * dx + dy * dy;
        if (r2 >= 1) continue;

        // Soft radial falloff * domain-warped FBM wisp density
        const falloff = Math.pow(1 - r2, 2.1);
        const nx = (x / size) * 4.2;
        const ny = (y / size) * 4.2;
        const warp = fbm(nx + 1.7, ny + 3.1);
        const n = fbm(nx + warp * 1.35, ny + warp * 1.15);
        const density = Math.max(0, (n - 0.22) * 1.45) * falloff;
        const alpha = Math.min(255, Math.round(density * 255));

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

  const steamSprites = [createFbmSteamSprite(1), createFbmSteamSprite(7)];

  function easeInOutSine(x) {
    return -(Math.cos(Math.PI * Math.max(0, Math.min(1, x))) - 1) / 2;
  }

  // Smooth crack-open & close cycle (~7.2s)
  function getCycleState(time) {
    const period = 7.2;
    const u = (time % period) / period;
    let open = 0;
    let venting = 0;

    if (u < 0.36) {
      const p = u / 0.36;
      open = easeInOutSine(p);
      venting = Math.sin(p * Math.PI) * (0.45 + 0.55 * open);
    } else if (u < 0.52) {
      open = 1;
      venting = 0.6 * (1 - (u - 0.36) / 0.16);
    } else if (u < 0.88) {
      const p = (u - 0.52) / 0.36;
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

    slatCount = width <= 768 ? 16 : 28;
    steamParticles = [];
  }

  function spawnSteamBurst(count, open) {
    const isMobile = width <= 768;
    const maxParticles = isMobile ? 64 : 110;
    const slatW = width / slatCount;

    for (let i = 0; i < count; i++) {
      if (steamParticles.length >= maxParticles) break;
      const idx = Math.floor(Math.random() * slatCount);
      const localOpen = getLocalOpen(idx, open);
      if (localOpen < 0.10) continue;

      const gapX = idx * slatW + (slatW * localOpen * 0.12);
      const spawnY = height * (0.24 + Math.random() * 0.68);

      steamParticles.push({
        x: gapX,
        y: spawnY,
        vx: -(18 + Math.random() * 20), // starts gentle behind glass
        vy: -(16 + Math.random() * 22),
        size: (isMobile ? 76 : 108) + Math.random() * 58,
        grow: 1.7 + Math.random() * 0.9,
        maxAlpha: 0.24 + Math.random() * 0.16,
        spriteIdx: i % steamSprites.length,
        rot: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 0.35,
        seed: Math.random() * Math.PI * 2,
        age: 0,
        life: 2.3 + Math.random() * 1.5
      });
    }
  }

  function updateSteam(dt, time) {
    const isMobile = width <= 768;
    const fanWindX = isMobile ? -95 : -135; // steady fan breeze from right -> left

    for (let i = steamParticles.length - 1; i >= 0; i--) {
      const p = steamParticles[i];
      p.age += dt;
      if (p.age >= p.life || p.x < -p.size * 2 || p.y < -p.size * 2) {
        steamParticles.splice(i, 1);
        continue;
      }

      const progress = p.age / p.life;
      if (progress > 0.26) {
        // Once out in front of the glass, right-side fan breeze smoothly accelerates it LEFT
        p.vx += (fanWindX - p.vx) * 1.6 * dt;
        const waveY = Math.sin(time * 2.0 + p.seed + p.x * 0.01) * 18;
        p.x += p.vx * dt;
        p.y += (p.vy + waveY) * dt;
      } else {
        // Emerging from behind the glass through the gap
        p.x += p.vx * dt;
        p.y += p.vy * dt;
      }
      p.rot += p.rotSpeed * dt;
    }
  }

  function drawSteamLayer(frontPass) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";

    for (let i = 0; i < steamParticles.length; i++) {
      const p = steamParticles[i];
      const progress = p.age / p.life;
      // Behind glass while emerging (<= 0.26), then in front sweeping left (> 0.26)
      const isFront = progress > 0.26;
      if (isFront !== frontPass) continue;

      const fadeIn = Math.min(1, progress / 0.15);
      const fadeOut = Math.pow(1 - progress, 1.45);
      const alpha = p.maxAlpha * fadeIn * fadeOut;
      if (alpha <= 0.004) continue;

      const curSize = p.size * (0.58 + progress * p.grow);
      // Slight horizontal elongation as the right-side fan carries it left
      const windStretch = frontPass ? 1.28 : 1.0;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.scale(windStretch, 1);
      ctx.globalAlpha = alpha;
      ctx.drawImage(
        steamSprites[p.spriteIdx],
        -curSize * 0.5,
        -curSize * 0.5,
        curSize,
        curSize
      );
      ctx.restore();
    }

    ctx.restore();
  }

  function drawFlutedGlass(open, time) {
    const slatW = width / slatCount;

    for (let i = 0; i < slatCount; i++) {
      const tNorm = i / Math.max(1, slatCount - 1);
      const localOpen = getLocalOpen(i, open);

      const faceW = slatW * (1 - localOpen * 0.26);
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
      hGrad.addColorStop(0, `rgba(255, 255, 255, ${0.24 + localOpen * 0.14})`);
      hGrad.addColorStop(0.16, "rgba(185, 228, 255, 0.10)");
      hGrad.addColorStop(0.55, "rgba(10, 14, 24, 0.18)");
      hGrad.addColorStop(0.88, "rgba(0, 0, 0, 0.36)");
      hGrad.addColorStop(1, "rgba(0, 0, 0, 0.50)");

      ctx.fillStyle = hGrad;
      ctx.fillRect(xLeft, 0, faceW, height);

      ctx.fillStyle = `rgba(255, 255, 255, ${0.24 + localOpen * 0.16})`;
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

    const { open, venting } = getCycleState(simTime);

    if (venting > 0.04) {
      const spawnRate = (width <= 768 ? 28 : 44) * venting;
      steamSpawnAcc += spawnRate * dt;
      const toSpawn = Math.floor(steamSpawnAcc);
      if (toSpawn > 0) {
        steamSpawnAcc -= toSpawn;
        spawnSteamBurst(toSpawn, open);
      }
    }

    updateSteam(dt, simTime);

    ctx.clearRect(0, 0, width, height);
    // 1. Steam emerging from BEHIND the glass slats
    drawSteamLayer(false);
    // 2. Fluted glass louvers
    drawFlutedGlass(open, simTime);
    // 3. Escaped steam in FRONT of the glass blowing LEFT from a right-side fan breeze
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
