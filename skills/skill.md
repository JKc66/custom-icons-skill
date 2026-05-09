---
name: custom-icons
description: "Professional workflow for creating bespoke vector and complex raster icons. Supports Design (visual), Path (vector-driven), Desire (conceptual), and 3D/complex chroma-key modes. Features AI prompt engineering, automated binarization, improved alpha cleanup, and SVG optimization."
---


# 🎨 Custom Icons Skill

A master workflow for crafting professional-grade iconography. This skill handles the entire pipeline: from conceptual "desire" and visual "design" to technical "path" refinement, transparent 3D PNG cleanup, and production-ready SVG optimization.

## 🚀 Installation

To integrate this skill into your environment:

```bash
npx skills add jkc66/custom-icons-skill
```

---

## 🤖 Agent Instructions (Strict Workflow)

When this skill is activated, you MUST follow this step-by-step interaction protocol:

### Phase 0: User Intent Comes First
Follow the user's explicit request over defaults in this skill.

- If the user gives subjects, style, output type, destination, colors, or framework, use those exact requirements.
- Do not substitute a different pipeline, format, style, subject, palette, or destination because it seems easier.
- Do not hand-author final Strategy A SVGs unless the user explicitly asks for manual/deterministic SVG code.
- Do not convert a Strategy B/3D request into SVG unless the user explicitly asks for SVG.
- Do not ask setup questions when the user has already provided enough information to proceed.
- Ask a concise clarifying question only when a missing detail would change the output format, subject list, destination, or strategy.
- If the user asks to update this skill or its gallery, preserve existing conventions unless the user asks to change them.

### Phase 1: Discovery & Style Definition
Use discovery only when the request is underspecified. If the user has not provided enough detail, ask for the minimum missing information:

1.  **Style**: What style of icon? (e.g., 3D-effect, Flat, Monoline, Luxury Engraved, Minimalist).
2.  **Subjects**: What icons or desire should be represented?
3.  **Target environment**: Where will the icons be used? (e.g., Astro, React, Mobile App).

### Phase 2: Generation & Strategy Selection
For each icon, decide on the technical strategy based on complexity:

#### Strategy A: Vector (Monochrome/Simple)
*Use for: Logos, UI icons, line art.*
1.  **Generate**: "Minimalist [SUBJECT] icon, high-contrast black on pure white background. [STYLE]. No fills, no gradients. Isolated on white."
2.  **Process**: Binarize the generated image, trace it with `potrace`, and optimize it with `svgo`.
3.  **Rule**: Do not hand-author final SVG path data for new Strategy A icons unless the user explicitly asks for a deterministic/manual SVG. The default output must come from the generated image -> `skills/scripts/crop_and_trace.py` -> `potrace` -> `svgo` pipeline.
4.  **Color**: If the user specifies a color, apply that color after tracing. If updating the reference gallery and no color is specified, use the category color.

#### Strategy B: Raster (Complex/Multi-color)
*Use for: Detailed illustrations, 3D icons, colorful assets.*
1.  **Generate**: "[SUBJECT] icon, vibrant colors, [STYLE]. **Pure green background (#00FF00)**. No shadows, no reflections, isolated subject, generous padding."
2.  **Logic**: Background removed via chroma-keying to create a transparent PNG.
3.  **Rule**: Keep Strategy B outputs as transparent PNG/WebP unless the user explicitly asks for another format.

---

### Phase 3: Processing & Tracing

#### For Strategy A (Vector):
1.  **Binarize**: `python3 skills/scripts/crop_and_trace.py <source> tmp/output <name>`
2.  **Trace**: `potrace "tmp/output/<name>.pbm" --svg --flat -o "src/assets/icons/<name>.svg"`
3.  **Optimize**: `bunx svgo "src/assets/icons/<name>.svg"`
4.  **Color**: After tracing, apply the target category fill/stroke color to the optimized SVG only as a mechanical tinting step.
5.  **Validate**: Confirm the SVG parses, contains traced path data, and visually matches the requested subject/style.

#### For Strategy B (Complex):
1.  **Remove Green Screen** with the advanced chroma-key utility:
    ```bash
    python3 skills/scripts/remove_chroma_key.py \
      --input <source> \
      --out skills/icons/3D/<name>.png \
      --auto-key border \
      --soft-matte \
      --spill-cleanup \
      --edge-feather 1.0 \
      --force
    ```
    *Result: Creates a transparent PNG with spill cleanup and antialiased edges.*

2.  **Alternative Trim Workflow**:
    ```bash
    python3 skills/scripts/crop_and_trace.py <source> skills/icons/3D <name> \
      --chroma \
      --padding 12
    ```
    *Result: Creates a transparent, trimmed PNG at `skills/icons/3D/<name>.png`. Use this when trimming is more important than soft matte cleanup.*

3.  **Validate Alpha**: Check that the output has transparent corners, no green fringe, and a clear subject silhouette. If a fringe remains after the advanced utility, retry once with `--edge-contract 1`; if edges look too hard, use a smaller feather such as `--edge-feather 0.25`.


---

### Phase 4: Optimization & Delivery
1.  **Optimize**: For SVGs, use `svgo`. For PNGs, ensure they are trimmed and compressed.
2.  **Implement**: Show the user how to use the asset.
3.  **Gallery Consistency**: Keep each reference category at five icons when updating the gallery. Strategy A categories should use their thematic fill/stroke color: Tech `#00C8FF`, Lifestyle `#00E676`, Detailed `#FF3D00`.
4.  **Report Honestly**: Say which pipeline was used, where files were saved, and whether validation passed. If a requested step could not be completed, say exactly what failed.

---

## 🎯 When to Use This Skill

- **Brand Identity**: Creating a cohesive set of unique icons for a new brand.
- **AI-to-Vector**: Converting illustrations into clean, colorable SVGs.
- **High-Fidelity Assets**: Creating transparent PNGs for complex 3D or multi-color icons.

---

## 🛠 Icon Creation Modes

### 1. 🏗 Design Mode (Visual Structure)
> Minimalist [SUBJECT] icon, black on white, monoline style.

### 2. 🛣 Path Mode (Vector-Driven)
> Refine existing image into a clean SVG.

### 3. ✨ Desire Mode (Conceptual)
> Abstract representation of "[DESIRE]".

---

## 🎨 Style Library

| Style Modifier | Category | Visual Characteristics |
| :--- | :--- | :--- |
| **Luxury monoline** | Premium | Elegant, thin strokes |
| **Geometric bold** | Tech | 2px strokes, rounded caps |
| **Organic Ink** | Lifestyle | Textured edges, fluid |
| **3D Rendered** | Complex | Depth, lighting, multi-color, transparent PNG/WebP (Use Strategy B) |

---

## 📚 Resources & Utilities

- **Vector/Trim Script**: `./skills/scripts/crop_and_trace.py`
- **Advanced Chroma-Key Script**: `./skills/scripts/remove_chroma_key.py`
- **Reference Gallery**: `./skills/icons/` (Categorized by: `premium`, `tech`, `lifestyle`, `detailled`, `3D`)
