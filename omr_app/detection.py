"""Bubble fill measurement and answer classification (pure functions, config-driven)."""
import numpy as np

BLANK = "BLANK"
MULTIPLE = "MULTIPLE"
UNCERTAIN = "UNCERTAIN"
SPECIAL_VALUES = (BLANK, MULTIPLE, UNCERTAIN)

SHAPE_NONE, SHAPE_SOLID, SHAPE_STROKES = "none", "solid", "strokes"


def _runs(hit):
    """Lengths of circular runs of True in a 1-D bool array."""
    if hit.all():
        return [len(hit)]
    if not hit.any():
        return []
    start = int(np.argmin(hit))  # rotate so the sequence starts on a False
    h = np.roll(hit, -start)
    runs, n = [], 0
    for v in h:
        if v:
            n += 1
        elif n:
            runs.append(n)
            n = 0
    if n:
        runs.append(n)
    return runs


def stroke_shape(ink_patch, layout, fill_cfg, outer):
    """Classify the ink around the printed 'O' as none / solid / strokes (tick, cross).

    Only evaluated when the area just outside the 'O' is not broadly inked
    (outer < stroke_max_outer_fill): pen scribbles poking out of a real fill are not ticks.
    """
    m = layout.probe_mask
    bins = layout.probe_bins[m]
    ink = ink_patch[m]
    nb = layout.stroke_bins
    cov = np.bincount(bins, weights=ink.astype(float), minlength=nb) / np.maximum(np.bincount(bins, minlength=nb), 1)
    runs = _runs(cov >= fill_cfg["stroke_bin_min_cov"])
    if not runs:
        return SHAPE_NONE, runs
    if (outer < fill_cfg["stroke_max_outer_fill"] and len(runs) >= fill_cfg["stroke_min_runs"]
            and max(runs) <= fill_cfg["stroke_max_run_bins"]):
        return SHAPE_STROKES, runs
    return SHAPE_SOLID, runs


def ink_threshold(dark, centers, layout, fill_cfg):
    """Per-sheet pixel ink threshold, adapted to the paper noise and pen/pencil darkness of this sheet.

    Using the mean darkness inside the printed 'O' of all 40 bubbles:
      paper_level = median   (most bubbles are empty -> residual darkness of blank paper/noise)
      ink_level   = `ink_level_percentile` (marked bubbles dominate the top of the distribution)
    threshold = clip(paper_level + ink_relative_threshold * (ink_level - paper_level),
                     paper_level + dark_pixel_threshold_min, dark_pixel_threshold_max)
    Returns (threshold, ink_level, paper_level).
    """
    half = layout.patch_half_px
    hole_m = layout.hole_mask
    H, W = dark.shape
    vals = []
    for cx, cy in centers.values():
        x, y = int(round(cx)), int(round(cy))
        if half <= x < W - half and half <= y < H - half:
            vals.append(float(dark[y - half: y + half + 1, x - half: x + half + 1][hole_m].mean()))
    ink_level = float(np.percentile(vals, fill_cfg["ink_level_percentile"])) if vals else 0.0
    paper_level = float(np.median(vals)) if vals else 0.0
    lo = paper_level + fill_cfg["dark_pixel_threshold_min"]
    thr = paper_level + fill_cfg["ink_relative_threshold"] * (ink_level - paper_level)
    thr = float(min(max(thr, lo), max(lo, fill_cfg["dark_pixel_threshold_max"])))
    return thr, ink_level, paper_level


def measure_bubbles(dark, centers, layout, fill_cfg, thr, paper_level=0.0):
    """Measure every bubble on the illumination-normalised darkness map.

    Returns {(q, opt): {"fill", "hole", "outer", "hole_darkness", "darkness", "shape", "center"}}
      ink           = pixels with darkness >= bubble threshold, where
                      bubble threshold = min(sheet thr, paper + ink_relative_threshold * (hole_darkness - paper)),
                      never below paper + dark_pixel_threshold_min. A uniformly light (pencil) fill is
                      therefore measured against its own darkness; half fills / ticks stay partial.
      hole          = inked fraction of the paper inside the printed 'O'
      outer         = inked fraction of the bubble area outside the printed 'O'
      fill          = hole_weight * hole + (1 - hole_weight) * outer
      shape         = none / solid / strokes (tick-cross detector, see stroke_shape)
      hole_darkness = mean darkness inside the printed 'O' (faint-mark safety net)
      darkness      = mean darkness over hole+outer pixels (audit only)
    """
    half = layout.patch_half_px
    hole_m, outer_m = layout.hole_mask, layout.outer_mask
    n_hole, n_outer = max(1, int(hole_m.sum())), max(1, int(outer_m.sum()))
    area_m = hole_m | outer_m
    w_hole = float(fill_cfg["hole_weight"])
    H, W = dark.shape
    out = {}
    for key, (cx, cy) in centers.items():
        x, y = int(round(cx)), int(round(cy))
        if x - half < 0 or y - half < 0 or x + half + 1 > W or y + half + 1 > H:
            out[key] = {"fill": 0.0, "hole": 0.0, "outer": 0.0, "hole_darkness": 0.0, "darkness": 0.0,
                        "shape": SHAPE_NONE, "center": (x, y), "outside": True}
            continue
        d = dark[y - half: y + half + 1, x - half: x + half + 1]
        hd = float(d[hole_m].mean())
        lo = paper_level + fill_cfg["dark_pixel_threshold_min"]
        b_thr = max(lo, min(thr, paper_level + fill_cfg["ink_relative_threshold"] * (hd - paper_level)))
        ink = d >= b_thr
        hole, outer = ink[hole_m].sum() / n_hole, ink[outer_m].sum() / n_outer
        shape, _ = stroke_shape(ink, layout, fill_cfg, outer)
        out[key] = {
            "fill": float(w_hole * hole + (1 - w_hole) * outer),
            "hole": float(hole),
            "outer": float(outer),
            "hole_darkness": hd,
            "threshold": b_thr,
            "darkness": float(d[area_m].mean()),
            "shape": shape,
            "center": (x, y),
        }
    return out


def classify_question(bubbles: dict, th: dict):
    """Decide the answer of one question.

    ``bubbles``: {option: {"fill": float, "hole": float, "shape": str}}
    Returns (detected, reason, margin). Never guesses: ambiguous -> UNCERTAIN,
    two or more marks -> MULTIPLE, nothing -> BLANK.
    A bubble counts as MARKED only if fill >= min_fill AND the inside of the printed 'O'
    is filled (hole >= min_hole_fill) AND the ink is not a tick/cross stroke pattern.
    ``margin`` = distance of the decisive value from the nearest threshold (audit only).
    """
    min_fill, unc, mult, gap = th["min_fill"], th["uncertain_min_fill"], th["multiple_mark_fill"], th["ambiguity_gap"]
    min_hole = th.get("min_hole_fill", 0.0)
    fills = {o: b["fill"] for o, b in bubbles.items()}
    ranked = sorted(fills.items(), key=lambda kv: (-kv[1], kv[0]))
    (o1, f1), (o2, f2) = ranked[0], ranked[1]
    strokes = [o for o, f in ranked if f >= unc and bubbles[o].get("shape") == SHAPE_STROKES]
    hollow = [o for o, f in ranked if f >= min_fill and o not in strokes and bubbles[o].get("hole", 1.0) < min_hole]
    marked = [o for o, f in ranked if f >= min_fill and o not in strokes and o not in hollow]
    faint_d = th.get("faint_hole_darkness", 1.0)
    p_hole = th.get("partial_hole_fill", 1.0)
    partial = [o for o, f in ranked if o not in marked and f >= unc]
    if not marked:  # safety nets: a faint / thin mark must never silently become BLANK
        partial += [o for o, f in ranked if o not in partial and (
            bubbles[o].get("hole", 0.0) >= p_hole or bubbles[o].get("hole_darkness", 0.0) >= faint_d)]

    def _why(o):
        if o in strokes:
            kind = "tick/cross-like stroke mark"
        elif o in hollow:
            kind = f"inside of bubble not filled (hole {bubbles[o]['hole']:.2f} < {min_hole})"
        elif fills[o] < unc and bubbles[o].get("hole", 0.0) >= p_hole:
            kind = f"ink inside the O ({bubbles[o]['hole']:.2f})"
        elif fills[o] < unc:
            kind = f"faint mark (darkness inside O {bubbles[o].get('hole_darkness', 0):.2f})"
        else:
            kind = "partial/faint mark"
        return f"{o}: {kind} (fill {fills[o]:.2f})"

    if not marked:
        if not partial:
            return BLANK, "no option reaches the partial-mark threshold", round(unc - f1, 3)
        return UNCERTAIN, "; ".join(_why(o) for o in partial), round(min(abs(fills[o] - unc) for o in partial), 3)
    if len(marked) >= 2 and fills[marked[1]] >= mult:
        many = sorted(o for o in marked if fills[o] >= mult)
        return MULTIPLE, f"{len(many)} options marked: {'+'.join(many)}", round(fills[marked[1]] - mult, 3)
    if partial:
        return UNCERTAIN, f"{marked[0]} marked but " + "; ".join(_why(o) for o in partial), round(min(abs(fills[o] - unc) for o in partial), 3)
    if f1 - f2 < gap:
        return UNCERTAIN, f"{o1}/{o2} too close ({f1:.2f} vs {f2:.2f})", round(gap - (f1 - f2), 3)
    return o1, "single clear mark", round(min(f1 - min_fill, unc - f2, (f1 - f2) - gap, bubbles[o1].get("hole", 1.0) - min_hole), 3)
