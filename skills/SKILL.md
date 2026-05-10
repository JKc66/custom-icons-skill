---
name: custom-icons-skill
description: "Professional workflow for creating bespoke vector and complex raster icons. Professional icon design workflow including Design (visual), Path (vector), Desire (conceptual), and 3D chroma-key modes. Features AI prompt engineering, automated binarization, alpha cleanup, and SVG optimization."
---


# 🎨 Custom Icons Skill

A master workflow for crafting professional-grade iconography. This skill handles the entire pipeline: from conceptual "desire" and visual "design" to technical "path" refinement, transparent 3D PNG cleanup, and production-ready SVG optimization.

## 🤖 Agent Instructions (Strict Workflow)

When this skill is activated, you MUST follow this step-by-step interaction protocol:

### Phase 0: User Intent Comes First
Follow the user's explicit request over defaults in this skill.

- If the user provides specific subjects, style, output type, destination, colors, or framework, use those exact details as provided. If any detail is missing, request clarification.
- If the user's input contains conflicting or invalid details, clarify the conflict and request correction before proceeding. This takes priority over following the input strictly.
- If the user requests an unsupported format or style, inform them of the limitation and suggest alternatives.
- Do not substitute a different pipeline, format, style, subject, palette, or destination because it seems easier than the user's valid request.
- Do not hand-author final Strategy A SVGs unless the user explicitly asks for manual/deterministic SVG code.
- Do not convert a Strategy B/3D request into SVG unless the user explicitly asks for SVG.
- Do not ask setup questions when the user has already provided enough information to proceed.
- Ask a concise clarifying question only when a missing detail prevents accurate determination of the output format, subject list, destination, or strategy selection.
- If the user asks to update this skill or its gallery, preserve existing conventions unless the user asks to change them.
- Use a visible project-local temporary workspace for generated sources, masks, traces, and intermediate outputs: `tmp/custom-icons/<request-or-icon-name>/`.
- Do not delete the temporary workspace or intermediate files unless the user explicitly asks for cleanup. Final assets should be copied to the target destination; intermediate files should remain in the `tmp/` workspace as a reference until an explicit cleanup request is received.

### Phase 1: Discovery & Style Definition
Use discovery only when the request has missing required information. If the user input is incomplete, ask for the minimum missing information:

1.  **Style**: What style of icon? (e.g., 3D-effect, Flat, Monoline, Luxury Engraved, Minimalist).
2.  **Subjects**: What icons or desire should be represented?
3.  **Target environment**: Where will the icons be used? (e.g., Astro, React, Mobile App).

### Phase 2: Generation & Strategy Selection
For each icon, select a strategy based on the visual complexity:

#### Strategy Selection Flowchart
1.  **Analyze Request**: Check subject complexity and color requirements.
    -   If the request mixes Strategy A and Strategy B features, clarify which to prioritize or suggest splitting the task.
2.  **Select Strategy**:
    -   **Strategy A (Vector)**: Use for monochrome logos, UI icons, or simple line art.
    -   **Strategy B (Raster)**: Use for 3D icons, multi-color assets, or detailed illustrations.
3.  **Confirm Pipeline**:
    -   Strategy A -> Binarization -> Potrace -> SVGO.
    -   Strategy B -> Chroma-Key -> Transparent PNG/WebP.

| Strategy | Recommended Use Cases | Technical Pipeline |
| :--- | :--- | :--- |
| **Strategy A (Vector)** | Logos, UI icons, line art, monochrome | Image -> Binarization -> Potrace -> SVGO |
| **Strategy B (Raster)** | 3D icons, multi-color, detailed illustration | Image -> Chroma-Key -> Transparent PNG/WebP |

#### Prompt Construction Rules
Use a concise, labeled prompt spec for generation.

##### Content Constraints
1. **Asset type**: icon asset for the user's target environment.
2. **Primary request**: exact subject or concept.
3. **Style/medium**: requested style plus the selected strategy.
4. **Composition/framing**: centered, clear silhouette, generous padding.
5. **Color palette**: user-specified colors or category color.

##### Visual Constraints
- **No text**: unless explicitly requested.
- **Cleanliness**: No logos, trademarks, or watermarks.
- **Isolation**: No extra elements or complex backgrounds.

##### Examples
- *Vector*: "A monoline coffee cup icon, black on white, minimal."
- *Raster*: "3D isometric computer icon, vibrant colors, #00ff00 background."

For existing image/reference workflows, label each image by role: `Image 1: edit target`, `Image 2: style reference`, etc.

#### Strategy A: Vector (Monochrome/Simple)
*Use for: Logos, UI icons, line art.*
1.  **Generate**:
    ```text
    Asset type: scalable UI icon
    Primary request: [SUBJECT]
    Style/medium: [STYLE], high-contrast black vector-like line art
    Composition/framing: centered icon, clear silhouette, generous padding
    Color palette: black on pure white background
    Constraints: no fills unless requested; no gradients; no text; no logos or trademarks; no watermark; no extra elements
    ```
2.  **Process**: Binarize the generated image, trace it with `potrace`, and optimize it with `svgo`.
3.  **Rule**: Do not hand-author final SVG path data for new Strategy A icons unless the user explicitly asks for a deterministic/manual SVG. The default output must come from the generated image -> `scripts/crop_and_trace.py` -> `potrace` -> `svgo` pipeline.
4.  **Color**: If the user specifies a color, apply that color after tracing. If updating the reference gallery and no color is specified, use the category color.

#### Strategy B: Raster (Complex/Multi-color)
*Use for: Detailed illustrations, 3D icons, colorful assets.*
1.  **Generate**:
    ```text
    Asset type: transparent raster icon
    Primary request: [SUBJECT]
    Style/medium: [STYLE], vibrant detailed icon
    Composition/framing: centered isolated subject, clear silhouette, generous padding
    Scene/backdrop: perfectly flat solid chroma-key background, usually #00ff00
    Constraints: background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation; crisp edges; no halos; no text unless requested; no logos or trademarks; no watermark; no extra elements; do not use the chroma-key color anywhere in the subject
    ```
    Use `#ff00ff` instead of `#00ff00` when the subject contains significant green elements or a predominantly green color scheme.
2.  **Logic**: Background removed via chroma-keying to create a transparent PNG.
3.  **Rule**: Keep Strategy B outputs as transparent PNG/WebP unless the user explicitly asks for another format.

---

### Phase 3: Processing & Tracing

#### Temporary Workspace
Before processing, create a project-local workspace for the request:

```bash
mkdir -p tmp/custom-icons/<request-or-icon-name>
```

Save generated source images, cropped PNGs, PBM files, traced SVG drafts, validation snapshots, and alternate attempts in that folder. Use the user's requested destination only for final delivered assets; if no final destination is provided, leave the final assets in the same `tmp/custom-icons/<request-or-icon-name>/` workspace. 

- **Input Validation**: If the provided final destination path is invalid, or if the user provides an unsupported file format for input, notify the user and request a valid path/format before proceeding.

#### Error Handling
If any processing step fails (binarization, tracing, chroma-keying), report the specific error to the user and suggest corrective actions (e.g., retrying with adjusted parameters, checking file formats).

#### For Strategy A (Vector):
1.  **Binarize**: `python3 scripts/crop_and_trace.py <source> tmp/custom-icons/<request-or-icon-name> <name>`
2.  **Trace**: `potrace "tmp/custom-icons/<request-or-icon-name>/<name>.pbm" --svg --flat -o "tmp/custom-icons/<request-or-icon-name>/<name>.svg"`
3.  **Optimize**: `bunx svgo "tmp/custom-icons/<request-or-icon-name>/<name>.svg"`
4.  **Color**: After tracing, apply the target category fill/stroke color to the optimized SVG only as a mechanical tinting step.
5.  **Deliver**: Copy the optimized SVG from `tmp/custom-icons/<request-or-icon-name>/` to the user's requested destination when provided.
6.  **Validate**: Confirm the SVG parses, contains traced path data, and visually matches the requested subject/style.

#### For Strategy B (Complex):
1.  **Remove Green Screen** with the advanced chroma-key utility:
    ```bash
    python3 scripts/remove_chroma_key.py \
      --input <source> \
      --out tmp/custom-icons/<request-or-icon-name>/<name>.png \
      --auto-key border \
      --soft-matte \
      --spill-cleanup \
      --edge-feather 1.0 \
      --force
    ```
    *Result: Creates a transparent PNG with spill cleanup and antialiased edges.*

2.  **Alternative Trim Workflow**:
    ```bash
    python3 scripts/crop_and_trace.py <source> tmp/custom-icons/<request-or-icon-name> <name> \
      --chroma \
      --padding 12
    ```
    *Result: Creates a transparent, trimmed PNG at `tmp/custom-icons/<request-or-icon-name>/<name>.png`. Use this when trimming is more important than soft matte cleanup.*

3.  **Deliver**: Copy the transparent PNG/WebP from `tmp/custom-icons/<request-or-icon-name>/` to the user's requested destination when provided.
4.  **Validate Alpha**: Check that the output has transparent corners, no green fringe, and a clear subject silhouette. If a fringe remains after the advanced utility, retry once with `--edge-contract 1`; if edges look too hard, use a smaller feather such as `--edge-feather 0.25`.


---

### Phase 4: Optimization & Delivery
1.  **Optimize**: For SVGs, use `svgo`. For PNGs, ensure they are trimmed and compressed.
2.  **Implement**: Show the user how to use the asset.
3.  **Gallery Consistency**: Keep each reference category at five icons when updating the gallery. Strategy A categories should use their thematic fill/stroke color: Tech `#00C8FF`, Lifestyle `#00E676`, Detailed `#FF3D00`.
4.  **Report Honestly**: Say which pipeline was used, where final files were saved, where the `tmp/custom-icons/...` workspace is, and whether validation passed. If a requested step could not be completed, say exactly what failed.

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

### Scripts
- **Vector/Trim Script**: [scripts/crop_and_trace.py](scripts/crop_and_trace.py)
- **Advanced Chroma-Key Script**: [scripts/remove_chroma_key.py](scripts/remove_chroma_key.py)
