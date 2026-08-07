import re
with open('d:/VScode/MysteryBox/app/static/participant.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix gradient text
text = re.sub(r'text-transparent bg-clip-text bg-gradient-to-[a-z] from-indigo-\d+ to-violet-\d+', 'text-indigo-400', text)
text = re.sub(r'bg-clip-text text-transparent bg-gradient-to-[a-z] from-indigo-\d+ to-violet-\d+', 'text-indigo-400', text)
text = text.replace('text-transparent', '')
text = text.replace('bg-clip-text', '')

# Fix images
blank_img = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
text = re.sub(r'(<img[^>]+id="[^"]+"[^>]*)(>)', r'\1 src="' + blank_img + r'">', text)
text = text.replace('src="" src="', 'src="')
text = text.replace('src=""', f'src="{blank_img}"')

with open('d:/VScode/MysteryBox/app/static/participant.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('d:/VScode/MysteryBox/app/static/host.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'text-transparent bg-clip-text bg-gradient-to-[a-z] from-indigo-\d+ to-violet-\d+', 'text-indigo-400', text)
text = re.sub(r'bg-clip-text text-transparent bg-gradient-to-[a-z] from-indigo-\d+ to-violet-\d+', 'text-indigo-400', text)
text = text.replace('text-transparent', '')
text = text.replace('bg-clip-text', '')

text = re.sub(r'(<img[^>]+id="[^"]+"[^>]*)(>)', r'\1 src="' + blank_img + r'">', text)
text = text.replace('src="" src="', 'src="')
text = text.replace('src=""', f'src="{blank_img}"')

with open('d:/VScode/MysteryBox/app/static/host.html', 'w', encoding='utf-8') as f:
    f.write(text)
