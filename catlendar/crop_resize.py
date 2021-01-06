def crop_resize(im, resize_width, resize_height):
    resize_ratio = resize_width/resize_height
    image_width = im.width
    image_height = im.height
    image_ratio = image_width/image_height
    
    # Crop to match the resize ratio, before resize
    if resize_ratio > image_ratio:
        # Image is too narrow; crop top and bottom
        new_height = image_width / resize_ratio
        im = im.crop((0,
                     (image_height - new_height)//2,
                     image_width,
                     (image_height + new_height)//2))
    elif resize_ratio > image_ratio:
        # Image is too wide; crop left and right
        new_width = image_width * resize_ratio
        im = im.crop(((image_width - new_width)//2,
                      0,
                     (image_width + new_width)//2),
                    image_height)
    else:
        pass
    
    # resize
    im = im.resize((resize_width, resize_height))
    
    return im
