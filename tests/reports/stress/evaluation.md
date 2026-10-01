# OMR evaluation report

> Dataset is SYNTHETIC (generated from the blank sheet PDF). Real scanned sheets are still required to confirm field accuracy.

## Summary

| metric | value |
|---|---|
| sheets_tested | 150 |
| sheets_fully_correct | 141 |
| sheets_with_errors | 9 |
| review_required | 114 |
| failed | 0 |
| false_auto_approved | 0 |
| question_decisions | 1500 |
| question_errors | 9 |
| detection_accuracy | 0.994 |
| ms_per_sheet_mean | 272.1 |
| ms_per_sheet_max | 511.5 |

## Per category

| category | fully correct |
|---|---|
| stress | 141/150 |

## Per question accuracy

| question | accuracy |
|---|---|
| Q1 | 98.67% |
| Q2 | 98.67% |
| Q3 | 100.00% |
| Q4 | 99.33% |
| Q5 | 100.00% |
| Q6 | 98.67% |
| Q7 | 99.33% |
| Q8 | 100.00% |
| Q9 | 100.00% |
| Q10 | 99.33% |

## Sheets

| file | page | expected | got | answers ok | score | ms | notes |
|---|---|---|---|---|---|---|---|
| 001_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 303.9 |  |
| 002_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 239.0 |  |
| 003_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 239.7 |  |
| 004_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 217.9 |  |
| 005_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 200.2 |  |
| 006_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 187.5 |  |
| 007_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 168.6 |  |
| 008_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 197.2 |  |
| 009_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 172.5 |  |
| 010_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 166.9 |  |
| 011_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 190.3 |  |
| 012_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 178.6 |  |
| 013_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 175.4 | Q1: exp A got UNCERTAIN |
| 014_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 176.8 |  |
| 015_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 175.6 |  |
| 016_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 205.5 |  |
| 017_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 192.5 |  |
| 018_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 198.8 |  |
| 019_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 200.1 |  |
| 020_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 181.4 |  |
| 021_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 267.4 |  |
| 022_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 265.9 |  |
| 023_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 264.3 |  |
| 024_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 407.3 |  |
| 025_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 511.5 |  |
| 026_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 284.9 |  |
| 027_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 268.6 |  |
| 028_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 264.4 |  |
| 029_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 311.0 |  |
| 030_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 263.5 |  |
| 031_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 70.0 | 268.7 |  |
| 032_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 299.8 |  |
| 033_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 254.0 |  |
| 034_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 331.4 |  |
| 035_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 254.0 |  |
| 036_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 252.4 |  |
| 037_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 244.1 |  |
| 038_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 273.9 |  |
| 039_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 245.4 |  |
| 040_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 286.2 |  |
| 041_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 286.0 |  |
| 042_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 242.5 |  |
| 043_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 299.2 |  |
| 044_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 239.4 |  |
| 045_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 321.5 |  |
| 046_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 240.0 |  |
| 047_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 378.3 |  |
| 048_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 238.9 |  |
| 049_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 234.7 |  |
| 050_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 292.0 |  |
| 051_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 242.5 |  |
| 052_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 343.4 |  |
| 053_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 236.4 |  |
| 054_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 0.0 | 339.9 | Q1: exp D got UNCERTAIN |
| 055_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 235.3 |  |
| 056_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 230.0 |  |
| 057_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 342.8 |  |
| 058_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 257.0 |  |
| 059_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 268.9 |  |
| 060_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 238.8 |  |
| 061_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 260.0 |  |
| 062_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 276.8 |  |
| 063_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 235.5 |  |
| 064_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 311.3 |  |
| 065_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 290.7 |  |
| 066_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 273.9 |  |
| 067_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 241.4 |  |
| 068_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 347.3 |  |
| 069_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 242.8 |  |
| 070_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 339.6 |  |
| 071_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 280.3 |  |
| 072_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 246.6 |  |
| 073_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 10.0 | 354.8 | Q10: exp A got UNCERTAIN |
| 074_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 260.9 |  |
| 075_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 317.9 |  |
| 076_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 300.1 |  |
| 077_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 261.1 |  |
| 078_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 388.9 |  |
| 079_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 280.7 |  |
| 080_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 261.4 |  |
| 081_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 272.2 |  |
| 082_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 255.1 |  |
| 083_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 294.7 |  |
| 084_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 248.2 |  |
| 085_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 357.1 |  |
| 086_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 266.7 |  |
| 087_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 278.0 |  |
| 088_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 283.2 |  |
| 089_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 302.4 |  |
| 090_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 256.6 |  |
| 091_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 261.3 |  |
| 092_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 301.4 |  |
| 093_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 270.2 | Q6: exp B got UNCERTAIN |
| 094_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 0.0 | 281.8 | Q2: exp A got UNCERTAIN |
| 095_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 243.4 |  |
| 096_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 254.5 |  |
| 097_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 286.2 | Q2: exp D got UNCERTAIN |
| 098_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 238.1 |  |
| 099_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 300.5 |  |
| 100_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 262.1 |  |
| 101_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 261.6 |  |
| 102_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 291.9 |  |
| 103_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 274.4 | Q4: exp B got UNCERTAIN |
| 104_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 342.8 |  |
| 105_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 317.3 | Q7: exp UNCERTAIN got BLANK |
| 106_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 325.2 |  |
| 107_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 345.1 |  |
| 108_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 349.0 |  |
| 109_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 245.4 |  |
| 110_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 297.1 |  |
| 111_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 249.6 |  |
| 112_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 290.1 |  |
| 113_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 231.2 | Q6: exp C got UNCERTAIN |
| 114_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 261.2 |  |
| 115_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 267.3 |  |
| 116_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 278.5 |  |
| 117_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 251.7 |  |
| 118_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 279.5 |  |
| 119_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 349.9 |  |
| 120_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 319.9 |  |
| 121_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 269.5 |  |
| 122_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 282.9 |  |
| 123_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 341.9 |  |
| 124_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 268.1 |  |
| 125_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 314.3 |  |
| 126_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 269.4 |  |
| 127_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 320.5 |  |
| 128_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 261.9 |  |
| 129_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 311.8 |  |
| 130_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 251.5 |  |
| 131_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 290.5 |  |
| 132_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 232.7 |  |
| 133_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 287.8 |  |
| 134_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 251.2 |  |
| 135_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 278.7 |  |
| 136_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 263.2 |  |
| 137_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 268.2 |  |
| 138_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 291.4 |  |
| 139_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 247.7 |  |
| 140_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 391.0 |  |
| 141_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 315.9 |  |
| 142_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 266.5 |  |
| 143_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 292.6 |  |
| 144_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 261.7 |  |
| 145_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 261.1 |  |
| 146_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 267.0 |  |
| 147_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 286.7 |  |
| 148_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 247.1 |  |
| 149_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 268.9 |  |
| 150_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 246.0 |  |
