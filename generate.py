from PIL import Image, ImageDraw, ImageFont

def make_speechbubble(width, height):
    # load assets
    smile = Image.open("assets/infopanel_smile.png").convert("RGBA")
    bg = Image.open("assets/infopanel_contentBg.png").convert("RGBA")


    img = Image.new("RGBA", (width, height), "white")
    
    img.paste(smile, (0, 0))
    bg = bg.resize((width - 20, height - 20))
    img.paste(bg, (smile.width, 0))

    img.show()

make_speechbubble(200, 100)