const RAW_BASE = "https://raw.githubusercontent.com/jayedanik/nuvio-master-badge-system/main/";

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
    badges: ["4k", "remux", "dolby-vision", "dolby-atmos", "imax", "warnerbros", "english-flag"]
  },
  {
    title: "Avatar: Fire and Ash",
    meta: "2025 · 2160p IMAX UHD REMUX · Real-Debrid · 84.0 GB",
    release: "Avatar.Fire.and.Ash.2025.2160p.UHD.BluRay.REMUX.DV.Atmos.IMAX.HEVC.MKV",
    badges: ["4k", "remux", "dolby-vision", "dolby-atmos", "imax", "20thcentury", "english-flag"]
  },
  {
    title: "Mission: Impossible – The Final Reckoning",
    meta: "2025 · 2160p UHD REMUX · TorBox · 78.6 GB",
    release: "Mission.Impossible.The.Final.Reckoning.2025.2160p.UHD.REMUX.HDR10Plus.Atmos.IMAX.MKV",
    badges: ["4k", "remux", "hdr10plus", "dolby-atmos", "imax", "paramount_studio", "english-flag"]
  },
  {
    title: "Severance · S02E10",
    meta: "2025 · 2160p ATVP WEB-DL · Real-Debrid · 6.4 GB",
    release: "Severance.S02E10.2025.2160p.ATVP.WEB-DL.DDP5.1.Atmos.DV.H265.English.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "appletv", "cached", "english-flag"]
  },
  {
    title: "The Fantastic Four: First Steps",
    meta: "2025 · 2160p DSNP WEB-DL · TorBox · 18.4 GB",
    release: "The.Fantastic.Four.First.Steps.2025.2160p.DSNP.WEB-DL.DV.Atmos.IMAX.H265.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "imax", "disney", "english-flag"]
  },
  {
    title: "Solo Leveling · S02E13",
    meta: "2025 · 1080p CR WEB-DL · Dual-Audio · 1.8 GB",
    release: "[SubsPlease] Solo Leveling S2 - 13 (2025) (1080p) [Dual-Audio] [Crunchyroll] [AV1].mkv",
    badges: ["1080p", "web-dl", "av1", "dual", "crunchyroll", "japanese", "english-flag"]
  },
  {
    title: "Andor · S02E12",
    meta: "2025 · 2160p DSNP WEB-DL · Real-Debrid · 5.8 GB",
    release: "Andor.S02E12.2025.2160p.DSNP.WEB-DL.DV.Atmos.H265.English.MKV",
    badges: ["4k", "web-dl", "dolby-vision", "dolby-atmos", "disney", "cached", "english-flag"]
  },
  {
    title: "Formula 1 · Monaco Grand Prix",
    meta: "2026 · Live Sports Feed · 1080p 60 FPS",
    release: "F1.Grand.Prix.2026.Live.1080p.60fps.HDTV.AAC.English.TS",
    badges: ["live", "1080p", "60fps", "aac", "hdtv", "cached", "english-flag"]
  }
];

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

function renderFlagship(flagIdx, animate = true) {
  activeFlagshipIdx = (flagIdx + FLAGSHIPS.length) % FLAGSHIPS.length;
  const f = FLAGSHIPS[activeFlagshipIdx];
  const t = THEMES[f.idx];
  const url = RAW_BASE + t.json;

  flagTabsEl.querySelectorAll(".flag-tab").forEach((b, i) => b.classList.toggle("active", i === activeFlagshipIdx));
  const apply = () => {
    flagStageEl.innerHTML = `
      <div class="flag-media" data-open="${f.idx}">
        <img src="previews/preview-${t.id}.jpg" alt="${t.name}" />
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
    flagStageEl.classList.remove("flag-swapping");
  };

  if (animate) {
    flagStageEl.classList.add("flag-swapping");
    setTimeout(apply, 180);
  } else {
    apply();
  }
}

function resetFlagTimer() {
  if (flagTimer) clearInterval(flagTimer);
  flagTimer = setInterval(() => {
    if (!flagHoverPaused && !dialogEl.open) renderFlagship(activeFlagshipIdx + 1, true);
  }, 4000);
}

function initFlagships() {
  flagTabsEl.innerHTML = FLAGSHIPS.map((f, i) =>
    `<button type="button" class="flag-tab${i === 0 ? " active" : ""}" data-flag="${i}">${f.tab}</button>`
  ).join("");
  flagTabsEl.addEventListener("click", (e) => {
    const tab = e.target.closest(".flag-tab");
    if (tab) {
      renderFlagship(Number(tab.dataset.flag), true);
      resetFlagTimer();
    }
  });
  flagStageEl.addEventListener("mouseenter", () => { flagHoverPaused = true; });
  flagStageEl.addEventListener("mouseleave", () => { flagHoverPaused = false; });
  renderFlagship(0, false);
  resetFlagTimer();
}

let autoShuffleEnabled = true;
let simHoverPaused = false;
let simTimer = null;

function preloadThemeBadges(theme, titleObj) {
  return Promise.all(titleObj.badges.map((b) => new Promise((resolve) => {
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

  simCopyBtn.onclick = () => copyUrl(RAW_BASE + t.json, simCopyBtn);
  simInspectBtn.onclick = () => openDialog(safeIdx, titleObj.release);

  await preloadThemeBadges(t, titleObj);
  if (seq !== simRenderSeq) return;

  const layers = [simLayer0, simLayer1];
  const badgesHtml = titleObj.badges.map((b) => `<img src="${t.dir}/${b}.webp" alt="${b}" onerror="this.style.display='none'" />`).join("");

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

function stepSimulator() {
  if (!autoShuffleEnabled || simHoverPaused || dialogEl.open) return;
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

  gridEl.innerHTML = list.map((t) => {
    const idx = THEMES.indexOf(t);
    const jsonUrl = RAW_BASE + t.json;
    const isSaved = savedIds.has(t.id);
    return `
      <article class="theme-card">
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
}, { threshold: 0.08 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

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
