# 🎨 Custom Icons Skill

![Skill](https://img.shields.io/badge/Skill-Custom%20Icons-7c3aed?style=for-the-badge&logo=sparkfun&logoColor=white)
![Codex](https://img.shields.io/badge/Tested%20in-Codex-111827?style=for-the-badge&logo=openai&logoColor=white)
![Antigravity](https://img.shields.io/badge/Tested%20in-Antigravity-4285f4?style=for-the-badge&logo=google&logoColor=white)
![Icons](https://img.shields.io/badge/Output-SVG%20%2B%20PNG-10b981?style=for-the-badge&logo=svg&logoColor=white)

A specialized skill for creating and managing bespoke icons using AI generation, conceptual design, and vector tracing.

Tested with Codex and Antigravity.

## 🚀 Installation

To add this skill to your agent environment, run:

```bash
npx skills add jkc66/custom-icons-skill

bunx skills add jkc66/custom-icons-skill
```

## 🛠 Usage

### 1. Generate or Design
Use the instructions in [SKILL.md](skills/SKILL.md) to generate artwork or refine a conceptual "desire".

### 2. Process Image
Follow the Strategy A or Strategy B pipeline in [SKILL.md](skills/SKILL.md). Reference gallery assets live in `readme-assets/icons/`.

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

- `skills/SKILL.md`: Core logic and instructions for the AI agent.
- `skills/scripts/`: Processing utilities used by the skill.
- `readme-assets/icons/`: Categorized README reference gallery.

---

## 🖼 Reference Gallery

Explore the different styles supported by this skill:

### 💎 Premium (Strategy A)
*Monoline, elegant, thin strokes.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./readme-assets/icons/premium/quality.svg" width="200" /> | <img src="./readme-assets/icons/premium/design.svg" width="200" /> | <img src="./readme-assets/icons/premium/experience.svg" width="200" /> | <img src="./readme-assets/icons/premium/installation.svg" width="200" /> | <img src="./readme-assets/icons/premium/warranty.svg" width="200" /> |


### 🤖 Tech (Strategy A)
*Geometric, bold, 2px stroke weight.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./readme-assets/icons/tech/chip.svg" width="200" /> | <img src="./readme-assets/icons/tech/cloud.svg" width="200" /> | <img src="./readme-assets/icons/tech/code.svg" width="200" /> | <img src="./readme-assets/icons/tech/security.svg" width="200" /> | <img src="./readme-assets/icons/tech/database.svg" width="200" /> |

### 🌿 Lifestyle (Strategy A)
*Organic, hand-drawn, textured edges.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./readme-assets/icons/lifestyle/leaf.svg" width="200" /> | <img src="./readme-assets/icons/lifestyle/flower.svg" width="200" /> | <img src="./readme-assets/icons/lifestyle/sun.svg" width="200" /> | <img src="./readme-assets/icons/lifestyle/tree.svg" width="200" /> | <img src="./readme-assets/icons/lifestyle/wave.svg" width="200" /> |

### 🏛 Detailed (Strategy A)
*Intricate, high-detail vector art.*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./readme-assets/icons/detailled/museum.svg" width="200" /> | <img src="./readme-assets/icons/detailled/library.svg" width="200" /> | <img src="./readme-assets/icons/detailled/theater.svg" width="200" /> | <img src="./readme-assets/icons/detailled/cathedral.svg" width="200" /> | <img src="./readme-assets/icons/detailled/observatory.svg" width="200" /> |

### 🌈 Complex (Strategy B)
*3D, multi-color, transparent PNGs (Green Screen workflow).*

| | | | | |
| :---: | :---: | :---: | :---: | :---: |
| <img src="./readme-assets/icons/3D/cube.png" width="200" /> | <img src="./readme-assets/icons/3D/residence.webp" width="200" /> | <img src="./readme-assets/icons/3D/rocket.png" width="200" /> | <img src="./readme-assets/icons/3D/robot.png" width="200" /> | <img src="./readme-assets/icons/3D/balloon.png" width="200" /> |
