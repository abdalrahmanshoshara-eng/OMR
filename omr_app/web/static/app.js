/* OMR grader - single page UI (vanilla JS, no build step, works offline). */
"use strict";

const STATUS_AR = {
  AUTO_APPROVED: "معتمدة تلقائياً",
  REVIEW_REQUIRED: "تحتاج مراجعة",
  MANUALLY_REVIEWED: "تمت مراجعتها",
  FAILED: "فشلت القراءة",
};
const STATUS_HELP = {
  AUTO_APPROVED: "كل الأسئلة واضحة (إجابة واحدة أو فارغ) والمحاذاة موثوقة. لا تحتاج تدخلاً.",
  REVIEW_REQUIRED: "يوجد سؤال واحد على الأقل متعدد الإجابات أو غير واضح (أو الورقة كلها فارغة / المحاذاة ضعيفة). يجب أن يراجعها شخص ويعتمدها.",
  MANUALLY_REVIEWED: "راجعها مستخدم وحسم الأسئلة المشكوك بها ثم اعتمدها. كل تعديل محفوظ في سجل التدقيق.",
  FAILED: "تعذّر التعرف على الورقة: صورة مقصوصة، ليست ورقة الإجابة هذه، فارغة، أو ملف تالف. أعد مسحها.",
};
const VALUE_AR = { BLANK: "فارغ", MULTIPLE: "متعدد", UNCERTAIN: "غير واضح" };
const VALUE_HELP = {
  BLANK: "لم تُظلَّل أي دائرة.",
  MULTIPLE: "ظُلِّلت دائرتان أو أكثر بوضوح. لا يتم التخمين.",
  UNCERTAIN: "علامة جزئية أو باهتة أو إشارة ✓ / ×. لا يتم التخمين.",
};
const BATCH_STATE_AR = { queued: "في الانتظار", processing: "قيد المعالجة", done: "اكتملت", error: "خطأ" };

const $app = document.getElementById("app");
let META = null;
let KEYS = [];
let pollTimer = null;

// ------------------------------------------------------------------ utils
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmtScore = (v) => (v === null || v === undefined ? "—" : Number(v).toLocaleString("en", { maximumFractionDigits: 2 }));
const fmtDate = (ts) => new Date(ts * 1000).toLocaleString("ar-SY-u-nu-latn", { dateStyle: "medium", timeStyle: "short" });
const pct = (v) => Math.round((v || 0) * 100);
const badge = (st) => `<span class="badge st-${esc(st)}">${esc(STATUS_AR[st] || BATCH_STATE_AR[st] || st)}</span>`;
const keyLabel = (k) => (k ? `${k.exam} — ${k.specialization_label_ar || ""}${k.specialization_label ? " (" + k.specialization_label + ")" : ""}` : "");
const keyById = (id) => KEYS.find((k) => k.id === id);
const valueLabel = (v) => VALUE_AR[v] || v || "—";

function toast(msg, err = false) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "show" + (err ? " err" : "");
  clearTimeout(t._h);
  t._h = setTimeout(() => (t.className = ""), 3200);
}

async function api(path, opts = {}) {
  const res = await fetch(path, opts);
  if (!res.ok) {
    let msg = res.statusText;
    try { msg = (await res.json()).detail || msg; } catch (_) { /* not json */ }
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return res.headers.get("content-type")?.includes("json") ? res.json() : res;
}
const jsonOpts = (method, body) => ({ method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

function reviewer() {
  try { return localStorage.getItem("omr_reviewer") || ""; } catch (_) { return ""; }
}
function setReviewer(v) {
  try { localStorage.setItem("omr_reviewer", v); } catch (_) { /* storage blocked */ }
}

function keyOptions(selected) {
  const byExam = {};
  KEYS.forEach((k) => (byExam[k.exam] = byExam[k.exam] || []).push(k));
  return Object.entries(byExam).map(([exam, ks]) =>
    `<optgroup label="${esc(exam)}">${ks.map((k) =>
      `<option value="${esc(k.id)}" ${k.id === selected ? "selected" : ""}>${esc(k.specialization_label_ar || k.specialization)}${k.specialization_label ? " — " + esc(k.specialization_label) : ""}</option>`).join("")}</optgroup>`).join("");
}

function lightbox(src) {
  const lb = document.getElementById("lightbox");
  lb.querySelector("img").src = src;
  lb.hidden = false;
}
document.getElementById("lightbox").addEventListener("click", (e) => {
  if (e.target.matches("[data-close]") || e.target.id === "lightbox") e.currentTarget.hidden = true;
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") document.getElementById("lightbox").hidden = true; });

// ------------------------------------------------------------------ router
const routes = [
  [/^#?\/?$/, pageBatches, "batches"],
  [/^#\/new$/, pageNew, "new"],
  [/^#\/batch\/(\d+)$/, pageBatch, "batches"],
  [/^#\/sheet\/(\d+)$/, pageSheet, "batches"],
  [/^#\/keys$/, pageKeys, "keys"],
  [/^#\/help$/, pageHelp, "help"],
];

async function route() {
  clearInterval(pollTimer);
  const h = location.hash || "#/";
  for (const [re, fn, nav] of routes) {
    const m = h.match(re);
    if (m) {
      document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("active", a.dataset.nav === nav));
      try {
        await fn(...m.slice(1));
      } catch (e) {
        $app.innerHTML = `<div class="card empty"><div class="big">⚠️</div><p>${esc(e.message)}</p><a class="btn" href="#/">العودة</a></div>`;
      }
      window.scrollTo({ top: 0 });
      return;
    }
  }
  location.hash = "#/";
}
window.addEventListener("hashchange", route);

// ------------------------------------------------------------------ pages: batches
function statCards(c, total, avg, filter) {
  const card = (cls, v, l, st) =>
    `<button class="stat ${cls} ${filter === st ? "sel" : ""}" data-filter="${st ?? ""}" title="تصفية"><div class="v num">${v}</div><div class="l">${l}</div></button>`;
  const processed = total - (c.FAILED || 0);
  return `<div class="stats">
    ${card("t-total", total, "إجمالي الأوراق", "")}
    ${card("t-total", processed, "تمت قراءتها", "__processed")}
    ${card("t-ok", c.AUTO_APPROVED || 0, STATUS_AR.AUTO_APPROVED, "AUTO_APPROVED")}
    ${card("t-review", c.REVIEW_REQUIRED || 0, STATUS_AR.REVIEW_REQUIRED, "REVIEW_REQUIRED")}
    ${card("t-done", c.MANUALLY_REVIEWED || 0, STATUS_AR.MANUALLY_REVIEWED, "MANUALLY_REVIEWED")}
    ${card("t-fail", c.FAILED || 0, STATUS_AR.FAILED, "FAILED")}
    <div class="stat"><div class="v num">${avg === null || avg === undefined ? "—" : fmtScore(avg)}</div><div class="l">متوسط العلامة</div></div>
  </div>`;
}

async function pageBatches() {
  const batches = await api("/api/batches");
  const tot = { AUTO_APPROVED: 0, REVIEW_REQUIRED: 0, MANUALLY_REVIEWED: 0, FAILED: 0 };
  let sheets = 0;
  batches.forEach((b) => { Object.entries(b.counts).forEach(([k, v]) => (tot[k] = (tot[k] || 0) + v)); sheets += b.total_sheets; });
  $app.innerHTML = `
    <div class="page-head">
      <div><h1>الدفعات</h1><p class="sub">كل دفعة = مجموعة أوراق إجابة لنفس الامتحان والاختصاص.</p></div>
      <div class="actions"><a class="btn primary lg" href="#/new">+ رفع أوراق جديدة</a></div>
    </div>
    ${batches.length ? statCards(tot, sheets, null, null).replace(/<button/g, "<div").replace(/<\/button>/g, "</div>") : ""}
    <div class="card">
      ${batches.length ? `<div class="table-wrap"><table class="tbl">
        <thead><tr><th>#</th><th>الدفعة</th><th>الامتحان / الاختصاص</th><th>التاريخ</th><th>الحالة</th>
          <th>الأوراق</th><th>معتمدة</th><th>للمراجعة</th><th>فشلت</th><th>المتوسط</th></tr></thead>
        <tbody>${batches.map((b) => `
          <tr data-go="#/batch/${b.id}">
            <td class="num">${b.id}</td><td><b>${esc(b.name)}</b></td>
            <td>${esc(keyLabel(keyById(b.answer_key_id)) || b.answer_key_id)}</td>
            <td class="small muted">${fmtDate(b.created_at)}</td>
            <td>${badge(b.state)}${b.state === "processing" ? ` <span class="small num">${b.processed_files}/${b.total_files}</span>` : ""}</td>
            <td class="num">${b.total_sheets}</td>
            <td class="num" style="color:var(--ok)">${(b.counts.AUTO_APPROVED || 0) + (b.counts.MANUALLY_REVIEWED || 0)}</td>
            <td class="num" style="color:var(--review)"><b>${b.counts.REVIEW_REQUIRED || 0}</b></td>
            <td class="num" style="color:var(--fail)">${b.counts.FAILED || 0}</td>
            <td class="num">${b.avg_score === null ? "—" : fmtScore(b.avg_score)}</td>
          </tr>`).join("")}</tbody></table></div>`
        : `<div class="empty"><div class="big">🗂️</div><p>لا توجد دفعات بعد.<br>ابدأ برفع صور أو ملفات PDF لأوراق الإجابة الممسوحة.</p>
           <a class="btn primary lg" href="#/new">+ رفع أوراق</a></div>`}
    </div>`;
  $app.querySelectorAll("[data-go]").forEach((tr) => tr.addEventListener("click", () => (location.hash = tr.dataset.go)));
  if (batches.some((b) => b.state === "queued" || b.state === "processing")) pollTimer = setInterval(() => location.hash === "#/" || !location.hash ? pageBatches() : null, 2500);
}

// ------------------------------------------------------------------ page: new batch
async function pageNew() {
  let files = [];
  $app.innerHTML = `
    <div class="page-head"><div><h1>دفعة جديدة</h1><p class="sub">اختر الامتحان والاختصاص ثم ارفع الأوراق. يدعم PNG و JPG و PDF (متعدد الصفحات: كل صفحة = ورقة).</p></div></div>
    <form id="f" class="grid" style="grid-template-columns:minmax(0,1fr) minmax(0,1.3fr)">
      <div class="card grid">
        <label class="field">اسم الدفعة <small>اختياري — مثل: قاعة 3 / الفترة الصباحية</small>
          <input type="text" name="name" placeholder="دفعة ${new Date().toLocaleDateString("en-CA")}"></label>
        <label class="field">الامتحان والاختصاص (مفتاح الإجابة)
          <select name="answer_key_id" required>${keyOptions(KEYS[0]?.id)}</select>
          <small>يمكن تغيير الاختصاص لاحقاً لكل ورقة أو للدفعة كاملة، ويُعاد حساب العلامة.</small></label>
        <div id="keyPreview"></div>
      </div>
      <div class="card">
        <div class="dropzone" id="dz" tabindex="0">
          <div class="big">📄</div><b>اسحب الملفات إلى هنا أو اضغط للاختيار</b>
          <div class="muted small">صور الماسح الضوئي أو ملفات PDF • يمكن اختيار مئات الملفات دفعة واحدة</div>
          <input type="file" id="fi" multiple accept=".png,.jpg,.jpeg,.pdf,.tif,.tiff,.bmp,.webp" hidden>
        </div>
        <ul class="filelist" id="fl"></ul>
        <div class="row" style="margin-top:14px"><span class="muted" id="fcount">لم يتم اختيار ملفات</span><span class="spacer"></span>
          <button class="btn primary lg" id="go" disabled>بدء التصحيح ←</button></div>
      </div>
    </form>`;
  const f = document.getElementById("f"), dz = document.getElementById("dz"), fi = document.getElementById("fi");
  const preview = () => {
    const k = keyById(f.answer_key_id.value);
    document.getElementById("keyPreview").innerHTML = k ? `<div class="small muted">الإجابات الصحيحة:</div>${keyAnswersHtml(k)}` : "";
  };
  const render = () => {
    document.getElementById("fl").innerHTML = files.map((x, i) => `<li><span>${esc(x.name)}</span><span class="muted small num">${(x.size / 1024).toFixed(0)} KB <a href="#" data-rm="${i}">✕</a></span></li>`).join("");
    document.getElementById("fcount").textContent = files.length ? `${files.length} ملف` : "لم يتم اختيار ملفات";
    document.getElementById("go").disabled = !files.length;
  };
  const add = (list) => {
    const ok = [...list].filter((x) => /\.(png|jpe?g|pdf|tiff?|bmp|webp)$/i.test(x.name));
    if (ok.length < list.length) toast("تم تجاهل ملفات بصيغة غير مدعومة", true);
    files = files.concat(ok);
    render();
  };
  f.answer_key_id.addEventListener("change", preview);
  preview();
  dz.addEventListener("click", () => fi.click());
  dz.addEventListener("keydown", (e) => (e.key === "Enter" || e.key === " ") && fi.click());
  fi.addEventListener("change", () => add(fi.files));
  ["dragenter", "dragover"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("over"); }));
  dz.addEventListener("drop", (e) => add(e.dataTransfer.files));
  document.getElementById("fl").addEventListener("click", (e) => {
    if (e.target.dataset.rm !== undefined) { e.preventDefault(); files.splice(+e.target.dataset.rm, 1); render(); }
  });
  f.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("go");
    btn.disabled = true;
    btn.textContent = "جارِ الرفع…";
    const fd = new FormData();
    fd.append("answer_key_id", f.answer_key_id.value);
    fd.append("name", f.name.value);
    files.forEach((x) => fd.append("files", x, x.name));
    try {
      const b = await api("/api/batches", { method: "POST", body: fd });
      toast("تم الرفع، بدأت المعالجة");
      location.hash = `#/batch/${b.id}`;
    } catch (err) {
      toast(err.message, true);
      btn.disabled = false;
      btn.textContent = "بدء التصحيح ←";
    }
  });
}

// ------------------------------------------------------------------ page: batch
async function pageBatch(bid) {
  let filter = "", search = "";
  const load = async () => {
    const [b, sheets] = await Promise.all([api(`/api/batches/${bid}`), api(`/api/batches/${bid}/sheets`)]);
    return { b, sheets };
  };
  let { b, sheets } = await load();

  const render = () => {
    const key = keyById(b.answer_key_id);
    const busy = b.state === "queued" || b.state === "processing";
    const shown = sheets.filter((s) =>
      (!filter || (filter === "__processed" ? s.status !== "FAILED" : s.status === filter)) &&
      (!search || `${s.candidate_id} ${s.candidate_name || ""} ${s.source_file}`.toLowerCase().includes(search.toLowerCase())));
    const firstReview = sheets.find((s) => s.status === "REVIEW_REQUIRED");
    $app.innerHTML = `
      <div class="page-head">
        <div><div class="small"><a href="#/">الدفعات</a> ‹</div><h1>${esc(b.name)}</h1>
          <p class="sub">${esc(keyLabel(key))} • ${fmtDate(b.created_at)} • ${badge(b.state)}</p></div>
        <div class="actions">
          ${firstReview ? `<a class="btn primary" href="#/sheet/${firstReview.id}">ابدأ المراجعة (${b.counts.REVIEW_REQUIRED})</a>` : ""}
          <a class="btn" href="/api/batches/${bid}/export.xlsx">⬇ Excel</a>
          <a class="btn" href="/api/batches/${bid}/export.csv">⬇ CSV</a>
          <a class="btn" href="/api/batches/${bid}/export.csv?details=true" title="نسب التعبئة لكل خيار لكل سؤال">⬇ تفاصيل التدقيق CSV</a>
          <a class="btn" href="/api/batches/${bid}/export.json">⬇ JSON</a>
        </div>
      </div>
      ${busy ? `<div class="card" style="margin-bottom:16px"><div class="row"><b>جارِ معالجة الملفات…</b><span class="spacer"></span>
          <span class="num">${b.processed_files} / ${b.total_files}</span></div>
          <div class="progress" style="margin-top:8px"><div style="width:${(100 * b.processed_files) / Math.max(1, b.total_files)}%"></div></div></div>` : ""}
      ${b.state === "error" ? `<div class="card st-FAILED" style="margin-bottom:16px">خطأ في المعالجة: ${esc(b.error)}</div>` : ""}
      ${statCards(b.counts, b.total_sheets, b.avg_score, filter)}
      <div class="card">
        <div class="row" style="margin-bottom:12px">
          <input type="text" id="q" placeholder="بحث بالاسم أو الرقم أو اسم الملف…" value="${esc(search)}" style="flex:1;max-width:360px">
          <span class="spacer"></span>
          <label class="row small muted">تغيير الاختصاص لكل الدفعة:
            <select id="rekey">${keyOptions(b.answer_key_id)}</select></label>
        </div>
        ${shown.length ? `<div class="table-wrap"><table class="tbl"><thead><tr>
            <th>#</th><th>المرشح</th><th>الملف</th><th>الحالة</th><th>العلامة</th><th>الإجابات (س1 ← س10)</th><th>الملاحظات</th></tr></thead>
          <tbody>${shown.map((s) => sheetRow(s)).join("")}</tbody></table></div>`
          : `<div class="empty">${busy ? "بانتظار النتائج…" : "لا توجد أوراق مطابقة"}</div>`}
      </div>`;
    $app.querySelectorAll("[data-filter]").forEach((el) => el.addEventListener("click", () => { filter = filter === el.dataset.filter ? "" : el.dataset.filter; render(); }));
    $app.querySelectorAll("[data-go]").forEach((tr) => tr.addEventListener("click", () => (location.hash = tr.dataset.go)));
    const q = document.getElementById("q");
    q.addEventListener("input", () => { search = q.value; const pos = q.selectionStart; render(); const q2 = document.getElementById("q"); q2.focus(); q2.setSelectionRange(pos, pos); });
    document.getElementById("rekey").addEventListener("change", async (e) => {
      const k = keyById(e.target.value);
      if (!confirm(`تغيير مفتاح الإجابة لكل أوراق الدفعة إلى:\n${keyLabel(k)}\nوإعادة حساب كل العلامات؟`)) { e.target.value = b.answer_key_id; return; }
      try {
        await api(`/api/batches/${bid}/answer-key`, jsonOpts("POST", { answer_key_id: k.id, actor: reviewer() || null }));
        ({ b, sheets } = await load());
        render();
        toast("تم تغيير الاختصاص وإعادة حساب العلامات");
      } catch (err) { toast(err.message, true); }
    });
  };
  render();
  if (b.state === "queued" || b.state === "processing") {
    pollTimer = setInterval(async () => {
      if (!location.hash.startsWith(`#/batch/${bid}`)) return clearInterval(pollTimer);
      ({ b, sheets } = await load());
      if (document.activeElement?.id !== "q") render();
      if (!(b.state === "queued" || b.state === "processing")) { clearInterval(pollTimer); render(); toast("اكتملت معالجة الدفعة"); }
    }, 1500);
  }
}

function sheetRow(s) {
  const mini = Array.from({ length: META.questions }, (_, i) => {
    const q = String(i + 1), v = s.answers[q];
    const cls = !v ? "neutral" : VALUE_AR[v] ? v : s.correct_map[q] ? "correct" : "wrong";
    return `<span class="ans ${cls}" title="س${q}: ${esc(valueLabel(v))}">${esc(v ? (VALUE_AR[v] ? { BLANK: "–", MULTIPLE: "✱", UNCERTAIN: "?" }[v] : v) : "·")}</span>`;
  }).join("");
  const max = s.max_score || 100;
  return `<tr data-go="#/sheet/${s.id}">
    <td class="num muted">${s.id}</td>
    <td><b class="${s.candidate_name ? "" : "ltr"}">${esc(s.candidate_name || s.candidate_id)}</b>${s.candidate_name ? `<div class="small muted ltr">${esc(s.candidate_id)}</div>` : ""}</td>
    <td class="small muted"><span class="ltr">${esc(s.source_file)}</span>${s.page > 1 || /_p\d+$/.test(s.candidate_id || "") ? ` • ص${s.page}` : ""}</td>
    <td>${badge(s.status)}</td>
    <td>${s.score === null ? "—" : `<div class="scorebar"><b class="num">${fmtScore(s.score)}</b><div class="track"><div class="fillx" style="width:${(100 * s.score) / max}%"></div></div></div>`}</td>
    <td><div class="mini-answers">${s.status === "FAILED" ? "" : mini}</div></td>
    <td class="small">${esc((s.status_reasons || []).join(" • "))}</td>
  </tr>`;
}

// ------------------------------------------------------------------ page: sheet review
async function pageSheet(sid) {
  let s = await api(`/api/sheets/${sid}`);
  let ovr = {};
  let view = "overlay";

  const render = () => {
    const r = s.result;
    const key = keyById(r.answer_key_id) || keyById(s.batch.answer_key_id);
    const failed = r.status === "FAILED";
    const qs = r.questions || [];
    const finalOf = (qd) => (qd.q in ovr ? ovr[qd.q] || qd.detected : qd.override || qd.detected);
    const unresolved = qs.filter((qd) => ["MULTIPLE", "UNCERTAIN"].includes(finalOf(qd)));
    // live preview of score with pending overrides
    let preview = 0;
    qs.forEach((qd) => { if (key && finalOf(qd) === key.answers[String(qd.q)]) preview += Number((key.scoring.question_scores || {})[qd.q] ?? key.scoring.question_score); });
    const dirty = Object.keys(ovr).length > 0;
    const art = r.artifacts || {};
    const img = (k) => `/api/sheets/${sid}/image/${k}?v=${encodeURIComponent(s.updated_at)}`;

    $app.innerHTML = `
      <div class="page-head">
        <div><div class="small"><a href="#/">الدفعات</a> ‹ <a href="#/batch/${s.batch_id}">${esc(s.batch.name)}</a> ‹</div>
          <h1 class="${r.candidate_name ? "" : "ltr"}">${esc(r.candidate_name || r.candidate_id)}</h1>
          <p class="sub"><span class="ltr">${esc(r.source_file)}</span>${r.page > 1 ? " • صفحة " + r.page : ""} • ورقة ${s.nav.position} من ${s.nav.total} • متبقٍ للمراجعة: <b>${s.nav.review_left}</b></p></div>
        <div class="actions">
          <a class="btn ${s.nav.prev ? "" : "disabled"}" ${s.nav.prev ? `href="#/sheet/${s.nav.prev}"` : ""}>→ السابقة</a>
          <a class="btn ${s.nav.next ? "" : "disabled"}" ${s.nav.next ? `href="#/sheet/${s.nav.next}"` : ""}>التالية ←</a>
        </div>
      </div>
      <div class="review-grid">
        <section class="card viewer">
          ${failed ? `<div class="empty"><div class="big">⚠️</div><p><b>لم يتم التعرف على الورقة</b><br>${esc(r.error || "")}</p>
              <p class="small">الحلول: أعد مسح الورقة كاملة بوضوح (بدون قص)، وتأكد أنها ورقة الإجابة المعتمدة، ثم ارفعها في دفعة جديدة.</p>
              <a class="btn" href="${img("original")}" target="_blank">فتح الملف الأصلي</a></div>` : `
          <div class="tabs chips">
            <button class="chip ${view === "overlay" ? "sel" : ""}" data-view="overlay">الورقة مع نتيجة التصحيح</button>
            <button class="chip ${view === "aligned" ? "sel" : ""}" data-view="aligned">الورقة بعد المحاذاة</button>
            <a class="chip" href="${img("original")}" target="_blank">الملف الأصلي ↗</a>
          </div>
          <img class="sheet" src="${img(view)}" alt="صورة الورقة" title="اضغط للتكبير">
          <div class="small muted" style="margin-top:6px">الدوائر: <span style="color:var(--ok)">■ صحيحة</span> • <span style="color:var(--wrong)">■ خاطئة</span> •
            <span style="color:var(--unsure)">■ غير واضحة/متعددة</span> • <span style="color:#0078c8">○ الإجابة الصحيحة</span> • الرقم = نسبة التعبئة %</div>
          <div class="crops">
            ${["candidate_name", "specialization", "exam_date"].filter((k) => (art.fields || {})[k]).map((k) => `
              <div class="crop"><span class="small muted">${{ candidate_name: "الاسم (كما كُتب)", specialization: "الاختصاص (كما كُتب)", exam_date: "تاريخ الامتحان" }[k]}</span>
              <img src="${img("field_" + k)}" alt="${k}" data-zoom></div>`).join("")}
          </div>`}
        </section>

        <section>
          <div class="card status-banner st-${esc(r.status)}">
            ${badge(r.status)}
            <div class="small">${esc(STATUS_HELP[r.status] || "")}</div>
            <div class="score num">${failed ? "—" : fmtScore(r.score)}<span class="muted" style="font-size:16px"> / ${fmtScore(r.max_score)}</span></div>
            ${(r.status_reasons || []).length ? `<ul class="reasons">${r.status_reasons.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
          </div>

          <div class="card">
            <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">
              <label class="field">رقم / معرّف المرشح <input type="text" id="cid" dir="auto" value="${esc(r.candidate_id)}"></label>
              <label class="field">اسم المرشح <small>يُدخل يدوياً من صورة الاسم</small><input type="text" id="cname" dir="auto" value="${esc(r.candidate_name || "")}" placeholder="الاسم الكامل"></label>
              <label class="field">الاختصاص (مفتاح الإجابة) <select id="ckey">${keyOptions(r.answer_key_id)}</select></label>
              <label class="field">اسم المراجِع <input type="text" id="actor" value="${esc(reviewer())}" placeholder="اسمك (يُحفظ في السجل)"></label>
            </div>
          </div>

          ${failed ? "" : `<div class="card">
            <div class="row" style="margin-bottom:6px"><h2 style="margin:0">الأسئلة</h2><span class="spacer"></span>
              <span class="small muted">الشريط = نسبة تعبئة الدائرة • <span class="key-mark"></span> = إجابة المفتاح • "تعديل…" لحسم السؤال يدوياً</span></div>
            <table class="qtable"><thead><tr><th>س</th><th>نسب التعبئة</th><th>المكتشف</th><th>الصحيح</th><th>النهائي</th><th></th></tr></thead><tbody>
            ${qs.map((qd) => {
              const fin = finalOf(qd), exp = key ? key.answers[String(qd.q)] : qd.expected;
              const ok = fin === exp, special = VALUE_AR[fin];
              const attn = ["MULTIPLE", "UNCERTAIN"].includes(fin);
              const cur = qd.q in ovr ? ovr[qd.q] : qd.override;
              return `<tr class="q ${attn ? "attn" : ""}">
                <td class="qnum num">${qd.q}</td>
                <td><div class="fills">${META.options.map((o) => `
                    <div class="fill ${qd.detected === o || (qd.detected in VALUE_AR && qd.fills[o] >= META.thresholds.classification.uncertain_min_fill) ? "sel" : ""} ${o === exp ? "exp" : ""} ${qd.shapes?.[o] === "strokes" ? "stroke" : ""}"
                      title="${o}: تعبئة ${pct(qd.fills[o])}% • داخل الدائرة ${pct(qd.hole?.[o])}%${qd.shapes?.[o] === "strokes" ? " • شكل ✓/×" : ""}">
                      <span class="o">${o}</span><span class="p num">${pct(qd.fills[o])}%</span><div class="bar"><i style="width:${pct(qd.fills[o])}%"></i></div></div>`).join("")}</div>
                  <div class="reason">${esc(qd.reason)}</div></td>
                <td><span class="ans ${VALUE_AR[qd.detected] ? qd.detected : "neutral"}" title="${esc(VALUE_HELP[qd.detected] || "")}">${esc(valueLabel(qd.detected))}</span></td>
                <td><span class="ans neutral">${esc(exp || "—")}</span></td>
                <td><span class="ans ${special ? fin : ok ? "correct" : "wrong"}">${esc(valueLabel(fin))}</span></td>
                <td><select class="ovr ${cur ? "set" : ""}" data-q="${qd.q}" aria-label="تعديل السؤال ${qd.q}">
                    <option value="">${cur ? "↺ إلغاء التعديل" : "تعديل…"}</option>
                    ${[...META.options, "BLANK"].map((o) => `<option value="${o}" ${cur === o ? "selected" : ""}>${o === "BLANK" ? "فارغ" : o}</option>`).join("")}
                  </select></td></tr>`;
            }).join("")}
            </tbody></table>
            <div class="review-actions">
              <button class="btn" id="save">💾 حفظ</button>
              <button class="btn success" id="approve" ${unresolved.length ? "disabled" : ""}
                title="${unresolved.length ? "احسم الأسئلة: " + unresolved.map((x) => x.q).join("، ") : "اعتماد الورقة"}">✔ اعتماد الورقة</button>
              ${s.nav.next_review ? `<button class="btn primary" id="approveNext" ${unresolved.length ? "disabled" : ""}>✔ اعتماد والانتقال للتالية ←</button>` : ""}
              ${r.status === "MANUALLY_REVIEWED" ? `<button class="btn" id="reopen">↺ إعادة فتح المراجعة</button>` : ""}
              <span class="spacer"></span>
              ${dirty ? `<span class="small" style="color:var(--review)">تعديلات غير محفوظة • العلامة بعد التعديل: <b class="num">${fmtScore(preview)}</b></span>` : ""}
              ${unresolved.length ? `<span class="small" style="color:var(--review)">يجب حسم: ${unresolved.map((x) => "س" + x.q).join("، ")}</span>` : ""}
            </div>
          </div>`}

          <div class="card">
            <details class="tech"><summary>تفاصيل تقنية (المحاذاة، الحبر، الإعدادات)</summary>
              <dl class="kv">
                <dt>المحاذاة</dt><dd>${r.alignment?.ok ? "ناجحة" : "فشلت"} ${r.alignment?.low_confidence ? "(ثقة منخفضة)" : ""}</dd>
                <dt>نقاط التطابق (inliers)</dt><dd class="num">${r.alignment?.inliers ?? "—"} / ${r.alignment?.good_matches ?? "—"}</dd>
                <dt>الدوران</dt><dd class="num">${r.alignment?.rotation_deg ?? "—"}°</dd>
                <dt>المقياس</dt><dd class="num">${r.alignment?.scale ?? "—"}</dd>
                <dt>دوائر مطابقة للقالب</dt><dd class="num">${r.alignment?.glyph_matches ?? "—"} / 40 (خطأ ${r.alignment?.residual_px ?? "—"} px)</dd>
                <dt>مستوى الورق / الحبر</dt><dd class="num">${r.ink?.paper_level ?? "—"} / ${r.ink?.ink_level ?? "—"} (عتبة ${r.ink?.pixel_threshold ?? "—"})</dd>
                <dt>أبعاد الصورة</dt><dd class="num">${r.image?.width ?? "—"} × ${r.image?.height ?? "—"}</dd>
                <dt>زمن المعالجة</dt><dd class="num">${r.processing_ms ?? "—"} ms</dd>
                <dt>بصمة الإعدادات</dt><dd class="num">${esc(r.config_fingerprint)} (محرك ${esc(r.engine_version)})</dd>
              </dl>
              <div class="row" style="margin-top:10px">
                <button class="btn sm" id="reprocess">⟳ إعادة المعالجة بالإعدادات الحالية</button>
                <a class="btn sm" id="dljson" href="#">⬇ نتيجة الورقة JSON</a></div>
            </details>
          </div>

          <div class="card"><h3>سجل التدقيق</h3>
            <ul class="audit">${(s.audit || []).slice().reverse().map((a) => `<li><time>${fmtDate(a.ts)}</time><b>${esc(auditLabel(a.action))}</b>
              ${a.actor ? ` — ${esc(a.actor)}` : ""}<div class="small muted">${esc(auditText(a))}</div></li>`).join("") || "<li class='muted'>لا يوجد</li>"}</ul></div>
        </section>
      </div>`;

    // events
    $app.querySelectorAll("[data-view]").forEach((b) => b.addEventListener("click", () => { view = b.dataset.view; render(); }));
    $app.querySelectorAll("img.sheet, img[data-zoom]").forEach((im) => im.addEventListener("click", () => lightbox(im.src)));
    $app.querySelectorAll("select.ovr").forEach((sel) => sel.addEventListener("change", () => {
      const q = +sel.dataset.q, qd = qs.find((x) => x.q === q), v = sel.value || null;
      if ((v || null) === (qd.override || null)) delete ovr[q]; else ovr[q] = v;
      render();
    }));
    document.getElementById("actor")?.addEventListener("change", (e) => setReviewer(e.target.value.trim()));
    const save = async (extra = {}) => {
      const body = {
        candidate_id: document.getElementById("cid").value,
        candidate_name: document.getElementById("cname").value,
        answer_key_id: document.getElementById("ckey").value,
        actor: document.getElementById("actor").value.trim() || null,
        overrides: Object.fromEntries(Object.entries(ovr).map(([q, v]) => [q, v])),
        ...extra,
      };
      setReviewer(body.actor || "");
      s = await api(`/api/sheets/${sid}`, jsonOpts("PATCH", body));
      ovr = {};
      return s;
    };
    const wrap = (fn) => async () => { try { await fn(); } catch (e) { toast(e.message, true); } };
    document.getElementById("save")?.addEventListener("click", wrap(async () => { await save(); render(); toast("تم الحفظ"); }));
    document.getElementById("ckey")?.addEventListener("change", wrap(async () => { await save(); render(); toast("تم تغيير الاختصاص وإعادة حساب العلامة"); }));
    if (failed) {
      ["cid", "cname"].forEach((id) => document.getElementById(id).addEventListener("change", wrap(async () => { await save(); render(); toast("تم الحفظ"); })));
    }
    document.getElementById("approve")?.addEventListener("click", wrap(async () => { await save({ approve: true }); render(); toast("تم اعتماد الورقة"); }));
    document.getElementById("approveNext")?.addEventListener("click", wrap(async () => {
      const next = s.nav.next_review;
      await save({ approve: true });
      toast("تم الاعتماد");
      location.hash = `#/sheet/${s.nav.next_review || next}`;
    }));
    document.getElementById("reopen")?.addEventListener("click", wrap(async () => { await save({ reopen: true }); render(); toast("أعيد فتح المراجعة"); }));
    document.getElementById("reprocess")?.addEventListener("click", wrap(async () => {
      s = await api(`/api/sheets/${sid}/reprocess`, { method: "POST" });
      render();
      toast("تمت إعادة المعالجة");
    }));
    document.getElementById("dljson")?.addEventListener("click", (e) => {
      e.preventDefault();
      const blob = new Blob([JSON.stringify(s.result, null, 1)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${s.result.candidate_id}.json`;
      a.click();
      URL.revokeObjectURL(a.href);
    });
  };
  render();
}

function auditLabel(a) {
  return { processed: "تمت القراءة الآلية", review: "مراجعة يدوية", reprocessed: "إعادة معالجة", answer_key_changed: "تغيير الاختصاص" }[a] || a;
}
function auditText(a) {
  const d = a.details || {};
  if (a.action === "processed") return `${STATUS_AR[d.status] || d.status} • العلامة ${fmtScore(d.score)}${(d.reasons || []).length ? " • " + d.reasons.join("، ") : ""}`;
  if (a.action === "answer_key_changed") return `${d.from} ← ${d.to} • العلامة ${fmtScore(d.score)}`;
  const parts = [];
  Object.entries(d).forEach(([k, v]) => {
    if (/^Q\d+$/.test(k)) parts.push(`س${k.slice(1)}: ${valueLabel(v.from)} ← ${valueLabel(v.to)} (المكتشف: ${valueLabel(v.detected)})`);
    else if (k === "candidate_id") parts.push(`المعرّف: ${v.from} ← ${v.to}`);
    else if (k === "candidate_name") parts.push(`الاسم: ${v.from || "—"} ← ${v.to}`);
    else if (k === "answer_key_id") parts.push(`الاختصاص: ${v.from} ← ${v.to}`);
    else if (k === "approved") parts.push("اعتماد");
    else if (k === "reopened") parts.push("إعادة فتح");
  });
  if (d.score !== undefined) parts.push(`العلامة ${fmtScore(d.score)} • ${STATUS_AR[d.status] || d.status}`);
  return parts.join(" • ");
}

// ------------------------------------------------------------------ page: answer keys
function keyAnswersHtml(k) {
  return `<div class="key-answers">${Object.entries(k.answers).map(([q, a]) => `<div><span class="muted">${q}</span><b>${esc(a)}</b></div>`).join("")}</div>`;
}

async function pageKeys(editId) {
  KEYS = await api("/api/keys");
  $app.innerHTML = `
    <div class="page-head"><div><h1>مفاتيح الإجابة</h1>
      <p class="sub">كل مفتاح ملف JSON مستقل في <code>config/answer_keys/</code> — يمكن إضافة امتحان أو اختصاص جديد دون تعديل الكود.</p></div>
      <div class="actions"><button class="btn primary" id="newKey">+ مفتاح جديد</button></div></div>
    <div id="formHost"></div>
    <div class="keys">${KEYS.map((k) => `
      <div class="card"><div class="row"><div><b>${esc(k.specialization_label_ar || k.specialization)}</b>
        <div class="small muted">${esc(k.specialization_label || "")} • ${esc(k.exam)}</div></div><span class="spacer"></span>
        <button class="btn sm" data-edit="${esc(k.id)}">تعديل</button></div>
        ${keyAnswersHtml(k)}
        <div class="small muted">العلامة الكلية <b class="num">${k.scoring.total_score}</b> • لكل سؤال <b class="num">${k.scoring.question_score ?? "مخصص"}</b>
          • الخطأ <b class="num">${k.scoring.wrong_score}</b> • الفارغ <b class="num">${k.scoring.blank_score}</b></div>
        <div class="small muted mono">${esc(k.id)}</div></div>`).join("")}</div>`;
  const showForm = (k) => {
    const isNew = !k;
    k = k || { id: "", exam: KEYS[0]?.exam || "", specialization: "", specialization_label: "", specialization_label_ar: "",
      answers: Object.fromEntries(Array.from({ length: META.questions }, (_, i) => [String(i + 1), "A"])),
      scoring: { total_score: 100, question_score: 100 / META.questions, wrong_score: 0, blank_score: 0 } };
    document.getElementById("formHost").innerHTML = `
      <form class="card" id="kf" style="margin-bottom:16px"><h2>${isNew ? "مفتاح إجابة جديد" : "تعديل: " + esc(k.id)}</h2>
        <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
          <label class="field">اسم الامتحان<input type="text" name="exam" required value="${esc(k.exam)}"></label>
          <label class="field">الاختصاص بالعربية<input type="text" name="specialization_label_ar" required value="${esc(k.specialization_label_ar || "")}"></label>
          <label class="field">الاختصاص بالإنجليزية<input type="text" name="specialization_label" value="${esc(k.specialization_label || "")}"></label>
          <label class="field">رمز الاختصاص <small>أحرف إنجليزية صغيرة و _</small><input type="text" name="specialization" required pattern="[a-z0-9_\\-]+" value="${esc(k.specialization)}"></label>
          <label class="field">المعرّف <small>اسم الملف</small><input type="text" name="id" required pattern="[a-z0-9][a-z0-9_\\-]+" value="${esc(k.id)}" ${isNew ? "" : "readonly"}></label>
        </div>
        <h3 style="margin-top:14px">الإجابات الصحيحة</h3>
        <div class="key-form-answers">${Object.keys(k.answers).map((q) => `<label>السؤال ${q}<select name="a${q}">${META.options.map((o) => `<option ${k.answers[q] === o ? "selected" : ""}>${o}</option>`).join("")}</select></label>`).join("")}</div>
        <h3 style="margin-top:14px">التنقيط</h3>
        <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
          <label class="field">العلامة الكلية<input type="number" step="any" name="total_score" value="${k.scoring.total_score}"></label>
          <label class="field">علامة السؤال<input type="number" step="any" name="question_score" value="${k.scoring.question_score ?? ""}"></label>
          <label class="field">علامة الإجابة الخاطئة<input type="number" step="any" name="wrong_score" value="${k.scoring.wrong_score}"></label>
          <label class="field">علامة السؤال الفارغ<input type="number" step="any" name="blank_score" value="${k.scoring.blank_score}"></label>
        </div>
        <div class="row" style="margin-top:14px"><button class="btn primary">حفظ المفتاح</button><button type="button" class="btn" id="cancel">إلغاء</button></div>
      </form>`;
    const f = document.getElementById("kf");
    const slug = () => { if (isNew && f.exam.value && f.specialization.value) f.id.value = (f.exam.value.toLowerCase().replace(/[^a-z0-9]+/g, "_") + "_" + f.specialization.value).replace(/^_+|_+$/g, ""); };
    f.exam.addEventListener("input", slug);
    f.specialization.addEventListener("input", slug);
    document.getElementById("cancel").onclick = () => (document.getElementById("formHost").innerHTML = "");
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = {
        id: f.id.value.trim(), exam: f.exam.value.trim(), specialization: f.specialization.value.trim(),
        specialization_label: f.specialization_label.value.trim(), specialization_label_ar: f.specialization_label_ar.value.trim(),
        answers: Object.fromEntries(Object.keys(k.answers).map((q) => [q, f["a" + q].value])),
        scoring: { ...k.scoring, total_score: +f.total_score.value, question_score: +f.question_score.value, wrong_score: +f.wrong_score.value, blank_score: +f.blank_score.value },
      };
      try { await api("/api/keys", jsonOpts("POST", body)); toast("تم حفظ مفتاح الإجابة"); pageKeys(); } catch (err) { toast(err.message, true); }
    });
    f.scrollIntoView({ behavior: "smooth" });
  };
  document.getElementById("newKey").onclick = () => showForm(null);
  $app.querySelectorAll("[data-edit]").forEach((b) => (b.onclick = () => showForm(keyById(b.dataset.edit))));
}

// ------------------------------------------------------------------ page: help
async function pageHelp() {
  const docs = META.threshold_docs || {};
  const rows = [];
  Object.entries(META.thresholds).forEach(([sec, vals]) => Object.entries(vals).forEach(([k, v]) => rows.push([`${sec}.${k}`, v, docs[k] || ""])));
  $app.innerHTML = `
    <div class="page-head"><div><h1>دليل الحالات والإعدادات</h1><p class="sub">كيف يقرر النظام، وماذا تعني كل حالة.</p></div></div>
    <h2>حالة الورقة</h2>
    <div class="legend">${Object.keys(STATUS_AR).map((k) => `<div class="card">${badge(k)}<p>${STATUS_HELP[k]}</p></div>`).join("")}</div>
    <h2 style="margin-top:22px">نتيجة السؤال</h2>
    <div class="legend">
      <div class="card"><span class="ans correct">B</span> <span class="ans wrong">C</span><p>دائرة واحدة مظللة بوضوح. أخضر = يطابق المفتاح، أحمر = خطأ.</p></div>
      ${Object.keys(VALUE_AR).map((v) => `<div class="card"><span class="ans ${v}">${VALUE_AR[v]}</span> <span class="small muted mono">${v}</span><p>${VALUE_HELP[v]}</p></div>`).join("")}
    </div>
    <div class="card" style="margin-top:22px"><h2>كيف تتم القراءة (بدون ذكاء اصطناعي)</h2>
      <ol>
        <li><b>التحميل:</b> صورة أو PDF (كل صفحة ورقة مستقلة).</li>
        <li><b>المحاذاة:</b> مطابقة معالم الورقة المطبوعة (ORB) مع النسخة الأصلية ← تصحيح الدوران والإزاحة والمقياس والمنظور، ثم ضبط دقيق على كل دائرة "O" مطبوعة.</li>
        <li><b>توحيد الإضاءة:</b> تقدير لون الورق محلياً لإلغاء اختلاف السطوع والتباين والظلال.</li>
        <li><b>قياس التعبئة:</b> نسبة الحبر داخل الدائرة المطبوعة وحولها (مع استبعاد خط الدائرة نفسه)، وكشف إشارات ✓ و ×.</li>
        <li><b>التصنيف:</b> حسب العتبات أدناه ← إجابة / فارغ / متعدد / غير واضح. لا تخمين أبداً.</li>
        <li><b>المقارنة والعلامة:</b> مع مفتاح الإجابة المختار، وتُحفظ كل النسب والقرارات للتدقيق.</li>
      </ol>
      <p class="small muted">النتائج حتمية: نفس الصورة ونفس الإعدادات تعطي نفس النتيجة دائماً. بصمة الإعدادات الحالية: <code>${esc(META.config_fingerprint)}</code></p>
    </div>
    <div class="card"><h2>العتبات الحالية</h2>
      <p class="small muted">للتعديل: حرّر <code>${esc(META.config_dir)}/thresholds.json</code> ثم أعد تشغيل الخادم (أو استخدم "إعادة المعالجة" على ورقة).</p>
      <div class="table-wrap"><table class="tbl th-table"><thead><tr><th>المفتاح</th><th>القيمة</th><th>الشرح</th></tr></thead>
      <tbody>${rows.map(([k, v, d]) => `<tr style="cursor:default"><td>${esc(k)}</td><td class="num">${esc(JSON.stringify(v))}</td><td class="small">${esc(d)}</td></tr>`).join("")}</tbody></table></div>
    </div>`;
}

// ------------------------------------------------------------------ boot
(async function boot() {
  try {
    [META, KEYS] = await Promise.all([api("/api/meta"), api("/api/keys")]);
  } catch (e) {
    $app.innerHTML = `<div class="card empty"><div class="big">⚠️</div><p>تعذّر الاتصال بالخادم: ${esc(e.message)}</p></div>`;
    return;
  }
  route();
})();
