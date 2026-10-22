"""Assemble finished clips into the music video, from a project.json.

    python3 assemble.py project.json --clips clips --out cut.mp4

- Cuts snap to the start of the nearest sung line (lyric-timing.json) a quarter second early.
- For each shot the newest version wins: clips/shot07-7A-v3.mp4 beats -v2 beats the plain file.
  (Files are looked up by label: <label>.mp4, or anything ending -<label>[-vN].mp4.)
- A shot's "speed" (e.g. 0.6) plays that clip slower. Short clips are slowed to fit; long ones trimmed. Never looped.
- Missing clips show as black and are listed at the end.
"""
import argparse, glob, json, os, re, subprocess, sys, tempfile
FPS, W, H = 24, 1920, 1080

def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: sys.exit('ffmpeg failed:\n' + ' '.join(c) + '\n' + r.stderr[-1500:])
    return r.stdout
def sec(t):
    m, s = t.split(':'); return int(m) * 60 + float(s)
def length(p):
    return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',p]).strip())
def newest(folder, label):
    c = glob.glob(os.path.join(folder, f'{label}.mp4')) + glob.glob(os.path.join(folder, f'*-{label}.mp4')) + glob.glob(os.path.join(folder, f'*-{label}-v*.mp4'))
    def ver(p):
        m = re.search(r'-v(\d+)\.mp4$', p); return int(m.group(1)) if m else 1
    return max(c, key=ver) if c else None

ap = argparse.ArgumentParser()
ap.add_argument('project'); ap.add_argument('--clips', default='clips')
ap.add_argument('--timing', default='lyric-timing.json'); ap.add_argument('--out', default='cut.mp4')
a = ap.parse_args()
P = json.load(open(a.project, encoding='utf-8'))
shots = sorted(P['shots'], key=lambda s: s['n'])
cuts = [sec(shots[0]['start'])] + [sec(s['start']) for s in shots[1:]] + [sec(shots[-1]['end'])]
if os.path.exists(a.timing):
    starts = [l['start'] for l in json.load(open(a.timing))['lines']]
    for i in range(1, len(cuts) - 1):
        near = min(starts, key=lambda x: abs(x - cuts[i]))
        if abs(near - cuts[i]) <= P.get('snap', 0.8):
            cuts[i] = max(near - P.get('lead', 0.25), cuts[i-1] + 1.0)
tmp = tempfile.mkdtemp(); parts = []; missing = []; slowed = []
for i, s in enumerate(shots):
    dur = cuts[i+1] - cuts[i]; out = os.path.join(tmp, f'{s["n"]:03d}.mp4'); src = newest(a.clips, s['label'])
    vf = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p'
    if not src:
        missing.append(s['label']); run(['ffmpeg','-y','-v','error','-f','lavfi','-i',f'color=black:s={W}x{H}:r={FPS}','-t',f'{dur:.3f}','-c:v','libx264',out])
    else:
        speed = s.get('speed', 1.0); L = length(src)
        if speed == 1.0 and L < dur: speed = L / dur
        if speed != 1.0: slowed.append((s['n'], s['label'], round(speed*100)))
        run(['ffmpeg','-y','-v','error','-i',src,'-an','-vf',f'setpts=PTS/{speed},{vf}','-t',f'{dur:.3f}','-c:v','libx264','-crf','16',out])
    parts.append(out)
lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
song = P['song']
run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',lst,'-i',song,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-shortest',a.out])
print('Done:', a.out); print('Slowed:', slowed); print('Missing:', missing)
