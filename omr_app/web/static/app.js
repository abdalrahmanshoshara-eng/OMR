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
// clickable table rows are focusable; Enter opens them
document.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.matches?.("[data-go]")) location.hash = e.target.dataset.go; });

const svgIcon = (paths, size = 20) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
const ICON = {
  alert: svgIcon('<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>', 34),
  folder: svgIcon('<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>', 34),
  upload: svgIcon('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M12 3v13"/><path d="m7 8 5-5 5 5"/>', 34),
  search: svgIcon('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 34),
  download: svgIcon('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M12 3v13"/><path d="m7 11 5 5 5-5"/>', 17),
  save: svgIcon('<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/>', 17),
  check: svgIcon('<path d="M20 6 9 17l-5-5"/>', 17),
  undo: svgIcon('<path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/>', 15),
};
const emptyState = (icon, html) => `<div class="empty"><div class="big">${icon}</div>${html}</div>`;

// styled replacement for window.confirm(); resolves true on OK
function confirmDialog(msg, { ok = "تأكيد", cancel = "إلغاء", danger = false } = {}) {
  return new Promise((resolve) => {
    const d = document.createElement("dialog");
    d.className = "dlg";
    d.innerHTML = `<form method="dialog"><p>${esc(msg).replace(/\n/g, "<br>")}</p>
      <div class="row"><span class="spacer"></span><button class="btn" value="0">${esc(cancel)}</button>
      <button class="btn ${danger ? "danger" : "primary"}" value="1">${esc(ok)}</button></div></form>`;
    d.addEventListener("close", () => { resolve(d.returnValue === "1"); d.remove(); });
    document.body.append(d);
    d.showModal();
  });
}

// ------------------------------------------------------------------ router
let leaveGuard = null;   // page-provided: returns true while there is unsaved work
let pageCleanup = null;  // page-provided: removes page-level listeners
let currentHash = null;
window.addEventListener("beforeunload", (e) => { if (leaveGuard?.()) { e.preventDefault(); e.returnValue = ""; } });

const routes = [
  [/^#?\/?$/, pageBatches, "batches"],
  [/^#\/new$/, pageNew, "new"],
  [/^#\/batch\/(\d+)$/, pageBatch, "batches"],
  [/^#\/sheet\/(\d+)$/, pageSheet, "batches"],
  [/^#\/keys$/, pageKeys, "keys"],
  [/^#\/help$/, pageHelp, "help"],
];

async function route() {
  const h = location.hash || "#/";
  if (currentHash !== null && h !== currentHash && leaveGuard?.()) {
    history.replaceState(null, "", currentHash);
    const leave = await confirmDialog("توجد تعديلات غير محفوظة على هذه الورقة.\nهل تريد المغادرة دون حفظ؟",
      { ok: "مغادرة دون حفظ", cancel: "البقاء في الصفحة", danger: true });
    if (leave) { leaveGuard = null; location.hash = h; }
    return;
  }
  clearInterval(pollTimer);
  leaveGuard = null;
  pageCleanup?.();
  pageCleanup = null;
  currentHash = h;
  for (const [re, fn, nav] of routes) {
    const m = h.match(re);
    if (m) {
      document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("active", a.dataset.nav === nav));
      document.body.classList.add("busy");
      try {
        await fn(...m.slice(1));
      } catch (e) {
        $app.innerHTML = `<div class="card">${emptyState(ICON.alert, `<p>${esc(e.message)}</p><a class="btn" href="#/">العودة</a>`)}</div>`;
      } finally {
        document.body.classList.remove("busy");
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
          <tr data-go="#/batch/${b.id}" tabindex="0">
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
        : emptyState(ICON.folder, `<p><b>لا توجد دفعات بعد</b><br>ابدأ برفع صور أو ملفات PDF لأوراق الإجابة الممسوحة.</p>
           <a class="btn primary lg" href="#/new">+ رفع أوراق</a>`)}
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
        <label class="field">الامتحان والاختصاص (سلم التصحيح)
          <select name="answer_key_id" required>${keyOptions(KEYS[0]?.id)}</select>
          <small>يمكن تغيير الاختصاص لاحقاً لكل ورقة أو للدفعة كاملة، ويُعاد حساب العلامة.</small></label>
        <div id="keyPreview"></div>
      </div>
      <div class="card">
        <div class="dropzone" id="dz" tabindex="0">
          <div class="big">${ICON.upload}</div><b>اسحب الملفات إلى هنا أو اضغط للاختيار</b>
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
    const mb = files.reduce((t, x) => t + x.size, 0) / 1048576;
    document.getElementById("fcount").textContent = files.length ? `${files.length} ملف • ${mb.toFixed(1)} MB` : "لم يتم اختيار ملفات";
    const go = document.getElementById("go");
    go.disabled = !files.length;
    go.textContent = files.length ? `بدء تصحيح ${files.length} ملف ←` : "بدء التصحيح ←";
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
      render();
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
          <a class="btn" href="/api/batches/${bid}/export.xlsx">${ICON.download} Excel</a>
          <a class="btn" href="/api/batches/${bid}/export.pdf">${ICON.download} PDF</a>
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
            <th>#</th><th>المرشح</th><th>الملف</th><th>الحالة</th><th>العلامة</th><th>الإجابات (س1 ← س${META.questions})</th><th>الملاحظات</th></tr></thead>
          <tbody>${shown.map((s) => sheetRow(s)).join("")}</tbody></table></div>`
          : emptyState(ICON.search, `<p>${busy ? "بانتظار النتائج…" : "لا توجد أوراق مطابقة للبحث أو التصفية"}</p>`)}
      </div>`;
    $app.querySelectorAll("[data-filter]").forEach((el) => el.addEventListener("click", () => { filter = filter === el.dataset.filter ? "" : el.dataset.filter; render(); }));
    $app.querySelectorAll("[data-go]").forEach((tr) => tr.addEventListener("click", () => (location.hash = tr.dataset.go)));
    const q = document.getElementById("q");
    q.addEventListener("input", () => { search = q.value; const pos = q.selectionStart; render(); const q2 = document.getElementById("q"); q2.focus(); q2.setSelectionRange(pos, pos); });
    document.getElementById("rekey").addEventListener("change", async (e) => {
      const k = keyById(e.target.value);
      if (!(await confirmDialog(`تغيير سلم التصحيح لكل أوراق الدفعة إلى:\n${keyLabel(k)}\nوإعادة حساب كل العلامات؟`, { ok: "تغيير وإعادة الحساب" }))) { e.target.value = b.answer_key_id; return; }
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
  return `<tr data-go="#/sheet/${s.id}" tabindex="0">
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
  let focusQ = null;       // question targeted by keyboard shortcuts
  let scrollToFocus = false;

  const qs = () => s.result.questions || [];
  const finalOf = (qd) => (qd.q in ovr ? ovr[qd.q] || qd.detected : qd.override || qd.detected);
  const needsDecision = (qd) => ["MULTIPLE", "UNCERTAIN"].includes(finalOf(qd));
  const firstOpen = () => (qs().find(needsDecision) || null)?.q ?? null;
  focusQ = firstOpen();
  leaveGuard = () => Object.keys(ovr).length > 0;

  // choose v for question q (null/"" = back to the machine reading)
  const pick = (q, v) => {
    const qd = qs().find((x) => x.q === q);
    if (!qd) return;
    const target = !v || v === qd.detected ? null : v;
    if (target === (qd.override || null)) delete ovr[q]; else ovr[q] = target;
    const next = qs().find((x) => x.q > q && needsDecision(x)) || qs().find(needsDecision);
    focusQ = next ? next.q : q;
    scrollToFocus = true;
    render();
  };

  const render = () => {
    const r = s.result;
    const key = keyById(r.answer_key_id) || keyById(s.batch.answer_key_id);
    const failed = r.status === "FAILED";
    const unresolved = qs().filter(needsDecision);
    // live preview of score with pending overrides
    let preview = 0;
    qs().forEach((qd) => { if (key && finalOf(qd) === key.answers[String(qd.q)]) preview += Number((key.scoring.question_scores || {})[qd.q] ?? key.scoring.question_score); });
    const dirty = Object.keys(ovr).length > 0;
    const art = r.artifacts || {};
    const img = (k) => `/api/sheets/${sid}/image/${k}?v=${encodeURIComponent(s.updated_at)}`;
    const resolved = (r.questions || []).filter((qd) => ["MULTIPLE", "UNCERTAIN"].includes(qd.detected) && !needsDecision(qd)).length;
    const flagged = (r.questions || []).filter((qd) => ["MULTIPLE", "UNCERTAIN"].includes(qd.detected)).length;

    $app.innerHTML = `
      <div class="page-head">
        <div><div class="small"><a href="#/">الدفعات</a> ‹ <a href="#/batch/${s.batch_id}">${esc(s.batch.name)}</a> ‹</div>
          <h1 class="${r.candidate_name ? "" : "ltr"}">${esc(r.candidate_name || r.candidate_id)}</h1>
          <p class="sub"><span class="ltr">${esc(r.source_file)}</span>${r.page > 1 ? " • صفحة " + r.page : ""} • ورقة ${s.nav.position} من ${s.nav.total} • متبقٍ للمراجعة: <b>${s.nav.review_left}</b></p></div>
        <div class="actions">
          <a class="btn ${s.nav.prev ? "" : "disabled"}" ${s.nav.prev ? `href="#/sheet/${s.nav.prev}"` : ""} title="P">→ السابقة</a>
          <a class="btn ${s.nav.next ? "" : "disabled"}" ${s.nav.next ? `href="#/sheet/${s.nav.next}"` : ""} title="N">التالية ←</a>
        </div>
      </div>
      <div class="review-grid">
        <section class="card viewer">
          ${failed ? emptyState(ICON.alert, `<p><b>لم يتم التعرف على الورقة</b><br>${esc(r.error || "")}</p>
              <p class="small">الحلول: أعد مسح الورقة كاملة بوضوح (بدون قص)، وتأكد أنها ورقة الإجابة المعتمدة، ثم ارفعها في دفعة جديدة.</p>
              <a class="btn" href="${img("original")}" target="_blank">فتح الملف الأصلي</a>`) : `
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
            <div class="score num">${failed ? "—" : fmtScore(dirty ? preview : r.score)}<span class="muted" style="font-size:16px"> / ${fmtScore(r.max_score)}</span></div>
            <div class="small" style="flex-basis:100%">${esc(STATUS_HELP[r.status] || "")}</div>
            ${flagged ? `<div class="resolve" style="flex-basis:100%"><div class="row small"><b>الأسئلة المشكوك بها</b><span class="spacer"></span><span class="num">${resolved} / ${flagged}</span></div>
              <div class="progress"><div style="width:${(100 * resolved) / flagged}%"></div></div></div>` : ""}
            ${(r.status_reasons || []).length ? `<ul class="reasons">${r.status_reasons.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
          </div>

          <div class="card">
            <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(180px,1fr))">
              <label class="field">رقم / معرّف المرشح <input type="text" id="cid" dir="auto" value="${esc(r.candidate_id)}"></label>
              <label class="field">اسم المرشح <small>يُدخل يدوياً من صورة الاسم</small><input type="text" id="cname" dir="auto" value="${esc(r.candidate_name || "")}" placeholder="الاسم الكامل"></label>
              <label class="field">الاختصاص (سلم التصحيح) <select id="ckey">${keyOptions(r.answer_key_id)}</select></label>
              <label class="field">اسم المراجِع <input type="text" id="actor" value="${esc(reviewer())}" placeholder="اسمك (يُحفظ في السجل)"></label>
            </div>
          </div>

          ${failed ? "" : `<div class="card">
            <div class="row" style="margin-bottom:6px"><h2 style="margin:0">الأسئلة</h2><span class="spacer"></span>
              <span class="small muted">اضغط على الخيار لاختياره يدوياً • <span class="key-mark"></span> = إجابة سلم التصحيح</span></div>
            <div class="kbd-hint small muted">
              <span><kbd>A</kbd>–<kbd>D</kbd> اختيار</span><span><kbd>0</kbd> فارغ</span><span><kbd>↑</kbd><kbd>↓</kbd> السؤال</span>
              <span><kbd>Enter</kbd> اعتماد</span><span><kbd>Ctrl</kbd>+<kbd>S</kbd> حفظ</span><span><kbd>N</kbd>/<kbd>P</kbd> الورقة التالية/السابقة</span>
            </div>
            <table class="qtable"><thead><tr><th>س</th><th>الخيارات (نسبة التعبئة)</th><th>المكتشف</th><th>الصحيح</th><th>النهائي</th><th></th></tr></thead><tbody>
            ${qs().map((qd) => {
              const fin = finalOf(qd), exp = key ? key.answers[String(qd.q)] : qd.expected;
              const ok = fin === exp, special = VALUE_AR[fin];
              const cur = qd.q in ovr ? ovr[qd.q] : qd.override;
              return `<tr class="q ${needsDecision(qd) ? "attn" : ""} ${focusQ === qd.q ? "cur" : ""} ${cur ? "edited" : ""}" data-row="${qd.q}">
                <td class="qnum num">${qd.q}</td>
                <td><div class="fills">${META.options.map((o) => `
                    <button type="button" data-q="${qd.q}" data-pick="${o}"
                      class="fill ${qd.detected === o || (qd.detected in VALUE_AR && qd.fills[o] >= META.thresholds.classification.uncertain_min_fill) ? "sel" : ""} ${o === exp ? "exp" : ""} ${qd.shapes?.[o] === "strokes" ? "stroke" : ""} ${cur && fin === o ? "pick" : ""}"
                      title="اختيار ${o} • تعبئة ${pct(qd.fills[o])}% • داخل الدائرة ${pct(qd.hole?.[o])}%${qd.shapes?.[o] === "strokes" ? " • شكل ✓/×" : ""}">
                      <span class="o">${o}</span><span class="p num">${pct(qd.fills[o])}%</span><span class="bar"><i style="width:${pct(qd.fills[o])}%"></i></span></button>`).join("")}</div>
                  <div class="reason">${esc(qd.reason)}</div></td>
                <td><span class="ans ${VALUE_AR[qd.detected] ? qd.detected : "neutral"}" title="${esc(VALUE_HELP[qd.detected] || "")}">${esc(valueLabel(qd.detected))}</span></td>
                <td><span class="ans neutral">${esc(exp || "—")}</span></td>
                <td><span class="ans ${special ? fin : ok ? "correct" : "wrong"}">${esc(valueLabel(fin))}</span></td>
                <td class="qact">
                  <button type="button" class="btn sm ${cur && fin === "BLANK" ? "on" : ""}" data-q="${qd.q}" data-pick="BLANK" title="فارغ (0)">فارغ</button>
                  ${cur ? `<button type="button" class="btn sm icon" data-q="${qd.q}" data-pick="" title="إلغاء التعديل والعودة للقراءة الآلية">${ICON.undo}</button>` : ""}
                </td></tr>`;
            }).join("")}
            </tbody></table>
            <div class="review-actions">
              <button class="btn" id="save">${ICON.save} حفظ</button>
              <button class="btn success" id="approve" ${unresolved.length ? "disabled" : ""}
                title="${unresolved.length ? "احسم الأسئلة: " + unresolved.map((x) => x.q).join("، ") : "اعتماد الورقة"}">${ICON.check} اعتماد الورقة</button>
              ${s.nav.next_review ? `<button class="btn primary" id="approveNext" ${unresolved.length ? "disabled" : ""}>${ICON.check} اعتماد والانتقال للتالية ←</button>` : ""}
              ${r.status === "MANUALLY_REVIEWED" ? `<button class="btn" id="reopen">↺ إعادة فتح المراجعة</button>` : ""}
              <span class="spacer"></span>
              ${dirty ? `<span class="small pending">تعديلات غير محفوظة • العلامة بعد التعديل: <b class="num">${fmtScore(preview)}</b></span>` : ""}
              ${unresolved.length ? `<span class="small pending">يجب حسم: ${unresolved.map((x) => "س" + x.q).join("، ")}</span>` : ""}
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
                <a class="btn sm" id="dljson" href="#">${ICON.download} نتيجة الورقة JSON</a></div>
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
    $app.querySelectorAll("[data-pick]").forEach((b) => b.addEventListener("click", (e) => { e.stopPropagation(); pick(+b.dataset.q, b.dataset.pick); }));
    $app.querySelectorAll("tr[data-row]").forEach((tr) => tr.addEventListener("click", () => {
      if (focusQ === +tr.dataset.row) return;
      $app.querySelector("tr.q.cur")?.classList.remove("cur");
      focusQ = +tr.dataset.row;
      tr.classList.add("cur");
    }));
    if (scrollToFocus) {
      $app.querySelector("tr.q.cur")?.scrollIntoView({ block: "nearest", behavior: "smooth" });
      scrollToFocus = false;
    }
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
      focusQ = firstOpen() ?? focusQ;
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
      if (!(await confirmDialog("إعادة قراءة هذه الورقة بالإعدادات الحالية؟\nستُستبدل القراءة الآلية، وتبقى التعديلات اليدوية في سجل التدقيق.", { ok: "إعادة المعالجة" }))) return;
      s = await api(`/api/sheets/${sid}/reprocess`, { method: "POST" });
      ovr = {};
      focusQ = firstOpen();
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

  // keyboard shortcuts (layout independent: e.code, so they also work on an Arabic keyboard)
  const onKey = (e) => {
    if (e.altKey || e.metaKey || document.querySelector("dialog[open]") || !document.getElementById("lightbox").hidden) return;
    if (e.target.closest?.("input, select, textarea")) return;
    const click = (id) => { const b = document.getElementById(id); if (b && !b.disabled) { b.click(); return true; } return false; };
    if (e.ctrlKey) {
      if (e.code === "KeyS") { e.preventDefault(); click("save"); }
      return;
    }
    if (s.result.status === "FAILED") return;
    const opts = { KeyA: "A", KeyB: "B", KeyC: "C", KeyD: "D", KeyE: "E", Digit0: "BLANK", Numpad0: "BLANK" };
    const v = opts[e.code];
    if (v && (v === "BLANK" || META.options.includes(v)) && focusQ !== null) { e.preventDefault(); pick(focusQ, v); return; }
    if ((e.code === "ArrowDown" || e.code === "ArrowUp") && qs().length) {
      e.preventDefault();
      const i = qs().findIndex((x) => x.q === focusQ);
      const j = Math.max(0, Math.min(qs().length - 1, (i < 0 ? 0 : i + (e.code === "ArrowDown" ? 1 : -1))));
      focusQ = qs()[j].q;
      scrollToFocus = true;
      render();
      return;
    }
    if (e.code === "Enter" && !e.target.closest?.("button, a, [data-go]")) { e.preventDefault(); click("approveNext") || click("approve"); return; }
    if (e.code === "KeyN" && s.nav.next) location.hash = `#/sheet/${s.nav.next}`;
    if (e.code === "KeyP" && s.nav.prev) location.hash = `#/sheet/${s.nav.prev}`;
  };
  document.addEventListener("keydown", onKey);
  pageCleanup = () => document.removeEventListener("keydown", onKey);
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
    <div class="page-head"><div><h1>سلالم التصحيح</h1>
      <p class="sub">كل سلم تصحيح ملف JSON مستقل في <code>config/answer_keys/</code> — يمكن إضافة امتحان أو اختصاص جديد دون تعديل الكود.</p></div>
      <div class="actions"><button class="btn primary" id="newKey">+ سلم تصحيح جديد</button></div></div>
    <div id="formHost"></div>
    <div class="keys">${KEYS.map((k) => `
      <div class="card"><div class="row"><div><b>${esc(k.specialization_label_ar || k.specialization)}</b>
        <div class="small muted">${esc(k.specialization_label || "")} • ${esc(k.exam)}</div></div><span class="spacer"></span>
        <button class="btn sm" data-edit="${esc(k.id)}">تعديل</button></div>
        ${keyAnswersHtml(k)}
        <div class="small muted">عدد الأسئلة <b class="num">${Object.keys(k.answers).length}</b> • العلامة الكلية <b class="num">${k.scoring.total_score}</b>
          • لكل سؤال <b class="num">${k.scoring.question_score === undefined ? "مخصص" : fmtScore(k.scoring.question_score)}</b></div>
        <div class="small muted mono">${esc(k.id)}</div></div>`).join("")}</div>`;
  const showForm = (k) => {
    const isNew = !k;
    k = k || { id: "", exam: KEYS[0]?.exam || "", specialization: "", specialization_label: "", specialization_label_ar: "",
      answers: Object.fromEntries(Array.from({ length: META.questions }, (_, i) => [String(i + 1), "A"])),
      scoring: { total_score: 100, question_score: 100 / META.questions } };
    let answers = Object.values(k.answers);
    document.getElementById("formHost").innerHTML = `
      <form class="card" id="kf" style="margin-bottom:16px"><h2>${isNew ? "سلم تصحيح جديد" : "تعديل: " + esc(k.id)}</h2>
        <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
          <label class="field">اسم الامتحان<input type="text" name="exam" required value="${esc(k.exam)}"></label>
          <label class="field">الاختصاص بالعربية<input type="text" name="specialization_label_ar" required value="${esc(k.specialization_label_ar || "")}"></label>
          <label class="field">الاختصاص بالإنجليزية<input type="text" name="specialization_label" value="${esc(k.specialization_label || "")}"></label>
          <label class="field">رمز الاختصاص <small>أحرف إنجليزية صغيرة و _</small><input type="text" name="specialization" required pattern="[a-z0-9_\\-]+" value="${esc(k.specialization)}"></label>
          <label class="field">المعرّف <small>اسم الملف</small><input type="text" name="id" required pattern="[a-z0-9][a-z0-9_\\-]+" value="${esc(k.id)}" ${isNew ? "" : "readonly"}></label>
        </div>
        <div class="row" style="margin-top:14px"><h3 style="margin:0">الإجابات الصحيحة</h3><span class="spacer"></span>
          <label class="row small">عدد الأسئلة <input type="number" name="qcount" min="1" max="500" step="1" value="${answers.length}" style="width:80px"></label>
          <button type="button" class="btn sm" id="addQ">+ إضافة سؤال</button>
          <button type="button" class="btn sm" id="delQ">− حذف آخر سؤال</button></div>
        <p class="small" style="color:var(--review)" id="qwarn"></p>
        <div class="key-form-answers" id="qhost"></div>
        <h3 style="margin-top:14px">التنقيط</h3>
        <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
          <label class="field">العلامة الكلية<input type="number" step="any" name="total_score" value="${k.scoring.total_score}"></label>
          <label class="field">علامة السؤال <small>تُحسب تلقائياً عند تغيير عدد الأسئلة</small><input type="number" step="any" name="question_score" value="${k.scoring.question_score ?? ""}"></label>
        </div>
        <div class="row" style="margin-top:14px"><button class="btn primary">حفظ سلم التصحيح</button><button type="button" class="btn" id="cancel">إلغاء</button></div>
      </form>`;
    const f = document.getElementById("kf");
    const slug = () => { if (isNew && f.exam.value && f.specialization.value) f.id.value = (f.exam.value.toLowerCase().replace(/[^a-z0-9]+/g, "_") + "_" + f.specialization.value).replace(/^_+|_+$/g, ""); };
    const renderQs = () => {
      document.getElementById("qhost").innerHTML = answers.map((a, i) => `<label>السؤال ${i + 1}<select data-i="${i}">${META.options.map((o) => `<option ${a === o ? "selected" : ""}>${o}</option>`).join("")}</select></label>`).join("");
      f.qcount.value = answers.length;
      document.getElementById("qwarn").textContent = answers.length === META.questions ? "" :
        `تنبيه: ورقة الإجابة المطبوعة الحالية فيها ${META.questions} أسئلة فقط. الأوراق المصححة بهذا السلم ستُحوَّل إلى المراجعة لأن عدد الأسئلة مختلف.`;
    };
    const setCount = (n) => {
      n = Math.max(1, Math.min(500, Math.floor(n) || 1));
      answers = Array.from({ length: n }, (_, i) => answers[i] || META.options[0]);
      f.question_score.value = +(+f.total_score.value / n).toFixed(4);
      renderQs();
    };
    renderQs();
    document.getElementById("qhost").addEventListener("change", (e) => { if (e.target.dataset.i !== undefined) answers[+e.target.dataset.i] = e.target.value; });
    f.qcount.addEventListener("change", () => setCount(+f.qcount.value));
    document.getElementById("addQ").onclick = () => setCount(answers.length + 1);
    document.getElementById("delQ").onclick = () => setCount(answers.length - 1);
    f.total_score.addEventListener("change", () => (f.question_score.value = +(+f.total_score.value / answers.length).toFixed(4)));
    f.exam.addEventListener("input", slug);
    f.specialization.addEventListener("input", slug);
    document.getElementById("cancel").onclick = () => (document.getElementById("formHost").innerHTML = "");
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = {
        id: f.id.value.trim(), exam: f.exam.value.trim(), specialization: f.specialization.value.trim(),
        specialization_label: f.specialization_label.value.trim(), specialization_label_ar: f.specialization_label_ar.value.trim(),
        answers: Object.fromEntries(answers.map((a, i) => [String(i + 1), a])),
        scoring: { ...k.scoring, total_score: +f.total_score.value, question_score: +f.question_score.value },
      };
      try { await api("/api/keys", jsonOpts("POST", body)); toast("تم حفظ سلم التصحيح"); pageKeys(); } catch (err) { toast(err.message, true); }
    });
    f.scrollIntoView({ behavior: "smooth" });
  };
  document.getElementById("newKey").onclick = () => showForm(null);
  $app.querySelectorAll("[data-edit]").forEach((b) => (b.onclick = () => showForm(keyById(b.dataset.edit))));
}

// ------------------------------------------------------------------ page: help
async function pageHelp() {
  $app.innerHTML = `
    <div class="page-head"><div><h1>دليل الحالات والإعدادات</h1><p class="sub">كيف يقرر النظام، وماذا تعني كل حالة.</p></div></div>
    <h2>حالة الورقة</h2>
    <div class="legend">${Object.keys(STATUS_AR).map((k) => `<div class="card">${badge(k)}<p>${STATUS_HELP[k]}</p></div>`).join("")}</div>
    <h2 style="margin-top:22px">نتيجة السؤال</h2>
    <div class="legend">
      <div class="card"><span class="ans correct">B</span> <span class="ans wrong">C</span><p>دائرة واحدة مظللة بوضوح. أخضر = يطابق سلم التصحيح، أحمر = خطأ.</p></div>
      ${Object.keys(VALUE_AR).map((v) => `<div class="card"><span class="ans ${v}">${VALUE_AR[v]}</span> <span class="small muted mono">${v}</span><p>${VALUE_HELP[v]}</p></div>`).join("")}
    </div>
    <div class="card" style="margin-top:22px"><h2>كيف تتم القراءة (بدون ذكاء اصطناعي)</h2>
      <ol>
        <li><b>التحميل:</b> صورة أو PDF (كل صفحة ورقة مستقلة).</li>
        <li><b>المحاذاة:</b> مطابقة معالم الورقة المطبوعة (ORB) مع النسخة الأصلية ← تصحيح الدوران والإزاحة والمقياس والمنظور، ثم ضبط دقيق على كل دائرة "O" مطبوعة.</li>
        <li><b>توحيد الإضاءة:</b> تقدير لون الورق محلياً لإلغاء اختلاف السطوع والتباين والظلال.</li>
        <li><b>قياس التعبئة:</b> نسبة الحبر داخل الدائرة المطبوعة وحولها (مع استبعاد خط الدائرة نفسه)، وكشف إشارات ✓ و ×.</li>
        <li><b>التصنيف:</b> حسب العتبات المحددة في الإعدادات ← إجابة / فارغ / متعدد / غير واضح. لا تخمين أبداً.</li>
        <li><b>المقارنة والعلامة:</b> مع سلم التصحيح المختار، وتُحفظ كل النسب والقرارات للتدقيق.</li>
      </ol>
      <p class="small muted">النتائج حتمية: نفس الصورة ونفس الإعدادات تعطي نفس النتيجة دائماً. بصمة الإعدادات الحالية: <code>${esc(META.config_fingerprint)}</code></p>
    </div>`;
}

// ------------------------------------------------------------------ sidebar
// Desktop: inline sidebar, open/closed choice remembered. Phone: overlay drawer, always starts closed.
(function sidebar() {
  const mq = window.matchMedia("(max-width: 860px)");
  const btn = document.getElementById("sidebarToggle");
  const overlay = document.getElementById("sidebarOverlay");
  const KEY = "omr-sidebar-open";
  const set = (open) => {
    document.body.classList.toggle("sidebar-open", open);
    document.body.classList.toggle("sidebar-closed", !open);
    btn.setAttribute("aria-expanded", String(open));
    overlay.hidden = !(open && mq.matches);
  };
  const apply = () => {
    let remembered = true;
    try { remembered = localStorage.getItem(KEY) !== "0"; } catch { /* storage unavailable */ }
    set(mq.matches ? false : remembered);
  };
  btn.addEventListener("click", () => {
    const open = !document.body.classList.contains("sidebar-open");
    if (!mq.matches) { try { localStorage.setItem(KEY, open ? "1" : "0"); } catch { /* ignore */ } }
    set(open);
  });
  overlay.addEventListener("click", () => set(false));
  document.getElementById("nav").addEventListener("click", (e) => { if (mq.matches && e.target.closest("a")) set(false); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && mq.matches) set(false); });
  mq.addEventListener("change", apply);
  apply();
})();

// ------------------------------------------------------------------ boot
(async function boot() {
  try {
    [META, KEYS] = await Promise.all([api("/api/meta"), api("/api/keys")]);
  } catch (e) {
    $app.innerHTML = `<div class="card">${emptyState(ICON.alert, `<p>تعذّر الاتصال بالخادم: ${esc(e.message)}</p>`)}</div>`;
    return;
  }
  route();
})();
