import os
import re
import hashlib


article_dir = './source/_posts'
pic_dir = '../images'
target_dir = '../scene/blog'

'http://45.76.195.123/images/2019/06/03/42.jpg'
'https://raw.githubusercontent.com/guerbai/scene/main/blog/20210704003041.jpg'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


for _, _, files in os.walk(article_dir):
    count = 0
    for file_name in files:
        p = article_dir + '/' + file_name
        with open(p, 'r') as f:
            c = f.read()
            images = re.findall(r"45.76.195.123/images/(.*?)\)", c)
            for image in images:
                count += 1
                try:
                    suffix = image.split('.')[-1]
                    image_p = pic_dir + '/' + image
                    md5_value = md5(image_p)
                    command = "cp " + image_p + " " + target_dir + "/" + md5_value + "." + suffix
                    os.system("cp " + image_p + " " + target_dir + "/" + md5_value + "." + suffix)
                    c = c.replace('http://45.76.195.123/images/'+image, 'https://raw.githubusercontent.com/guerbai/scene/main/blog/'+md5_value+'.'+suffix)
                except FileNotFoundError:
                    print (file_name)
                    print (image)
            with open(p, 'w') as f:
                f.write(c)

    
print (count)

