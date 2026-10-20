"""Jesus Savior Redeemer Friend — script-only LTX prompts (no starting pictures).

Ed's direction (Oct 16, 2026):
- No pictures. LTX makes every clip from the written description alone.
- Oct 19, 2026: Yeshua's description rewritten to match the character sheet
  (references/01_Yeshua.png): long wavy hair, hooded rough-woven mantle with blue
  stripes and tzitzit, brown woven sash, ankle-length tunic; temples and beard edges
  never cut (Lev 19:27) but no modern curled sidelocks. Baptism: clothes laid aside,
  linen loincloth, rising from the water in prayer (Matt 3:16, Luke 3:21).
- Subtle: Yeshua is seen from behind, over the shoulder, or as a side silhouette.
  Never His full face or eyes; at most the edge of His cheek and beard.
- Don't tell the story. The camera simply witnesses one quiet moment from it,
  in gentle slow motion.
- Feeling comes from the other people's faces, hands and bodies, and from the light.

Run:  python3 prompts/build_script_only.py   -> writes prompts/scenes-ltx-script-only.md and .json
"""
import json, os

BODY = ("Yeshua, a first-century Galilean Jewish man in his early thirties, six feet tall and noticeably "
        "taller than those around him, lean and weathered with sun-tanned olive skin and calloused hands. "
        "Long dark brown wavy hair falling past his shoulders; full, natural dark beard. Following the "
        "Torah (Leviticus 19:27), the hair at his temples and the edges of his beard are never cut or "
        "trimmed: the side hair grows down freely and blends into his long hair and beard, with no "
        "separate curled sidelocks.")
CLOTHES = ("He wears an ankle-length undyed cream tunic of rough, coarse hand-woven linen, slightly frayed "
           "at the hem, tied at the waist with a wide brown woven sash whose long ends hang down the front; "
           "over it a large rough-woven cream mantle with two thin indigo-blue stripes near its edges, drawn "
           "up over his head as a hood and falling over his shoulders and arms, with blue-and-white knotted "
           "tassels (tzitzit) hanging from its four corners; worn brown leather strap sandals.")
LOOK = BODY + " " + CLOTHES
# How Yeshua is seen, coordinated across the whole song (Ed, Oct 19, 2026):
# a slow introduction that turns from His back to His side.
VIEW = {
 "back":    "We see him only from behind: his back, hooded head and shoulders; his face is never seen.",
 "turning": ("We see him from behind and slightly to one side, over his shoulder: at most the edge of his "
             "beard and hood; his face stays turned away."),
 "half":    ("We see him from the side and slightly behind: the edge of his cheek and the line of his nose and "
             "beard in soft shadow under his hood; never his full face, never his eyes looking at us."),
 "profile": ("We see him in side profile: forehead, nose, beard and hood outlined in warm light, his eyes "
             "looking ahead, never toward the camera; never seen from the front."),
 "far":     "He is seen small and far away; his face is not visible.",
 "glimpse": "Only part of him is seen, a hand, a sleeve, a tassel or a distant figure; his face is not visible.",
}
# Stages by song section: back (0:00-0:30), turning (0:30-1:34), half-side (1:34-3:21), profile (3:21-end)
def stage(n):
    return "back" if n <= 5 else "turning" if n <= 15 else "half" if n <= 33 else "profile"
FAR = {1, 5, 19, 23, 25, 30, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 47, 49, 50, 51, 53, 54}
GLIMPSE = {11, 17, 18, 21, 26, 27, 29, 32}
def view(n):
    return VIEW["far"] if n in FAR else VIEW["glimpse"] if n in GLIMPSE else VIEW[stage(n)]
SLOW = ("This is not a story being told: the camera quietly witnesses one moment already in progress, "
        "in gentle slow motion, fabric, hair, dust and water drifting softly as if time is held still.")
AVOID = ("Avoid: printed words or titles, black bars, white edge lines, collage or grid, vignette, color "
         "grade, pink tint (keep warm natural gold), plastic or overly smooth skin, film grain, fast "
         "action, jarring cuts, blood, Yeshua's face seen from the front, Yeshua looking at the camera, a young or "
         "clean-shaven Yeshua, short or trimmed hair, trimmed sideburns, curled sidelocks, modern clothing on anyone, lens flare; he kneels only when praying.")

# (shot, label, seconds, mood, moment · camera · how it ends)
SHOTS = [
 (1, '1B', 6, 'Longing',
  "Early morning over misty Judean hills; far below, a lone figure in cream walks a winding stony path toward Jerusalem, his staff and long shadow reaching ahead. A drone glides slowly high above and behind him. It ends wide and high, Yeshua small on the path, the golden city faint on the horizon."),
 (2, '2A', 8, 'Stillness',
  "Night in the quiet wilderness; Yeshua kneels in prayer beside a small campfire, seen from behind, his head bowed, sparks lifting slowly into a sky of stars. The camera eases forward through dark bushes at human height. It ends medium, from behind, his kneeling back lit warm by the fire."),
 (3, '3A', 8, 'Holy awe',
  "The Jordan River at midday. Yeshua and John the Baptist stand waist-deep in the river, both bare-chested in simple linen loincloths, wet skin glistening. John, a rugged, muscular, sun-weathered man with long wild dark curly hair and a thick grey-streaked beard, stands close beside him, one strong hand on Yeshua's upper back and the other holding his arm, helping him rise up out of the water. Water pours from Yeshua's long hair and bare shoulders; his head is bowed in prayer. Above them the clouds part, a beam of soft golden light falls, and a white dove glides down toward Yeshua. A few onlookers on the bank watch in wonder. The camera sits low at water level behind Yeshua and tilts up slowly. It ends low behind his shoulder, the light and the dove above him."),
 (4, '5A', 8, 'Gentle authority',
  "A small stone synagogue on the Sabbath; Yeshua stands at the reading table holding an open parchment scroll on two wooden rollers, seen from behind, over his shoulder. Before him the seated listeners lean in, faces lit by window light, an old man slowly closing his eyes in wonder. The camera drifts slowly past his shoulder. It ends medium close over his shoulder on the listening faces."),
 (5, '5B', 6, 'Warmth',
  "The same synagogue from high in the rafters; shafts of dusty sunlight fall through a small high window onto the room, every head gently turned toward the tall figure at the reading table. The camera descends slowly through the light. It ends wide and high, the whole room turned toward Yeshua."),
 (6, 'W1', 6, 'Journey',
  "A dusty road through golden hills in late afternoon; Yeshua walks steadily with his staff, seen from behind and slightly to one side, his mantle over his head, the edge of his beard just showing past the hood, heat haze shimmering. The camera tracks a step behind and beside him at his walking pace. It ends medium, three-quarters from behind, the road and Jerusalem far ahead."),
 (7, '7A', 6, 'Hope',
  "Inside a crowded stone house, roof tiles lifted away above; four men lower a paralyzed man on a mat on ropes through the opening, dust and light pouring down slowly. Yeshua stands below, seen from behind and slightly to the side, his head tilted up so the line of his beard shows. The lowered man's face is full of fragile hope. The camera looks up from the floor behind Yeshua. It ends medium and low, the man on the mat descending above Yeshua's shoulders."),
 (8, '7B', 6, 'Release',
  "The same house; the once-paralyzed man rises slowly to his feet, his face breaking into tearful astonishment, his friends' hands over their mouths. Yeshua stands beside him, seen over his shoulder, the edge of his beard just visible. The camera watches at eye level from behind and to the side of Yeshua. It ends medium, the healed man standing, Yeshua's shoulder at the edge of the frame."),
 (9, '6A', 8, 'Tenderness',
  "A narrow sunlit street; a leper in torn, ragged clothes kneels on the stones, and Yeshua, seen over his shoulder, rests his hand gently on the man's head. The man's face, lifted, softens from shame into tears of relief as the pale patches and sores on his face and hands slowly fade away until his skin is clean. The camera moves slowly around behind Yeshua's shoulder. It ends close on the man's tearful, clean face, Yeshua's hand and sleeve at the edge of frame."),
 (10, '13A', 8, 'Abundance',
  "A green hillside by the Sea of Galilee; a small boy holds up a basket of barley loaves and two fish, beaming, while Yeshua kneels to his height, seen from behind and slightly to the side. Around them, people pass bread hand to hand, smiling. The camera pushes in slowly at child height. It ends medium close on the boy's bright face over Yeshua's shoulder."),
 (11, '8A', 6, 'Faith',
  "A crowded market street; a woman in a dark mantle reaches through the crowd in slow motion, her trembling fingers closing on the knotted tassel at the corner of a cream mantle. Her face shows desperate hope turning to wonder. The camera stays low and close beside her hand. It ends extreme close on her fingers holding the tassel, the cream cloth filling the frame."),
 (12, '9A', 6, 'Joy',
  "A village wedding courtyard at dusk; servants pour from tall stone water jars and deep red wine flows into a clay cup. The steward tastes, his eyes widening, and he laughs, raising the cup. Yeshua stands in the background among the guests, turned three-quarters away. The camera pans slowly along the jars. It ends medium close on the steward laughing, cup raised."),
 (13, '10A', 8, 'Grief turned to joy',
  "At the gate of a small village; a widow in black holds her young son, alive, both weeping and laughing, her hands on his face. Mourners lower their heads in astonishment. Yeshua stands at the edge of the frame, turned three-quarters away. The camera pushes in slowly at eye level. It ends close on mother and son, Yeshua's shoulder soft at the frame edge."),
 (14, '14A', 8, 'Friendship',
  "The shore of Galilee at sunrise; fishermen at their nets look up, faces open and curious, as Yeshua stands on the sand, turned slightly so the edge of his beard shows past his hood, one hand extended toward them in welcome. The camera moves slowly behind his outstretched hand. It ends close behind his hand and shoulder, Peter's weathered face looking up at him."),
 (15, 'W2', 6, 'Nostalgia',
  "A golden hill road at sunset; Yeshua walks a little ahead of us and to one side, turned three-quarters away, his mantle and tassels stirring in the breeze, the sun low ahead. The camera follows low, behind and beside him. It ends medium, three-quarters from behind, the edge of his hood and beard against the warm sky."),
 (16, '25A', 8, 'Mercy',
  "A grassy hillside above the sea; Yeshua sits on a rock, seen from the side and slightly behind, his face turned toward the people, the line of his cheek and beard in soft shadow under his hood, his open hands resting on his knees, while families sit on the grass below him listening, a mother holding her child close, faces peaceful. The camera drifts slowly among the listeners. It ends medium beside and slightly behind him, his open hands and the listening faces, the sun beyond."),
 (17, '15A', 8, 'Freedom',
  "A village lane; a healed man runs home in slow motion, arms open, and his wife and children run to meet him and throw their arms around him, laughing and crying. Far down the lane behind, a tall cream figure watches. The camera moves alongside the running man. It ends medium on the family's embrace."),
 (18, '16A', 8, 'Mourning to song',
  "A widow sits in a courtyard; village women gently set a garland of white and yellow flowers on her head, and her tear-wet face slowly lifts into a trembling smile. The camera stays close, at eye level. It ends close on her face beneath the garland."),
 (19, '26A', 6, 'Tension',
  "A small wooden fishing boat in a night storm on the Sea of Galilee; rain sweeps across black waves, a tall figure in cream stands at the stern, seen far below from above. The drone descends slowly through the rain. It ends wide and high, the tossing boat and the standing figure."),
 (20, '4A', 8, 'Awe',
  "Night on the sea, moonlight on the waves; over the frightened disciples' shoulders we see a tall cream silhouette walking slowly across the water toward the boat, his mantle moving in the wind. The disciples' faces turn from fear to awe. The camera sits inside the boat behind them. It ends medium over their shoulders, the silhouette on the waves."),
 (21, '11C', 6, 'Longing',
  "The dusty Jericho road; a blind beggar sits by the wayside, his clouded eyes lifted, his hands reaching toward the sound of a passing crowd. A cream sleeve and a hand come into frame from behind and reach toward his face. The camera is close at eye level. It ends extreme close on his upturned face and the reaching hand."),
 (22, '11A', 8, 'Wonder',
  "The same road; Bartimaeus blinks slowly into the light, his eyes now clear, and breaks into astonished laughter, hands on his cheeks. Yeshua stands before him, seen from the side and slightly behind, the edge of his cheek and beard catching the light. The camera is low beside Yeshua's shoulder. It ends close and low on Bartimaeus looking up, laughing."),
 (23, '12B', 8, 'Peace after storm',
  "The Sea of Galilee just after a storm; the water turns glassy and calm, the clouds parting to golden light, the small boat resting still. The drone rises slowly as the clouds open. It ends wide and high on the boat on the calm, golden sea."),
 (24, '23A', 8, 'Friendship',
  "A charcoal fire on the shore at dawn; Yeshua sits by the fire, seen from the side and slightly behind, firelight warming the edge of his cheek and beard, handing bread to Peter, whose wet face softens into a grateful, tearful smile. Fish cook on the coals, smoke curling slowly. The camera sits at seated height beside and behind Yeshua. It ends medium on Peter receiving the bread over Yeshua's shoulder."),
 (25, '23B', 6, 'Warmth',
  "The same shore from above; a small glowing fire, a few figures sitting around it, the boat pulled up on the sand, the sunrise spreading gold over the water. The drone rises slowly. It ends wide and high on the small fire on the sunrise shore."),
 (26, 'W3', 6, 'Nostalgia',
  "A stony path in warm afternoon light; close on Yeshua's dusty sandalled feet and the hem of his tunic as he walks, the end of his staff touching the ground, dust drifting in the sunbeams. The camera tracks at ground level beside his feet. It ends extreme close on his feet, dust floating in the light."),
 (27, '17A', 6, 'Joy',
  "A village street; the healed man lifts his rolled-up mat high over his head and walks, laughing, through a parting crowd whose faces are full of amazement. The camera is low. It ends medium and low on the man lifting his mat high against the sky."),
 (28, '18A', 6, 'Rest',
  "The shade of an old olive tree in the afternoon; Yeshua sits against the trunk, seen from the side, his face turned down toward the boy, the line of his cheek and beard in soft dappled shadow, a small boy leaning sleepily on his arm, leaves stirring, light dappling the ground. The camera sits beside them at seated height. It ends medium close on the boy resting, Yeshua's shoulder and beard edge in soft shadow."),
 (29, '19A', 6, 'Celebration',
  "A village square at dusk; men and women dance in a circle, arms linked, skirts and mantles swinging in slow motion, faces full of laughter. The camera moves inside the circle. It ends medium on dancers spinning past, joyful faces."),
 (30, '19B', 6, 'Exultation',
  "The same square from above; the whole circle of dancers turning, lamps glowing, the hills around golden in the last light. The camera cranes up slowly. It ends wide and high on the whole square and the hills."),
 (31, '21A', 6, 'Victory',
  "A market square; a woman who was bent for years slowly straightens and stands tall, her radiant face lifting toward the sky, her hands held in the hands of Yeshua, seen from the side and slightly behind, the edge of his cheek and beard in soft light. The camera is at eye level beside his shoulder. It ends close on her radiant face."),
 (32, '20A', 6, 'Courage',
  "Night on the sea; from behind Peter we see his hand reaching out over the waves, and a strong hand in a cream sleeve grasping it firmly. Peter's face, in profile, shows fear giving way to trust. The camera stays behind Peter's shoulder. It ends medium on the two hands meeting above the water."),
 (33, '22A', 6, 'Freedom',
  "The road out of Jericho; Bartimaeus walks beside Yeshua, laughing and looking at everything, while Yeshua walks beside him, seen from the side and slightly behind, the edge of his cheek and beard lit by the low sun. Dust glows in the low sun. The camera tracks beside them. It ends medium on Bartimaeus laughing, Yeshua's shoulder and the edge of his face beside him."),
 (34, '25B', 8, 'Majesty',
  "The hillside above the Sea of Galilee from high above; a great crowd seated on the green slope, a lone figure in cream sitting before them, the shining sea beyond. The drone glides slowly. It ends wide and high on the hillside and the sea."),
 (35, '13B', 8, 'Abundance',
  "From high above the shore; thousands of people seated in groups on the grass, baskets passing from hand to hand, the sea glittering beyond. The drone drifts slowly. It ends wide and high on thousands eating by the sea."),
 (36, '8B', 6, 'Faith',
  "A busy market street from above; a tall figure in a cream mantle moves slowly through the crowd toward the town gate, people turning to follow him. The drone tracks high above. It ends wide and high on the crowd around him, the gate ahead."),
 (37, '9B', 6, 'Joy',
  "A wedding courtyard from high above at night; guests dance in rings, lamps and torches glowing, cups raised. The camera cranes slowly overhead. It ends wide and high on the courtyard full of dancing guests."),
 (38, '10B', 8, 'Triumph',
  "The gate of the village of Nain from above; a crowd gathers around the widow and her son, people embracing, mourning cloths falling away. The drone rises slowly, stopping lower. It ends wide and high on the crowd around the family at the gate."),
 (39, '24A', 8, 'Devotion',
  "A road through golden hills at evening; Yeshua walks at the head of the people, seen in side profile, warm sunset light along his forehead, nose and beard, his eyes on the road ahead; following him are many people walking together, faces soft with love and gratitude. The camera tracks beside him at eye level. It ends medium in side profile, the people behind him, Jerusalem ahead in the sunset."),
 (40, '2B', 8, 'Nostalgia',
  "A hilltop at night above a misty valley; Yeshua kneels in prayer, a small dark silhouette against a sky full of stars, a tiny campfire glowing beside him. The drone orbits slowly, high. It ends wide and high on him praying above the misty valley."),
 (41, 'W4', 6, 'Remembrance',
  "A country road in golden light; Yeshua walks among his followers, seen in side profile, a woman beside him smiling as she speaks to him. The camera tracks at his side at eye level. It ends full figure in side profile, Yeshua walking among his followers."),
 (42, '16B', 8, 'Joy',
  "A village courtyard from above; women dance slowly around the widow, who sits at the center wearing her white and yellow garland, petals drifting. The camera rises slowly. It ends wide and high on the widow in the center with her garland."),
 (43, '15B', 8, 'Love',
  "A village lane from above; a small family holds each other tight in the middle of the lane, neighbors coming out of doorways. The drone rises slowly. It ends wide and high, the family small, embracing."),
 (44, 'W5', 8, 'Nostalgia',
  "A stony hill path from straight above; a tall figure in a cream mantle walks slowly through a flock of sheep, the sheep parting around him, long shadows on the ground. The drone looks straight down and tracks with him. It ends wide and top-down on him and the sheep around him."),
 (45, '3B', 8, 'Remembrance',
  "The Jordan River from above; rays of light fall through the clouds onto the water, two small figures standing in the river, a crowd on the bank. The drone descends slowly. It ends wide and high on the light rays on the river."),
 (46, '6B', 8, 'Tenderness',
  "A narrow village street from above; a kneeling man and a tall figure in cream bending over him, passers-by stopping to watch, sunlight across the stones. The drone rises gently. It ends wide and high on the two of them in the street."),
 (47, '11B', 8, 'Gratitude',
  "The Jericho road from above; a crowd moves along the road, and at its front a man in a ragged mantle walks beside a tall figure in cream, palm trees along the way. The drone drifts slowly. It ends wide and high on the two of them on the road."),
 (48, 'W6', 8, 'Belonging',
  "A road at sunset; the camera walks beside Yeshua, low, his side profile against the sunset sky as he leads the way, and around and behind him his followers walk close together, faces bright and glad, children running alongside. It ends medium and low on his side profile, the followers filling the road."),
 (49, '20B', 8, 'Wonder',
  "The Sea of Galilee at night from above; two small figures stand together on the moonlit water, the fishing boat a short distance away. The drone circles slowly. It ends wide and high on the two figures and the boat."),
 (50, '22B', 8, 'Belonging',
  "A long road from above; a great crowd follows a tall figure in cream, the road winding through green fields toward the hills. The drone glides slowly. It ends wide and high on the crowd following him."),
 (51, '21B', 8, 'Joy remembered',
  "A seaside market town from above; the crowded square and stalls, boats along the shore, the sea glittering in the afternoon sun. The drone drifts slowly. It ends wide and high on the market and the sea."),
 (52, '12A', 8, 'Awe',
  "Inside the small fishing boat just after the storm; the wet disciples look up, faces full of awe and quiet wonder, as golden light breaks through the parting clouds. Yeshua stands at the stern, seen in side profile against the golden light, looking out over the calm water. The camera holds steady at eye level inside the boat. It ends medium on the disciples looking up at the golden sky, Yeshua's profile at the edge of the frame."),
 (53, '24B', 8, 'Climax',
  "Golden hills at sunset from above; a long procession of people follows a tall figure in cream along the road toward Jerusalem, the city glowing on its hill. The drone rises slowly. It ends wide and high on everyone following him toward Jerusalem at sunset."),
 (54, '18B', 8, 'Peaceful farewell',
  "An old olive tree on a hill above the sea at sunset; a single figure in cream sits beneath it, small, the sea calm and golden. The drone rises very slowly. It ends wide and high on the olive tree and the sea at sunset, the light softly fading."),
]

# Shots where He has laid His clothes aside (the baptism) use His body description only.
NO_CLOTHES = {3}


def prompt(moment, mood, look=LOOK, view_text=""):
    return f"{look} {view_text} {SLOW} {moment} Mood: {mood.lower()}, carried by the warm natural light, the slow movement and the faces of anyone near him. {AVOID}"


rows = []
for n, lab, sec, mood, moment in SHOTS:
    rows.append({'shot': n, 'label': lab, 'duration': sec, 'fps': 24, 'mood': mood, 'prompt': prompt(moment, mood, BODY if n in NO_CLOTHES else LOOK, view(n))})

here = os.path.dirname(os.path.abspath(__file__))
json.dump(rows, open(os.path.join(here, 'scenes-ltx-script-only.json'), 'w'), indent=1, ensure_ascii=False)
md = ["# Jesus Savior Redeemer Friend — script-only LTX prompts", "",
      "No starting pictures. Each shot is sent to LTX as text-to-video (ltx-2-5-pro, 1920×1080, 24 fps, no audio).",
      "Ed's direction (Oct 16, 2026): subtle — Yeshua seen from behind, over the shoulder or in side silhouette, never His full face or eyes; don't tell the story, just witness one moment from it in gentle slow motion; the feeling lives in the other people's faces and in the light.", ""]
for r in rows:
    md += [f"## Shot {r['shot']} · {r['label']} · {r['duration']} s · {r['mood']}", "", r['prompt'], ""]
open(os.path.join(here, 'scenes-ltx-script-only.md'), 'w').write("\n".join(md))
print(len(rows), 'shots written')
