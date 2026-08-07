import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove HTML headers like <!-- ── Header ── -->
    content = re.sub(r'<!--\s*[─═]+.*?[-═]+\s*-->\n?', '', content)
    
    # Remove JS/Python headers like // ══════ or # ── GET
    content = re.sub(r'//\s*[═─]{10,}.*\n?', '', content)
    content = re.sub(r'#\s*[─═]{2,}.*\n?', '', content)

    # Emoji replacements for host.html and participant.html
    if filepath.endswith('.html'):
        if '<script src="https://unpkg.com/lucide@latest"></script>' not in content:
            content = content.replace('</head>', '  <script src="https://unpkg.com/lucide@latest"></script>\n</head>')
        
        if 'lucide.createIcons();' not in content:
            # We'll just call it globally or at the end of the script
            # Or inside DOMContentLoaded
            content = content.replace("connectWS();", "connectWS();\n  lucide.createIcons();")
            content = content.replace("loadQR();", "loadQR();\n  lucide.createIcons();")

        # Map emojis to lucide tags
        replacements = {
            '⏳': '<i data-lucide="hourglass" class="w-6 h-6"></i>',
            '📸': '<i data-lucide="camera" class="w-6 h-6"></i>',
            '⭐': '<i data-lucide="star" class="w-6 h-6"></i>',
            '🏆': '<i data-lucide="trophy" class="w-6 h-6"></i>',
            '🔄': '<i data-lucide="rotate-ccw" class="w-6 h-6"></i>',
            '⏪': '<i data-lucide="rewind" class="w-6 h-6"></i>',
            '📊': '<i data-lucide="bar-chart-2" class="w-4 h-4 inline"></i>',
            '📦': '<i data-lucide="package" class="w-4 h-4 inline"></i>',
            '↻': '<i data-lucide="refresh-cw" class="w-4 h-4 inline"></i>',
            '✅': '<i data-lucide="check-circle" class="w-12 h-12"></i>',
            '🎉': '<i data-lucide="party-popper" class="w-12 h-12"></i>',
            '🔒': '<i data-lucide="lock" class="w-10 h-10"></i>',
            '⚠️': '<i data-lucide="alert-triangle" class="w-10 h-10"></i>',
            '🖼️': '<i data-lucide="image" class="w-12 h-12"></i>',
        }
        for emoji, svg in replacements.items():
            content = content.replace(emoji, svg)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

for root, _, files in os.walk('app'):
    for file in files:
        if file.endswith(('.html', '.py')):
            clean_file(os.path.join(root, file))

# Fix the main python file
clean_file('app/main.py')
