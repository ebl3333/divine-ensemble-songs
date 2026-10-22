# Divine Ensemble Video Kit

The recipe we used for "Jesus Savior Redeemer Friend" (54 shots, 6:32), ready for the next song.
Tell Claude: **"Make the next video with the video kit"** and attach the song, lyrics and timing.

## The steps (Claude does all of them)
1. **Plan.** Lyric timing -> shot list (one shot per line or two, 4-9 seconds each, instrumental breaks slow). Every shot = a Bible scene + camera + how it ends + mood. Save as SHOT-LIST.md and project.json (copy project.example.json).
2. **Character sheets.** One sheet per recurring person (Yeshua, John, Peter, healed man, etc.) in Higgsfield. They keep faces and clothes the same.
3. **First frames.** Higgsfield `gpt_image_2_5`, 16:9, with the character sheets as references. About 8 at a time (it rate-limits).
4. **Clips.** `ltx.py` builds the prompt; the clip is made by LTX (`ltx-2-5-pro`, 1920x1080, 24 fps, no audio, 6 or 8 s, about 4 minutes each).
5. **Save.** Botty downloads each clip into `clips/` in this repo as `shotNN-<label>.mp4` (`-v2`, `-v3` for redos).
6. **Look.** Claude samples 4 frames from every clip and checks them against the rules below before showing Ed.
7. **Cut.** `assemble.py` joins the newest clip of every shot, snaps cuts to the lyrics, lays the song under it.
8. **Words.** `subs.py` makes lyrics, title and end credits; ffmpeg burns them in. Send Ed a 720p review copy first.
9. **Fix.** Ed names shot numbers; Claude redoes only those (new frame, new clip, new cut). Nothing is posted until Ed approves.

## Commands (run inside this folder, or let Claude run them)
    python3 ltx.py project.json --shot 20 --view far --image "<frame url>" --moment "<what happens>" --mood "awe"
    python3 assemble.py project.json --clips clips --timing lyric-timing.json --out cut.mp4
    python3 subs.py project.json lyric-timing.json lyrics.ass
    ffmpeg -i cut.mp4 -vf "ass=lyrics.ass" -c:v libx264 -crf 20 -c:a copy final.mp4
    ffmpeg -i final.mp4 -vf scale=1280:720 -c:v libx264 -crf 26 -c:a aac review-720p.mp4

## Standing rules (Ed's, learned the hard way)
- **Biblical accuracy first.** Real scenes, real clothing: undyed wool, tassels (Num 15:38), hair and beard untrimmed (Lev 19:27). No modern items, no European look (watch buildings: no white-block Greek-island towns).
- **Yeshua's face is shown on a plan:** across the song his view slowly turns from his back, to his side, to (only when asked) facing. Never looking straight into the camera unless Ed asks. Words in the prompt: far / turning / glimpse / half / profile / facing.
- **Make the main action obvious.** If a viewer can't tell what happened (wine poured into a cup, a boy alive again, who is Jesus next to Bartimaeus) it gets redone. Put Yeshua beside the person so he is recognisable, taller than everyone.
- **No nudity, no bare torsos** (the boy raised from the dead wears a tunic). No clothing at the riverbank/baptism; no cloth in the water.
- **Realistic.** Natural warm light, real skin, no plastic look, no film grain, no vignette, no text in frame, no black bars.
- **Slow, gentle motion.** Instrumentals filmed slow and played at 60-75%. Use `speed` in project.json for a clip that moves too fast (shot 30 played at 0.6).
- **Crowds stay behind or beside** the main people, never walking across in front of them.
- **Distance when asked:** "far away" means a tiny figure; put the reactions of the people in the foreground (shot 20: Ed rejected two close versions of Jesus on the water).
- **Dead bodies are refused by the image model** ("nsfw"): show the moment of sitting up alive, burial linen slipping.
- **Credits:** Lyrics (writer), Producer Edward Liu, Production Dazadi Music, dazadi.org. This song: Lyrics Jay Michael Bowman. Put the credits of each new song in project.json.

## Limits and costs
- LTX: 75 submits per 24 hours (failed ones count). About $1.02 per 6 s clip, $1.36 per 8 s. Check the balance before a big batch.
- Higgsfield: submit about 8 frames at a time.
- A 54-shot first pass is about $65-75 and about 6 hours of Claude's working time, plus redos.
