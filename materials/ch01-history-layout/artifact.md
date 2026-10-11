# Textbook Template Execution Contract

## Reference

Retained reference: `templates/textbook-style-v1.0.dotx`, SHA256 `eef8ce505c3d9afb3493e61af1f38ee26bca6ff9a0aa12f7ad3e2a8cacad6473`. One section, one rendered reference page; Parent actually viewed the complete page. Task-local render and package inventory: `/home/reggie/.local/state/jiaocai-ch01-history-layout-20261012/template-render/`, `template-parts.json`, `template-style.json`. The runtime bundle manifest resolves Python3.12.14, Node24.19.0, headless LibreOffice25.2 and Poppler under `/home/reggie/.cache/codex-runtimes/codex-primary-runtime/dependencies/`; no dependency-loader tool is exposed, so this installed runtime's manifest and absolute binaries are used directly.

## Page System and Typography

One A4 portrait mirrored-margin section. Top/bottom25mm, inside30/outside25mm, header/footer15mm. Body: Noto Serif CJK SC12pt, justified,1.5 spacing,2-character first-line indent. Chapter/section/subsection: Noto Sans CJK SC18/16/14pt; headings keep with next. FigureCaption, TableCaption, SourceNote, TableBody and Reference:10.5pt/1.2 spacing. Code: Noto Sans Mono CJK SC10.5pt. Header/footer9pt. Template named styles and settings remain authoritative and unchanged; ordinary Body paragraphs release direct keep-together to flow without excessive blank areas.

## Slots and Preservation

The template body consists only of chapter/section/subsection example slots. Replace these with the complete chapter manuscript using the same named styles; retain section geometry. Chapter numbering starts at1; section/subsection SEQ uses the existing primitives. Header STYLEREF cached title is replaced with the current chapter title; footer PAGE is preserved. Add real TOC/PAGEREF using section bookmarks, native figure/table SEQ/REF using stable `fig1_N`/`tbl1_N`, and nine answer bookmarks. Settings already specify updateFields; no headless LibreOffice save is used on final Word. Cached TOC page values are derived from the actual rendered PDF; Microsoft Word-native refresh remains untested.

Lists use the template Body font and natural bullet/number text, with12pt left indent. Tables are155mm, three-line borders1pt/0.5pt, no verticals, repeated header and unsplit normal rows; column widths follow actual cell content. Figures inline155mm and centered; source/caption remain separate. Bibliography retains all nine original source entries, including URLs with line-break opportunities.

## Package Inventory and Fidelity Gates

Editable parts: main document, document relationships (images/hyperlinks), core metadata, chapter start override in numbering, current header cache, content type (template to document). New media parts are allowed. Every other original package part is preserve-only and must have identical uncompressed bytes, including styles, settings, fontTable, theme and footer. The original template itself must retain its exact SHA. Paragraph/body content is the new chapter; expected movement arises from content replacement, not geometry/style changes.

Final checks cover all manuscript prose/table cells, seven image bytes/alt descriptions and actual insert sizes, caption/REF/TOC/bookmark targets, font embedding, page numbers and final TOC cache. Every final page is actually viewed at full rendered resolution; screenshots, tests and text extraction are distinct evidence. Document remains an AI-reviewed complete draft, not a human classroom or publisher acceptance.
