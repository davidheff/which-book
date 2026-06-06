import os
from PIL import Image, ImageDraw, ImageFont

BG2 = (15, 20, 25)     # outer
BG  = (27, 35, 44)     # inner panel

EMOJI = "\N{SAXOPHONE}"   # 🎷
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\seguiemj.ttf",          # Segoe UI Emoji (color)
    "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    "/System/Library/Fonts/Apple Color Emoji.ttc",
]

def emoji_font(px):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, px)
            except Exception:
                pass
    raise SystemExit("No color emoji font found")

def make(S):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=BG2)
    pad = int(S * 0.06)
    d.rounded_rectangle([pad, pad, S - pad, S - pad], radius=int(S * 0.20), fill=BG)

    # Render the saxophone emoji big and centered.
    px = int(S * 0.64)
    font = emoji_font(px)
    glyph = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glyph)
    gd.text((S // 2, int(S * 0.52)), EMOJI, font=font, embedded_color=True, anchor="mm")
    img.alpha_composite(glyph)
    return img

def make_glyph(S):
    """Sax glyph on a transparent background (for the browser-tab favicon)."""
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = emoji_font(int(S * 0.92))
    d.text((S // 2, S // 2), EMOJI, font=font, embedded_color=True, anchor="mm")
    return img

# Opaque tiled icons for the home screen (iOS requires opaque; Android masks them).
master = make(1024)
for size, name in [(512, "icon-512.png"), (192, "icon-192.png"),
                   (180, "apple-touch-icon.png")]:
    master.resize((size, size), Image.LANCZOS).save(name)
    print("wrote", name)

# Transparent favicon for browser tabs.
glyph = make_glyph(256)
glyph.resize((32, 32), Image.LANCZOS).save("favicon-32.png")
print("wrote favicon-32.png (transparent)")
