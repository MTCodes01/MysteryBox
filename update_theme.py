import os, re

def update_theme(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # HTML
    content = content.replace('class="dark"', '')

    # Fonts
    if 'Press+Start+2P' not in content:
        content = content.replace('family=Inter', 'family=Press+Start+2P&family=Inter')

    # Tailwind config
    content = content.replace("brand: { DEFAULT: '#7c3aed', light: '#a78bfa', dark: '#5b21b6' }",
                              "brand: { DEFAULT: '#dc2626', light: '#ef4444', dark: '#b91c1c' }")

    # Body
    content = content.replace('bg-gray-950 text-gray-100', 'bg-[#fcf5f5] text-gray-900 bg-[radial-gradient(#f4d6d6_3px,transparent_3px)] [background-size:24px_24px]')

    # Text colors
    content = content.replace('text-gray-400', 'text-gray-500')
    content = content.replace('text-gray-300', 'text-gray-700')
    content = content.replace('text-gray-100', 'text-gray-900')
    
    # Backgrounds & Borders
    content = content.replace('bg-gray-900/80', 'bg-white/80 shadow-sm border-b-0 shadow-red-900/5')
    content = content.replace('bg-gray-900', 'bg-white shadow-xl shadow-red-900/5 border-red-100')
    content = content.replace('border-gray-800', 'border-red-100')
    content = content.replace('border-gray-700', 'border-red-200')
    content = content.replace('bg-gray-800/60', 'bg-red-50/60')
    content = content.replace('bg-gray-800', 'bg-red-50')
    content = content.replace('hover:bg-gray-800', 'hover:bg-red-100')
    content = content.replace('hover:border-gray-600', 'hover:border-red-300')
    
    # Header icons
    content = content.replace('bg-gray-600', 'bg-red-200')
    content = content.replace('hover:bg-gray-700', 'hover:bg-red-100')
    
    # Violet to Red
    content = content.replace('from-violet-600', 'from-red-500')
    content = content.replace('to-purple-800', 'to-red-700')
    content = content.replace('text-violet-400', 'text-red-600')
    content = content.replace('text-violet-300', 'text-red-500')
    content = content.replace('bg-violet-900/40', 'bg-red-100')
    content = content.replace('bg-violet-900/30', 'bg-red-50')
    content = content.replace('border-violet-700/40', 'border-red-200')
    content = content.replace('border-violet-700/60', 'border-red-200')
    content = content.replace('accent-violet-500', 'accent-red-600')
    content = content.replace('hover:border-violet-600', 'hover:border-red-500')
    content = content.replace('hover:bg-violet-950/20', 'hover:bg-red-50')
    content = content.replace('bg-violet-600', 'bg-red-600')
    content = content.replace('hover:bg-violet-500', 'hover:bg-red-500')
    content = content.replace('bg-violet-900/60', 'bg-red-100')
    content = content.replace('border-violet-700/50', 'border-red-200')
    content = content.replace('bg-violet-500', 'bg-red-500')
    
    content = content.replace('bg-violet-900/50', 'bg-red-100')
    
    content = content.replace('text-white font-bold', 'text-white font-["Press_Start_2P"]')
    
    # Headings font
    content = content.replace('font-extrabold', 'font-["Press_Start_2P"] tracking-tight text-xl')

    # Remove some dark mode specific classes
    content = content.replace('bg-black', 'bg-gray-100')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filename}')

update_theme('d:/VScode/MysteryBox/app/static/participant.html')
update_theme('d:/VScode/MysteryBox/app/static/host.html')
