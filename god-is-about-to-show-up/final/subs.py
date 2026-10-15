import json
d = json.load(open('timing/timing/god-is-about-to-show-up.json')); d = d.get('data', d)
L = sorted(d['lines'], key=lambda l: l['start'])

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,Inter Medium,64,&H00FFFFFF,&H00FFFFFF,&H00141414,&HA0000000,0,0,0,0,100,100,1,0,1,3.2,2.5,2,120,120,78,1
Style: Title,Inter,96,&H00E6F4FF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,3,0,1,2.2,3,5,100,100,0,1
Style: Sub,Inter,52,&H00BFE3F5,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,6,0,1,1.8,2,5,100,100,0,1
Style: Credit,Inter,44,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,2,0,1,1.4,1.5,5,100,100,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
for i, l in enumerate(L):
    a = l['start']
    nxt = L[i + 1]['start'] if i + 1 < len(L) else a + 5
    b = min(nxt - 0.05, l['end'] if l.get('end') else 1e9, a + 7.0)
    ev.append(f"Dialogue: 0,{ts(a - 0.1)},{ts(b)},Lyric,,0,0,0,,{{\\fad(180,220)\\blur0.6}}{l['text']}")

# opening title over the moon intro
ev.append("Dialogue: 0,0:00:02.50,0:00:09.50,Title,,0,0,0,,{\\fad(1200,1200)\\pos(640,300)}God Is About to Show Up")
ev.append("Dialogue: 0,0:00:03.20,0:00:09.50,Sub,,0,0,0,,{\\fad(1200,1200)\\pos(640,385)}DIVINE ENSEMBLE")
# end card
E = 332.0
cr = [("Title", "God Is About to Show Up", 420, 0.0), ("Sub", "DIVINE ENSEMBLE", 520, 0.4),
      ("Credit", "Songwriter  Michael Bowman", 630, 1.0), ("Credit", "Producer  Edward Liu", 690, 1.3),
      ("Credit", "Production  Dazadi Music", 750, 1.6), ("Sub", "dazadi.org", 850, 2.0)]
for st, t, y, dl in cr:
    ev.append(f"Dialogue: 1,{ts(E + dl)},{ts(E + 8.5)},{st},,0,0,0,,{{\\fad(900,900)\\pos(960,{y})}}{t}")
open('lyrics.ass', 'w').write(hdr + "\n".join(ev) + "\n")
print(len(ev))
