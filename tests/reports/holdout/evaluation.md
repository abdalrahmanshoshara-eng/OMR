# OMR evaluation report

> Dataset is SYNTHETIC (generated from the blank sheet PDF). Real scanned sheets are still required to confirm field accuracy.

## Summary

| metric | value |
|---|---|
| sheets_tested | 200 |
| sheets_fully_correct | 186 |
| sheets_with_errors | 14 |
| review_required | 151 |
| failed | 0 |
| false_auto_approved | 0 |
| question_decisions | 2000 |
| question_errors | 23 |
| detection_accuracy | 0.9885 |
| ms_per_sheet_mean | 276.8 |
| ms_per_sheet_max | 387.5 |

## Per category

| category | fully correct |
|---|---|
| stress | 186/200 |

## Per question accuracy

| question | accuracy |
|---|---|
| Q1 | 99.50% |
| Q2 | 99.50% |
| Q3 | 99.50% |
| Q4 | 99.00% |
| Q5 | 98.50% |
| Q6 | 99.00% |
| Q7 | 98.50% |
| Q8 | 99.00% |
| Q9 | 98.00% |
| Q10 | 98.00% |

## Sheets

| file | page | expected | got | answers ok | score | ms | notes |
|---|---|---|---|---|---|---|---|
| 001_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 355.6 |  |
| 002_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 286.0 |  |
| 003_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 276.0 |  |
| 004_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 266.9 |  |
| 005_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 263.0 |  |
| 006_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 279.9 | Q8: exp C got UNCERTAIN |
| 007_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 253.1 |  |
| 008_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 313.1 |  |
| 009_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 259.5 |  |
| 010_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 295.9 |  |
| 011_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 272.9 |  |
| 012_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 245.4 |  |
| 013_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 283.7 |  |
| 014_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 233.7 |  |
| 015_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 361.8 |  |
| 016_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 236.1 |  |
| 017_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 272.5 |  |
| 018_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 231.8 |  |
| 019_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 301.7 |  |
| 020_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 243.2 |  |
| 021_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 233.9 |  |
| 022_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 240.4 |  |
| 023_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 236.5 |  |
| 024_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 230.2 |  |
| 025_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 310.8 |  |
| 026_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 242.8 |  |
| 027_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 275.5 |  |
| 028_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 249.2 |  |
| 029_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 231.3 |  |
| 030_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 235.7 |  |
| 031_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 289.6 |  |
| 032_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 226.0 |  |
| 033_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 266.6 |  |
| 034_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 235.3 |  |
| 035_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 294.0 |  |
| 036_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 228.0 |  |
| 037_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 311.4 |  |
| 038_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 230.9 |  |
| 039_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 298.5 |  |
| 040_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 235.8 |  |
| 041_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 321.9 |  |
| 042_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 234.7 |  |
| 043_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 325.0 |  |
| 044_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 249.6 |  |
| 045_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 321.2 |  |
| 046_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 233.4 |  |
| 047_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 330.5 |  |
| 048_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 251.0 |  |
| 049_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 329.9 |  |
| 050_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 251.7 |  |
| 051_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 189.4 |  |
| 052_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 187.0 |  |
| 053_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 193.8 |  |
| 054_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 211.5 |  |
| 055_stress_200dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 0.0 | 178.8 | Q10: exp C got UNCERTAIN |
| 056_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 196.1 |  |
| 057_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 208.8 |  |
| 058_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 208.6 |  |
| 059_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 193.3 |  |
| 060_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 215.0 |  |
| 061_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 190.3 |  |
| 062_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 189.9 |  |
| 063_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 181.1 |  |
| 064_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 174.3 |  |
| 065_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 209.7 |  |
| 066_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 300.0 |  |
| 067_stress_200dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 10.0 | 257.4 | Q4: exp A got UNCERTAIN |
| 068_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 268.8 |  |
| 069_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 280.8 |  |
| 070_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 328.7 |  |
| 071_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 10.0 | 312.3 | Q6: exp D got UNCERTAIN |
| 072_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 253.6 |  |
| 073_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 294.4 |  |
| 074_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 248.9 |  |
| 075_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 310.8 |  |
| 076_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 299.3 |  |
| 077_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 327.1 |  |
| 078_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 362.9 |  |
| 079_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 294.4 |  |
| 080_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 236.5 |  |
| 081_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 365.2 |  |
| 082_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 252.9 | Q9: exp B got UNCERTAIN |
| 083_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 246.1 | Q4: exp A got UNCERTAIN |
| 084_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 274.1 |  |
| 085_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 235.3 |  |
| 086_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 296.8 |  |
| 087_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 239.5 |  |
| 088_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 255.6 |  |
| 089_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 318.5 |  |
| 090_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 231.1 |  |
| 091_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 320.3 |  |
| 092_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 240.8 |  |
| 093_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 0.0 | 330.8 | Q3: exp D got UNCERTAIN; Q6: exp D got UNCERTAIN |
| 094_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 279.6 |  |
| 095_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 338.7 |  |
| 096_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 239.6 |  |
| 097_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 322.7 |  |
| 098_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 251.0 |  |
| 099_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 316.6 |  |
| 100_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 257.7 |  |
| 101_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 296.0 |  |
| 102_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 246.6 |  |
| 103_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 322.8 |  |
| 104_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 50.0 | 243.1 |  |
| 105_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 258.5 |  |
| 106_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 236.9 |  |
| 107_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 314.4 |  |
| 108_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 248.9 |  |
| 109_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 336.1 |  |
| 110_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 237.1 | Q10: exp A got UNCERTAIN |
| 111_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 313.7 |  |
| 112_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 231.7 |  |
| 113_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 335.4 |  |
| 114_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 235.8 |  |
| 115_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 237.6 |  |
| 116_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 333.3 |  |
| 117_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 235.0 |  |
| 118_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 308.2 |  |
| 119_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 252.7 |  |
| 120_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 335.0 |  |
| 121_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 237.4 |  |
| 122_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 345.6 |  |
| 123_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 254.8 |  |
| 124_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 336.8 |  |
| 125_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 250.1 |  |
| 126_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 325.1 |  |
| 127_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 259.1 |  |
| 128_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 320.6 |  |
| 129_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 250.7 |  |
| 130_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 30.0 | 323.4 |  |
| 131_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 246.5 |  |
| 132_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 332.7 |  |
| 133_stress_300dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 40.0 | 257.9 | Q5: exp D got UNCERTAIN |
| 134_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 328.0 |  |
| 135_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 259.4 |  |
| 136_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 339.8 |  |
| 137_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 236.8 |  |
| 138_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 263.7 |  |
| 139_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 285.3 |  |
| 140_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 281.7 |  |
| 141_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 291.7 |  |
| 142_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 256.6 |  |
| 143_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 304.5 |  |
| 144_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 287.1 |  |
| 145_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 260.0 |  |
| 146_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 297.4 |  |
| 147_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 20.0 | 251.3 | Q1: exp A got UNCERTAIN; Q5: exp A got UNCERTAIN |
| 148_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 345.0 |  |
| 149_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 253.1 |  |
| 150_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 270.2 |  |
| 151_stress_150dpi.jpg | 1 | AUTO_APPROVED | REVIEW_REQUIRED | False | 0.0 | 280.6 | Q7: exp C got UNCERTAIN; Q8: exp D got UNCERTAIN; Q9: exp A got UNCERTAIN; Q10: exp C got UNCERTAIN |
| 152_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 305.1 |  |
| 153_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 365.1 |  |
| 154_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 30.0 | 293.9 | Q2: exp B got UNCERTAIN; Q7: exp C got UNCERTAIN |
| 155_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 295.6 |  |
| 156_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 261.0 |  |
| 157_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 364.3 |  |
| 158_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 282.3 |  |
| 159_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 281.2 |  |
| 160_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 325.6 |  |
| 161_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 250.9 |  |
| 162_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 348.6 |  |
| 163_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 256.6 |  |
| 164_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 363.3 |  |
| 165_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 276.0 |  |
| 166_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 339.6 |  |
| 167_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 294.2 |  |
| 168_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 281.4 |  |
| 169_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 269.5 |  |
| 170_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 40.0 | 242.4 |  |
| 171_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 360.1 |  |
| 172_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 258.5 |  |
| 173_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 0.0 | 349.0 |  |
| 174_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 254.5 |  |
| 175_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 387.5 |  |
| 176_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 255.0 |  |
| 177_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 351.4 |  |
| 178_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 50.0 | 249.9 | Q9: exp A got UNCERTAIN |
| 179_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 353.6 |  |
| 180_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 265.0 |  |
| 181_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 352.5 |  |
| 182_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 258.6 |  |
| 183_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 351.2 |  |
| 184_stress_150dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 10.0 | 256.6 |  |
| 185_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 341.7 |  |
| 186_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 60.0 | 265.8 |  |
| 187_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 40.0 | 273.7 |  |
| 188_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 50.0 | 342.8 |  |
| 189_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 246.5 |  |
| 190_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 336.8 |  |
| 191_stress_300dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 261.2 |  |
| 192_stress_150dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | False | 10.0 | 355.1 | Q5: exp A got UNCERTAIN; Q7: exp A got UNCERTAIN; Q9: exp C got UNCERTAIN; Q10: exp C got UNCERTAIN |
| 193_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 249.4 |  |
| 194_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 30.0 | 302.1 |  |
| 195_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 0.0 | 235.5 |  |
| 196_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 296.8 |  |
| 197_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 10.0 | 231.7 |  |
| 198_stress_300dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 267.1 |  |
| 199_stress_200dpi.jpg | 1 | REVIEW_REQUIRED | REVIEW_REQUIRED | True | 20.0 | 285.1 |  |
| 200_stress_200dpi.jpg | 1 | AUTO_APPROVED | AUTO_APPROVED | True | 20.0 | 267.5 |  |
