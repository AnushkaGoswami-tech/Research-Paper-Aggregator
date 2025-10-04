const API = location.origin; // same origin (Flask serves frontend)

// Elements
const q = document.getElementById("q");
const btnSearch = document.getElementById("btnSearch");
const results = document.getElementById("results");
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modalTitle");
const modalBody = document.getElementById("modalBody");

// Keep results globally so we can reference them by index
let currentPapers = [];

btnSearch.addEventListener("click", () => search(q.value));
q.addEventListener("keydown", (e) => {
  if (e.key === "Enter") search(q.value);
});

// ---- Helpers ----
function escapeHTML(s) {
  return (s ?? "").toString()
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

// ---- Render a paper card ----
function card(paper, i) {
  const authors = paper.authors?.join(", ") || "—";
  const pub = paper.published ? new Date(paper.published).toDateString() : "—";
  const hasPdf = !!paper.pdf_url;

  return `
    <article class="glass rounded-2xl shadow-lg p-6">
      <h3 class="text-lg md:text-xl font-bold">${escapeHTML(paper.title)}</h3>
      <p class="text-sm text-slate-600 mt-1">Authors: ${escapeHTML(authors)}</p>
      <p class="text-xs text-slate-500">Published: ${escapeHTML(pub)}</p>

      <!-- No abstract/summary shown here -->

      <div class="mt-5 flex flex-wrap gap-2">
        <a href="${paper.link}" target="_blank"
           class="rounded-xl px-3 py-2 bg-white border border-slate-200 hover:bg-slate-100">Open on arXiv</a>
        ${hasPdf ? `<a href="${paper.pdf_url}" target="_blank"
             class="rounded-xl px-3 py-2 bg-white border border-slate-200 hover:bg-slate-100">Open PDF</a>` : ""}
        <button class="rounded-xl px-3 py-2 bg-slate-900 text-white"
                onclick="summarizeAbstract(${i})">
          Summarize
        </button>
        ${hasPdf ? `
          <button class="rounded-xl px-3 py-2 bg-sky-700 text-white"
                  onclick="summarizePDF(${i})">
            Summarize PDF
          </button>` : ""}
      </div>
    </article>
  `;
}

// ---- Search ----
async function search(query) {
  results.innerHTML = "";
  if (!query || !query.trim()) {
    results.innerHTML = `<p class="text-red-600">Please enter a search query.</p>`;
    return;
  }

  results.innerHTML = `<p class="text-slate-600">Loading…</p>`;

  try {
    const url = `${API}/api/search?` + new URLSearchParams({ query, max_results: 20 });
    const r = await fetch(url);
    const data = await r.json();

    console.log("API Response:", data); // 👈 Debug log

    if (!r.ok) throw new Error(data.error || "Search failed");

    currentPapers = data.results || [];

    if (!currentPapers.length) {
      results.innerHTML = `<p class="text-slate-600">No results found for “${escapeHTML(data.query)}”.</p>`;
      return;
    }

    results.innerHTML = `
      <div class="text-sm text-slate-500 mb-3">${data.count} results for “${escapeHTML(data.query)}”</div>
      <div class="grid gap-4 md:grid-cols-2">
        ${currentPapers.map((p, i) => card(p, i)).join("")}
      </div>
    `;
  } catch (err) {
    console.error("Search error:", err);
    results.innerHTML = `<p class="text-red-700">Error: ${escapeHTML(err.message)}</p>`;
  }
}

// ---- Summarize (abstract or PDF) ----
async function summarizeAbstract(i) {
  const paper = currentPapers[i];
  if (!paper) return;

  showModal("Summarizing Abstract…", "Please wait.");
  try {
    const r = await fetch(`${API}/api/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: paper.summary, sentences: 6 })
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || "Summarization failed");
    showModal(paper.title, data.summary || "(Empty summary)");
  } catch (err) {
    showModal("Error", err.message);
  }
}

async function summarizePDF(i) {
  const paper = currentPapers[i];
  if (!paper) return;

  showModal("Summarizing PDF…", "Fetching and extracting text…");
  try {
    const r = await fetch(`${API}/api/summarize_url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pdf_url: paper.pdf_url, sentences: 7, max_pages: 4 })
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || "Summarization failed");
    showModal(paper.title, data.summary || "(Empty summary)");
  } catch (err) {
    showModal("Error", err.message);
  }
}

// ---- Modal ----
function showModal(title, body) {
  modalTitle.textContent = title;
  modalBody.textContent = body;
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function hideModal() {
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}
