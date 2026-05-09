# 🎨 Custom Icons Skill

A specialized skill for creating and managing bespoke icons using AI generation, conceptual design, and vector tracing.

## 🚀 Installation

To add this skill to your agent environment, run:

```bash
npx skills add jkc66/custom-icons-skill
```

## 🛠 Usage

### 1. Generate or Design
Use the instructions in [skill.md](skills/skill.md) to generate artwork or refine a conceptual "desire".

### 2. Process Image
Follow the Strategy A or Strategy B pipeline in [skill.md](skills/skill.md). Reference gallery assets live in `skills/icons/`.

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

- `skills/skill.md`: Core logic and instructions for the AI agent.
- `skills/scripts/`: Processing utilities used by the skill.
- `skills/icons/`: Categorized reference gallery.

---

## 🖼 Reference Gallery

Explore the different styles supported by this skill:

### 💎 Premium (Strategy A)
*Monoline, elegant, thin strokes.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./skills/icons/premium/quality.svg" width="200" /> | <img src="./skills/icons/premium/design.svg" width="200" /> | <img src="./skills/icons/premium/experience.svg" width="200" /> | <img src="./skills/icons/premium/installation.svg" width="200" /> | <img src="./skills/icons/premium/warranty.svg" width="200" /> |


### 🤖 Tech (Strategy A)
*Geometric, bold, 2px stroke weight.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./skills/icons/tech/chip.svg" width="200" /> | <img src="./skills/icons/tech/cloud.svg" width="200" /> | <img src="./skills/icons/tech/code.svg" width="200" /> | <img src="./skills/icons/tech/security.svg" width="200" /> | <img src="./skills/icons/tech/database.svg" width="200" /> |

### 🌿 Lifestyle (Strategy A)
*Organic, hand-drawn, textured edges.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./skills/icons/lifestyle/leaf.svg" width="200" /> | <img src="./skills/icons/lifestyle/flower.svg" width="200" /> | <img src="./skills/icons/lifestyle/sun.svg" width="200" /> | <img src="./skills/icons/lifestyle/tree.svg" width="200" /> | <img src="./skills/icons/lifestyle/wave.svg" width="200" /> |

### 🏛 Detailed (Strategy A)
*Intricate, high-detail vector art.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./skills/icons/detailled/museum.svg" width="200" /> | <img src="./skills/icons/detailled/library.svg" width="200" /> | <img src="./skills/icons/detailled/theater.svg" width="200" /> | <img src="./skills/icons/detailled/cathedral.svg" width="200" /> | <img src="./skills/icons/detailled/observatory.svg" width="200" /> |

### 🌈 Complex (Strategy B)
*3D, multi-color, transparent PNGs (Green Screen workflow).*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./skills/icons/3D/cube.png" width="200" /> | <img src="./skills/icons/3D/residence.webp" width="200" /> | <img src="./skills/icons/3D/rocket.png" width="200" /> | <img src="./skills/icons/3D/robot.png" width="200" /> | <img src="./skills/icons/3D/balloon.png" width="200" /> |

