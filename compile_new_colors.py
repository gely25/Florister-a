import os
import re
import json

def compile_frames():
    d = 'framesdelcapullo'
    out = 'apps/accounts/static/accounts/js/flower-frames.js'
    
    files = [f for f in os.listdir(d) if f.lower().endswith('.svg')]
    def get_num(s):
        m = re.search(r'\d+', s)
        return int(m.group()) if m else 0
    
    files.sort(key=get_num)
    
    frames = []
    for f in files:
        with open(os.path.join(d, f), 'r', encoding='utf-8') as f_obj:
            content = f_obj.read().strip()
            # Restore to a slightly softer version of the original #FFCACA
            content = content.replace('#FFCACA', '#F2B8B8')
            # Make the borders stand out more (thicker and deep red/black)
            content = content.replace('stroke="black"', 'stroke="#36171E" stroke-width="2"')
            # Dark internal spaces to match the border
            content = content.replace('fill="black"', 'fill="#36171E"')
            frames.append(content)
    
    js_content = 'window.FLOWER_FRAMES = ' + json.dumps(frames) + ';'
    with open(out, 'w', encoding='utf-8') as f_out:
        f_out.write(js_content)

if __name__ == '__main__':
    compile_frames()
