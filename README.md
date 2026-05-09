# 🎨 Custom Icons Skill

A specialized skill for creating and managing bespoke icons using AI generation, conceptual design, and vector tracing.

## 🚀 Installation

To add this skill to your agent environment, run:

```bash
npx skills add jkc66/custom-icons-skill
```

## ✨ Features

- **Icon Modes**: Specialized workflows for **Design** (visual), **Path** (vector), and **Desire** (conceptual).
- **AI Prompt Templates**: Optimized, high-contrast prompts for generating traceable artwork.
- **Automated Processing**: Python utilities for image binarization and prep for `potrace`.
- **Framework Ready**: Best practices for implementing colorable SVGs in modern frameworks like Astro.
- **Reference Gallery**: Curated examples of high-quality, professional icons.

## 🛠 Usage

### 1. Generate or Design
Use the instructions in [SKILL.md](file:///home/ubuntu/custom-icons-skill/SKILL.md) to generate artwork or refine a conceptual "desire".

### 2. Process Image
Prepare the image for tracing:

```bash
python3 scripts/crop_and_trace.py path/to/source.png tmp/icons my-new-icon
```

### 3. Trace to SVG
Ensure `potrace` is installed:

```bash
potrace tmp/icons/my-new-icon.pbm --svg --flat -o src/assets/icons/my-new-icon.svg
```

### 4. Optimize
Minify the SVG:

```bash
bunx svgo src/assets/icons/my-new-icon.svg --multipass
```

## 📂 Structure

- `SKILL.md`: Core logic and instructions for the AI agent.
- `scripts/`: Automation and processing utilities.
- `resources/icons/`: Categorized reference gallery.

---

## 🖼 Reference Gallery

Explore the different styles supported by this skill:

### 💎 Premium (Strategy A)
*Monoline, elegant, thin strokes.*

| | | | |
| :---: | :---: | :---: | :---: |
| <img src="./resources/icons/premium/quality.svg" width="100" /> | <img src="./resources/icons/premium/design.svg" width="100" /> | <img src="./resources/icons/premium/experience.svg" width="100" /> | <img src="./resources/icons/premium/installation.svg" width="100" /> |

### 🤖 Tech (Strategy A)
*Geometric, bold, 2px stroke weight.*

| | | | |
| :---: | :---: | :---: | :---: |
| *[Placeholder]* | *[Placeholder]* | *[Placeholder]* | *[Placeholder]* |

### 🌿 Lifestyle (Strategy A)
*Organic, hand-drawn, textured edges.*

| | | | |
| :---: | :---: | :---: | :---: |
| *[Placeholder]* | *[Placeholder]* | *[Placeholder]* | *[Placeholder]* |

### 🌈 Complex (Strategy B)
*3D, multi-color, transparent PNGs (Green Screen workflow).*

| | | | |
| :---: | :---: | :---: | :---: |
| *[Placeholder]* | *[Placeholder]* | *[Placeholder]* | *[Placeholder]* |






