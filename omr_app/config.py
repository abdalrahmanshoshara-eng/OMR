"""Loading of the JSON configuration (sheet layout, thresholds, answer keys).

Nothing sheet- or exam-specific is hard-coded in the engine: everything is read from
the config directory (default: <repo>/config, override with env OMR_CONFIG_DIR).
"""
import hashlib
import json
import os
import re
import shutil
from copy import deepcopy
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_DIR = REPO_ROOT / "config"

VALID_KEY_ID = re.compile(r"^[a-z0-9][a-z0-9_\-]{1,80}$")


class ConfigError(Exception):
    pass


def config_dir() -> Path:
    return Path(os.environ.get("OMR_CONFIG_DIR", DEFAULT_CONFIG_DIR))


def _read_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f"Missing config file: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}: {e}") from e


def _require(obj, keys, where):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ConfigError(f"{where}: missing keys {missing}")


def load_sheet_config(cfg_dir: Path = None) -> dict:
    cfg_dir = Path(cfg_dir or config_dir())
    cfg = _read_json(cfg_dir / "sheet_config.json")
    _require(cfg, ["reference", "omr_template", "questions", "bubble", "alignment"], "sheet_config.json")
    cfg["_dir"] = str(cfg_dir)
    return cfg


def load_thresholds(cfg_dir: Path = None) -> dict:
    cfg_dir = Path(cfg_dir or config_dir())
    th = _read_json(cfg_dir / "thresholds.json")
    _require(th, ["image", "fill", "classification", "review"], "thresholds.json")
    c = th["classification"]
    _require(c, ["min_fill", "uncertain_min_fill", "multiple_mark_fill", "ambiguity_gap"], "thresholds.classification")
    if not 0 <= c["uncertain_min_fill"] <= c["min_fill"] <= 1:
        raise ConfigError("thresholds: require 0 <= uncertain_min_fill <= min_fill <= 1")
    th.pop("_doc", None)
    return th


def config_fingerprint(*objs) -> str:
    """Short hash of the effective configuration, stored with every result for auditability."""
    blob = json.dumps(objs, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


# --------------------------------------------------------------------------- answer keys
def answer_keys_dir(cfg_dir: Path = None) -> Path:
    """<config>/answer_keys, or $OMR_ANSWER_KEYS_DIR (e.g. on the data volume so keys edited in the UI
    survive rebuilds and never conflict with `git pull`); that dir is seeded from <config>/answer_keys once."""
    if cfg_dir or not os.environ.get("OMR_ANSWER_KEYS_DIR"):
        return Path(cfg_dir or config_dir()) / "answer_keys"
    d = Path(os.environ["OMR_ANSWER_KEYS_DIR"])
    if not d.exists():
        shutil.copytree(config_dir() / "answer_keys", d)
    return d


def validate_answer_key(key: dict, num_questions: int, options) -> dict:
    """num_questions is the printed sheet's count; a key may have more or fewer (graded on the overlap)."""
    _require(key, ["id", "exam", "specialization", "answers"], f"answer key {key.get('id', '?')}")
    if not VALID_KEY_ID.match(str(key["id"])):
        raise ConfigError(f"answer key id '{key['id']}' must match {VALID_KEY_ID.pattern}")
    answers = {str(k): str(v).strip().upper() for k, v in key["answers"].items()}
    n = len(answers)
    if not n or set(answers) != {str(i) for i in range(1, n + 1)}:
        raise ConfigError(f"answer key {key['id']}: answers must be numbered 1..N without gaps")
    bad = {q: a for q, a in answers.items() if a not in options}
    if bad:
        raise ConfigError(f"answer key {key['id']}: invalid options {bad} (allowed {options})")
    key = deepcopy(key)
    key["answers"] = answers
    scoring = {"total_score": 100, "wrong_score": 0, "blank_score": 0, **key.get("scoring", {})}
    if "question_score" not in scoring and "question_scores" not in scoring:
        scoring["question_score"] = scoring["total_score"] / n
    key["scoring"] = scoring
    return key


def load_answer_keys(cfg_dir: Path = None, num_questions: int = None, options=None) -> dict:
    if num_questions is None or options is None:
        sc = load_sheet_config(cfg_dir)
        num_questions = sc["questions"]["count"]
        options = sc["questions"]["options"]
    keys = {}
    for path in sorted(answer_keys_dir(cfg_dir).glob("*.json")):
        key = validate_answer_key(_read_json(path), num_questions, options)
        if key["id"] in keys:
            raise ConfigError(f"duplicate answer key id '{key['id']}' in {path}")
        key["_file"] = path.name
        keys[key["id"]] = key
    return keys


def save_answer_key(key: dict, cfg_dir: Path = None) -> dict:
    sc = load_sheet_config(cfg_dir)
    key = validate_answer_key(key, sc["questions"]["count"], sc["questions"]["options"])
    key.pop("_file", None)
    path = answer_keys_dir(cfg_dir) / f"{key['id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(key, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return key
