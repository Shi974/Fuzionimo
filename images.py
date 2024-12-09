#import os
import json
from PIL import Image
import wget
from pathlib import Path
import glob

def download_img() :
  with open('animals.json') as f :
    animal_list = json.load(f)
    url = [animal["img"] for animal in animal_list]
    try :
      for url2 in url :
        url2 = url2.strip()
        if url2 :
          path = 'img'
          file_name = wget.download(url2, out = path)
          print('Image Successfully Downloaded: ', file_name)
    except Exception as e :
      print(e)
    print('All done')

def resize_img() :
  try :
    for image in glob.glob('img/*.png') :
    #for image in glob.glob('img/*-256.png') :
      im = Image.open(image)
      #image_list.append(im)
    #with Image.open("img/corgi.png") as im :
      file_name = Path(im.filename).stem
      # Provide the target width and height of the image
      #(width, height) = (im.width // 2, im.height // 2)
      (width, height) = (128, 128)
      im_resized = im.resize((width, height))
      #im_resized.save('img/' + file_name + "-256.png")
      im_resized.save('img/' + file_name + "-128.png")
      #print(file_name)
      #print(im_resized.size)
    print("All done")
  except Exception as e :
    print(e)
    
def img_prop() :
  try :
    for image in glob.glob('img/*.png') :
      im = Image.open(image)
      print(im.size)
  except Exception as e :
    print(e)

#download_img()
resize_img()
#img_prop()