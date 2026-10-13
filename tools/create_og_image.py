"""Render the site's typographic social sharing card (requires Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2
image = Image.new("RGB", (1200 * SCALE, 630 * SCALE), "#18201d")
draw = ImageDraw.Draw(image)


def text(position, value, size, color, bold=False):
    font_name = "malgunbd.ttf" if bold else "malgun.ttf"
    font = ImageFont.truetype(str(Path("C:/Windows/Fonts") / font_name), size * SCALE)
    draw.text(tuple(v * SCALE for v in position), value, font=font, fill=color)


def line(points, color, width):
    draw.line([(x * SCALE, y * SCALE) for x, y in points], fill=color, width=width * SCALE)


line([(76, 74), (1124, 74)], "#455347", 1)
text((76, 99), "SEOSEOUL WORKS", 22, "#c9f36a", True)
text((70, 203), "서서울웍스", 100, "#f5f6f1", True)
text((76, 352), "소프트웨어와 출판", 34, "#c9f36a", True)
text((76, 410), "기술과 콘텐츠를 만듭니다.", 27, "#c6cec8")
line([(76, 533), (1124, 533)], "#455347", 1)
text((76, 554), "seoseoulworks.com", 20, "#c6cec8")

# Reuse the geometric S from the site's favicon as a brand mark.
mark = Image.open(ROOT / "assets/apple-touch-icon.png").convert("RGBA")
mark = mark.resize((180 * SCALE, 180 * SCALE), Image.Resampling.LANCZOS)
image.paste(mark, (944 * SCALE, 217 * SCALE), mark)
output = ROOT / "assets/images/og-image.png"
image.resize((1200, 630), Image.Resampling.LANCZOS).save(output, optimize=True)
print(f"Created {output.name} (1200 x 630, {output.stat().st_size:,} bytes)")
