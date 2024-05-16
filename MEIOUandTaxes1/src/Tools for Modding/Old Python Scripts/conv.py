from PIL import Image

img = Image.open('Global_average_temprature_per_year_meiou_new.png')
img = img.convert('P', palette=Image.ADAPTIVE, colors=128)
img = img.convert('RGB')
img.save('Global_average_temprature_per_year_meiou_simple.png')
