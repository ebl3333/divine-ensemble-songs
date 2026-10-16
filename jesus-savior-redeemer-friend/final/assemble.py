"""Jesus Savior Redeemer Friend — assemble the finished LTX clips into one music video.

How to run (from inside the jesus-savior-redeemer-friend folder):

    python3 final/assemble.py --clips clips --song final/song.mp3 --out final/Jesus-Savior-Redeemer-Friend.mp4

What it does:
1. Reads the 54 shots and their times from SHOT-LIST.md.
2. Moves each cut onto the exact start of the nearest sung line in final/lyric-timing.json
   (a quarter-second early, so the picture lands with the first word).
3. Takes the clip for each shot (named by its label, e.g. clips/1B.mp4, clips/W1.mp4)
   and fits it to its slot: a longer clip is trimmed, a shorter clip is gently slowed.
   No clip is ever repeated or looped.
4. Joins all shots in order, lays the song underneath, and writes one 1920x1080, 24 fps video.

Any clip that is not made yet is shown as a black gap, and listed at the end, so you can
preview the cut while clips are still being generated.
"""
import argparse, json, os, re, subprocess, sys, tempfile

FPS, W, H = 24, 1920, 1080
LEAD = 0.25    # cut this many seconds before a sung line starts
SNAP = 0.8     # only move a cut onto a lyric line if it is this close

# Shot number -> clip label in prompts/scenes-ltx-style.md
SHOT_CLIPS = {
    1: '1B',  2: '2A',  3: '3A',  4: '5A',  5: '5B',  6: 'W1',  7: '7A',  8: '7B',
    9: '6A', 10: '13A', 11: '8A', 12: '9A', 13: '10A', 14: '14A', 15: 'W2', 16: '25A',
    17: '15A', 18: '16A', 19: '26A', 20: '4A', 21: '11C', 22: '11A', 23: '12B', 24: '23A',
    25: '23B', 26: 'W3', 27: '17A', 28: '18A', 29: '19A', 30: '19B', 31: '21A', 32: '20A',
    33: '22A', 34: '25B', 35: '13B', 36: '8B', 37: '9B', 38: '10B', 39: '24A', 40: '2B',
    41: 'W4', 42: '16B', 43: '15B', 44: 'W5', 45: '3B', 46: '6B', 47: '11B', 48: 'W6',
    49: '20B', 50: '22B', 51: '21B', 52: '12A', 53: '24B', 54: '18B',
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('ffmpeg failed:\n' + ' '.join(cmd) + '\n' + r.stderr[-2000:])
    return r.stdout


def seconds(mmss):
    m, s = mmss.split(':')
    return int(m) * 60 + float(s)


def read_shots(path):
    shots = []
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\|\s*(\d+)\s*\|\s*(\d+:\d\d)\s*[–-]\s*(\d+:\d\d)\s*\|', line)
        if m:
            shots.append((int(m.group(1)), seconds(m.group(2)), seconds(m.group(3))))
    shots.sort()
    if [n for n, _, _ in shots] != list(range(1, len(shots) + 1)):
        sys.exit('SHOT-LIST.md shot numbers are not 1, 2, 3 ... in order')
    return shots


def snap_cuts(shots, timing_path):
    starts = [l['start'] for l in json.load(open(timing_path, encoding='utf-8'))['lines']]
    cuts = [shots[0][1]] + [s for _, s, _ in shots[1:]] + [shots[-1][2]]
    for i in range(1, len(cuts) - 1):
        near = min(starts, key=lambda x: abs(x - cuts[i]))
        if abs(near - cuts[i]) <= SNAP:
            cuts[i] = max(near - LEAD, cuts[i - 1] + 1.0)
    return cuts


def clip_length(path):
    out = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
               '-of', 'default=nw=1:nk=1', path])
    return float(out.strip())


def find_clip(folder, label):
    for ext in ('.mp4', '.mov', '.webm'):
        p = os.path.join(folder, label + ext)
        if os.path.exists(p):
            return p
    return None


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument('--clips', default=os.path.join(here, 'clips'))
    ap.add_argument('--song', required=True, help='the song audio file (mp3, wav, m4a)')
    ap.add_argument('--out', default=os.path.join(here, 'final', 'Jesus-Savior-Redeemer-Friend.mp4'))
    ap.add_argument('--shots', default=os.path.join(here, 'SHOT-LIST.md'))
    ap.add_argument('--timing', default=os.path.join(here, 'final', 'lyric-timing.json'))
    a = ap.parse_args()

    shots = read_shots(a.shots)
    cuts = snap_cuts(shots, a.timing)
    song_len = clip_length(a.song)
    cuts[-1] = min(cuts[-1], song_len)

    missing, slowed = [], []
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, (n, _, _) in enumerate(shots):
            dur = round(cuts[i + 1] - cuts[i], 3)
            label = SHOT_CLIPS[n]
            src = find_clip(a.clips, label)
            part = os.path.join(tmp, f'{n:02d}.mp4')
            look = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p'
            if src is None:
                missing.append(f'shot {n} needs {label}')
                run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
                     f'color=black:s={W}x{H}:r={FPS}:d={dur}', '-c:v', 'libx264', '-crf', '18', part])
            else:
                length = clip_length(src)
                speed = 1.0
                if length < dur:
                    speed = length / dur
                    slowed.append(f'shot {n} ({label}) plays at {speed:.0%} speed')
                vf = f'setpts=PTS/{speed},{look},trim=duration={dur},setpts=PTS-STARTPTS'
                run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-an', '-vf', vf,
                     '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', part])
            parts.append(part)

        listing = os.path.join(tmp, 'list.txt')
        with open(listing, 'w') as f:
            f.writelines(f"file '{p}'\n" for p in parts)
        video = os.path.join(tmp, 'video.mp4')
        run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listing, '-c', 'copy', video])

        start = cuts[0]
        total = cuts[-1] - start
        run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-ss', str(start), '-i', a.song,
             '-map', '0:v', '-map', '1:a', '-t', str(total), '-c:v', 'copy',
             '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', a.out])

    print(f'Done: {a.out}  ({total:.1f} seconds, {len(shots)} shots)')
    if slowed:
        print('Slowed to fit their slot:\n  ' + '\n  '.join(slowed))
    if missing:
        print('Clips not made yet (shown as black):\n  ' + '\n  '.join(missing))


if __name__ == '__main__':
    main()
