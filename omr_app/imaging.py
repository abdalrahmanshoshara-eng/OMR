"""Image input + photometric preprocessing."""
import logging
from pathlib import Path

import cv2
import numpy as np
from dotmap import DotMap

log = logging.getLogger("omr_app.imaging")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
PDF_EXTS = {".pdf"}
SUPPORTED_EXTS = IMAGE_EXTS | PDF_EXTS


def _pymupdf():
    try:
        import pymupdf  # PyMuPDF >= 1.24
    except ImportError:  # pragma: no cover
        import fitz as pymupdf
    return pymupdf


def render_pdf_page(path, page_index: int, dpi: float) -> np.ndarray:
    fz = _pymupdf()
    with fz.open(str(path)) as doc:
        page = doc[page_index]
        pix = page.get_pixmap(matrix=fz.Matrix(dpi / 72, dpi / 72), colorspace=fz.csGRAY)
        return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()


def load_input(path, pdf_dpi=200):
    """Return list of (page_number, gray_image) for an image or (multi-page) PDF.

    PDFs are rendered with OMRChecker's ``ImageUtils.load_omr_image`` (all pages).
    Raises ValueError when the file cannot be decoded.
    """
    path = Path(path)
    ext = path.suffix.lower()
    if ext in PDF_EXTS:
        from src.utils.image import ImageUtils

        tuning = DotMap({"pdf_params": {"pdf_dpi": pdf_dpi, "pdf_page": None}}, _dynamic=False)
        pages = ImageUtils.load_omr_image(path, tuning)
        if not pages:
            raise ValueError("PDF could not be opened or has no pages")
        return [(i + 1, img) for i, (_name, img) in enumerate(pages)]
    if ext in IMAGE_EXTS:
        # imdecode instead of imread: works with non-ASCII (e.g. Arabic) file names on Windows
        data = np.fromfile(str(path), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE) if data.size else None
        if img is None:
            raise ValueError("image could not be decoded")
        return [(1, img)]
    raise ValueError(f"unsupported file type '{ext}'")


def darkness_map(gray: np.ndarray, blur_ksize: int, kernel_px: int) -> np.ndarray:
    """Illumination-normalised darkness in [0, 1] (0 = paper white, 1 = black).

    The local paper-white level is estimated with a grey dilation (max filter) larger
    than any bubble, so brightness gradients, shadows and contrast differences between
    scanners cancel out.
    """
    g = gray
    if blur_ksize and blur_ksize > 1:
        g = cv2.GaussianBlur(g, (blur_ksize | 1, blur_ksize | 1), 0)
    k = max(3, kernel_px | 1)
    # denoise before the max filter, otherwise scanner noise biases the paper level upwards
    bg = cv2.dilate(cv2.medianBlur(g, 5), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    bg = cv2.GaussianBlur(bg, (k, k), 0).astype(np.float32)
    dark = 1.0 - g.astype(np.float32) / np.maximum(bg, 1.0)
    return np.clip(dark, 0.0, 1.0)
