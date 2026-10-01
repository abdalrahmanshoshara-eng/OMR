"""
Institute OMR grading engine built on top of OMRChecker.

Pipeline (fully deterministic, OpenCV only - no ML / OCR):
    image/PDF -> preprocessing -> alignment (ORB homography + glyph refinement)
    -> bubble fill measurement -> answer classification -> answer-key comparison -> score
"""

__version__ = "1.0.0"
