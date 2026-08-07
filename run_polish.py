import os, re

def polish(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Gradient Text on headings/text
    content = re.sub(
        r'bg-clip-text text-transparent bg-gradient-to-r from-indigo-\d+ to-[a-z]+-\d+',
        r'text-indigo-400',
        content
    )
    # Also clean up any lingering text-transparent if it was separate
    content = content.replace('text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-violet-600', 'text-indigo-400')
    content = content.replace('bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-violet-600', 'text-indigo-400')

    # 2. Bounce easing
    content = content.replace('animate-bounce', 'animate-pulse-soft')

    # 3. Layout transition (CSS)
    content = content.replace(
        '.progress-bar { transition: width 0.6s cubic-bezier(0.4,0,0.2,1); }',
        '.progress-bar { transition: transform 0.6s cubic-bezier(0.4,0,0.2,1); transform-origin: left; width: 100%; transform: scaleX(0); }'
    )
    
    # 3b. Layout transition (JS updates)
    content = content.replace(
        "bar.style.width = cur + '%';",
        "bar.style.transform = `scaleX(${cur / 100})`;"
    )
    content = content.replace(
        "document.getElementById('vote-progress-bar').style.width = `${(voted / total) * 100}%`;",
        "document.getElementById('vote-progress-bar').style.transform = `scaleX(${voted / total})`;"
    )
    content = content.replace(
        "document.getElementById('phase-progress-bar').style.width = `${pct}%`;",
        "document.getElementById('phase-progress-bar').style.transform = `scaleX(${pct / 100})`;"
    )

    # 4. Broken image initially
    # Find img tags without src or with empty src and hide them
    content = content.replace('<img id="preview-img" class="w-full', '<img id="preview-img" style="display:none;" class="w-full')
    content = content.replace('<img id="done-preview-img" class="mx-auto', '<img id="done-preview-img" style="display:none;" class="mx-auto')
    content = content.replace('<img id="vote-image" class="w-full', '<img id="vote-image" style="display:none;" class="w-full')
    content = content.replace('<img id="qr-img" class="w-52 h-52 object-contain" src=""', '<img id="qr-img" class="w-52 h-52 object-contain" src="" style="display:none;"')

    # JS updates to show image once loaded
    content = content.replace("document.getElementById('preview-img').src = e.target.result;", "const pImg = document.getElementById('preview-img'); pImg.src = e.target.result; pImg.style.display = 'block';")
    content = content.replace("document.getElementById('done-preview-img').src = URL.createObjectURL(file);", "const dpImg = document.getElementById('done-preview-img'); dpImg.src = URL.createObjectURL(file); dpImg.style.display = 'block';")
    content = content.replace("document.getElementById('vote-image').src = img.url;", "const vImg = document.getElementById('vote-image'); vImg.src = img.url; vImg.style.display = 'block';")
    content = content.replace("document.getElementById('qr-img').src = qrcodeUrl;", "const qImg = document.getElementById('qr-img'); qImg.src = qrcodeUrl; qImg.style.display = 'block';")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Polished {filename}')

polish('d:/VScode/MysteryBox/app/static/participant.html')
polish('d:/VScode/MysteryBox/app/static/host.html')
