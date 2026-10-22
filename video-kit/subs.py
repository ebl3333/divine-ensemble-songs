"""Write lyrics.ass (lyrics, opening title, end credits) from project.json + lyric-timing.json.

    python3 subs.py project.json lyric-timing.json lyrics.ass
    ffmpeg -i cut.mp4 -vf "ass=lyrics.ass" -c:v libx264 -crf 20 -c:a copy final.mp4
"""
import json, sys
proj, timing, out = sys.argv[1:4]
P = json.load(open(proj, encoding='utf-8')); L = sorted(json.load(open(timing))['lines'], key=lambda l: l['start'])
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h}:{m:02d}:{s:05.2f}'
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Lyric,Inter Medium,64,&H00FFFFFF,&H00FFFFFF,&H00141414,&HA0000000,0,0,0,0,100,100,1,0,1,3.2,2.5,2,120,120,78,1
Style: Title,Inter,92,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,2,2,5,100,100,0,1
Style: Sub,Inter,40,&H00E8E8E8,&H00E8E8E8,&H00101010,&H96000000,0,0,0,0,100,100,8,0,1,1.4,1.5,5,100,100,0,1
Style: Credit,Inter,44,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,1.4,1.5,5,100,100,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
ev = []
for i, l in enumerate(L):
    end = l['end'] or min((L[i+1]['start'] if i+1 < len(L) else l['start'] + 5), l['start'] + 6)
    ev.append(f"Dialogue: 0,{ts(l['start'])},{ts(end)},Lyric,,0,0,0,,{{\\fad(200,250)}}{l['text']}")
ev.append(f"Dialogue: 0,{ts(1)},{ts(8.2)},Title,,0,0,0,,{{\\fad(1200,900)\\pos(960,470)}}{P['title']}")
ev.append(f"Dialogue: 0,{ts(1.8)},{ts(8.2)},Sub,,0,0,0,,{{\\fad(1200,900)\\pos(960,570)}}{P['artist']}")
last = max(l['end'] or l['start'] + 4 for l in L) + 1.3; total = max(l['start'] for l in L) + 18
rows = [("Title", P['title'], 420, 0), ("Sub", P['artist'], 520, .4)] + [("Credit", c, 640 + 60*i, 1 + .3*i) for i, c in enumerate(P['credits'])]
rows.append(("Sub", P.get('footer', ''), 640 + 60*len(P['credits']) + 100, 2))
for st, t, y, dl in rows:
    ev.append(f"Dialogue: 1,{ts(last + dl)},{ts(total)},{st},,0,0,0,,{{\\fad(900,1200)\\pos(960,{y})}}{t}")
open(out, 'w').write(hdr + "\n".join(ev) + "\n"); print(len(ev), 'events ->', out)
