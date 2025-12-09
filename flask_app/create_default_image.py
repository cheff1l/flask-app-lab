from PIL import Image, ImageDraw

img = Image.new('RGB', (128, 128), color='#6c757d')
draw = ImageDraw.Draw(img)

draw.ellipse([32, 20, 96, 84], fill='white')
draw.ellipse([20, 70, 108, 158], fill='white')

img.save('app/users/static/profile_pics/profile_default.jpg')
print("✓ Дефолтне зображення створено!")
