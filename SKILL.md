---
name: custom-icons
description: "Professional workflow for creating bespoke vector icons. Supports Design (visual), Path (vector-driven), and Desire (conceptual) modes. Features AI prompt engineering, automated binarization, and SVG optimization."
---


# 🎨 Custom Icons Skill

A master workflow for crafting professional-grade vector iconography. This skill handles the entire pipeline: from conceptual "desire" and visual "design" to technical "path" refinement and production-ready SVG optimization.

## 🚀 Installation

To integrate this skill into your environment:

```bash
npx skills add jkc66/custom-icons-skill
```

---

## 🤖 Agent Instructions (Strict Workflow)

When this skill is activated, you MUST follow this step-by-step interaction protocol:

### Phase 1: Discovery & Style Definition
Before generating anything, ask the user:
1.  **What style of icon are you looking for?** (e.g., 3D-effect, Flat, Monoline, Luxury Engraved, Minimalist).
2.  **What icons do you need?** (Ask for a list of subjects or the "desire" behind them).
3.  **What is the target environment?** (e.g., Astro, React, Mobile App).

### Phase 2: Generation & Strategy Selection
For each icon, decide on the technical strategy based on complexity:

#### Strategy A: Vector (Monochrome/Simple)
*Use for: Logos, UI icons, line art.*
1.  **Generate**: "Minimalist [SUBJECT] icon, high-contrast black on pure white background. [STYLE]. No fills, no gradients. Isolated on white."
2.  **Logic**: Traced to SVG, colored via CSS later.

#### Strategy B: Raster (Complex/Multi-color)
*Use for: Detailed illustrations, 3D icons, colorful assets.*
1.  **Generate**: "[SUBJECT] icon, vibrant colors, [STYLE]. **Pure green background (#00FF00)**. No shadows, isolated subject."
2.  **Logic**: Background removed via chroma-keying to create a transparent PNG.

---

### Phase 3: Processing & Tracing

#### For Strategy A (Vector):
1.  **Binarize**: `python3 scripts/crop_and_trace.py <source> tmp/output <name>`
2.  **Trace**: `potrace "tmp/output/<name>.pbm" --svg --flat -o "src/assets/icons/<name>.svg"`
3.  **Optimize**: `bunx svgo "src/assets/icons/<name>.svg"`

#### For Strategy B (Complex):
1.  **Remove Green Screen**:
    ```bash
    python3 scripts/crop_and_trace.py <source> tmp/output <name> --chroma
    ```
    *Result: Creates a transparent, trimmed PNG at `tmp/output/<name>.png`.*


---

### Phase 4: Optimization & Delivery
1.  **Optimize**: For SVGs, use `svgo`. For PNGs, ensure they are trimmed and compressed.
2.  **Implement**: Show the user how to use the asset.

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
| **3D Rendered** | Complex | Depth, lighting, multi-color (Use Strategy B) |

---

## 📚 Resources & Utilities

- **Processing Script**: `./scripts/crop_and_trace.py`
- **Reference Gallery**: `./resources/icons/` (Categorized by: `premium`, `tech`, `lifestyle`, `complex`)




