import os
import shutil

try:
    shutil.rmtree('./_posts/')
except FileNotFoundError:
    pass

try:
    shutil.rmtree('./_site/')
except FileNotFoundError:
    pass

os.mkdir('./_posts')

for article in os.listdir('./source/_posts/'):
    with open('./source/_posts/'+article, 'r') as source_article:
        i = 0
        jekyll_content = ''
        for line in source_article.readlines():
            if '```Python' in line:
                jekyll_content += '```python\n'
            elif '```JavaScript' in line:
                jekyll_content += '```javascript\n'
            else:
                jekyll_content += line
            if i == 2:
                write_date = line.split(' ')[1].replace('.', '-')
            i += 1
        target_article_name = './_posts/'+write_date+'-'+article
        with open(target_article_name, 'w') as target_article:
            target_article.write(jekyll_content)
            print (target_article_name)
