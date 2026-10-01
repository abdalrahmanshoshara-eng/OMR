# OMR evaluation report

> Dataset is SYNTHETIC (generated from the blank sheet PDF). Real scanned sheets are still required to confirm field accuracy.

## Summary

| metric | value |
|---|---|
| sheets_tested | 200 |
| sheets_fully_correct | 181 |
| sheets_with_errors | 19 |
| review_required | 150 |
| failed | 0 |
| false_auto_approved | 0 |
| question_decisions | 2000 |
| question_errors | 21 |
| detection_accuracy | 0.9895 |
| ms_per_sheet_mean | 288.0 |
| ms_per_sheet_max | 454.1 |

## Per category

| category | fully correct |
|---|---|
| stress | 181/200 |

## Per question accuracy

| question | accuracy |
|---|---|
| Q1 | 99.50% |
| Q2 | 98.50% |
| Q3 | 98.50% |
| Q4 | 99.00% |
| Q5 | 98.50% |
| Q6 | 99.00% |
| Q7 | 98.50% |
| Q8 | 99.50% |
| Q9 | 99.50% |
| Q10 | 99.00% |

## Sheets

| file | page | expected | got | answers ok | score | ms | notes |
|---|---|---|---|---|---|---|---|
| 001_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 283.2 |  |
| 002_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 234.8 |  |
| 003_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 289.1 |  |
| 004_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 30.0 | 273.8 | Q3: exp A got UNCERTAIN |
| 005_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 274.9 |  |
| 006_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 337.2 |  |
| 007_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 327.0 |  |
| 008_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 262.1 |  |
| 009_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 256.9 |  |
| 010_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 283.4 |  |
| 011_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 316.3 |  |
| 012_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 245.2 |  |
| 013_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 249.5 |  |
| 014_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 322.0 |  |
| 015_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 261.5 |  |
| 016_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 320.6 |  |
| 017_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 342.8 |  |
| 018_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 270.8 |  |
| 019_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 352.7 |  |
| 020_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 282.6 |  |
| 021_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 349.5 |  |
| 022_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 454.1 |  |
| 023_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 40.0 | 287.4 | Q2: exp C got UNCERTAIN |
| 024_stress_200dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 30.0 | 376.4 | Q2: exp C got UNCERTAIN; Q7: exp C got UNCERTAIN |
| 025_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 336.3 |  |
| 026_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 369.4 |  |
| 027_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 450.9 |  |
| 028_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 330.3 |  |
| 029_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 341.2 |  |
| 030_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 301.5 |  |
| 031_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 294.5 |  |
| 032_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 272.2 |  |
| 033_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 283.0 |  |
| 034_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 347.9 |  |
| 035_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 253.8 |  |
| 036_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 343.5 |  |
| 037_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 279.1 |  |
| 038_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 279.8 |  |
| 039_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 286.6 |  |
| 040_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 341.9 |  |
| 041_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 0.0 | 275.3 | Q5: exp D got UNCERTAIN |
| 042_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 337.8 |  |
| 043_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 255.8 |  |
| 044_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 345.3 |  |
| 045_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 258.5 |  |
| 046_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 284.7 |  |
| 047_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 246.3 |  |
| 048_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 377.3 |  |
| 049_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 60.0 | 255.8 |  |
| 050_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 298.7 |  |
| 051_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 261.2 |  |
| 052_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 294.6 |  |
| 053_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 333.1 |  |
| 054_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 264.2 |  |
| 055_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 396.0 |  |
| 056_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 262.6 |  |
| 057_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 258.3 |  |
| 058_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 234.0 |  |
| 059_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 310.2 |  |
| 060_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 238.2 |  |
| 061_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 304.5 |  |
| 062_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 239.1 |  |
| 063_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 339.3 |  |
| 064_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 275.0 |  |
| 065_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 308.9 |  |
| 066_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 234.8 |  |
| 067_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 342.1 |  |
| 068_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 242.9 |  |
| 069_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 333.6 |  |
| 070_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 231.2 |  |
| 071_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 290.2 |  |
| 072_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 243.7 | Q3: exp D got UNCERTAIN; Q5: exp D got UNCERTAIN |
| 073_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 308.1 |  |
| 074_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 235.0 |  |
| 075_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 338.5 | Q8: exp B got UNCERTAIN |
| 076_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 225.9 | Q7: exp C got UNCERTAIN |
| 077_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 259.6 |  |
| 078_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 233.1 |  |
| 079_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 333.5 |  |
| 080_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 294.1 |  |
| 081_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 233.0 |  |
| 082_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 266.8 |  |
| 083_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 273.7 |  |
| 084_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 251.0 |  |
| 085_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 290.0 |  |
| 086_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 311.8 |  |
| 087_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 228.7 | Q10: exp B got UNCERTAIN |
| 088_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 285.4 |  |
| 089_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 239.8 |  |
| 090_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 292.1 |  |
| 091_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 229.6 |  |
| 092_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 317.6 |  |
| 093_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 256.4 |  |
| 094_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 251.7 |  |
| 095_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 233.1 |  |
| 096_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 282.1 |  |
| 097_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 250.7 |  |
| 098_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 348.4 |  |
| 099_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 270.7 |  |
| 100_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 289.6 |  |
| 101_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 307.2 |  |
| 102_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 236.3 |  |
| 103_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 285.3 |  |
| 104_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 248.3 |  |
| 105_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 260.0 |  |
| 106_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 263.7 |  |
| 107_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 314.9 |  |
| 108_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 252.8 |  |
| 109_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 297.9 |  |
| 110_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 233.4 |  |
| 111_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 336.4 |  |
| 112_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 277.1 |  |
| 113_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 300.8 |  |
| 114_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 281.2 |  |
| 115_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 338.5 |  |
| 116_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 254.9 |  |
| 117_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 40.0 | 279.5 | Q7: exp B got UNCERTAIN |
| 118_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 286.5 |  |
| 119_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 247.5 |  |
| 120_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 297.9 |  |
| 121_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 260.5 |  |
| 122_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 293.1 |  |
| 123_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 235.8 |  |
| 124_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 314.6 |  |
| 125_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 262.2 |  |
| 126_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 333.6 |  |
| 127_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 257.0 |  |
| 128_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 332.9 |  |
| 129_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 294.3 |  |
| 130_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 271.2 |  |
| 131_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 272.2 |  |
| 132_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 264.7 |  |
| 133_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 320.2 |  |
| 134_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 262.2 |  |
| 135_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 278.9 |  |
| 136_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 60.0 | 256.4 |  |
| 137_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 275.9 |  |
| 138_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 436.2 |  |
| 139_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 296.7 |  |
| 140_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 235.0 |  |
| 141_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 240.6 | Q9: exp C got UNCERTAIN |
| 142_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 366.2 |  |
| 143_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 244.9 |  |
| 144_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 328.7 |  |
| 145_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 290.9 |  |
| 146_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 299.3 |  |
| 147_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 297.2 | Q4: exp D got UNCERTAIN |
| 148_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 313.9 |  |
| 149_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 313.9 |  |
| 150_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 339.5 |  |
| 151_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 261.9 |  |
| 152_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 337.4 |  |
| 153_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 259.3 |  |
| 154_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 368.0 |  |
| 155_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 237.6 | Q2: exp D got UNCERTAIN |
| 156_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 287.0 |  |
| 157_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 257.4 |  |
| 158_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 244.5 |  |
| 159_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 245.0 |  |
| 160_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 351.4 |  |
| 161_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 251.1 |  |
| 162_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 264.8 | Q10: exp D got UNCERTAIN |
| 163_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 20.0 | 260.6 | Q6: exp A got UNCERTAIN |
| 164_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 265.3 |  |
| 165_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 235.7 |  |
| 166_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 311.3 |  |
| 167_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 244.8 |  |
| 168_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 329.3 |  |
| 169_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 244.1 |  |
| 170_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 306.5 |  |
| 171_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 249.9 |  |
| 172_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 289.9 |  |
| 173_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 261.6 |  |
| 174_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 331.7 |  |
| 175_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 259.6 |  |
| 176_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 313.2 |  |
| 177_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 243.8 |  |
| 178_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 334.2 |  |
| 179_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 240.4 |  |
| 180_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 293.9 |  |
| 181_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 259.4 |  |
| 182_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 40.0 | 262.1 | Q4: exp A got UNCERTAIN |
| 183_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 323.8 | Q1: exp B got UNCERTAIN |
| 184_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 243.8 |  |
| 185_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 326.9 | Q3: exp B got UNCERTAIN |
| 186_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 239.1 |  |
| 187_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 336.9 |  |
| 188_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 251.6 |  |
| 189_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 310.3 | Q6: exp C got UNCERTAIN |
| 190_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 240.0 |  |
| 191_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 323.3 |  |
| 192_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 267.6 |  |
| 193_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 345.7 |  |
| 194_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 243.9 |  |
| 195_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 338.7 |  |
| 196_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 237.8 | Q5: exp D got UNCERTAIN |
| 197_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 275.0 |  |
| 198_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 252.4 |  |
| 199_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 325.6 |  |
| 200_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 252.2 |  |
