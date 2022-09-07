from PIL import Image, ImageDraw, ImageFont


__all__ = ["create_demotivator"]

TITLE_FONT = ImageFont.truetype(font="TNR.ttf", size=32)
TEXT_FONT = ImageFont.truetype(font="TNR.ttf", size=22)

def create_demotivator(im: Image.Image, title: str, text: str, border_width: int = 3, padding: int = 10) -> Image.Image:

    if im.size[0] > 256 or im.size[1] > 256:
        im.thumbnail(size=(256, 256), resample=Image.ANTIALIAS)

    background = Image.new(mode="RGB", size=(512, 512))

    image_pos = (
        int(background.size[0] / 2 - im.size[0] / 2),
        int(background.size[0] / 2.5 - im.size[1] / 2),
    )

    div_pos = (
        int(background.size[0] / 2 - 256 / 2),
        int(background.size[0] / 2.5 - 256 / 2),
    )

    div = [
        (div_pos[0] - padding, div_pos[1] - padding), # top left corner
        (div_pos[0] + 256 + padding, div_pos[1] - padding), # top right corner
        (div_pos[0] + 256 + padding, div_pos[1] + 256 + padding), # bottom right corner
        (div_pos[0] - padding, div_pos[1] + 256 + padding), # bottom left corner
        (div_pos[0] - padding, div_pos[1] - padding), # top left corner
    ]

    title_pos = (int(background.size[0] / 2), div[3][1] + 36 + border_width)
    text_pos = (int(background.size[0] / 2), title_pos[1] + 31)

    background.paste(im=im, box=image_pos)

    background_draw = ImageDraw.Draw(im=background)
    background_draw.line(xy=div, fill=(255, 255, 255), width=border_width, joint="curve")

    background_draw.text(xy=title_pos, text=title, font=TITLE_FONT, fill=(255, 255, 255), anchor="mm")
    background_draw.text(xy=text_pos, text=text, font=TEXT_FONT, fill=(255, 255, 255), anchor="mm")

    return background


if __name__ == "__main__":
    import argparse


    parser = argparse.ArgumentParser(description="Testing image demotivator.")
    parser.add_argument("-i", dest="image", help="image path")
    args = parser.parse_args()

    image = Image.open(fp=args.image)
    dem = create_demotivator(im=image, title="сок фруто няня", text="ооо, закладочка")
    dem.show()
