from catlendar.month_calendar import month_calendar
from catlendar.crop_resize import crop_resize
from PIL import Image

for month, bg in zip([x+1 for x in range(12)],
                     ["red", "green", "blue", "green", "red", "yellow", "red", "blue", "yellow", "black", "blue", "black"]):
    cal = month_calendar(2021, month, 850, 550)
    photo = Image.open(f"./images/2021/{month:02}.jpg")
    
    # photo = photo.resize((840, 540))
    photo = crop_resize(photo, 840, 540)
    
    image = Image.new(mode="RGBA", size=(850, 1100), color=bg)
    image.paste(photo, (5, 5))
    image.paste(cal.image, (0, 550), cal.image)
    image.save(f"./{month}.png")
