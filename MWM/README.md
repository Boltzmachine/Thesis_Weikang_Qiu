# MWM source and dissertation integration

- Source: https://www.overleaf.com/project/6a736986680ecc7e91861ff9
- Imported: 2026-09-27
- Source revision: `61c25b86a19eb3951657a51db93e648fa96867c1`
- Paper title: **Mind World Models: Joint Learning of Motor EEG Representations and Action-Conditioned World Dynamics**

`main.tex` includes the complete five main-text sections. The latest appendix (`006_appendix.tex`) and submission statements (`007_statements.tex`) are retained as source material but are not included in the dissertation. Appendix-pointer sentences in the experiments section are omitted while the appendix is excluded.

Integration changes are limited to the chapter wrapper, shared `mwm` macro names, MWM-prefixed cross-reference labels, explicit figure paths, standalone PDF rendering of the three TikZ diagrams, figure float placement, and table typography. The regression and classification result tables are transposed (tasks as rows) for readability; every value and emphasis mark is preserved. Scientific prose, equations, and reported results otherwise follow the source revision. Headline values are defined in the MWM block of `../macros.tex`; references are merged into `../bibfile.bib`.

The complete Overleaf checkout and the pre-import MWM are preserved outside OneDrive at `/Users/qiuweikang/Thesis_Backups/Thesis_Weikang_Qiu/mwm_overleaf_20260927_102433`.
