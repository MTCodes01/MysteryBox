import os, re

def update_theme_modern(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Backgrounds
    content = content.replace('bg-[#140b0b]', 'bg-zinc-950')
    content = content.replace('bg-[radial-gradient(rgba(220,38,38,0.15)_3px,transparent_3px)] [background-size:24px_24px]', 'bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-zinc-900 via-zinc-950 to-zinc-950')
    
    # 2. Glassmorphism cards & headers
    content = content.replace('bg-[#1c0f0f]/80 shadow-lg border-b border-red-900/30 shadow-black/20', 'bg-zinc-900/60 backdrop-blur-xl border-b border-white/5 shadow-xl shadow-black/50')
    content = content.replace('bg-[#1c0f0f] shadow-xl shadow-black/40 border-red-900/30', 'bg-zinc-900/60 backdrop-blur-xl shadow-2xl shadow-black/50 border border-white/5')
    
    # 3. Text Colors (gray to zinc for cooler tone)
    content = content.replace('text-gray-100', 'text-zinc-100')
    content = content.replace('text-gray-300', 'text-zinc-300')
    content = content.replace('text-gray-400', 'text-zinc-400')
    content = content.replace('text-gray-900', 'text-zinc-900')
    
    # 4. Red replacements (backgrounds, borders)
    content = content.replace('bg-red-950/40', 'bg-white/5')
    content = content.replace('bg-red-900/30', 'bg-white/10')
    content = content.replace('bg-red-900/40', 'bg-white/10')
    content = content.replace('bg-red-800', 'bg-indigo-500')
    
    content = content.replace('border-red-900/50', 'border-white/10')
    content = content.replace('border-red-900/70', 'border-white/20')
    content = content.replace('border-red-200', 'border-white/20')
    
    # 5. Hovers
    content = content.replace('hover:bg-red-900/50', 'hover:bg-white/10 hover:scale-[1.02] transition-all')
    content = content.replace('hover:bg-red-900/30', 'hover:bg-white/5 hover:scale-[1.02] transition-all')
    content = content.replace('hover:bg-red-100', 'hover:bg-white/10 hover:scale-[1.02] transition-all')
    content = content.replace('hover:border-red-700/50', 'hover:border-indigo-500/50')
    
    # 6. Text Red Accents
    content = content.replace('text-red-400', 'text-indigo-400')
    content = content.replace('text-red-500', 'text-indigo-400')
    content = content.replace('text-red-600', 'text-indigo-400')
    
    # 7. Forms and Actions
    content = content.replace('accent-red-500', 'accent-indigo-500')
    content = content.replace('accent-red-600', 'accent-indigo-500')
    content = content.replace('bg-red-600 hover:bg-red-500', 'bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 shadow-lg shadow-indigo-500/25')
    content = content.replace('bg-red-500', 'bg-indigo-500')
    content = content.replace('from-red-500 to-red-700', 'from-indigo-500 to-violet-600')
    
    # 8. Typography update
    content = content.replace('family=Press+Start+2P&family=Inter:wght@400;500;600;700;800', 'family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800')
    content = content.replace('font-["Press_Start_2P"]', 'font-[\'Outfit\'] font-bold tracking-tight')
    
    # 9. Colors tailwind config
    content = content.replace("brand: { DEFAULT: '#dc2626', light: '#ef4444', dark: '#b91c1c' }", "brand: { DEFAULT: '#6366f1', light: '#818cf8', dark: '#4f46e5' }")

    # 10. Specific fix for border / hover bg in upload drop zone
    content = content.replace('border-color: #dc2626;', 'border-color: #6366f1;')
    content = content.replace('background: rgba(220,38,38,0.1);', 'background: rgba(99,102,241,0.1);')

    # Remove extra tracking-tight duplicate if any
    content = content.replace('tracking-tight tracking-tight', 'tracking-tight')
    content = content.replace('font-[\'Outfit\'] font-bold tracking-tight text-xl', 'font-[\'Outfit\'] font-bold tracking-tight text-2xl')

    # Add rounded-2xl to cards if they don't have it (they should)
    
    # Fix dark gray backgrounds
    content = content.replace('bg-black', 'bg-zinc-950/50')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filename}')

update_theme_modern('d:/VScode/MysteryBox/app/static/participant.html')
update_theme_modern('d:/VScode/MysteryBox/app/static/host.html')
