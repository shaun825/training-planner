import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="CrossFit + Trail Run - May 2026",
    page_icon=":runner:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
.block-container{padding-top:.75rem;padding-bottom:0;max-width:1120px;}
header{display:none!important;}#MainMenu{display:none;}footer{display:none;}
</style>
""", unsafe_allow_html=True)

# =========================================================================
# WEEK METADATA
# =========================================================================
WEEK_META = [
    {"label": "Week 1 \u00b7 May 4\u201310",  "km": 25, "cycle": 1,
     "dates": ["Mon 4","Tue 5","Wed 6","Thu 7","Fri 8","Sat 9","Sun 10"]},
    {"label": "Week 2 \u00b7 May 11\u201317", "km": 25, "cycle": 2,
     "dates": ["Mon 11","Tue 12","Wed 13","Thu 14","Fri 15","Sat 16","Sun 17"]},
    {"label": "Week 3 \u00b7 May 18\u201324", "km": 27, "cycle": 3,
     "dates": ["Mon 18","Tue 19","Wed 20","Thu 21","Fri 22","Sat 23","Sun 24"]},
    {"label": "Week 4 \u00b7 May 25\u201331", "km": 26, "cycle": 4,
     "dates": ["Mon 25","Tue 26","Wed 27","Thu 28","Fri 29","Sat 30","Sun 31"]},
]

# =========================================================================
# SUNDAY LONG TRAIL RUNS (fixed, not in palette)
# =========================================================================
LONG_TRAILS = [
    {
        "km": "11 km", "name": "Trail Run \u2014 Long",
        "wu": [
            "3 min walk then easy jog to trail",
            "10 high knees + 10 butt kicks",
            "10 walking lunges each leg",
            "10 leg swings each direction",
            "4 \u00d7 20 sec build-up strides, ease back to easy pace",
        ],
        "wod": "LONG TRAIL \u2014 11 km\nEffort: Easy to moderate (Zone 2, Zone 3 on climbs)\n\n\u2192 km 0\u20133: pure easy, find your trail legs\n\u2192 km 3\u20139: steady effort, let terrain dictate\n\u2192 km 9\u201311: gradual build, finish feeling strong\n\nWeek 1 total: ~25 km including mid-week runs.",
    },
    {
        "km": "11 km", "name": "Trail Run \u2014 Recovery",
        "wu": [
            "3 min walk then very easy jog to trail",
            "8 leg swings front/back each leg",
            "8 hip circles each direction",
            "2 min easy jog \u2014 check in with your body, legs may feel heavy",
        ],
        "wod": "RECOVERY TRAIL \u2014 11 km\nEffort: Easy throughout (Zone 1\u20132).\n\n\u2192 Full run at conversational pace \u2014 you should be able to sing\n\u2192 Walk any tight or technical section\n\u2192 Moving meditation, not training\n\nPost-run: 5 min easy walk + hip flexors, calves, hamstrings stretch.",
    },
    {
        "km": "12 km", "name": "Trail Run \u2014 Long",
        "wu": [
            "3 min walk then easy jog to trail",
            "10 high knees + 10 butt kicks",
            "10 walking lunges each leg",
            "4 \u00d7 20 sec easy strides \u2014 do not go too hard, 12 km ahead",
        ],
        "wod": "LONG TRAIL \u2014 12 km\nYour longest single run of the month. Approach with patience.\n\n\u2192 km 0\u20133: fully easy, let body warm into it\n\u2192 km 3\u20139: comfortable effort, enjoy the scenery\n\u2192 km 9\u201311: build slightly if feeling good\n\u2192 km 11\u201312: easy cool-down back home\n\nCarry water and a gel/dates if going over 75 min.",
    },
    {
        "km": "12 km", "name": "Trail Run \u2014 Final",
        "wu": [
            "3 min walk then easy jog \u2014 savour this last run",
            "10 high knees + 10 butt kicks",
            "10 walking lunges each leg",
            "10 leg swings each direction",
        ],
        "wod": "FINAL TRAIL \u2014 12 km\nThe last run of the month. Run it your way.\n\n\u2192 Easy and celebratory \u2014 you have earned this\n\u2192 Or push the second half if legs are good\n\u2192 Try for a PB on your favourite trail segment\n\nMonth done: ~102 km total running, full cycle complete.",
    },
]

# =========================================================================
# WARMUP HELPERS
# =========================================================================
def wu_squat():
    return [
        "90 sec jumping jacks or jump rope",
        "10 hip circles each direction",
        "10 slow air squats \u2014 focus on depth and knee tracking",
        "10 leg swings front/back each leg",
        "Warm-up sets: 5@40%, 3@60%, 2@75% of working weight",
    ]

def wu_deadlift():
    return [
        "90 sec jumping jacks or easy row",
        "10 good mornings with PVC or empty bar",
        "10 slow hip hinge RDLs with empty bar",
        "Warm-up sets: 5@40%, 3@60%, 2@75%, 1@85%",
    ]

def wu_clean():
    return [
        "90 sec jump rope or light jog",
        "10 arm circles + 10 hip circles each direction",
        "PVC: 10 pass-throughs, 10 overhead squats",
        "Empty bar: 5 hang muscle cleans \u2192 5 hang power cleans \u2014 2 sets",
        "Practice front rack: elbows high, bar on shoulders",
    ]

def wu_snatch():
    return [
        "90 sec jump rope",
        "10 large arm circles each direction",
        "PVC: 10 overhead squats, 10 snatch-grip deadlifts",
        "Empty bar: 3\u00d75 hang muscle snatches \u2192 3\u00d73 hang power snatches",
        "5 reps: fast drop into catch position (starfish drill)",
    ]

def wu_gymnastics():
    return [
        "Shoulder Floss: 3 min per side",
        "Rotate: thumbs-up t-spine stretch, gymnastics kips, head in/out of window in HS hold",
        "T-Spine Peanut Rotation: 1 min each position",
        "See Misfit Movement Index for full technique cues",
    ]

def wu_press():
    return [
        "90 sec arm circles, shoulder rolls, jumping jacks",
        "10 PVC pass-throughs",
        "10 strict overhead press with PVC",
        "5 push press with empty bar \u2014 focus on dip-drive-press timing",
        "2\u00d75 at 40% then 50% working weight",
    ]

def wu_kb():
    return [
        "90 sec jumping jacks",
        "10 hip circles each direction",
        "10 hip hinges \u2014 hands slide down shins",
        "10 KB deadlifts with light KB",
        "2 min: 10 KB swings + 5 goblet squats (light, preview movements)",
    ]

def wu_run():
    return [
        "3 min: Brisk walk then easy jog to trail",
        "10 high knees + 10 butt kicks",
        "10 leg swings front/back each leg",
        "8 walking lunges each leg",
        "4 \u00d7 20 sec build-up strides, easy jog back",
    ]

def wu_tempo():
    return [
        "2 min easy jog, progressive",
        "10 high knees + 10 butt kicks",
        "10 leg swings each leg",
        "4 \u00d7 20 sec build-up strides to tempo pace",
        "60 sec easy jog shakeout",
    ]

def wu_barbell_complex():
    return [
        "90 sec arm circles, hip openers, jumping jacks",
        "10 PVC pass-throughs",
        "5 empty-bar deadlifts \u2192 5 hang cleans \u2192 5 front squats \u2192 5 push press (one complex)",
        "Rest 60 sec, repeat with light load",
    ]

# =========================================================================
# WEEKLY BLOCKS  (9 per week \u2014 Sun long trail is auto-placed)
# Block types: S=Strength, O=Olympic, G=Gymnastics, M=MetCon, T=Trail, E=Endurance
# =========================================================================
BLOCKS = {
    # -----------------------------------------------------------
    # WEEK 1  \u2014 Cycle W1/4
    # Strength: Back Squat 5\u00d75 / Deadlift 5\u00d73
    # Olympic: Hang Power Clean (positional awareness base)
    # Gymnastics: Misfit HSPU W1 \u2014 HS holds 5 min + HSPU ladder
    # Press: Push Press 5\u00d75
    # -----------------------------------------------------------
    0: [
        {
            "id": "squat", "type": "S", "name": "Back Squat",
            "cycle_label": "Strength A \u00b7 W1/4", "scheme": "5\u00d75 @ 75\u201380%",
            "wu": wu_squat(),
            "str": "Back Squat \u2014 5\u00d75 @ 75\u201380% 1RM\nRest 2\u20133 min between sets.\nCues: big breath and brace before descent, drive knees out, chest stays tall.\nWeek 1 of 4 \u2014 establish volume at moderate intensity. Record working weight.",
            "wod": "SQUAT OPENER\nFor time \u2014 21\u201315\u20139:\nBack Squats (95/135 lb)\nBurpees\n\nThen: 2 \u00d7 max-rep air squats (rest 90 sec between)\n\nScale: 50\u201360% 1RM on barbell.\nTarget: sub-12 min for 21-15-9.",
            "tags": ["Barbell", "15\u201320 min"],
        },
        {
            "id": "deadlift", "type": "S", "name": "Deadlift",
            "cycle_label": "Strength B \u00b7 W1/4", "scheme": "5\u00d73 @ 80%",
            "wu": wu_deadlift(),
            "str": "Deadlift \u2014 5\u00d73 @ 80% 1RM\nRest 3 min between sets.\nCues: hips back, chest tall, lat engagement before lift, bar drags up shins.\nWeek 1 of 4 \u2014 volume base. Record working weight for progression.",
            "wod": "DEAD SPRINT\nFor time \u2014 21\u201315\u20139:\nDeadlifts (155/225 lb)\nBox Jumps (24 in or broad jumps)\n\nRest 3 min, then 3 Rounds:\n15 KB Swings (35/53 lb)\n15 Push-ups\n\nTarget: sub-10 min for 21-15-9.",
            "tags": ["Barbell", "KB", "18\u201328 min"],
        },
        {
            "id": "olympic", "type": "O", "name": "Hang Power Clean",
            "cycle_label": "Olympic \u00b7 W1/4", "scheme": "Build to 3RM, then 3\u00d73@85%",
            "wu": wu_clean(),
            "str": "Hang Power Clean \u2014 Build to a heavy triple (3RM).\nThen: 3\u00d73 @ 85% of today's 3RM.\nFocus: explosive hip extension, fast elbow turnover, solid catch.\nWeek 1: hang position builds positional awareness before full clean progression.",
            "wod": "CLEAN MACHINE\n4 Rounds for time:\n12 Hang Power Cleans (75/115 lb)\n12 Burpees\n15 Pull-ups\n\nRest 60 sec between rounds.\nScale: reduce load, sub ring rows for pull-ups.\nTarget: 22\u201330 min.",
            "tags": ["Barbell", "Pull-up bar", "22\u201330 min"],
        },
        {
            "id": "gymnastics", "type": "G", "name": "HSPU / Gymnastics",
            "cycle_label": "Misfit HSPU \u00b7 W1/6", "scheme": "HS holds 5 min + HSPU ladder",
            "wu": wu_gymnastics(),
            "str": "Handstand Holds \u2014 Accumulate 5 min total (15 min cap)\nPositional focus. Push limits each set, no gaming.\n\nDB Wall Press: 3\u00d715\nSlow and controlled. Focus on core engagement and dumbbell path.\nSee Misfit Movement Index for all technique cues.",
            "wod": "HSPU LADDER \u2014 Week 1\nClimb the ladder \u00d73\nRest 3:00\nMax rep HSPU:\n  Under 10 reps \u2014 count by 1s\n  10\u201320 reps \u2014 count by 2s\n  20+ reps \u2014 count by 3s\n\nSub: pike push-ups or Z-press with DB.\nHandstand hold: 10 \u00d7 3\u20135 sec (straight line, close to wall).",
            "tags": ["Bodyweight", "Gymnastics", "20\u201330 min"],
        },
        {
            "id": "press", "type": "S", "name": "Push Press",
            "cycle_label": "Press Cycle \u00b7 W1/4", "scheme": "5\u00d75 @ 75\u201380%",
            "wu": wu_press(),
            "str": "Push Press \u2014 5\u00d75 @ 75\u201380% 1RM\nRest 2 min between sets.\nCues: vertical dip (no forward lean), explosive leg drive, press to lockout, ribs down on return.\nWeek 1 of 4 \u2014 establish working weight and groove movement pattern.",
            "wod": "PRESS CHIPPER\n21\u201315\u20139 for time:\nPush Press (75/115 lb)\nBurpees\n\nThen: 5 min AMRAP\n5 DB Push Press each arm\n10 Push-ups\n\nTarget: sub-12 min for 21-15-9.",
            "tags": ["Barbell", "18\u201325 min"],
        },
        {
            "id": "metcon_a", "type": "M", "name": "KB MetCon",
            "cycle_label": "MetCon A", "scheme": "AMRAP 20 min",
            "wu": wu_kb(),
            "str": None,
            "wod": "KB OPENER\nAMRAP 20 min:\n10 KB Swings (35/53 lb)\n10 Goblet Squats (same KB)\n8 DB Renegade Rows (4 each side, 20/35 lb)\n12 Push-ups\n\nScale: reduce weight, keep push-ups strict.\nTarget: 6\u20138 rounds.",
            "tags": ["KB", "Dumbbell", "20 min AMRAP"],
        },
        {
            "id": "metcon_b", "type": "M", "name": "Benchmark \u2014 Frankie",
            "cycle_label": "MetCon B \u00b7 Benchmark", "scheme": "21\u201315\u20139 for time",
            "wu": [
                "90 sec jumping jacks",
                "10 arm circles each direction",
                "5 empty-bar thrusters (smooth squat-to-press)",
                "3 kipping pull-up swings on bar",
                "10 air squats",
            ],
            "str": None,
            "wod": "FRANKIE\n21\u201315\u20139 for time:\nThrusters (65/95 lb)\nPull-ups\n\nBenchmark WOD \u2014 give it everything. Record your time.\n\nScale: reduce load, sub ring rows for pull-ups.\nTarget: sub-10 min advanced, sub-15 min intermediate.",
            "tags": ["Barbell", "Pull-up bar", "10\u201318 min"],
        },
        {
            "id": "trail_mid", "type": "T", "name": "Trail Run \u2014 Hills", "km": "9 km",
            "cycle_label": "Trail Run \u00b7 Suggested: Tuesday", "scheme": "9 km \u2014 hill surges",
            "wu": wu_run(),
            "str": None,
            "wod": "HILL TRADER \u2014 9 km\nEffort: Moderate with hill surges\n\n\u2192 km 0\u20132: easy warm-up, find rhythm\n\u2192 km 2\u20137: 5\u00d7 hill efforts, push hard uphill (20\u201330 sec), recover on flat\n\u2192 km 7\u20139: steady cool-down effort\n\nTip: shorten stride and lean forward on climbs. Power hiking is fine.",
            "tags": ["Trail", "9 km", "~55\u201370 min"],
        },
        {
            "id": "run_session", "type": "E", "name": "Tempo Run", "km": "~5 km",
            "cycle_label": "Endurance Run \u00b7 Suggested: Wednesday", "scheme": "5\u00d71 km @ tempo",
            "wu": wu_tempo(),
            "str": None,
            "wod": "TEMPO GRIND \u2014 ~5 km\n5\u00d71 km at tempo pace (comfortably hard)\nJog 90 sec between reps\n\nThen: 3 Rounds:\n15 Push-ups\n15 Sit-ups\n15 Air squats\n(No rest between rounds)\n\nTempo = effort where you can answer a question but not hold a conversation.",
            "tags": ["Running", "~5 km", "35\u201345 min"],
        },
    ],

    # -----------------------------------------------------------
    # WEEK 2  \u2014 Cycle W2/4
    # Strength: Back Squat 5\u00d73 / Deadlift 4\u00d73 (increased intensity)
    # Olympic: Power Snatch (alternating with clean cycle)
    # Gymnastics: Misfit HSPU W2 \u2014 HS holds 6 min + strict/kipping ladders
    # Press: Strict Press 5\u00d73
    # -----------------------------------------------------------
    1: [
        {
            "id": "squat", "type": "S", "name": "Back Squat",
            "cycle_label": "Strength A \u00b7 W2/4", "scheme": "5\u00d73 @ 82\u201385%",
            "wu": wu_squat(),
            "str": "Back Squat \u2014 5\u00d73 @ 82\u201385% 1RM\nRest 2\u20133 min between sets.\nIncreased intensity from Week 1. Focus on speed out of the hole.\nCues: aggressive breathing, stay braced through full set.",
            "wod": "FRONT LOADED\n3 Rounds for time:\n10 Front Squats (95/135 lb)\n20 Wall Ball shots (14/20 lb)\n15 Pull-ups\n\nScale: reduce load, break wall balls 10+10.\nTarget: 22\u201330 min.",
            "tags": ["Barbell", "Wall ball", "Pull-up bar", "24\u201332 min"],
        },
        {
            "id": "deadlift", "type": "S", "name": "Deadlift",
            "cycle_label": "Strength B \u00b7 W2/4", "scheme": "4\u00d73 @ 82.5%",
            "wu": wu_deadlift(),
            "str": "Deadlift \u2014 4\u00d73 @ 82.5% 1RM\nRest 3 min between sets.\nProgression from Week 1: same reps, higher intensity.\nFocus on maintaining perfect setup on every single rep.",
            "wod": "DEAD WEIGHT\n5 Rounds for time:\n5 Deadlifts (275/185 lb \u2014 heavy)\n10 Box Jumps (24 in)\n15 Push-ups\n\nRest 90 sec between rounds.\nTarget: 20\u201326 min.",
            "tags": ["Barbell", "20\u201328 min"],
        },
        {
            "id": "olympic", "type": "O", "name": "Power Snatch",
            "cycle_label": "Olympic \u00b7 W2/4", "scheme": "Build to heavy single, then 5\u00d72@80%",
            "wu": wu_snatch(),
            "str": "Power Snatch \u2014 Build to a heavy single over 15 min.\nThen: 5\u00d72 @ 80% of today's heavy single.\nFocus: bar close to body, aggressive hip extension, fast pull-under.\nWeek 2: snatch focus \u2014 alternates with clean in the 4-week Olympic cycle.",
            "wod": "SNATCH & DASH\n10 Rounds for time:\n3 Power Snatches (65/95 lb)\n6 Burpees\n9 Air squats\n\nGo unbroken on snatches every round.\nScale: keep load light enough to not break singles.\nTarget: 18\u201324 min.",
            "tags": ["Barbell", "18\u201326 min"],
        },
        {
            "id": "gymnastics", "type": "G", "name": "HSPU / Gymnastics",
            "cycle_label": "Misfit HSPU \u00b7 W2/6", "scheme": "HS holds 6 min + HSPU ladders",
            "wu": wu_gymnastics(),
            "str": "Handstand Holds \u2014 Accumulate 6 min total (18 min cap)\nFaster than Week 1. Positional focus, push limits.\n\nDB Wall Press: 3\u00d715\nOnly increase weight if Week 1 felt easy.",
            "wod": "HSPU LADDERS \u2014 Week 2\n2 Rounds:\nClimb the strict HSPU ladder by 1s\nRest 90 sec\nClimb the kipping HSPU ladder by 2s\nRest 3 min\n\nKick down before you fail on strict HSPU.\nCool down: t-spine peanut rotation, 1 min each position.\nHandstand hold: 10 \u00d7 5\u20137 sec.",
            "tags": ["Bodyweight", "Gymnastics", "25\u201335 min"],
        },
        {
            "id": "press", "type": "S", "name": "Strict Press",
            "cycle_label": "Press Cycle \u00b7 W2/4", "scheme": "5\u00d73 @ 75\u201380%",
            "wu": wu_press(),
            "str": "Strict Press \u2014 5\u00d73 @ 75\u201380% 1RM\nRest 2 min between sets.\nWeek 2 of press cycle \u2014 strict press after push press volume in W1.\nCues: ribs down, glutes tight, vertical bar path, no layback.",
            "wod": "SHOULDER COMPLEX\n3 Rounds:\n10 Strict Press (75/105 lb)\n10 Push Press (same)\n10 Push Jerk (same)\n(No rest between movements)\nRest 2 min between rounds\n\nThen: 50 push-up challenge, any sets, no time limit.\nTarget: ~20 min.",
            "tags": ["Barbell", "20\u201325 min"],
        },
        {
            "id": "metcon_a", "type": "M", "name": "KB Storm",
            "cycle_label": "MetCon A", "scheme": "AMRAP 20 min",
            "wu": wu_kb(),
            "str": None,
            "wod": "KB STORM\nAMRAP 20 min:\n10 KB Swings (44/70 lb)\n10 Goblet Squats (same KB)\n8 DB Renegade Rows (4 each side, 25/35 lb)\n12 Push-ups\n\nScale: reduce weights. Keep push-ups strict.\nTarget: 6\u20138 rounds.",
            "tags": ["KB", "Dumbbell", "20 min AMRAP"],
        },
        {
            "id": "metcon_b", "type": "M", "name": "Benchmark \u2014 Helen",
            "cycle_label": "MetCon B \u00b7 Benchmark", "scheme": "3 rounds for time",
            "wu": [
                "90 sec light jog or row",
                "10 arm circles each direction",
                "5 KB deadlifts, 5 KB swings (light)",
                "5 jumping pull-ups or banded pull-ups",
                "10 air squats",
            ],
            "str": None,
            "wod": "HELEN \u2014 benchmark WOD\n3 Rounds for time:\n400m run\n21 KB Swings (35/53 lb)\n12 Pull-ups\n\nRecord time. Compare across future cycles.\n\nScale: reduce KB weight, sub ring rows for pull-ups.\nTarget: sub-12 min advanced, sub-18 min intermediate.",
            "tags": ["KB", "Pull-up bar", "Running", "12\u201320 min"],
        },
        {
            "id": "trail_mid", "type": "T", "name": "Trail Run \u2014 Fartlek", "km": "9 km",
            "cycle_label": "Trail Run \u00b7 Suggested: Tuesday", "scheme": "9 km \u2014 fartlek",
            "wu": wu_run(),
            "str": None,
            "wod": "FARTLEK \u2014 9 km\nEffort: Moderate with unstructured speed surges\n\n\u2192 km 0\u20131.5: easy warm-up\n\u2192 km 1.5\u20137.5: pick a tree/rock/bend and surge to it (10\u201330 sec), then recover. Aim for 10\u201315 surges.\n\u2192 km 7.5\u20139: easy cool-down\n\nFartlek = speed play in Swedish. Run by feel, no watch splits needed.",
            "tags": ["Trail", "9 km", "Fartlek", "~55\u201370 min"],
        },
        {
            "id": "run_session", "type": "E", "name": "200m Intervals", "km": "~5 km",
            "cycle_label": "Endurance Run \u00b7 Suggested: Wednesday", "scheme": "10\u00d7200m sprints",
            "wu": wu_tempo(),
            "str": None,
            "wod": "SPEED LADDER \u2014 ~5 km\n10\u00d7200m at 90\u201395% effort\nRest: walk/jog 200m between reps (total ~4 km + warm-up)\n\nThen: Tabata Wall Ball\n8 Rounds: 20 sec max wall ball / 10 sec rest\nCount reps in lowest round as score.\n\nAim for consistent 200m splits within 3 sec of each other.",
            "tags": ["Running", "~5 km", "Wall ball", "35\u201345 min"],
        },
    ],

    # -----------------------------------------------------------
    # WEEK 3  \u2014 Cycle W3/4  (peak week \u2014 highest intensity)
    # Strength: Back Squat 3\u00d73 @ 88% / Deadlift 3\u00d72 @ 87.5%
    # Olympic: Power Clean \u2014 build to 2RM
    # Gymnastics: Misfit HSPU W3 \u2014 HS holds 7 min + unbroken kipping
    # Press: Push Jerk 5\u00d73
    # -----------------------------------------------------------
    2: [
        {
            "id": "squat", "type": "S", "name": "Back Squat",
            "cycle_label": "Strength A \u00b7 W3/4 \u2014 PEAK", "scheme": "3\u00d73 @ 85\u201390%",
            "wu": wu_squat(),
            "str": "Back Squat \u2014 3\u00d73 @ 85\u201390% 1RM\nRest 3 min between sets.\nPeak week \u2014 reduce volume, increase intensity.\nFocus on perfect positioning under heavy load. This is the hardest week.",
            "wod": "SQUAT CLINIC\nFor time:\n50 Air squats\n40 Wall Ball shots (14/20 lb)\n30 KB Goblet Squats (44/70 lb)\n20 Front Squats (95/135 lb)\n10 Back Squats (115/185 lb)\n\nAll squats. One theme. Record total time.",
            "tags": ["Barbell", "KB", "Wall ball", "20\u201328 min"],
        },
        {
            "id": "deadlift", "type": "S", "name": "Deadlift",
            "cycle_label": "Strength B \u00b7 W3/4 \u2014 PEAK", "scheme": "3\u00d72 @ 87.5%",
            "wu": wu_deadlift(),
            "str": "Deadlift \u2014 3\u00d72 @ 87.5% 1RM\nRest 3\u20134 min between sets.\nNear-maximal loading. Treat each double as a serious effort.\nThis sets up next week's 1RM test \u2014 don't leave anything on the floor.",
            "wod": "TRIPLE THREAT\n3 Rounds for time:\n12 Deadlifts (185/275 lb)\n9 Hang Power Cleans (95/135 lb)\n6 Push Jerks (same bar)\n12 Pull-ups\n\nScale loads to 65\u201370% 1RM.\nTarget: 22\u201330 min.",
            "tags": ["Barbell", "Pull-up bar", "24\u201332 min"],
        },
        {
            "id": "olympic", "type": "O", "name": "Power Clean",
            "cycle_label": "Olympic \u00b7 W3/4", "scheme": "Build to 2RM, then 4\u00d72@85%",
            "wu": wu_clean(),
            "str": "Power Clean \u2014 Build to a heavy double (2RM).\nThen: 4\u00d72 @ 85% of today's 2RM.\nFocus: full hip extension, aggressive shrug, fast elbows.\nWeek 3: heavier loading before Clean & Jerk test week.",
            "wod": "CLEAN SWEEP\nFor time:\n30 Hang Squat Cleans (65/95 lb)\n30 Box Jumps\n20 Hang Squat Cleans\n20 Burpees\n10 Hang Squat Cleans\n10 Toes-to-bar\n\nScale: reduce load to weight you can cycle in sets of 5+.\nTarget: 18\u201326 min.",
            "tags": ["Barbell", "20\u201328 min"],
        },
        {
            "id": "gymnastics", "type": "G", "name": "HSPU / Gymnastics",
            "cycle_label": "Misfit HSPU \u00b7 W3/6", "scheme": "HS holds 7 min + unbroken kipping HSPU",
            "wu": wu_gymnastics(),
            "str": "Handstand Holds \u2014 Accumulate 7 min total (20 min cap)\nPeak volume week for holds. Push limits every set.\n\nDB Wall Press: 3\u00d715\nOnly increase weight if Week 2 felt easy.",
            "wod": "UNBROKEN HSPU \u2014 Week 3\nClimb the ladder \u00d73\nRest 3:00\nMax rep HSPU:\n  Under 10 reps \u2014 count by 1s\n  10\u201320 reps \u2014 count by 2s\n  20+ reps \u2014 count by 3s\n\nHandstand hold: 10 \u00d7 7\u20139 sec.\nT-spine peanut rotation cool-down.",
            "tags": ["Bodyweight", "Gymnastics", "25\u201335 min"],
        },
        {
            "id": "press", "type": "S", "name": "Push Jerk",
            "cycle_label": "Press Cycle \u00b7 W3/4", "scheme": "5\u00d73 \u2014 build to heavy triple",
            "wu": wu_press(),
            "str": "Push Jerk \u2014 Build to a heavy triple. Then 5\u00d73 @ 80% of today's best.\nWeek 3 of press cycle \u2014 introducing jerk footwork and power transfer.\nFocus: aggressive dip-drive, punch to lockout, receive feet wide.",
            "wod": "JERK COMPLEX\n5 Rounds:\n3 Push Jerks (building weight)\n5 Front Squats (same bar)\n7 Push-ups (strict)\n\nRest 90 sec between rounds.\n\nFinisher: 3\u00d710 DB Z-press (strict overhead strength accessory).\nTarget: ~25 min total.",
            "tags": ["Barbell", "22\u201328 min"],
        },
        {
            "id": "metcon_a", "type": "M", "name": "Barbell Complex",
            "cycle_label": "MetCon A \u00b7 CFB Style", "scheme": "6 rounds \u2014 rest = work time",
            "wu": wu_barbell_complex(),
            "str": None,
            "wod": "THE COMPLEX (CFB Style)\n6 Rounds \u2014 rest = work time:\n6 Deadlifts\n5 Hang Power Cleans\n4 Front Squats\n3 Push Press\n2 Hang Squat Cleans\n1 Thruster\n(Same barbell throughout: 75/115 lb)\n\nDo NOT put bar down mid-complex.\nTarget: each round under 90 sec.",
            "tags": ["Barbell", "20\u201330 min"],
        },
        {
            "id": "metcon_b", "type": "M", "name": "Body Shop Chipper",
            "cycle_label": "MetCon B \u00b7 Chipper", "scheme": "For time",
            "wu": [
                "3 min easy jog",
                "10 high knees + 10 butt kicks",
                "10 arm circles each direction",
                "10 air squats + 10 push-ups (1 warm-up round)",
            ],
            "str": None,
            "wod": "BODY SHOP\nFor time:\n1 mile run\n50 Push-ups\n800m run\n50 Sit-ups\n400m run\n50 Air squats\n200m run\n50 Lunges (alternating)\n\nScale: reduce reps to 30-30-30-30 or take walk breaks on runs.\nTarget: 30\u201345 min.",
            "tags": ["Running", "Bodyweight", "35\u201350 min"],
        },
        {
            "id": "trail_mid", "type": "T", "name": "Trail Run \u2014 Neg. Splits", "km": "10 km",
            "cycle_label": "Trail Run \u00b7 Suggested: Tuesday", "scheme": "10 km \u2014 negative splits",
            "wu": wu_run(),
            "str": None,
            "wod": "NEGATIVE SPLITS \u2014 10 km\nGoal: every 2 km section faster than the last.\n\n\u2192 km 0\u20132: very easy, hold back (feels almost too slow)\n\u2192 km 2\u20134: comfortable, start to feel the run\n\u2192 km 4\u20136: moderate, building confidence\n\u2192 km 6\u20138: comfortably hard, pushing now\n\u2192 km 8\u201310: strong finish, everything left on the trail\n\nSkill run: learning to start controlled and finish fast.",
            "tags": ["Trail", "10 km", "~60\u201375 min"],
        },
        {
            "id": "run_session", "type": "E", "name": "Interval Run", "km": "~5 km",
            "cycle_label": "Endurance Run \u00b7 Suggested: Wednesday", "scheme": "5\u00d71 km @ tempo + KB",
            "wu": wu_tempo(),
            "str": None,
            "wod": "TEMPO + KB \u2014 ~5 km\n5\u00d71 km at tempo effort\nRest: 90 sec easy jog between reps\n\nThen: 3 Rounds\n15 KB Swings (44/70 lb)\n10 Goblet Squats (same)\n10 Dips (chairs/box)\n\nRecord each 1 km split. Aim for km 5 faster than km 1.",
            "tags": ["Running", "~5 km", "KB", "40\u201350 min"],
        },
    ],

    # -----------------------------------------------------------
    # WEEK 4  \u2014 Cycle W4/4  (TEST WEEK)
    # Strength: Back Squat 1RM test / Deadlift 1RM test
    # Olympic: Clean & Jerk \u2014 heavy singles + complex
    # Gymnastics: Misfit HSPU W4 \u2014 HS holds 6 min (faster) + HSPU test
    # Press: Push Press 1RM test
    # -----------------------------------------------------------
    3: [
        {
            "id": "squat", "type": "S", "name": "Back Squat \u2014 1RM Test",
            "cycle_label": "Strength A \u00b7 W4/4 \u2014 TEST", "scheme": "Work to 1RM",
            "wu": wu_squat(),
            "str": "Back Squat \u2014 Work to a 1RM (or 3RM if 1RM not available today).\nThen: 2\u00d75 @ 65% (speed squats \u2014 move bar explosively on the way up).\nThis closes the 4-week strength cycle. Record your number.",
            "wod": "POST-TEST METCON\n3 Rounds for time:\n10 Front Squats (95/135 lb)\n20 Wall Ball shots (14/20 lb)\n15 Pull-ups\n\nLighter MetCon after heavy strength \u2014 let legs recover.\nTarget: 22\u201330 min.",
            "tags": ["Barbell", "Wall ball", "24\u201332 min"],
        },
        {
            "id": "deadlift", "type": "S", "name": "Deadlift \u2014 1RM Test",
            "cycle_label": "Strength B \u00b7 W4/4 \u2014 TEST", "scheme": "Work to 1RM",
            "wu": wu_deadlift(),
            "str": "Deadlift \u2014 Build to a 1RM attempt.\nThen: 3\u00d72 @ 90% of today's 1RM.\nRecord your number. This closes the 4-week strength cycle.\nMinimum 8 warm-up sets. Take your time on the build.",
            "wod": "FINAL PULL\n3 Rounds for time:\n12 Deadlifts (185/275 lb)\n9 Hang Power Cleans (95/135 lb)\n6 Push Jerks\n12 Pull-ups\n\nScale loads to 65\u201370% 1RM.\nTarget: 22\u201330 min.",
            "tags": ["Barbell", "Pull-up bar", "24\u201332 min"],
        },
        {
            "id": "olympic", "type": "O", "name": "Clean & Jerk",
            "cycle_label": "Olympic \u00b7 W4/4 \u2014 TEST", "scheme": "Heavy single + 4\u00d71+1@85%",
            "wu": wu_clean(),
            "str": "Clean & Jerk \u2014 Build to a heavy single over 15 min.\nThen: 4\u00d7 (1 power clean + 1 split jerk) @ 85% of today's heavy.\nWeek 4: peak of the Olympic cycle \u2014 combine clean + jerk.\nFocus: fast elbows on clean, aggressive dip-drive on jerk.",
            "wod": "C&J GRIND\n5 Rounds for time:\n5 Clean & Jerks (85/125 lb)\n10 Toes-to-bar\n15 Wall Ball shots (14/20 lb)\n\nTarget: 22\u201328 min.",
            "tags": ["Barbell", "Wall ball", "24\u201330 min"],
        },
        {
            "id": "gymnastics", "type": "G", "name": "HSPU / Gymnastics",
            "cycle_label": "Misfit HSPU \u00b7 W4/6", "scheme": "HS holds 6 min (faster) + HSPU test",
            "wu": wu_gymnastics(),
            "str": "Handstand Holds \u2014 Accumulate 6 min total (18 min cap)\nFaster than Week 2. This is your deload after the W3 peak.\n\nDB Wall Press: 3\u00d715 (increase weight only if W3 felt easy).",
            "wod": "HSPU TEST \u2014 Week 4\n2 Rounds:\nClimb the strict HSPU ladder by 1s\nRest 90 sec\nClimb the kipping HSPU ladder by 2s\nRest 3 min\n\nKick down before you fail on strict HSPU.\nHandstand hold: 10 \u00d7 9\u201311 sec.\nCompare scores to Week 2 \u2014 this is your progress check.",
            "tags": ["Bodyweight", "Gymnastics", "25\u201335 min"],
        },
        {
            "id": "press", "type": "S", "name": "Push Press \u2014 1RM Test",
            "cycle_label": "Press Cycle \u00b7 W4/4 \u2014 TEST", "scheme": "Work to 1RM",
            "wu": wu_press(),
            "str": "Push Press \u2014 Work to a 1RM.\nThen: 2\u00d75 @ 70% (speed presses).\nThis closes the 4-week press cycle. Record your number.\nOptional: attempt strict press 1RM after 10+ min full rest.",
            "wod": "PRESS TEST FINISHER\n4 Rounds:\n5 Push Press (@ 70% of today's 1RM)\n10 Pull-ups\n15 Push-ups\n20 Air squats\n\nLight and fast \u2014 recover after the heavy press work.\nTarget: 15\u201320 min.",
            "tags": ["Barbell", "15\u201322 min"],
        },
        {
            "id": "metcon_a", "type": "M", "name": "KB + Burpees AMRAP",
            "cycle_label": "MetCon A", "scheme": "AMRAP 20 min",
            "wu": wu_kb(),
            "str": None,
            "wod": "BURPEE BOSS\nAMRAP 20 min:\n5 Burpee box jumps (or burpee broad jumps)\n10 KB Swings (44/70 lb)\n15 KB Goblet Squats (same)\n200m run\n\nScale: reduce KB weight, replace box jumps with regular burpees.\nTarget: 5\u20136+ rounds.",
            "tags": ["KB", "Running", "20 min AMRAP"],
        },
        {
            "id": "metcon_b", "type": "M", "name": "The Closer",
            "cycle_label": "MetCon B \u00b7 Month-End Benchmark", "scheme": "For time",
            "wu": [
                "2 min easy jog",
                "10 arm + hip circles each direction",
                "10 air squats + 10 push-ups + 5 pull-ups (1 preview round)",
                "5 wall ball throws + 5 KB swings (light preview of movements)",
            ],
            "str": None,
            "wod": "THE CLOSER \u2014 month-end benchmark\nFor time:\n1.5 km run\n50 Wall Ball shots (14/20 lb)\n40 KB Swings (35/53 lb)\n30 Pull-ups\n20 Deadlifts (155/225 lb)\n10 Clean & Jerks (95/135 lb)\n1.5 km run\n\nEvery piece of equipment. One final test.\nScale: reduce all reps by 30% if needed. Finish the run.\nTarget: 38\u201352 min.",
            "tags": ["All equipment", "~3 km running", "40\u201355 min"],
        },
        {
            "id": "trail_mid", "type": "T", "name": "Trail Run \u2014 Hill Reps", "km": "9 km",
            "cycle_label": "Trail Run \u00b7 Suggested: Tuesday", "scheme": "9 km \u2014 hill reps",
            "wu": wu_run(),
            "str": None,
            "wod": "HILL REPS \u2014 9 km\nEffort: Hard on hills, easy recovery on flat/downhill\n\n\u2192 2 km easy warm-up jog to your hill\n\u2192 6 \u00d7 uphill effort (50\u2013100 m steep section)\n  \u2013 Push hard at 90% effort (~20\u201330 sec)\n  \u2013 Walk/jog back down (full recovery)\n\u2192 3 km easy jog home\n\nHill reps build explosive leg power that transfers directly to CrossFit squats and cleans.",
            "tags": ["Trail", "9 km", "Hill reps", "~55\u201370 min"],
        },
        {
            "id": "run_session", "type": "E", "name": "Tempo Finisher", "km": "~5 km",
            "cycle_label": "Endurance Run \u00b7 Suggested: Wednesday", "scheme": "4\u00d71 km @ tempo + KB",
            "wu": wu_tempo(),
            "str": None,
            "wod": "TEMPO FINISHER \u2014 ~5 km\n4\u00d71 km at tempo effort\nRest: 90 sec easy jog between reps\n\nThen: 3 Rounds\n15 KB Swings (44/70 lb)\n10 Goblet Squats (same)\n10 Dips (chairs/box)\n\nFinal tempo run of the month \u2014 make it count.\nRecord splits and compare to Week 1.",
            "tags": ["Running", "~5 km", "KB", "38\u201348 min"],
        },
    ],
}

# =========================================================================

# =========================================================================
# SERIALIZE — base64 encode: A-Za-z0-9+/= only, safe in all contexts
# =========================================================================
import base64 as _b64
APP_VERSION = "v5"
APP_DATA_B64 = _b64.b64encode(json.dumps({
    "blocks":     {str(k): v for k, v in BLOCKS.items()},
    "weekMeta":   WEEK_META,
    "longTrails": LONG_TRAILS,
    "version":    APP_VERSION,
}).encode("utf-8")).decode("ascii")

# =========================================================================
# HTML / CSS / JS
# =========================================================================
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{{
  --bg:#fff;--bg2:#f6f6f4;--bg3:#ededea;
  --tx:#1a1a18;--tx2:#5c5c58;--tx3:#9a9a94;
  --bd:rgba(0,0,0,.08);--bd2:rgba(0,0,0,.16);
  --rad:8px;--rad-lg:12px;
  --S-bg:#EEEDFE;--S-t:#3C3489;
  --O-bg:#FAECE7;--O-t:#712B13;
  --G-bg:#E1F5EE;--G-t:#085041;
  --M-bg:#FAEEDA;--M-t:#633806;
  --T-bg:#EAF3DE;--T-t:#27500A;
  --E-bg:#E6F1FB;--E-t:#0C447C;
  --R-bg:#F1EFE8;--R-t:#5F5E5A;
}}
@media(prefers-color-scheme:dark){{
:root{{
  --bg:#1c1c1a;--bg2:#252523;--bg3:#2e2e2b;
  --tx:#e6e6e0;--tx2:#a0a09a;--tx3:#666660;
  --bd:rgba(255,255,255,.08);--bd2:rgba(255,255,255,.18);
  --S-bg:#26215C;--S-t:#CECBF6;
  --O-bg:#4A1B0C;--O-t:#F5C4B3;
  --G-bg:#04342C;--G-t:#9FE1CB;
  --M-bg:#412402;--M-t:#FAC775;
  --T-bg:#173404;--T-t:#C0DD97;
  --E-bg:#042C53;--E-t:#B5D4F4;
  --R-bg:#2C2C2A;--R-t:#D3D1C7;
}}
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--tx);padding:1rem 1.25rem;font-size:14px;}}

/* ── TABS ── */
.tab-nav{{display:flex;gap:4px;margin-bottom:1.25rem;border-bottom:0.5px solid var(--bd);padding-bottom:0;}}
.tab-btn{{background:none;border:none;padding:.5rem 1rem;font-size:14px;color:var(--tx2);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-0.5px;transition:color .12s,border-color .12s;}}
.tab-btn.active{{color:var(--tx);border-bottom-color:var(--tx);font-weight:500;}}
.tab-btn:hover:not(.active){{color:var(--tx);}}
.tab-content{{display:none;}}.tab-content.active{{display:block;}}

/* ── WEEK HEADER ── */
.week-header{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:1rem;}}
.nav-btn{{background:none;border:0.5px solid var(--bd2);border-radius:var(--rad);padding:4px 12px;font-size:16px;cursor:pointer;color:var(--tx2);transition:background .1s;}}
.nav-btn:hover{{background:var(--bg2);}}
.week-label{{font-size:16px;font-weight:500;}}
.cycle-badges{{display:flex;flex-wrap:wrap;gap:5px;margin-left:4px;}}
.cycle-badge{{font-size:10px;padding:2px 7px;border-radius:4px;font-weight:500;}}
.km-control{{margin-left:auto;display:flex;align-items:center;gap:6px;}}
.km-label{{font-size:12px;color:var(--tx3);}}
.km-input{{width:60px;padding:4px 6px;border:0.5px solid var(--bd2);border-radius:var(--rad);background:var(--bg);color:var(--tx);font-size:14px;text-align:center;}}

/* ── PALETTE ── */
.palette-hdr{{font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);margin-bottom:8px;}}
.palette{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:6px;margin-bottom:1.25rem;}}
.blk{{border-radius:var(--rad);padding:8px 10px;cursor:pointer;border:1.5px solid transparent;transition:border-color .12s,opacity .12s;position:relative;}}
.blk:hover{{border-color:var(--bd2);}}
.blk.selected{{border-color:var(--tx);}}
.blk.used{{opacity:.35;cursor:default;pointer-events:none;}}
.blk-name{{font-size:12px;font-weight:500;margin-bottom:2px;}}
.blk-cycle{{font-size:10px;opacity:.75;}}
.blk-scheme{{font-size:10px;margin-top:2px;opacity:.65;}}

/* ── WEEK GRID ── */
.grid-wrap{{overflow-x:auto;}}
.grid{{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:5px;min-width:700px;}}
.grid-col{{display:flex;flex-direction:column;gap:5px;}}
.day-hdr{{font-size:11px;font-weight:500;color:var(--tx3);text-align:center;padding:4px 0;}}
.day-date{{font-size:10px;color:var(--tx3);text-align:center;margin-top:1px;}}
.slot{{border:0.5px dashed var(--bd2);border-radius:var(--rad);padding:7px 8px;min-height:58px;cursor:pointer;transition:border-color .12s,background .12s;position:relative;}}
.slot:hover:not(.locked){{border-color:var(--tx2);background:var(--bg2);}}
.slot.ready{{border-color:var(--tx);border-style:solid;background:var(--bg2);}}
.slot.locked{{cursor:default;border-style:solid;}}
.slot-label{{font-size:10px;color:var(--tx3);margin-bottom:3px;}}
.slot-empty{{font-size:11px;color:var(--tx3);padding-top:4px;}}
.slot-blk{{border-radius:5px;padding:5px 6px;}}
.slot-blk-name{{font-size:11px;font-weight:500;}}
.slot-blk-sub{{font-size:10px;margin-top:1px;opacity:.75;}}
.slot-remove{{position:absolute;top:4px;right:5px;font-size:11px;color:var(--tx3);background:none;border:none;cursor:pointer;padding:0 2px;line-height:1;}}
.slot-remove:hover{{color:var(--tx);}}
.rest-col .slot{{background:var(--R-bg);border-color:transparent;border-style:solid;}}
.sun-slot{{background:var(--T-bg);border-color:transparent;border-style:solid;}}

/* ── PROGRESS ── */
.progress{{display:flex;gap:16px;flex-wrap:wrap;margin:1rem 0;padding:.75rem 1rem;background:var(--bg2);border-radius:var(--rad);font-size:12px;}}
.prog-item{{display:flex;align-items:center;gap:6px;}}
.prog-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0;}}
.prog-val{{font-weight:500;}}

/* ── DETAIL PANEL ── */
.detail{{border:0.5px solid var(--bd);border-radius:var(--rad-lg);padding:1.25rem;margin-top:1rem;background:var(--bg);}}
.detail-top{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:1rem;}}
.detail-icon{{width:44px;height:44px;border-radius:var(--rad);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:500;text-align:center;line-height:1.3;flex-shrink:0;}}
.detail-title{{font-size:16px;font-weight:500;}}
.detail-sub{{font-size:12px;color:var(--tx3);}}
.detail-tags{{margin-left:auto;display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;}}
.detail-tag{{font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid var(--bd);color:var(--tx2);}}
.sec-lbl{{font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);margin:0 0 6px;}}
.wu-list{{border:0.5px solid var(--bd);border-radius:var(--rad);padding:.5rem .75rem;margin-bottom:1rem;}}
.wu-item{{font-size:13px;color:var(--tx2);padding:4px 0;border-bottom:0.5px solid var(--bd);display:flex;align-items:flex-start;gap:8px;}}
.wu-item:last-child{{border-bottom:none;}}
.wu-dot{{width:5px;height:5px;border-radius:50%;background:var(--bd2);margin-top:6px;flex-shrink:0;}}
.wod-box{{border-radius:var(--rad);padding:.75rem 1rem;}}
.wod-text{{font-size:13px;line-height:1.75;white-space:pre-line;color:var(--tx2);}}
.str-box{{border-radius:var(--rad);padding:.75rem 1rem;margin-bottom:.75rem;}}

/* ── CALENDAR (tab 2) ── */
.cal-grid{{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;}}
.cal-dow{{font-size:11px;color:var(--tx3);text-align:center;padding:4px 0 6px;}}
.cal-day{{border:0.5px solid var(--bd);border-radius:var(--rad);padding:7px 8px;min-height:72px;cursor:pointer;background:var(--bg);transition:border-color .12s;}}
.cal-day:hover:not(.cal-rest){{border-color:var(--bd2);}}
.cal-day.cal-sel{{border:1.5px solid var(--tx2);}}
.cal-day.cal-rest{{cursor:default;background:var(--bg2);}}
.cal-day.cal-empty{{border:none;background:none;cursor:default;min-height:0;}}
.cal-dnum{{font-size:12px;font-weight:500;color:var(--tx2);}}
.cal-badge{{font-size:10px;padding:2px 5px;border-radius:4px;margin-top:4px;display:inline-block;font-weight:500;line-height:1.4;}}
.cal-name{{font-size:10px;color:var(--tx3);margin-top:3px;line-height:1.3;}}
.cal-km{{font-size:10px;font-weight:500;margin-top:2px;}}
.cal-detail{{border:0.5px solid var(--bd);border-radius:var(--rad-lg);padding:1.25rem;margin-top:.85rem;background:var(--bg);}}
.legend{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1.25rem;}}
.badge-sm{{font-size:11px;padding:3px 7px;border-radius:5px;font-weight:500;display:inline-block;}}
@media(max-width:640px){{
  .palette{{grid-template-columns:repeat(2,1fr);}}
  .grid{{grid-template-columns:repeat(7,minmax(90px,1fr));}}
  body{{padding:.75rem;}}
}}
</style>
</head>
<body>

<!-- ═══════ TABS ═══════ -->
<div style="display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:.25rem">
  <div>
    <h1 style="font-size:20px;font-weight:500;margin-bottom:2px">May 2026 &mdash; CrossFit + Trail Running</h1>
    <p style="font-size:12px;color:var(--tx3)">Trail: Tue &amp; Sun &nbsp;&middot;&nbsp; 25&ndash;27 km/week &nbsp;&middot;&nbsp; 4-week cycles &nbsp;&middot;&nbsp; Rest: Saturday</p>
  </div>
  <span id="ver-badge" style="font-size:10px;padding:2px 8px;border-radius:4px;background:var(--bg3);color:var(--tx3);font-family:monospace"></span>
</div>
<div class="tab-nav">
  <button class="tab-btn active" onclick="switchTab('planner')">Week Planner</button>
  <button class="tab-btn" onclick="switchTab('calendar')">Month Calendar</button>
</div>

<!-- ═══════ TAB 1: WEEK PLANNER ═══════ -->
<div id="tab-planner" class="tab-content active">

  <!-- Week header -->
  <div class="week-header">
    <button class="nav-btn" id="btn-prev" onclick="shiftWeek(-1)">&#8592;</button>
    <div>
      <div class="week-label" id="wk-label"></div>
      <div class="cycle-badges" id="wk-cycles"></div>
    </div>
    <button class="nav-btn" id="btn-next" onclick="shiftWeek(1)">&#8594;</button>
    <div class="km-control">
      <span class="km-label">Weekly target</span>
      <input class="km-input" type="number" id="km-input" min="10" max="60" onchange="setKm(+this.value)">
      <span style="font-size:13px;color:var(--tx3)">km</span>
    </div>
  </div>

  <!-- Palette -->
  <div class="palette-hdr" id="pal-hdr">Available blocks this week &mdash; click to select, then click a slot to place</div>
  <div class="palette" id="palette"></div>

  <!-- Week grid -->
  <div class="grid-wrap">
    <div class="grid" id="week-grid"></div>
  </div>

  <!-- Progress -->
  <div class="progress" id="progress"></div>

  <!-- Detail panel -->
  <div id="detail-panel" style="display:none"></div>
</div>

<!-- ═══════ TAB 2: MONTH CALENDAR ═══════ -->
<div id="tab-calendar" class="tab-content">
  <div class="legend" id="legend"></div>
  <div class="cal-grid" id="cal-grid">
    <div class="cal-dow">Mon</div><div class="cal-dow">Tue</div><div class="cal-dow">Wed</div>
    <div class="cal-dow">Thu</div><div class="cal-dow">Fri</div><div class="cal-dow">Sat</div><div class="cal-dow">Sun</div>
  </div>
  <div id="cal-detail"></div>
</div>

<!-- ═══════ JAVASCRIPT ═══════ -->
<script>
// ── Decode base64 payload (bulletproof: only A-Za-z0-9+/= chars) ──
(function() {{
  try {{
    var _d = JSON.parse(atob("{APP_DATA_B64}"));
    window.BLOCKS      = _d.blocks;
    window.WEEK_META   = _d.weekMeta;
    window.LONG_TRAILS = _d.longTrails;
    window.APP_VERSION = _d.version;
  }} catch(e) {{
    document.body.innerHTML = '<div style="padding:2rem;color:red;font-family:monospace">' +
      '<b>Data load error ('+e+')</b></div>';
  }}
}})();
var BLOCKS      = window.BLOCKS;
var WEEK_META   = window.WEEK_META;
var LONG_TRAILS = window.LONG_TRAILS;

// ── Type config ──
var TYPE = {{
  S: {{l:"Strength",   bg:"var(--S-bg)", tc:"var(--S-t)"}},
  O: {{l:"Olympic",    bg:"var(--O-bg)", tc:"var(--O-t)"}},
  G: {{l:"Gymnastics", bg:"var(--G-bg)", tc:"var(--G-t)"}},
  M: {{l:"MetCon",     bg:"var(--M-bg)", tc:"var(--M-t)"}},
  T: {{l:"Trail Run",  bg:"var(--T-bg)", tc:"var(--T-t)"}},
  E: {{l:"Endurance",  bg:"var(--E-bg)", tc:"var(--E-t)"}},
  R: {{l:"Rest",       bg:"var(--R-bg)", tc:"var(--R-t)"}}
}};

// ── App state ──
var state = {{
  week: 0,
  km: [25,25,27,26],
  assignments: {{"0":{{}},"1":{{}},"2":{{}},"3":{{}}}},
  selected: null,
  detailBlock: null
}};

var DAYS  = ["mon","tue","wed","thu","fri"];
var TIMES = ["am","pm"];
var DAY_LABELS = ["Mon","Tue","Wed","Thu","Fri"];

// ── State persistence ──
function saveState() {{
  try {{ localStorage.setItem("cf_planner_v3", JSON.stringify(state)); }} catch(e) {{}}
}}
function loadState() {{
  try {{
    var s = localStorage.getItem("cf_planner_v3");
    if (s) {{
      var parsed = JSON.parse(s);
      if (parsed.assignments) {{
        state.week = parsed.week || 0;
        state.km   = parsed.km   || [25,25,27,26];
        state.assignments = parsed.assignments;
        for (var w = 0; w < 4; w++) {{
          if (!state.assignments[String(w)]) state.assignments[String(w)] = {{}};
        }}
      }}
    }}
  }} catch(e) {{}}
}}

// ── Block helpers ──
function blocksForWeek(w) {{ return BLOCKS[w] || []; }}
function assignmentsForWeek(w) {{ return state.assignments[String(w)] || {{}}; }}
function placedIds(w) {{
  var a = assignmentsForWeek(w), ids = {{}};
  Object.values(a).forEach(function(id){{ if(id) ids[id] = true; }});
  return ids;
}}
function findBlock(w, id) {{
  return blocksForWeek(w).find(function(b){{ return b.id === id; }}) || null;
}}

// ── Slot key helper ──
function slotKey(day, time) {{ return day + "_" + time; }}

// ── KM planned ──
function kmPlanned(w) {{
  var ids = placedIds(w);
  var total = 0;
  if (ids["trail_mid"])  total += (w === 2 ? 10 : 9);
  if (ids["run_session"]) total += 5;
  total += LONG_TRAILS[w].km.replace(/[^0-9]/g,"") * 1;
  return total;
}}

// ── Tab switching ──
function switchTab(name) {{
  document.querySelectorAll(".tab-content").forEach(function(el){{ el.classList.remove("active"); }});
  document.querySelectorAll(".tab-btn").forEach(function(el){{ el.classList.remove("active"); }});
  document.getElementById("tab-"+name).classList.add("active");
  var btns = document.querySelectorAll(".tab-btn");
  btns.forEach(function(b){{ if(b.textContent.toLowerCase().includes(name.substring(0,4))) b.classList.add("active"); }});
  if (name === "calendar") renderCalendar();
}}

// ── Week navigation ──
function shiftWeek(delta) {{
  state.week = Math.max(0, Math.min(3, state.week + delta));
  state.selected = null;
  state.detailBlock = null;
  saveState();
  renderPlanner();
}}
function setKm(v) {{
  if (v >= 10 && v <= 60) {{
    state.km[state.week] = v;
    saveState();
    renderProgress();
  }}
}}

// ── Select block ──
function selectBlock(id) {{
  state.selected = (state.selected === id) ? null : id;
  renderPalette();
}}

// ── Click a grid slot ──
function clickSlot(day, time) {{
  var w   = state.week;
  var key = slotKey(day, time);
  var a   = assignmentsForWeek(w);
  var cur = a[key];

  if (cur) {{
    // clicking a placed block: show its detail
    var blk = findBlock(w, cur);
    if (blk) showDetail(blk);
    return;
  }}

  if (state.selected) {{
    // place the selected block
    var placed = placedIds(w);
    if (placed[state.selected]) return; // already placed elsewhere
    state.assignments[String(w)][key] = state.selected;
    state.selected = null;
    saveState();
    renderPlanner();
  }}
}}

// ── Remove block from slot ──
function removeSlot(day, time) {{
  var w   = state.week;
  var key = slotKey(day, time);
  var a   = assignmentsForWeek(w);
  if (a[key]) {{
    var id = a[key];
    delete state.assignments[String(w)][key];
    state.selected = null;
    // hide detail if it was showing this block
    if (state.detailBlock && state.detailBlock.id === id) {{
      state.detailBlock = null;
      document.getElementById("detail-panel").style.display = "none";
    }}
    saveState();
    renderPlanner();
  }}
}}

// ── Show detail ──
function showDetail(blk) {{
  state.detailBlock = blk;
  var tp = TYPE[blk.type] || TYPE.S;
  var h  = "<div class='detail'>";
  h += "<div class='detail-top'>";
  h += "<div class='detail-icon' style='background:"+tp.bg+";color:"+tp.tc+"'>"+(tp.l.replace(" ","<br>"))+"</div>";
  h += "<div><div class='detail-title'>"+blk.name+"</div>";
  h += "<div class='detail-sub'>"+blk.cycle_label+(blk.km?" &nbsp;\u00b7 "+blk.km:"")+"</div></div>";
  h += "<div class='detail-tags'>"+(blk.tags||[]).map(function(t){{return"<span class='detail-tag'>"+t+"</span>";}}).join("")+"</div>";
  h += "</div>";

  if (blk.wu && blk.wu.length) {{
    h += "<div class='sec-lbl' style='margin-top:.25rem'>Warm-up &nbsp;&middot;&nbsp; 6&ndash;8 min</div>";
    h += "<div class='wu-list'>"+blk.wu.map(function(i){{
      return "<div class='wu-item'><div class='wu-dot'></div><div>"+i+"</div></div>";
    }}).join("")+"</div>";
  }}

  if (blk.str) {{
    h += "<div class='sec-lbl'>Strength / Skill work</div>";
    h += "<div class='str-box' style='background:"+tp.bg+"'>";
    h += "<div class='wod-text' style='color:"+tp.tc+"'>"+blk.str+"</div></div>";
  }}

  var wodLabel = blk.type==="T"?"Run plan":blk.type==="E"?"Endurance WOD":"Workout of the Day";
  h += "<div class='sec-lbl'>"+wodLabel+"</div>";
  h += "<div class='wod-box' style='background:var(--bg2);border:0.5px solid var(--bd)'>";
  h += "<div class='wod-text'>"+blk.wod+"</div></div>";
  h += "</div>";

  var panel = document.getElementById("detail-panel");
  panel.innerHTML = h;
  panel.style.display = "block";
  panel.scrollIntoView({{behavior:"smooth",block:"nearest"}});
}}

// ── Render palette ──
function renderPalette() {{
  var w     = state.week;
  var blks  = blocksForWeek(w);
  var placed = placedIds(w);
  var sel   = state.selected;
  var html  = "";
  blks.forEach(function(b) {{
    var tp   = TYPE[b.type] || TYPE.S;
    var isUsed = !!placed[b.id];
    var isSel  = sel === b.id;
    var cls  = "blk"+(isUsed?" used":"")+(isSel?" selected":"");
    html += "<div class='"+cls+"' style='background:"+tp.bg+"' onclick='selectBlock(\""+b.id+"\")'>";
    html += "<div class='blk-name' style='color:"+tp.tc+"'>"+b.name+"</div>";
    html += "<div class='blk-cycle' style='color:"+tp.tc+"'>"+b.cycle_label+"</div>";
    html += "<div class='blk-scheme' style='color:"+tp.tc+"'>"+b.scheme+"</div>";
    html += "</div>";
  }});
  document.getElementById("palette").innerHTML = html;

  var total = blks.length;
  var usedCount = Object.keys(placed).length;
  document.getElementById("pal-hdr").textContent =
    sel ? "Block selected \u2014 click an empty slot to place it (or click the block again to deselect)"
        : "Available blocks ("+(total-usedCount)+" remaining) \u2014 click a block to select, then click a slot";
}}

// ── Render week grid ──
function renderGrid() {{
  var w    = state.week;
  var meta = WEEK_META[w];
  var a    = assignmentsForWeek(w);
  var sel  = state.selected;
  var html = "";

  // Mon–Fri
  DAYS.forEach(function(day, di) {{
    html += "<div class='grid-col'>";
    html += "<div class='day-hdr'>"+DAY_LABELS[di]+"</div>";
    html += "<div class='day-date' style='font-size:10px;color:var(--tx3);text-align:center'>"+meta.dates[di]+"</div>";
    TIMES.forEach(function(t) {{
      var key  = slotKey(day, t);
      var blkId = a[key];
      var blk  = blkId ? findBlock(w, blkId) : null;
      var isReady = !!sel && !blkId;
      html += "<div class='slot"+(isReady?" ready":"")+"' onclick='clickSlot(\""+day+"\",\""+t+"\")'>";
      html += "<div class='slot-label'>"+t.toUpperCase()+"</div>";
      if (blk) {{
        var tp = TYPE[blk.type] || TYPE.S;
        html += "<div class='slot-blk' style='background:"+tp.bg+"'>";
        html += "<div class='slot-blk-name' style='color:"+tp.tc+"'>"+blk.name+"</div>";
        html += "<div class='slot-blk-sub' style='color:"+tp.tc+"'>"+blk.scheme+"</div>";
        html += "</div>";
        html += "<button class='slot-remove' onclick='event.stopPropagation();removeSlot(\""+day+"\",\""+t+"\")' title='Return to palette'>\u00d7</button>";
      }} else {{
        html += "<div class='slot-empty'>"+(isReady?"+ place":"+ add")+"</div>";
      }}
      html += "</div>";
    }});
    html += "</div>";
  }});

  // Saturday REST
  html += "<div class='grid-col rest-col'>";
  html += "<div class='day-hdr' style='color:var(--R-t)'>Sat</div>";
  html += "<div class='day-date' style='font-size:10px;color:var(--tx3);text-align:center'>"+meta.dates[5]+"</div>";
  html += "<div class='slot locked' style='background:var(--R-bg);border-color:transparent;min-height:120px;display:flex;align-items:center;justify-content:center'>";
  html += "<div style='text-align:center;'><div style='font-size:13px;font-weight:500;color:var(--R-t)'>REST</div>";
  html += "<div style='font-size:11px;color:var(--R-t);opacity:.7;margin-top:4px'>Recovery day</div></div>";
  html += "</div>";
  html += "</div>";

  // Sunday LONG TRAIL (fixed)
  var lt = LONG_TRAILS[w];
  html += "<div class='grid-col'>";
  html += "<div class='day-hdr' style='color:var(--T-t)'>Sun</div>";
  html += "<div class='day-date' style='font-size:10px;color:var(--tx3);text-align:center'>"+meta.dates[6]+"</div>";
  html += "<div class='slot sun-slot locked' style='min-height:120px;cursor:pointer' onclick='showSundayDetail("+w+")'>";
  html += "<div class='slot-label' style='color:var(--T-t)'>TRAIL</div>";
  html += "<div class='slot-blk' style='background:transparent'>";
  html += "<div class='slot-blk-name' style='color:var(--T-t)'>"+lt.name+"</div>";
  html += "<div style='font-size:18px;font-weight:500;color:var(--T-t);margin:4px 0 2px'>"+lt.km+"</div>";
  html += "<div class='slot-blk-sub' style='color:var(--T-t)'>Click for plan</div>";
  html += "</div></div>";
  html += "</div>";

  document.getElementById("week-grid").innerHTML = html;
}}

// ── Show Sunday detail ──
function showSundayDetail(w) {{
  var lt = LONG_TRAILS[w];
  var tp = TYPE["T"];
  var b  = {{
    name: lt.name, type: "T", cycle_label: "Long Trail Run \u00b7 Sunday (fixed)",
    km: lt.km, wu: lt.wu, str: null, wod: lt.wod, tags: [lt.km, "Trail", "~60\u201390 min"]
  }};
  showDetail(b);
}}

// ── Render progress ──
function renderProgress() {{
  var w     = state.week;
  var a     = assignmentsForWeek(w);
  var placed = Object.keys(a).filter(function(k){{ return !!a[k]; }}).length;
  var total  = blocksForWeek(w).length;
  var twoADays = 0;
  DAYS.forEach(function(d) {{
    if (a[slotKey(d,"am")] && a[slotKey(d,"pm")]) twoADays++;
  }});
  var kmPl   = kmPlanned(w);
  var kmTgt  = state.km[w];
  var kmPct  = Math.min(100, Math.round(kmPl/kmTgt*100));

  var html = "";
  html += "<div class='prog-item'><div class='prog-dot' style='background:var(--tx2)'></div>";
  html += "<span class='prog-val'>"+placed+"/"+total+"</span><span style='color:var(--tx3)'>&nbsp;blocks placed</span></div>";
  html += "<div class='prog-item'><div class='prog-dot' style='background:var(--S-t)'></div>";
  html += "<span class='prog-val'>"+twoADays+"/4</span><span style='color:var(--tx3)'>&nbsp;two-a-days</span></div>";
  html += "<div class='prog-item'><div class='prog-dot' style='background:var(--T-t)'></div>";
  html += "<span class='prog-val'>"+kmPl+"/"+kmTgt+" km</span><span style='color:var(--tx3)'>&nbsp;running planned</span></div>";

  if (twoADays === 4 && placed === total) {{
    html += "<div class='prog-item' style='margin-left:auto'>";
    html += "<span style='color:var(--T-t);font-weight:500'>Week complete \u2713</span></div>";
  }} else if (twoADays > 4) {{
    html += "<div class='prog-item' style='margin-left:auto'>";
    html += "<span style='color:var(--O-t)'>"+twoADays+" two-a-days scheduled (aim for 4)</span></div>";
  }}

  document.getElementById("progress").innerHTML = html;
  // update km input
  var inp = document.getElementById("km-input");
  if (inp) inp.value = state.km[w];
}}

// ── Render week header ──
function renderHeader() {{
  var w    = state.week;
  var meta = WEEK_META[w];
  document.getElementById("wk-label").textContent = meta.label;
  document.getElementById("btn-prev").disabled = (w === 0);
  document.getElementById("btn-next").disabled = (w === 3);

  var cycles = [
    {{l:"Squat W"+meta.cycle+"/4", tp:"S"}},
    {{l:"Deadlift W"+meta.cycle+"/4", tp:"S"}},
    {{l:"Olympic W"+meta.cycle+"/4", tp:"O"}},
    {{l:"HSPU W"+meta.cycle+"/6", tp:"G"}},
    {{l:"Press W"+meta.cycle+"/4", tp:"S"}},
  ];
  var html = cycles.map(function(c) {{
    var tp = TYPE[c.tp];
    return "<span class='cycle-badge' style='background:"+tp.bg+";color:"+tp.tc+"'>"+c.l+"</span>";
  }}).join("");
  document.getElementById("wk-cycles").innerHTML = html;
}}

// ── Render full planner ──
function renderPlanner() {{
  renderHeader();
  renderPalette();
  renderGrid();
  renderProgress();
  // hide old detail if week changed
  if (state.detailBlock) {{
    var stillValid = findBlock(state.week, state.detailBlock.id);
    if (!stillValid) {{
      state.detailBlock = null;
      document.getElementById("detail-panel").style.display = "none";
    }}
  }}
}}

// ═══════════════════════════════════════════════════════════
// MONTH CALENDAR DATA (fixed base schedule)
// ═══════════════════════════════════════════════════════════
var CAL = {{
  1: {{t:"M",n:"KB MetCon"}},
  2: {{t:"R",n:"Rest Day"}},
  3: {{t:"T",n:"Trail Run",km:"10 km"}},
  4: {{t:"S",n:"Back Squat",sub:"5\u00d75 @ 75%"}},
  5: {{t:"T",n:"Trail Run",km:"9 km"}},
  6: {{t:"E",n:"Tempo Run",km:"~5 km"}},
  7: {{t:"O",n:"Hang Pwr Clean",sub:"3RM then 3\u00d73"}},
  8: {{t:"G",n:"HSPU / Pull-ups",sub:"Misfit W1"}},
  9: {{t:"R",n:"Rest Day"}},
  10: {{t:"T",n:"Trail Run",km:"11 km"}},
  11: {{t:"S",n:"Deadlift",sub:"5\u00d73 @ 80%"}},
  12: {{t:"T",n:"Trail Run",km:"9 km"}},
  13: {{t:"E",n:"200m Intervals",km:"~5 km"}},
  14: {{t:"O",n:"Power Snatch",sub:"Heavy single"}},
  15: {{t:"M",n:"KB Storm",sub:"AMRAP 20"}},
  16: {{t:"R",n:"Rest Day"}},
  17: {{t:"T",n:"Trail Run",km:"11 km"}},
  18: {{t:"S",n:"Back Squat",sub:"3\u00d73 @ 88%"}},
  19: {{t:"T",n:"Trail Run",km:"10 km"}},
  20: {{t:"E",n:"Tempo + KB",km:"~5 km"}},
  21: {{t:"O",n:"Power Clean",sub:"2RM then 4\u00d72"}},
  22: {{t:"G",n:"HSPU / Pull-ups",sub:"Misfit W3"}},
  23: {{t:"R",n:"Rest Day"}},
  24: {{t:"T",n:"Trail Run",km:"12 km"}},
  25: {{t:"S",n:"Squat 1RM Test",sub:"Test week"}},
  26: {{t:"T",n:"Trail Run",km:"9 km"}},
  27: {{t:"E",n:"Tempo Finisher",km:"~5 km"}},
  28: {{t:"O",n:"Clean & Jerk",sub:"Heavy single"}},
  29: {{t:"S",n:"Deadlift 1RM",sub:"Test week"}},
  30: {{t:"R",n:"Rest Day"}},
  31: {{t:"T",n:"Trail Run",km:"12 km"}},
}};

var calSel = null;

function renderCalendar() {{
  var grid = document.getElementById("cal-grid");
  // Remove old day cells (keep the 7 header divs)
  while (grid.children.length > 7) grid.removeChild(grid.lastChild);

  // Legend
  var leg = document.getElementById("legend");
  var types = [["S","Strength"],["O","Olympic"],["G","Gymnastics"],["M","MetCon"],["T","Trail Run"],["E","Endurance"],["R","Rest"]];
  leg.innerHTML = types.map(function(x) {{
    var tp = TYPE[x[0]];
    return "<span class='badge-sm' style='background:"+tp.bg+";color:"+tp.tc+"'>"+x[1]+"</span>";
  }}).join("");

  // May 1 = Friday = index 4 (Mon=0 … Sun=6)
  for (var i = 0; i < 4; i++) {{
    var e = document.createElement("div"); e.className="cal-day cal-empty"; grid.appendChild(e);
  }}

  for (var d = 1; d <= 31; d++) {{
    var cd  = CAL[d];
    var tp  = TYPE[cd.t];
    var div = document.createElement("div");
    div.className = "cal-day" + (cd.t==="R"?" cal-rest":"");
    var inner = "<div class='cal-dnum'>"+d+"</div>";
    inner += "<div class='cal-badge' style='background:"+tp.bg+";color:"+tp.tc+"'>"+tp.l+"</div>";
    inner += "<div class='cal-name'>"+cd.n+"</div>";
    if (cd.km) inner += "<div class='cal-km' style='color:"+tp.tc+"'>"+cd.km+"</div>";
    if (cd.sub) inner += "<div style='font-size:10px;color:var(--tx3);margin-top:2px'>"+cd.sub+"</div>";
    div.innerHTML = inner;
    if (cd.t !== "R") {{
      (function(day, el) {{
        el.addEventListener("click", function() {{ openCalDay(day, el); }});
      }})(d, div);
    }}
    grid.appendChild(div);
  }}
}}

function openCalDay(d, el) {{
  if (calSel === el) {{
    calSel.classList.remove("cal-sel");
    calSel = null;
    document.getElementById("cal-detail").innerHTML = "";
    return;
  }}
  if (calSel) calSel.classList.remove("cal-sel");
  calSel = el; el.classList.add("cal-sel");

  var cd  = CAL[d];
  var tp  = TYPE[cd.t];
  var wkIdx = d <= 10 ? 0 : d <= 17 ? 1 : d <= 24 ? 2 : 3;
  var blk = null;
  if (cd.t !== "T" || (d !== 10 && d !== 17 && d !== 24 && d !== 31)) {{
    blk = findBlock(wkIdx, cd.t==="T" ? "trail_mid" : cd.t==="E" ? "run_session" :
      cd.t==="S" ? (d<=11||d===25||d===29 ? "squat" : "press") :
      cd.t==="O" ? "olympic" : cd.t==="G" ? "gymnastics" : "metcon_a");
  }}
  if (cd.t==="T" && (d===10||d===17||d===24||d===31)) {{
    showSundayDetail(wkIdx);
    return;
  }}
  if (blk) {{ showDetail(blk); return; }}

  // fallback card
  var days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  var dayName = days[(d+3)%7];
  var h = "<div class='cal-detail'>";
  h += "<div class='detail-top'>";
  h += "<div class='detail-icon' style='background:"+tp.bg+";color:"+tp.tc+"'>"+tp.l.replace(" ","<br>")+"</div>";
  h += "<div><div class='detail-title'>May "+d+" \u2014 "+dayName+"</div>";
  h += "<div class='detail-sub'>"+cd.n+(cd.km?" \u00b7 "+cd.km:"")+"</div></div></div>";
  h += "<p style='font-size:13px;color:var(--tx2);margin-top:.5rem'>Open the Week Planner tab to assign and view detailed workouts for this day.</p>";
  h += "</div>";
  document.getElementById("cal-detail").innerHTML = h;
  el.scrollIntoView({{behavior:"smooth",block:"nearest"}});
}}

// ═══════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════
function init() {{
  // Show version badge — confirms correct deployment
  var vb = document.getElementById('ver-badge');
  if (vb) vb.textContent = window.APP_VERSION || 'unknown';

  loadState();
  renderPlanner();
}}
init();
</script>
</body>
</html>"""

components.html(HTML, height=1800, scrolling=True)
