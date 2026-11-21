#!/usr/bin/env python3
"""Render the Virelia passport spread (1024x1024 PNG).

Drawn fresh in this session with PIL primitives: two cream pages of an
open passport on a dark cover, a drawn coat of arms, a stylised drawn
portrait, data fields, a correct MRZ, neighbouring-state stamps and a
daylight-only visa condition that reveals the country's character.

Fictional country: the Republic of Virelia, a fog-bound lighthouse
archipelago. Capital: Lumenharbour. Holder: Elena Ruth Marlowe,
lighthouse keeper. Issue 12 MAR 2024, expiry 12 MAR 2034; every stamp
falls between those dates. Passport number VRL847291 everywhere.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT + "DejaVuSerif.ttf"
SERIF_B = FONT + "DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = FONT + "DejaVuSans.ttf"
SANS_B = FONT + "DejaVuSans-Bold.ttf"
MONO = FONT + "DejaVuSansMono.ttf"
MONO_B = FONT + "DejaVuSansMono-Bold.ttf"

INK = (31, 42, 68)        # deep navy ink
INK_SOFT = (74, 84, 106)  # muted ink
GOLD = (176, 141, 62)
CREAM = (246, 240, 220)
CREAM_D = (232, 224, 198)
COVER = (35, 44, 58)

def f(path, size):
    return ImageFont.truetype(path, size)

def letterspaced(draw, cx, y, text, font, fill, spacing=4):
    """Draw text centred with extra letter spacing."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing

def field(draw, x, y, label, value, value_font=None, label_w=118):
    """One label/value row. Returns y of the value baseline area."""
    draw.text((x, y), label.upper(), font=f(SANS, 10), fill=INK_SOFT)
    draw.text((x, y + 14), value, font=value_font or f(SERIF_B, 15),
              fill=INK)
    draw.line([(x, y + 36), (x + 262, y + 36)], fill=(190, 182, 158), width=1)

def draw_arms(draw, cx, top):
    """Coat of arms: shield, lighthouse, rays, waves, star."""
    w, h = 66, 78
    x0, y0 = cx - w // 2, top
    # shield
    shield = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h - 22),
              (cx, y0 + h), (x0, y0 + h - 22)]
    draw.polygon(shield, fill=(28, 48, 84), outline=GOLD, width=2)
    # star above shield
    sx, sy = cx, y0 - 12
    star = []
    for i in range(10):
        r = 7 if i % 2 == 0 else 3
        a = math.pi * i / 5 - math.pi / 2
        star.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    draw.polygon(star, fill=GOLD)
    # light beams: narrow triangles fanning outward from the lamp room
    for dx in (-16, -8, 0, 8, 16):
        ax = cx + int(dx * 0.7)
        bx = cx + int(dx * 1.3)
        draw.polygon([(ax, y0 + 14), (bx - 3, y0 + 30),
                      (bx + 3, y0 + 30)], fill=(240, 205, 90))
    # lighthouse tower
    draw.polygon([(cx - 8, y0 + 30), (cx + 8, y0 + 30), (cx + 6, y0 + 56),
                  (cx - 6, y0 + 56)], fill=(245, 240, 225))
    draw.rectangle([cx - 8, y0 + 38, cx + 8, y0 + 43], fill=(178, 52, 48))
    draw.rectangle([cx - 7, y0 + 48, cx + 7, y0 + 52], fill=(178, 52, 48))
    draw.rectangle([cx - 9, y0 + 26, cx + 9, y0 + 31], fill=(245, 240, 225))
    # waves
    for wy in (y0 + 60, y0 + 66):
        for k in range(3):
            wx = x0 + 10 + k * 18
            draw.arc([wx, wy, wx + 16, wy + 10], 180, 360, fill=(150, 190, 210), width=2)

def draw_portrait(base, x, y, w, h):
    """Stylised drawn portrait: lighthouse keeper, head and shoulders."""
    img = Image.new("RGB", (w, h), (122, 138, 148))
    d = ImageDraw.Draw(img)
    # foggy sea gradient
    for i in range(h):
        t = i / h
        c = tuple(int(a + (b - a) * t) for a, b in zip((122, 138, 148), (168, 180, 184)))
        d.line([(0, i), (w, i)], fill=c)
    # distant lighthouse silhouette: wider tower in lighter grey, with a
    # soft glow halo around the lamp so it reads as a lighthouse, not a dot
    d.ellipse([w - 44, 2, w - 16, 28], fill=(247, 224, 138))
    d.polygon([(w - 40, 18), (w - 30, 18), (w - 32, 66), (w - 38, 66)],
              fill=(150, 165, 175))
    d.rectangle([w - 41, 16, w - 29, 20], fill=(150, 165, 175))
    d.line([(w - 42, 66), (w - 28, 66)], fill=(150, 165, 175), width=2)
    d.ellipse([w - 38, 8, w - 22, 22], fill=(240, 205, 90))
    # shoulders / coat
    d.polygon([(8, h), (52, 128), (98, 128), (142, h)], fill=(32, 46, 72))
    # shirt + lapels
    d.polygon([(62, 128), (88, 128), (75, 168)], fill=(240, 236, 222))
    d.polygon([(52, 128), (75, 168), (66, 128)], fill=(24, 36, 58))
    d.polygon([(98, 128), (75, 168), (84, 128)], fill=(24, 36, 58))
    # neck
    d.rectangle([66, 112, 84, 134], fill=(216, 178, 138))
    # neck shadow under the chin
    d.rectangle([66, 112, 84, 121], fill=(198, 158, 118))
    # face
    d.ellipse([52, 34, 98, 106], fill=(232, 195, 154))
    # hair: dark frame around face
    d.pieslice([46, 26, 104, 96], 180, 360, fill=(58, 40, 30))
    d.polygon([(48, 60), (58, 58), (54, 118), (46, 108)], fill=(58, 40, 30))
    d.polygon([(102, 60), (92, 58), (96, 118), (104, 108)], fill=(58, 40, 30))
    d.ellipse([50, 30, 100, 62], fill=(58, 40, 30))
    d.ellipse([54, 40, 96, 104], fill=(232, 195, 154))
    # soft cheek shadows and a jaw shadow so the face is not one flat fill
    d.ellipse([58, 82, 67, 87], fill=(226, 186, 146))
    d.ellipse([83, 82, 92, 87], fill=(226, 186, 146))
    d.arc([56, 62, 94, 108], 15, 165, fill=(208, 170, 130), width=3)
    # hair strands: thin lighter lines so the hair reads as strands, not a block
    for sx, sy0, sy1 in ((50, 62, 108), (55, 60, 104), (100, 62, 108), (95, 60, 104)):
        d.line([(sx, sy0), (sx - 1 if sx < 75 else sx + 1, sy1)],
               fill=(84, 60, 44), width=1)
    d.arc([54, 30, 96, 56], 200, 340, fill=(84, 60, 44), width=1)
    # keeper cap
    d.pieslice([48, 22, 102, 58], 180, 360, fill=(28, 42, 66))
    d.rectangle([48, 44, 102, 52], fill=(28, 42, 66))
    d.ellipse([70, 44, 80, 54], fill=(240, 205, 90))
    # cap brim highlight: lighter dome edge and brim top edge
    d.arc([48, 22, 102, 58], 180, 360, fill=(74, 96, 136), width=2)
    d.line([(50, 45), (100, 45)], fill=(96, 122, 162), width=2)
    # brows, eyes, nose, mouth
    d.line([(60, 66), (70, 64)], fill=(58, 40, 30), width=2)
    d.line([(80, 64), (90, 66)], fill=(58, 40, 30), width=2)
    # eyes with whites, iris and pupil (was flat dark dots)
    d.ellipse([60, 68, 69, 76], fill=(246, 243, 236))
    d.ellipse([81, 68, 90, 76], fill=(246, 243, 236))
    d.ellipse([62, 69, 67, 74], fill=(58, 72, 100))
    d.ellipse([83, 69, 88, 74], fill=(58, 72, 100))
    d.ellipse([63, 70, 66, 73], fill=(18, 18, 22))
    d.ellipse([84, 70, 87, 73], fill=(18, 18, 22))
    d.line([(75, 76), (74, 88), (77, 89)], fill=(196, 150, 112), width=2)
    d.line([(67, 96), (83, 96)], fill=(150, 80, 70), width=2)
    base.paste(img, (x, y))
    d0 = ImageDraw.Draw(base)
    d0.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)
    d0.rectangle([x + 4, y + 4, x + w - 5, y + h - 5], outline=GOLD, width=1)

def make_stamp(lines, color, kind="rect", rotate=5, size=(210, 132)):
    """One ink stamp on its own layer, rotated for a hand-stamped look."""
    layer = Image.new("RGBA", (size[0] + 30, size[1] + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = layer.width // 2, layer.height // 2
    if kind == "oval":
        d.ellipse([cx - 100, cy - 58, cx + 100, cy + 58], outline=color, width=3)
        d.ellipse([cx - 92, cy - 50, cx + 92, cy + 50], outline=color, width=1)
    else:
        d.rounded_rectangle([cx - 100, cy - 58, cx + 100, cy + 58], radius=8,
                            outline=color, width=3)
        d.rounded_rectangle([cx - 94, cy - 52, cx + 94, cy + 52], radius=6,
                            outline=color, width=1)
    y = cy - 44
    for i, (txt, sz, bold) in enumerate(lines):
        ft = f(MONO_B if bold else MONO, sz)
        d.text((cx, y), txt, font=ft, fill=color, anchor="ma")
        y += sz + 6
    return layer.rotate(rotate, expand=True, resample=Image.BICUBIC)

def main():
    img = Image.new("RGB", (W, H), COVER)
    d = ImageDraw.Draw(img, "RGBA")
    # cover texture: faint horizontal bands
    for yy in range(0, H, 6):
        d.line([(0, yy), (W, yy)], fill=(38, 48, 64, 40), width=1)
    # pages
    d.rectangle([28, 64, 996, 960], fill=CREAM, outline=GOLD, width=2)
    d.rectangle([512, 64, 514, 960], fill=(120, 110, 88))
    d.rectangle([34, 70, 508, 954], outline=CREAM_D, width=1)
    d.rectangle([518, 70, 990, 954], outline=CREAM_D, width=1)

    # ---------- LEFT PAGE: data page ----------
    draw_arms(d, 270, 92)
    d.text((270, 182), "REPUBLIC OF VIRELIA", font=f(SERIF_B, 21),
           fill=INK, anchor="ma")
    letterspaced(d, 270, 212, "PASSPORT", f(SERIF, 14), INK_SOFT, spacing=6)
    d.line([(120, 238), (420, 238)], fill=GOLD, width=2)
    # type / code / number row
    d.text((48, 254), "Type", font=f(SANS, 10), fill=INK_SOFT)
    d.text((48, 268), "P", font=f(SERIF_B, 15), fill=INK)
    d.text((150, 254), "Code", font=f(SANS, 10), fill=INK_SOFT)
    d.text((150, 268), "VRL", font=f(SERIF_B, 15), fill=INK)
    d.text((270, 254), "Passport No.", font=f(SANS, 10), fill=INK_SOFT)
    d.text((270, 268), "VRL847291", font=f(SERIF_B, 15), fill=INK)
    # portrait + fields
    draw_portrait(img, 48, 296, 150, 190)
    d = ImageDraw.Draw(img, "RGBA")
    field(d, 216, 296, "Surname", "MARLOWE")
    field(d, 216, 342, "Given names", "ELENA RUTH")
    field(d, 216, 388, "Nationality", "VIRELIAN")
    field(d, 216, 434, "Date of birth", "04 JUN 1988")
    # signature under portrait
    d.text((48, 496), "Elena Marlowe", font=f(SERIF_I, 17), fill=(52, 58, 84))
    d.line([(48, 520), (198, 520)], fill=INK_SOFT, width=1)
    d.text((48, 526), "Holder's signature", font=f(SANS, 9), fill=INK_SOFT)
    # lower fields
    d.text((216, 480), "Sex", font=f(SANS, 10), fill=INK_SOFT)
    d.text((216, 494), "F", font=f(SERIF_B, 15), fill=INK)
    d.text((300, 480), "Place of birth", font=f(SANS, 10), fill=INK_SOFT)
    d.text((300, 494), "LUMENHARBOUR", font=f(SERIF_B, 15), fill=INK)
    d.line([(216, 530), (492, 530)], fill=(190, 182, 158), width=1)
    d.text((48, 556), "Occupation", font=f(SANS, 10), fill=INK_SOFT)
    d.text((48, 570), "LIGHTHOUSE KEEPER, NORTH LIGHT STATION",
           font=f(SERIF_B, 14), fill=INK)
    d.line([(48, 596), (492, 596)], fill=(190, 182, 158), width=1)
    d.text((48, 614), "Date of issue", font=f(SANS, 10), fill=INK_SOFT)
    d.text((48, 628), "12 MAR 2024", font=f(SERIF_B, 15), fill=INK)
    d.text((270, 614), "Date of expiry", font=f(SANS, 10), fill=INK_SOFT)
    d.text((270, 628), "12 MAR 2034", font=f(SERIF_B, 15), fill=INK)
    d.line([(48, 654), (492, 654)], fill=(190, 182, 158), width=1)
    d.text((48, 672), "Authority", font=f(SANS, 10), fill=INK_SOFT)
    d.text((48, 686), "MINISTRY OF THE LANTERN, LUMENHARBOUR",
           font=f(SERIF_B, 13), fill=INK)
    d.line([(48, 712), (492, 712)], fill=(190, 182, 158), width=1)
    d.text((48, 726), "This passport remains the property of the Republic "
           "of Virelia.", font=f(SERIF_I, 11), fill=INK_SOFT)
    # MRZ strip
    d.rectangle([48, 758, 492, 856], fill=(233, 227, 204), outline=INK_SOFT)
    d.text((60, 772), "P<VRLMARLOWE<<ELENA<RUTH<<<<<<<<<<<<<<<<<<<<",
           font=f(MONO, 15), fill=INK)
    d.text((60, 806), "VRL8472916VRL8806046F3403129<<<<<<<<<<<<<<08",
           font=f(MONO, 15), fill=INK)
    d.text((270, 924), "1", font=f(SERIF, 12), fill=INK_SOFT, anchor="ma")

    # ---------- RIGHT PAGE: travel history ----------
    d.text((754, 84), "VISAS AND ENDORSEMENTS", font=f(SERIF_B, 17),
           fill=INK, anchor="ma")
    d.line([(600, 112), (908, 112)], fill=GOLD, width=2)

    blue = (38, 84, 150, 235)
    purple = (110, 60, 140, 235)
    green = (34, 110, 70, 235)
    red = (178, 52, 48, 235)
    stamps = [
        (make_stamp([("OSTARA", 20, True), ("ARRIVED", 15, True),
                     ("18 JUN 2024", 14, False), ("PORT OF OSTARA", 11, False)],
                    blue, "rect", -5), (640, 190)),
        (make_stamp([("OSTARA", 20, True), ("DEPARTED", 15, True),
                     ("29 JUN 2024", 14, False), ("PORT OF OSTARA", 11, False)],
                    blue, "rect", 4), (860, 190)),
        (make_stamp([("KELVAR", 20, True), ("ARRIVED", 15, True),
                     ("02 SEP 2024", 14, False), ("KELVAR GATE", 11, False)],
                    purple, "oval", 6), (640, 340)),
        (make_stamp([("KELVAR", 20, True), ("DEPARTED", 15, True),
                     ("20 SEP 2024", 14, False), ("KELVAR GATE", 11, False)],
                    purple, "oval", -4), (860, 340)),
        (make_stamp([("DUNMAR", 20, True), ("ARRIVED", 15, True),
                     ("14 JAN 2025", 14, False), ("DUNMAR HARBOUR", 11, False)],
                    green, "rect", 3), (640, 490)),
        (make_stamp([("FOG TAX", 18, True), ("PAID", 16, True),
                     ("2 LUMEN", 14, False), ("14 JAN 2025", 11, False)],
                    red, "oval", -6), (860, 490)),
    ]
    for layer, (cx, cy) in stamps:
        img.paste(layer, (cx - layer.width // 2, cy - layer.height // 2), layer)
    d = ImageDraw.Draw(img, "RGBA")

    # visa condition box — the telling paperwork detail
    d.rectangle([548, 590, 976, 806], outline=INK, width=2)
    d.rectangle([554, 596, 970, 800], outline=GOLD, width=1)
    d.text((762, 610), "CONDITION OF ENTRY — VIRELIA", font=f(SERIF_B, 14),
           fill=INK, anchor="ma")
    d.line([(580, 636), (944, 636)], fill=GOLD, width=1)
    cond = [
        "This passport is valid for travel in daylight",
        "hours only. The holder must clear the fog line",
        "before 18:00 and may not enter the Outer Lights",
        "after dark. No night crossings. No exceptions",
        "for keepers on duty — see stamp FOG TAX PAID.",
        "",
        "Issued at Lumenharbour, 12 MAR 2024.",
    ]
    yy = 650
    for line in cond:
        if line:
            d.text((580, yy), line, font=f(SERIF, 14), fill=INK)
        yy += 20
    # motto + small lighthouse
    d.line([(640, 846), (884, 846)], fill=GOLD, width=1)
    d.text((762, 860), "BY LANTERN LIGHT WE KEEP THE WAY",
           font=f(SERIF, 12), fill=INK_SOFT, anchor="ma")
    d.text((762, 924), "2", font=f(SERIF, 12), fill=INK_SOFT, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()
