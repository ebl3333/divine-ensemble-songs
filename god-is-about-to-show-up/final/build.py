import json, subprocess, os, sys
FPS = 24
N = 'repo/god-is-about-to-show-up/clips/'
O = 'old/clips/'
AUDIO = 'audio/assets/audio/show-up/11-god-is-about-to-show-up.mp3'
SONG_END = 331.807

# (start, end, file, in_point, extra)
S = [
 (0.0, 16.0, O+'A1v2', 0.0, {'moon': True}),
 (16.0, 19.9, N+'A2', 0.0, {}),
 (19.9, 24.5, N+'B1', 0.0, {}),
 (24.5, 29.3, O+'B2v2', 0.5, {}),
 (29.3, 33.3, O+'B3v2', 2.0, {}),
 (33.3, 37.4, N+'C1', 0.6, {}),
 (37.4, 41.3, N+'C2', 0.0, {}),
 (41.3, 45.4, N+'C3', 1.2, {}),
 (45.4, 49.3, N+'C4', 0.0, {}),
 (49.3, 52.7, N+'D1a', 1.6, {}),
 (52.7, 56.6, N+'D2', 1.0, {}),
 (56.6, 60.7, N+'D3a', 1.0, {}),
 (60.7, 65.4, N+'D4', 0.0, {}),
 (65.4, 69.9, O+'05', 2.0, {}),
 (69.9, 77.3, N+'E2', 0.0, {}),
 (77.3, 81.3, N+'F1', 0.8, {}),
 (81.3, 85.5, N+'F2', 0.0, {}),
 (85.5, 90.0, N+'F3', 0.8, {}),
 (90.0, 94.2, N+'F4', 0.6, {}),
 (94.2, 98.5, N+'G1', 0.6, {}),
 (98.5, 102.4, N+'G2', 0.0, {}),
 (102.4, 106.6, N+'G3', 0.0, {}),
 (106.6, 110.5, N+'G4', 0.6, {}),
 (110.5, 113.9, N+'D1b', 1.8, {}),
 (113.9, 118.0, O+'B3v2', 2.0, {}),
 (118.0, 122.1, O+'11', 0.3, {}),
 (122.1, 126.5, N+'D4', 1.6, {}),
 (126.5, 131.1, N+'H1', 0.8, {}),
 (131.1, 136.6, N+'H2', 0.0, {}),
 (136.6, 140.4, N+'I1', 0.6, {}),
 (140.4, 144.4, N+'I2', 0.4, {}),
 (144.4, 148.4, N+'I3', 1.0, {}),
 (148.4, 152.7, N+'I4', 0.0, {}),
 (152.7, 156.8, N+'D1c', 0.0, {}),
 (156.8, 160.8, N+'B1', 1.0, {}),
 (160.8, 164.8, N+'D3b', 1.6, {}),
 (164.8, 169.2, N+'D4', 1.6, {}),
 (169.2, 173.9, N+'J1', 0.4, {}),
 (173.9, 181.2, N+'J2', 0.0, {}),
 (181.2, 184.7, N+'J3', 0.0, {}),
 (184.7, 188.8, N+'J4a', 0.4, {}),
 (188.8, 193.9, N+'J5', 0.0, {}),
 (193.9, 199.5, N+'J6', 0.0, {}),
 (199.5, 209.5, O+'02', 0.0, {}),
 (209.5, 219.5, O+'03', 0.0, {}),
 (219.5, 229.5, O+'09a', 0.0, {}),
 (229.5, 233.8, N+'J4b', 1.2, {}),
 (233.8, 238.1, N+'J5', 1.5, {}),
 (238.1, 242.1, N+'D3a', 2.0, {}),
 (242.1, 246.1, N+'D4', 2.0, {}),
 (246.1, 250.2, N+'G1', 1.9, {}),
 (250.2, 252.3, N+'D2', 3.0, {}),
 (252.3, 254.4, N+'D1c', 3.0, {}),
 (254.4, 256.3, N+'D3b', 3.5, {}),
 (256.3, 258.2, N+'D1c', 1.0, {}),
 (258.2, 260.7, N+'D4', 3.5, {}),
 (260.7, 263.3, N+'D1b', 3.4, {}),
 (263.3, 267.5, N+'J1', 1.8, {}),
 (267.5, 274.9, N+'J2', 0.0, {}),
 (274.9, 278.5, N+'J3', 2.4, {}),
 (278.5, 282.4, N+'B1', 2.1, {}),
 (282.4, 287.5, N+'J5', 0.9, {}),
 (287.5, 293.0, N+'J6', 0.5, {}),
 (293.0, 300.6, N+'C4', 0.0, {}),
 (300.6, 308.2, O+'16', 0.0, {}),
 (308.2, 315.9, O+'12', 0.0, {}),
 (315.9, 323.6, O+'15', 0.3, {}),
 (323.6, 327.3, N+'J3', 2.6, {}),
 (327.3, SONG_END, O+'18', 3.2, {}),
]

def dur(f):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))

def frames(t): return round(t * FPS)

os.makedirs('seg', exist_ok=True)
only = set(sys.argv[1:])
lst = []
for i, (a, b, f, tin, x) in enumerate(S):
    src = f + '.mp4'
    nfr = frames(b) - frames(a)
    slot = nfr / FPS
    out = f'seg/{i:02d}.mp4'
    lst.append(out)
    if only and str(i) not in only and not (only == {'all'}):
        if os.path.exists(out): continue
    avail = dur(src) - tin - 0.05
    if x.get('moon'):
        # play at 0.7x to 11.5s, then slow push in on the moon
        play = 11.5
        sp = (avail) / play
        zoom = f"zoompan=z='if(lt(on,{int(play*FPS)}),1,1+0.9*pow((on-{int(play*FPS)})/{nfr-int(play*FPS)},1.5))':x='(iw-iw/zoom)*0.43':y='(ih-ih/zoom)*0.25':d=1:s=1920x1080:fps={FPS}"
        vf = f"trim=start={tin},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=1920:1080,tpad=stop_mode=clone:stop={nfr},{zoom},trim=end_frame={nfr}"
    else:
        sp = min(1.0, avail / slot)
        vf = f"trim=start={tin},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,tpad=stop_mode=clone:stop={nfr},trim=end_frame={nfr}"
    vf += ",setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','16','-r',str(FPS),out], check=True)
    print(i, f, round(slot,2), 'speed', round(sp,2), flush=True)

with open('seg/list.txt','w') as fh:
    for p in lst: fh.write(f"file '{os.path.basename(p)}'\n")
