"""Build the LTX prompt for a shot and the ready-to-run database command that sends it.

    python3 ltx.py project.json --shot 20 --view half --seconds 8 \
        --image "https://....png" --moment "Night on the sea ... " --mood "awe"

Prints the full prompt and the one SQL command to run in the Supabase editor
(project cdrfarpwwqlmbdelxpsq). Claude can also run it for you. Rules baked in:
Yeshua's look is the same every shot; his face is only seen as far / turning / glimpse / half / profile
(or "facing" when asked); never looking at the camera; slow, gentle motion; the cost is about
$1.02 for 6 s and $1.36 for 8 s; the daily limit is 75 submits.
"""
import argparse, json
ap = argparse.ArgumentParser(); ap.add_argument('project')
ap.add_argument('--shot', required=True); ap.add_argument('--view', default='turning')
ap.add_argument('--seconds', type=int, default=8, choices=[6, 8, 10])
ap.add_argument('--image', required=True); ap.add_argument('--moment', required=True); ap.add_argument('--mood', default='warm')
a = ap.parse_args(); P = json.load(open(a.project, encoding='utf-8'))
prompt = (P['look'] + P['view_keys'][a.view] + P['slow'] + a.moment +
          f" Mood: {a.mood}, carried by the warm natural light, the slow movement and the faces of anyone near him." + P['avoid'])
q = lambda s: s.replace("'", "''")
sql = ("select net.http_post(url:='https://cdrfarpwwqlmbdelxpsq.supabase.co/functions/v1/ltx-bridge', "
       "headers:='{\"Content-Type\":\"application/json\"}'::jsonb, body:=jsonb_build_object('token',(select token from bridge_config where id=1),"
       "'mode','submit','kind','image-to-video','request',jsonb_build_object('model','ltx-2-5-pro','duration',%d,'resolution','1920x1080','fps',24,"
       "'generate_audio',false,'image_uri','%s','prompt','%s'))) as req_id;" % (a.seconds, q(a.image), q(prompt)))
print('PROMPT:\n' + prompt + '\n\nSQL:\n' + sql)
