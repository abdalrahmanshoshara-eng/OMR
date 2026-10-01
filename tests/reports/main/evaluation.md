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
| ms_per_sheet_mean | 277.0 |
| ms_per_sheet_max | 377.6 |

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
| 001_01_all_correct_business_management_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 304.9 |  |
| 002_01_all_correct_business_management_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 286.9 |  |
| 003_01_all_correct_commercial_banking_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 294.4 |  |
| 004_01_all_correct_commercial_banking_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 343.4 |  |
| 005_01_all_correct_applied_statistics_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 260.2 |  |
| 006_01_all_correct_applied_statistics_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 312.8 |  |
| 007_02_wrong_answers_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 253.1 |  |
| 008_02_wrong_answers_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 293.4 |  |
| 009_02_wrong_answers_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 261.5 |  |
| 010_02_wrong_answers_3.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 348.9 |  |
| 011_03_blank_1blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 254.1 |  |
| 012_03_blank_2blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 275.1 |  |
| 013_03_blank_3blank.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 70.0 | 243.2 |  |
| 014_03_blank_10blank.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 277.8 |  |
| 015_04_multiple_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 243.8 |  |
| 016_04_multiple_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 285.1 |  |
| 017_04_multiple_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 80.0 | 245.0 |  |
| 018_05_light_mark_ink120.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 303.6 |  |
| 019_05_light_mark_ink140.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 238.0 |  |
| 020_05_light_mark_ink155.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 269.1 |  |
| 021_06_very_dark_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 247.2 |  |
| 022_06_very_dark_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 279.8 |  |
| 023_07_rotated_-4deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 253.4 |  |
| 024_07_rotated_-2deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 284.1 |  |
| 025_07_rotated_+2deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 254.5 |  |
| 026_07_rotated_+4deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 80.0 | 266.9 |  |
| 027_07_rotated_+180deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 249.1 |  |
| 028_07_rotated_+88deg.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 281.6 |  |
| 029_08_scan_quality_100dpi_jpeg60.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 259.1 |  |
| 030_08_scan_quality_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 265.8 |  |
| 031_08_scan_quality_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 258.6 |  |
| 032_08_scan_quality_low_contrast.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 271.5 |  |
| 033_08_scan_quality_dark_scan.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 250.4 |  |
| 034_08_scan_quality_shadow_gradient.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 255.2 |  |
| 035_08_scan_quality_scaled_shifted.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 285.3 |  |
| 036_08_scan_quality_phone_perspective.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 366.6 |  |
| 037_08_scan_quality_blurry.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 348.4 |  |
| 038_09_noise_sigma10_speckle0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 289.5 |  |
| 039_09_noise_sigma18_speckle300.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 304.6 |  |
| 040_09_noise_sigma25_speckle800.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 313.5 |  |
| 041_10_invalid_cropped_bottom_missing.jpg | 1 | FAILED | FAILED | None | None | 178.3 | (answer area is cut off / outside the image (cropped or incomplete scan)) |
| 042_10_invalid_cropped_right_half.jpg | 1 | FAILED | FAILED | None | None | 162.4 | (answer area is cut off / outside the image (cropped or incomplete scan)) |
| 043_10_invalid_blank_white_page.jpg | 1 | FAILED | FAILED | None | None | 14.6 | (no image features found (blank or unreadable image)) |
| 044_10_invalid_different_omr_sheet.jpg | 1 | FAILED | FAILED | None | None | 322.7 | (sheet not recognised: only 13 consistent feature matches) |
| 045_10_invalid_random_noise_image.jpg | 1 | FAILED | FAILED | None | None | 338.4 | (too few feature matches with the reference sheet (0)) |
| 046_11_multi_page_pdf_5sheets.pdf | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 302.7 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 2 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 327.9 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 3 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 272.8 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 4 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 285.4 |  |
| 046_11_multi_page_pdf_5sheets.pdf | 5 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 273.3 |  |
| 047_12_tricky_tick_mark_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 309.5 |  |
| 048_12_tricky_tick_mark_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 293.6 |  |
| 049_12_tricky_tick_mark_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 281.0 |  |
| 050_12_tricky_cross_mark_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 260.3 |  |
| 051_12_tricky_cross_mark_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 273.0 |  |
| 052_12_tricky_cross_mark_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 233.5 |  |
| 053_12_tricky_half_filled_0.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 299.2 |  |
| 054_12_tricky_half_filled_1.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 236.3 |  |
| 055_12_tricky_half_filled_2.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 90.0 | 279.2 |  |
| 056_12_tricky_stray_dot_on_other_option_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 236.5 |  |
| 057_12_tricky_stray_dot_on_other_option_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 319.1 |  |
| 058_12_tricky_stray_dot_on_other_option_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 100.0 | 240.4 |  |
| 059_12_tricky_erased_then_remarked_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 323.2 |  |
| 060_12_tricky_erased_then_remarked_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 232.6 |  |
| 061_12_tricky_erased_then_remarked_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 330.9 |  |
| 062_12_tricky_underfilled_small_mark_0.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 364.8 |  |
| 063_12_tricky_underfilled_small_mark_1.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 377.6 |  |
| 064_12_tricky_underfilled_small_mark_2.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 90.0 | 284.6 |  |
