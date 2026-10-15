"""God Is About to Show Up, v3 edit: beat-cut, effects, collages, unified grade."""
import json, subprocess, os, sys, bisect
FPS = 24
W, H = 1920, 1080
N = 'repo/god-is-about-to-show-up/clips/'
O = 'old/clips/'
D = 'repo/god-is-about-to-show-up/clips/dance/'
F = 'repo/god-is-about-to-show-up/clips/fire/'
SONG_END = 331.807
beats = json.load(open('beats.json'))['beats']

def T(t, lim=0.3):
    """snap a time to the nearest beat"""
    i = bisect.bisect_left(beats, t)
    c = [b for b in beats[max(0, i-1):i+1]]
    b = min(c, key=lambda x: abs(x - t)) if c else t
    return b if abs(b - t) <= lim else t

# helpers to describe shots
def c(f, tin=0.0, **o): return ('c', f, tin, o)
def g(layout, panels, **o): return ('g', layout, panels, o)

# timeline: (start, end, [shots]) – shots share the slot, split on bar lines
TL = [
 (0.0, 10.0, [c(O+'12', 0, slowmo=1, precrop='1440:808:240:136', bloom=.25)]),
 (10.0, 16.0, [c(F+'FH1', 1.0, bloom=.25)]),
 (16.0, 19.9, [c(N+'A2', 0, flash=1)]),
 (19.9, 24.5, [c(N+'B1', 0)]),
 (24.5, 29.3, [c(O+'B2v2', .5)]),
 (29.3, 33.3, [c(O+'B3v2', 2.0)]),
 (33.3, 37.4, [c(N+'C1', .6)]),
 (37.4, 41.3, [c(N+'C2', 0)]),
 (41.3, 45.4, [c(N+'C3', 1.2)]),
 (45.4, 49.3, [c(N+'C4', 0)]),
 # chorus 1
 (49.3, 52.7, [c(N+'D1a', 1.6, flash=1)]),
 (52.7, 56.6, [c(N+'D2', 1.0, flash=1), c(N+'D2', 3.2, zoom=1.2, punch=1)]),
 (56.6, 60.7, [c(N+'D3a', 1.0, flash=1), c(N+'D3b', 2.4, punch=1)]),
 (60.7, 65.4, [c(N+'D4', 0, bloom=.5, flash=1), g('4', [(N+'B1', 3.5), (N+'D2', 3.6), (N+'H1', 3.0), (N+'J5', 3.0)], flash=1)]),
 (65.4, 69.9, [c(O+'05', 2.0)]),
 (69.9, 77.3, [c(N+'E2', 0, bloom=.45), c(D+'DB3', 1.0, flash=1), g('3', [(N+'E2', 4.2), (N+'B1', 4.0), (N+'D2', 4.2)], flash=1)]),
 # verse 2
 (77.3, 81.3, [c(N+'F1', .8)]),
 (81.3, 85.5, [c(N+'F2', 0)]),
 (85.5, 90.0, [c(N+'F3', .8)]),
 (90.0, 94.2, [c(N+'F4', .6)]),
 (94.2, 98.5, [c(N+'G1', .6, bloom=.45)]),
 (98.5, 102.4, [c(N+'G2', 0), c(N+'G2', 3.2, bloom=.45, punch=1)]),
 (102.4, 106.6, [c(N+'G3', 0)]),
 (106.6, 110.5, [c(N+'G4', .6)]),
 # chorus 2
 (110.5, 113.9, [c(N+'D1b', 1.8, flash=1, bloom=.3)]),
 (113.9, 118.0, [c(O+'B3v2', 2.0, flash=1), c(O+'B3v2', 4.8, zoom=1.2, punch=1)]),
 (118.0, 122.1, [c(O+'11', 0.3, flash=1), c(N+'D3b', 3.0, punch=1)]),
 (122.1, 126.5, [g('4', [(N+'F2', 4.0), (N+'E2', 4.8), (N+'I4', 1.0), (N+'J1', 4.0)], flash=1), c(O+'15', 1.0, punch=1)]),
 (126.5, 131.1, [c(N+'H1', .8)]),
 (131.1, 136.6, [c(N+'H2', 0)]),
 (136.6, 140.4, [c(N+'I1', .6, bloom=.35)]),
 (140.4, 144.4, [c(N+'I2', .4)]),
 (144.4, 148.4, [c(N+'I3', 1.0)]),
 (148.4, 152.7, [c(N+'I4', 0)]),
 # chorus 3
 (152.7, 156.8, [c(N+'D1c', 0, flash=1)]),
 (156.8, 160.8, [c(N+'B1', 1.0, flash=1), c(N+'B1', 3.6, zoom=1.2, punch=1)]),
 (160.8, 164.8, [c(N+'D3b', 1.6, flash=1), c(N+'D3a', 3.6, punch=1)]),
 (164.8, 169.2, [g('3', [(N+'I4', 2.0), (N+'J5', 2.0), (N+'D2', 4.0)], flash=1), c(N+'D1c', 3.4, punch=1)]),
 (169.2, 173.9, [c(N+'J1', .4)]),
 (173.9, 181.2, [c(N+'J2', 0), c(N+'J2', 3.0, zoom=1.15, punch=1)]),
 (181.2, 184.7, [c(N+'J3', 0)]),
 (184.7, 188.8, [c(N+'J4a', .4)]),
 (188.8, 193.9, [c(N+'J5', 0)]),
 (193.9, 199.5, [c(N+'J6', 0)]),
 # music break 1 – dancing
 (199.5, 229.5, [c(D+'DA1', 0, flash=1), c(D+'DA2', 0, punch=1),
                 g('3', [(D+'DA3', 1.0), (D+'DA4', 1.0), (D+'DA1', 3.0)], flash=1),
                 c(D+'DA3', 2.5, punch=1), c(D+'DA4', 2.5, punch=1),
                 g('2', [(D+'DA1', 4.5), (D+'DA2', 4.5)], flash=1),
                 c(D+'DA4', 3.5, flash=1)]),
 (229.5, 233.8, [c(N+'J4b', 1.2, flash=1), c(O+'13', 2.0, punch=1)]),
 (233.8, 238.1, [c(N+'J5', 1.5, flash=1), c(N+'J5', 4.0, zoom=1.2, punch=1)]),
 (238.1, 242.1, [c(N+'D3a', 2.0, flash=1), c(O+'11', 4.0, punch=1)]),
 (242.1, 246.1, [g('4', [(D+'DA1', 2.0), (D+'DA2', 2.0), (D+'DB2', 2.0), (D+'DB4', 2.0)], flash=1), c(O+'06', 4.0, punch=1)]),
 (246.1, 250.2, [c(N+'G1', 3.0, bloom=.3)]),
 (250.2, 252.3, [c(N+'D2', 3.0, flash=1)]),
 (252.3, 254.4, [c(O+'02', 4.5, flash=1)]),
 (254.4, 256.3, [c(O+'01', 3.5, flash=1)]),
 (256.3, 258.2, [c(D+'DB4', 3.0, flash=1)]),
 (258.2, 260.7, [g('4', [(N+'B1', 4.0), (O+'B3v2', 5.0), (N+'J5', 4.0), (N+'H1', 4.0)], flash=1)]),
 (260.7, 263.3, [c(O+'16', 2.0, flash=1)]),
 (263.3, 267.5, [c(F+'FH2', 2.0)]),
 (267.5, 274.9, [c(O+'09a', 0.3)]),
 (274.9, 278.5, [c(O+'14', 2.0)]),
 (278.5, 282.4, [c(N+'B1', 2.1)]),
 (282.4, 287.5, [c(N+'J5', .9)]),
 (287.5, 293.0, [c(N+'J6', .5)]),
 # music break 2 – dancing
 (293.0, 323.6, [c(D+'DB1', 0, flash=1), c(D+'DB2', 0, punch=1),
                 g('3', [(D+'DB3', 1.0), (D+'DB4', 1.0), (D+'DB1', 3.0)], flash=1),
                 c(D+'DB3', 2.5, punch=1), c(D+'DB4', 2.5, punch=1),
                 g('4', [(D+'DA1', 3.0), (D+'DB2', 4.0), (D+'DA3', 4.0), (D+'DB3', 4.5)], flash=1),
                 c(D+'DB1', 4.0, punch=1)]),
 (323.6, 327.3, [c(N+'J3', 2.6)]),
 (327.3, SONG_END, [c(O+'18', 3.2, bloom=.3)]),
]

_dur = {}
def dur(f):
    if f not in _dur:
        _dur[f] = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f + '.mp4']))
    return _dur[f]

def fr(t): return round(t * FPS)

def src_chain(f, tin, nfr, pw, ph, zoom=1.0, slowmo=False, precrop=None):
    """trim, speed-fit and frame a clip to pw x ph"""
    slot = nfr / FPS
    avail = dur(f) - tin - 0.05
    sp = min(1.0, avail / slot)
    zc = f",crop=iw/{zoom}:ih/{zoom}" if zoom != 1.0 else ""
    pc = f"crop={precrop}," if precrop else ""
    mi = "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if slowmo else ""
    return (f"{pc}trim=start={tin},setpts=PTS-STARTPTS,{mi}setpts=PTS/{sp},fps={FPS}{zc},"
            f"scale={pw}:{ph}:force_original_aspect_ratio=increase,crop={pw}:{ph},"
            f"tpad=stop_mode=clone:stop={nfr},trim=end_frame={nfr},setsar=1"), sp

FX_ORDER = ['punch', 'slide', 'flash', 'focus', 'shake', 'flare']
def fx(o):
    e = o.get('fx')
    if e == 'punch':
        return f",scale=w='trunc({W}*(1+0.07*max(0,1-t/0.4))/2)*2':h=-2:eval=frame,crop={W}:{H}"
    if e == 'flash':
        return ",eq=brightness='0.30*max(0,1-t/0.22)':eval=frame"
    if e == 'slide':
        return f",scale=2304:1296,crop={W}:{H}:x='192*(1-pow(max(0,1-t/0.35),3))':y=108"
    if e == 'shake':
        return f",scale=2016:1134,crop={W}:{H}:x='48+40*sin(t*70)*max(0,1-t/0.5)':y='27+24*cos(t*55)*max(0,1-t/0.5)'"
    if e == 'focus':
        return ",split[fa][fb];[fb]gblur=sigma=26,format=yuva420p,fade=t=out:st=0:d=0.45:alpha=1[fc];[fa][fc]overlay"
    if e == 'flare':
        return (",split[fa][fb];[fb]colorbalance=rm=0.25:gm=0.12:bm=-0.15:rh=0.2:gh=0.1:bh=-0.1,eq=brightness=0.22,"
                "gblur=sigma=40,format=yuva420p,fade=t=out:st=0:d=0.5:alpha=1[fc];[fa][fc]overlay")
    return ""

def render(spec, nfr, out):
    kind = spec[0]
    if kind == 'c':
        _, f, tin, o = spec
        ch, sp = src_chain(f, tin, nfr, W, H, o.get('zoom', 1.0), o.get('slowmo', False), o.get('precrop'))
        inputs = ['-i', f + '.mp4']
        fg = f"[0:v]{ch}"
        if o.get('bloom'):
            b = o['bloom']
            fg += (f",format=gbrp,split[a][b];[b]eq=brightness=0.08:contrast=1.3,gblur=sigma=28[bl];"
                   f"[a][bl]blend=all_mode=screen:all_opacity={b}")
        fg += fx(o) + ",format=yuv420p[v]"
    else:
        _, layout, panels, o = spec
        gap = 8
        if layout == '2': pw, ph, grid = (W - gap) // 2, H, [(0, 0), ((W + gap) // 2, 0)]
        elif layout == '3': pw, ph, grid = (W - 2 * gap) // 3, H, [(0, 0), ((W - 2 * gap) // 3 + gap, 0), (2 * ((W - 2 * gap) // 3 + gap), 0)]
        else: pw, ph, grid = (W - gap) // 2, (H - gap) // 2, [(0, 0), ((W + gap) // 2, 0), (0, (H + gap) // 2), ((W + gap) // 2, (H + gap) // 2)]
        pw -= pw % 2; ph -= ph % 2
        inputs = []; fg = f"color=c=0x0b0f1e:s={W}x{H}:r={FPS}:d={nfr / FPS + 1},trim=end_frame={nfr}[bg0];"
        for k, (f, tin) in enumerate(panels):
            inputs += ['-i', f + '.mp4']
            ch, _ = src_chain(f, tin, nfr, pw, ph)
            fg += f"[{k}:v]{ch}[p{k}];"
        last = 'bg0'
        for k, (x, y) in enumerate(grid[:len(panels)]):
            # panels slide in one after another on the beat
            d = k * 0.12
            fg += f"[{last}][p{k}]overlay=x={x}:y={y}:enable='gte(t,{d})'[bg{k + 1}];"
            last = f'bg{k + 1}'
        fg += f"[{last}]null{fx(o)},format=yuv420p[v]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fg, '-map', '[v]', '-an',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-r', str(FPS), out], check=True)

def plan():
    segs = []
    for a, b, shots in TL:
        A = 0.0 if a == 0 else T(a)
        B = SONG_END if b == SONG_END else T(b)
        n = len(shots)
        if n == 1:
            cuts = [A, B]
        else:
            # split on bar lines (every 4 beats from A) as evenly as possible
            cuts = [A]
            for k in range(1, n):
                target = A + (B - A) * k / n
                ia = bisect.bisect_left(beats, A)
                cand = [beats[ia + 4 * m] for m in range(1, 40) if ia + 4 * m < len(beats) and beats[ia + 4 * m] < B - 0.5]
                cand += [beats[ia + 2 * m] for m in range(1, 80) if ia + 2 * m < len(beats) and beats[ia + 2 * m] < B - 0.5] if len(cand) < n - 1 else []
                pick = min(cand, key=lambda x: abs(x - target)) if cand else target
                if pick <= cuts[-1] + 0.4: pick = target
                cuts.append(pick)
            cuts.append(B)
        for k, s in enumerate(shots):
            segs.append((cuts[k], cuts[k + 1], s))
    # rotate a different beat effect onto every effect cut
    out, n = [], 0
    for a, b, s in segs:
        o = dict(s[-1])
        if o.pop('flash', None) or o.pop('punch', None):
            o['fx'] = FX_ORDER[n % len(FX_ORDER)]; n += 1
        out.append((a, b, s[:-1] + (o,)))
    return out

if __name__ == '__main__':
    os.makedirs('seg3', exist_ok=True)
    segs = plan()
    only = set(sys.argv[1:])
    names = []
    for i, (a, b, s) in enumerate(segs):
        nfr = fr(b) - fr(a)
        out = f'seg3/{i:03d}.mp4'; names.append(out)
        if only and str(i) not in only and os.path.exists(out): continue
        render(s, nfr, out)
        print(i, round(a, 2), round(b, 2), s[0], s[1] if s[0] == 'c' else s[1], flush=True)
    with open('seg3/list.txt', 'w') as fh:
        for p in names: fh.write(f"file '{os.path.basename(p)}'\n")
        fh.write("file 'zz_card.mp4'\n")
