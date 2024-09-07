import os
import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont


def nine_sliced(width, height, imagepath, slicingpath) -> Image:
    tilemap = Image.open(imagepath)
    with open(slicingpath, "r") as f:
        csvreader = csv.reader(f)
        slices = list(csvreader)
    horizontal = [
        (int(slices[0][i]), int(slices[0][i + 1])) for i in range(0, len(slices[0]), 2)
    ]
    vertical = [
        (int(slices[1][i]), int(slices[1][i + 1])) for i in range(0, len(slices[1]), 2)
    ]

    tiles = []
    for i in range(3):
        for j in range(3):
            tiles.append(
                tilemap.crop(
                    (horizontal[j][0], vertical[i][0], horizontal[j][1], vertical[i][1])
                )
            )

    height = max(height, tilemap.height)
    img = Image.new("RGBA", (width, height))

    positions = []
    for i in range(3):
        for j in range(3):
            if j == 0:
                x = 0
            elif j == 1:
                x = tiles[3].width
            else:
                x = width - tiles[5].width

            if i == 0:
                y = 0
            elif i == 1:
                y = tiles[1].height
            else:
                y = height - tiles[7].height

            positions.append((x, y))

    # i aint doing the math for this lol
    tiles[1] = tiles[1].resize(
        (width - tiles[0].width - tiles[2].width, tiles[1].height)
    )
    tiles[3] = tiles[3].resize(
        (tiles[3].width, height - tiles[0].height - tiles[6].height)
    )
    tiles[4] = tiles[4].resize(
        (
            width - tiles[3].width - tiles[5].width,
            height - tiles[1].height - tiles[7].height,
        )
    )
    tiles[5] = tiles[5].resize(
        (tiles[5].width, height - tiles[2].height - tiles[8].height)
    )
    tiles[7] = tiles[7].resize(
        (width - tiles[6].width - tiles[8].width, tiles[7].height)
    )

    for i in range(9):
        img.paste(tiles[i], positions[i])

    return img


def rasterize_text(text, wrapwidth, fontpath, fontsize, color) -> Image:
    # TODO: text hinting and justify alignment
    font = ImageFont.truetype(fontpath, fontsize)
    wrapper = textwrap.TextWrapper(width=wrapwidth)
    wrapped_text = wrapper.fill(text)
    _, _, width, height = font.getbbox(wrapped_text)
    height += wrapped_text.count("\n") * 2 * height
    img = Image.new("RGBA", (width, height), (0,) * 4)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), wrapped_text, font=font, fill=color)
    img = img.crop(img.getbbox())
    return img


def neptunfej(text, scale = 1, margin = (0, 0)) -> Image:
    path = os.path.dirname(__file__)
    padding = 17, 13
    text_img = rasterize_text(text, 80, os.path.join(path, "assets/verdanab.ttf"), 12, (82, 86, 89, 255))
    speechbubble = nine_sliced(
        text_img.width + 2 * padding[0],
        text_img.height + 2 * padding[1],
        os.path.join(path, "assets/9sliced.png"),
        os.path.join(path, "assets/slicing.csv"),
    )
    smile = Image.open(os.path.join(path, "assets/infopanel_smile.png"))

    fullwidht = speechbubble.width + smile.width + 2 * margin[0]
    fullheight = max(speechbubble.height, smile.height) + 2 * margin[1]
    img = Image.new("RGBA", (fullwidht, fullheight), (255,) * 4)

    img.paste(speechbubble, (smile.width - 1 + margin[0], 0 + margin[1]))
    img.alpha_composite(smile, margin)
    img.alpha_composite(text_img, (smile.width - 1 + padding[0] + margin[0], padding[1] + margin[1]))

    if scale != 1:
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.NEAREST)

    return img
