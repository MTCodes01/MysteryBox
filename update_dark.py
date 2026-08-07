import os, re

def update_theme_dark(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Body background and grid pattern
    content = content.replace('bg-[#fcf5f5] text-gray-900 bg-[radial-gradient(#f4d6d6_3px,transparent_3px)]',
                              'bg-[#140b0b] text-gray-100 bg-[radial-gradient(rgba(220,38,38,0.15)_3px,transparent_3px)]')
    
    # Text colors
    content = content.replace('text-gray-900', 'text-gray-100')
    content = content.replace('text-gray-700', 'text-gray-300')
    content = content.replace('text-gray-500', 'text-gray-400')
    
    # Cards & Headers
    content = content.replace('bg-white/80 shadow-sm border-b-0 shadow-red-900/5', 'bg-[#1c0f0f]/80 shadow-lg border-b border-red-900/30 shadow-black/20')
    content = content.replace('bg-white shadow-xl shadow-red-900/5 border-red-100', 'bg-[#1c0f0f] shadow-xl shadow-black/40 border-red-900/30')
    
    # Background colors
    content = content.replace('bg-gray-100', 'bg-black')
    content = content.replace('bg-red-50/60', 'bg-red-950/40')
    content = content.replace('bg-red-50', 'bg-red-950/40')
    content = content.replace('bg-red-100', 'bg-red-900/30')
    content = content.replace('bg-red-200', 'bg-red-800')
    
    # Borders
    content = content.replace('border-red-100', 'border-red-900/50')
    content = content.replace('border-red-200', 'border-red-900/70')
    
    # Hovers
    content = content.replace('hover:bg-red-100', 'hover:bg-red-900/50')
    content = content.replace('hover:bg-red-50', 'hover:bg-red-900/30')
    content = content.replace('hover:border-red-300', 'hover:border-red-700/50')
    
    # Text colors
    content = content.replace('text-red-500', 'text-red-400')
    content = content.replace('text-red-600', 'text-red-400')
    
    # Accents
    content = content.replace('accent-red-600', 'accent-red-500')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filename}')

update_theme_dark('d:/VScode/MysteryBox/app/static/participant.html')
update_theme_dark('d:/VScode/MysteryBox/app/static/host.html')
