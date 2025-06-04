# Codex1

This repository contains a small script to transform pain.001.001.03 XML files.

## Usage

```
python main.py input.xml output.xml
```

The script performs the following operations:

- Replace `<SvcLvl><Cd>NORM</Cd></SvcLvl>` with `SEPA`.
- Insert a `<ReqdExctnDt>` element containing today's date after each `<PmtTpInf>`.
- Remove structured address tags `<StrtNm>`, `<PstCd>`, and `<TwnNm>` while keeping the country code.

