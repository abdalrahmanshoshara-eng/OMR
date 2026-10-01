# OMR evaluation report

> Dataset is SYNTHETIC (generated from the blank sheet PDF). Real scanned sheets are still required to confirm field accuracy.

## Summary

| metric | value |
|---|---|
| sheets_tested | 68 |
| sheets_fully_correct | 68 |
| sheets_with_errors | 0 |
| review_required | 13 |
| failed | 5 |
| false_auto_approved | 0 |
| question_decisions | 630 |
| question_errors | 0 |
| detection_accuracy | 1.0 |
| ms_per_sheet_mean | 266.8 |
| ms_per_sheet_max | 367.5 |

## Per category

| category | fully correct |
|---|---|
| 01_all_correct | 6/6 |
| 02_wrong_answers | 4/4 |
| 03_blank | 4/4 |
| 04_multiple | 3/3 |
| 05_light_mark | 3/3 |
| 06_very_dark | 2/2 |
| 07_rotated | 6/6 |
| 08_scan_quality | 9/9 |
| 09_noise | 3/3 |
| 10_invalid | 5/5 |
| 11_multi_page_pdf | 5/5 |
| 12_tricky | 18/18 |

## Per question accuracy

| question | accuracy |
|---|---|
| Q1 | 100.00% |
| Q2 | 100.00% |
| Q3 | 100.00% |
| Q4 | 100.00% |
| Q5 | 100.00% |
| Q6 | 100.00% |
| Q7 | 100.00% |
| Q8 | 100.00% |
| Q9 | 100.00% |
| Q10 | 100.00% |

## Sheets

| file | page | expected | got | answers ok | score | ms | notes |
|---|---|---|---|---|---|---|---|
| 001_01_all_correct_business_management_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 263.2 |  |
| 002_01_all_correct_business_management_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 256.6 |  |
| 003_01_all_correct_commercial_banking_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 249.8 |  |
| 004_01_all_correct_commercial_banking_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 236.6 |  |
| 005_01_all_correct_applied_statistics_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 292.7 |  |
| 006_01_all_correct_applied_statistics_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 250.4 |  |
| 007_02_wrong_answers_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 281.2 |  |
| 008_02_wrong_answers_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 252.5 |  |
| 009_02_wrong_answers_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 273.1 |  |
| 010_02_wrong_answers_3.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 248.7 |  |
| 011_03_blank_1blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 292.1 |  |
| 012_03_blank_2blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 253.3 |  |
| 013_03_blank_3blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 70.0 | 290.0 |  |
| 014_03_blank_10blank.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 246.8 |  |
| 015_04_multiple_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 298.7 |  |
| 016_04_multiple_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 253.8 |  |
| 017_04_multiple_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 80.0 | 319.5 |  |
| 018_05_light_mark_ink120.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 258.0 |  |
| 019_05_light_mark_ink140.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 266.7 |  |
| 020_05_light_mark_ink155.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 251.0 |  |
| 021_06_very_dark_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 248.5 |  |
| 022_06_very_dark_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 285.4 |  |
| 023_07_rotated_-4deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 253.5 |  |
| 024_07_rotated_-2deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 271.2 |  |
| 025_07_rotated_+2deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 258.1 |  |
| 026_07_rotated_+4deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 264.7 |  |
| 027_07_rotated_+180deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 243.3 |  |
| 028_07_rotated_+88deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 263.2 |  |
| 029_08_scan_quality_100dpi_jpeg60.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 255.0 |  |
| 030_08_scan_quality_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 296.2 |  |
| 031_08_scan_quality_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 256.3 |  |
| 032_08_scan_quality_low_contrast.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 268.5 |  |
| 033_08_scan_quality_dark_scan.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 251.6 |  |
| 034_08_scan_quality_shadow_gradient.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 268.5 |  |
| 035_08_scan_quality_scaled_shifted.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 254.3 |  |
| 036_08_scan_quality_phone_perspective.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 281.1 |  |
| 037_08_scan_quality_blurry.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 253.5 |  |
| 038_09_noise_sigma10_speckle0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 278.7 |  |
| 039_09_noise_sigma18_speckle300.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 261.4 |  |
| 040_09_noise_sigma25_speckle800.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 270.6 |  |
| 041_10_invalid_cropped_bottom_missing.jpg | 1 | FAILED | FAILED | None | None | 229.0 | (answer area is cut off / outside the image (cropped or incomplete scan)) |
| 042_10_invalid_cropped_right_half.jpg | 1 | FAILED | FAILED | None | None | 157.7 | (answer area is cut off / outside the image (cropped or incomplete scan)) |
| 043_10_invalid_blank_white_page.jpg | 1 | FAILED | FAILED | None | None | 19.1 | (no image features found (blank or unreadable image)) |
| 044_10_invalid_different_omr_sheet.jpg | 1 | FAILED | FAILED | None | None | 308.9 | (sheet not recognised: only 13 consistent feature matches) |
| 045_10_invalid_random_noise_image.jpg | 1 | FAILED | FAILED | None | None | 367.5 | (too few feature matches with the reference sheet (0)) |
| 046_11_multi_page_pdf_5sheets.pdf | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 317.4 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 2 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 270.6 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 3 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 312.7 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 4 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 276.2 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 5 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 314.2 |  |
| 047_12_tricky_tick_mark_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 257.0 |  |
| 048_12_tricky_tick_mark_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 267.5 |  |
| 049_12_tricky_tick_mark_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 251.4 |  |
| 050_12_tricky_cross_mark_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 268.7 |  |
| 051_12_tricky_cross_mark_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 256.8 |  |
| 052_12_tricky_cross_mark_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 293.4 |  |
| 053_12_tricky_half_filled_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 254.7 |  |
| 054_12_tricky_half_filled_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 275.7 |  |
| 055_12_tricky_half_filled_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 263.2 |  |
| 056_12_tricky_stray_dot_on_other_option_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 295.8 |  |
| 057_12_tricky_stray_dot_on_other_option_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 265.8 |  |
| 058_12_tricky_stray_dot_on_other_option_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 302.7 |  |
| 059_12_tricky_erased_then_remarked_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 275.7 |  |
| 060_12_tricky_erased_then_remarked_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 279.4 |  |
| 061_12_tricky_erased_then_remarked_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 257.9 |  |
| 062_12_tricky_underfilled_small_mark_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 311.9 |  |
| 063_12_tricky_underfilled_small_mark_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 263.9 |  |
| 064_12_tricky_underfilled_small_mark_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 306.4 |  |
