import streamlit as st
import streamlit.components.v1 as components
import json
import base64 as _b64

st.set_page_config(
    page_title="CrossFit + Trail Run - May 2026",
    page_icon=":runner:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    "<style>.block-container{padding-top:.75rem;max-width:1120px;}"
    "header{display:none!important;}#MainMenu{display:none;}footer{display:none;}</style>",
    unsafe_allow_html=True,
)

# ============================================================
# DATA
# ============================================================
WEEK_META = [
    {"label": "Week 1 - May 4-10",  "km": 25, "cycle": 1, "dates": ["Mon 4","Tue 5","Wed 6","Thu 7","Fri 8","Sat 9","Sun 10"]},
    {"label": "Week 2 - May 11-17", "km": 25, "cycle": 2, "dates": ["Mon 11","Tue 12","Wed 13","Thu 14","Fri 15","Sat 16","Sun 17"]},
    {"label": "Week 3 - May 18-24", "km": 27, "cycle": 3, "dates": ["Mon 18","Tue 19","Wed 20","Thu 21","Fri 22","Sat 23","Sun 24"]},
    {"label": "Week 4 - May 25-31", "km": 26, "cycle": 4, "dates": ["Mon 25","Tue 26","Wed 27","Thu 28","Fri 29","Sat 30","Sun 31"]},
]

LONG_TRAILS = [
    {"km": "11 km", "name": "Long Trail Run",
     "wu": ["3 min walk then easy jog to trail","10 high knees + 10 butt kicks","10 walking lunges each leg","10 leg swings each direction","4 x 20 sec build-up strides"],
     "wod": "LONG TRAIL - 11 km\nEffort: Easy to moderate (Zone 2, Zone 3 on climbs)\n\nkm 0-3: pure easy, find your trail legs\nkm 3-9: steady effort, let terrain dictate\nkm 9-11: gradual build, finish feeling strong\n\nWeek 1 total with mid-week runs: approx 25 km."},
    {"km": "11 km", "name": "Recovery Trail Run",
     "wu": ["3 min walk then very easy jog to trail","8 leg swings front/back each leg","8 hip circles each direction","2 min easy jog - check in with your body"],
     "wod": "RECOVERY TRAIL - 11 km\nEffort: Easy throughout (Zone 1-2).\n\nFull run at conversational pace - you should be able to sing.\nWalk any tight or technical section.\nPost-run: 5 min easy walk + hip flexors, calves, hamstrings stretch."},
    {"km": "12 km", "name": "Long Trail Run",
     "wu": ["3 min walk then easy jog to trail","10 high knees + 10 butt kicks","10 walking lunges each leg","4 x 20 sec easy strides - do not go too hard, 12 km ahead"],
     "wod": "LONG TRAIL - 12 km\nYour longest single run of the month.\n\nkm 0-3: fully easy, let body warm into it\nkm 3-9: comfortable effort, enjoy the scenery\nkm 9-11: build slightly if feeling good\nkm 11-12: easy cool-down back home\n\nCarry water and a gel/dates if going over 75 min."},
    {"km": "12 km", "name": "Final Trail Run",
     "wu": ["3 min walk then easy jog - savour this last run","10 high knees + 10 butt kicks","10 walking lunges each leg","10 leg swings each direction"],
     "wod": "FINAL TRAIL - 12 km\nThe last run of the month. Run it your way.\n\nEasy and celebratory - you have earned this\nOr push the second half if legs are good\nTry for a PB on your favourite trail segment\n\nMonth done: approx 102 km total running, full 4-week cycle complete."},
]

def wu_run():
    return ["3 min brisk walk then easy jog to trail","10 high knees + 10 butt kicks","10 leg swings front/back each leg","8 walking lunges each leg","4 x 20 sec build-up strides, easy jog back"]

def wu_tempo():
    return ["2 min easy jog, progressive","10 high knees + 10 butt kicks","10 leg swings each leg","4 x 20 sec build-up strides to tempo pace","60 sec easy jog shakeout"]

def wu_squat():
    return ["90 sec jumping jacks or jump rope","10 hip circles each direction","10 slow air squats - focus on depth and knee tracking","10 leg swings front/back each leg","Warm-up sets: 5@40%, 3@60%, 2@75% of working weight"]

def wu_deadlift():
    return ["90 sec jumping jacks or easy row","10 good mornings with PVC or empty bar","10 slow hip hinge RDLs with empty bar","Warm-up sets: 5@40%, 3@60%, 2@75%, 1@85%"]

def wu_clean():
    return ["90 sec jump rope or light jog","10 arm circles + 10 hip circles each direction","PVC: 10 pass-throughs, 10 overhead squats","Empty bar: 5 hang muscle cleans then 5 hang power cleans - 2 sets","Practice front rack: elbows high, bar on shoulders"]

def wu_snatch():
    return ["90 sec jump rope","10 large arm circles each direction","PVC: 10 overhead squats, 10 snatch-grip deadlifts","Empty bar: 3x5 hang muscle snatches then 3x3 hang power snatches","5 reps fast drop into catch position (starfish drill)"]

def wu_press():
    return ["90 sec arm circles, shoulder rolls, jumping jacks","10 PVC pass-throughs","10 strict overhead press with PVC","5 push press with empty bar - focus on dip-drive-press timing","2x5 at 40% then 50% working weight"]

def wu_gymnastics():
    return ["Shoulder Floss: 3 min per side","Rotate: thumbs-up t-spine stretch, gymnastics kips, head in/out of window in HS hold","T-Spine Peanut Rotation: 1 min each position","See Misfit Movement Index for full technique cues"]

def wu_kb():
    return ["90 sec jumping jacks","10 hip circles each direction","10 hip hinges - hands slide down shins","10 KB deadlifts with light KB","2 min: 10 KB swings + 5 goblet squats (light)"]

def wu_barbell():
    return ["90 sec arm circles, hip openers, jumping jacks","10 PVC pass-throughs","5 empty-bar deadlifts then 5 hang cleans then 5 front squats then 5 push press (one complex)","Rest 60 sec, repeat with light load"]

BLOCKS = {
    0: [  # Week 1
        {"id": "squat",    "type": "S", "name": "Back Squat",        "cycle_label": "Strength A - W1/4", "scheme": "5x5 @ 75-80%",         "wu": wu_squat(),    "str": "Back Squat - 5x5 @ 75-80% 1RM\nRest 2-3 min between sets.\nCues: big breath and brace before descent, drive knees out, chest stays tall.\nWeek 1 of 4 - establish volume at moderate intensity. Record working weight.", "wod": "SQUAT OPENER\nFor time - 21-15-9:\nBack Squats (95/135 lb)\nBurpees\n\nThen: 2 x max-rep air squats (rest 90 sec between)\n\nScale: 50-60% 1RM on barbell.\nTarget: sub-12 min for 21-15-9.", "tags": ["Barbell", "15-20 min"]},
        {"id": "deadlift", "type": "S", "name": "Deadlift",          "cycle_label": "Strength B - W1/4", "scheme": "5x3 @ 80%",             "wu": wu_deadlift(), "str": "Deadlift - 5x3 @ 80% 1RM\nRest 3 min between sets.\nCues: hips back, chest tall, lat engagement before lift, bar drags up shins.\nWeek 1 of 4 - volume base. Record working weight for progression.", "wod": "DEAD SPRINT\nFor time - 21-15-9:\nDeadlifts (155/225 lb)\nBox Jumps (24 in or broad jumps)\n\nRest 3 min, then 3 Rounds:\n15 KB Swings (35/53 lb)\n15 Push-ups\n\nTarget: sub-10 min for 21-15-9.", "tags": ["Barbell", "KB", "18-28 min"]},
        {"id": "olympic",  "type": "O", "name": "Hang Power Clean",  "cycle_label": "Olympic - W1/4",    "scheme": "3RM then 3x3@85%",       "wu": wu_clean(),    "str": "Hang Power Clean - Build to a heavy triple (3RM).\nThen: 3x3 @ 85% of today's 3RM.\nFocus: explosive hip extension, fast elbow turnover, solid catch.\nWeek 1: hang position builds positional awareness before full clean.", "wod": "CLEAN MACHINE\n4 Rounds for time:\n12 Hang Power Cleans (75/115 lb)\n12 Burpees\n15 Pull-ups\n\nRest 60 sec between rounds.\nScale: reduce load, sub ring rows for pull-ups.\nTarget: 22-30 min.", "tags": ["Barbell", "Pull-up bar", "22-30 min"]},
        {"id": "gymnastics","type":"G", "name": "HSPU - Misfit W1",  "cycle_label": "Misfit HSPU - W1/6","scheme": "HS holds 5 min + HSPU ladder","wu": wu_gymnastics(),"str": "Handstand Holds - Accumulate 5 min total (15 min cap)\nPositional focus. Push limits each set, no gaming.\n\nDB Wall Press: 3x15\nSlow and controlled. Focus on core engagement and dumbbell path.", "wod": "HSPU LADDER - Week 1\nClimb the ladder x3\nRest 3:00\nMax rep HSPU:\n  Under 10 reps - count by 1s\n  10-20 reps - count by 2s\n  20+ reps - count by 3s\n\nSub: pike push-ups or Z-press with DB.\nHandstand hold: 10 x 3-5 sec (straight line, close to wall).", "tags": ["Bodyweight", "Gymnastics", "20-30 min"]},
        {"id": "press",    "type": "S", "name": "Push Press",        "cycle_label": "Press Cycle - W1/4","scheme": "5x5 @ 75-80%",           "wu": wu_press(),    "str": "Push Press - 5x5 @ 75-80% 1RM\nRest 2 min between sets.\nCues: vertical dip (no forward lean), explosive leg drive, press to lockout, ribs down.\nWeek 1 of 4 - establish working weight and groove pattern.", "wod": "PRESS CHIPPER\n21-15-9 for time:\nPush Press (75/115 lb)\nBurpees\n\nThen: 5 min AMRAP\n5 DB Push Press each arm\n10 Push-ups\n\nTarget: sub-12 min for 21-15-9.", "tags": ["Barbell", "18-25 min"]},
        {"id": "metcon_a", "type": "M", "name": "KB MetCon",         "cycle_label": "MetCon A",          "scheme": "AMRAP 20 min",            "wu": wu_kb(),       "str": None, "wod": "KB OPENER\nAMRAP 20 min:\n10 KB Swings (35/53 lb)\n10 Goblet Squats (same KB)\n8 DB Renegade Rows (4 each side, 20/35 lb)\n12 Push-ups\n\nScale: reduce weight, keep push-ups strict.\nTarget: 6-8 rounds.", "tags": ["KB", "Dumbbell", "20 min AMRAP"]},
        {"id": "metcon_b", "type": "M", "name": "Benchmark - Frankie","cycle_label": "MetCon B - Benchmark","scheme": "21-15-9 for time",   "wu": ["90 sec jumping jacks","10 arm circles each direction","5 empty-bar thrusters","3 kipping pull-up swings","10 air squats"], "str": None, "wod": "FRANKIE\n21-15-9 for time:\nThrusters (65/95 lb)\nPull-ups\n\nBenchmark WOD - give it everything. Record your time.\n\nScale: reduce load, sub ring rows.\nTarget: sub-10 min advanced, sub-15 min intermediate.", "tags": ["Barbell", "Pull-up bar", "10-18 min"]},
        {"id": "trail_mid","type": "T", "name": "Trail Run - Hills",  "cycle_label": "Trail Run - Tuesday","scheme": "9 km - hill surges", "km": "9 km", "wu": wu_run(), "str": None, "wod": "HILL TRADER - 9 km\nEffort: Moderate with hill surges\n\nkm 0-2: easy warm-up, find rhythm\nkm 2-7: 5x hill efforts, push hard uphill (20-30 sec), recover on flat\nkm 7-9: steady cool-down effort\n\nTip: shorten stride and lean forward on climbs.", "tags": ["Trail", "9 km", "55-70 min"]},
        {"id": "run_session","type":"E","name": "Tempo Run",          "cycle_label": "Endurance - Wednesday","scheme": "5x1 km @ tempo",    "km": "5 km",  "wu": wu_tempo(), "str": None, "wod": "TEMPO GRIND - approx 5 km\n5x1 km at tempo pace (comfortably hard)\nJog 90 sec between reps\n\nThen: 3 Rounds:\n15 Push-ups\n15 Sit-ups\n15 Air squats\n(No rest between rounds)\n\nTempo = effort where you can answer but not hold a conversation.", "tags": ["Running", "5 km", "35-45 min"]},
    ],
    1: [  # Week 2
        {"id": "squat",    "type": "S", "name": "Back Squat",        "cycle_label": "Strength A - W2/4", "scheme": "5x3 @ 82-85%",         "wu": wu_squat(),    "str": "Back Squat - 5x3 @ 82-85% 1RM\nRest 2-3 min between sets.\nIncreased intensity from Week 1. Focus on speed out of the hole.", "wod": "FRONT LOADED\n3 Rounds for time:\n10 Front Squats (95/135 lb)\n20 Wall Ball shots (14/20 lb)\n15 Pull-ups\n\nScale: reduce load, break wall balls 10+10.\nTarget: 22-30 min.", "tags": ["Barbell", "Wall ball", "24-32 min"]},
        {"id": "deadlift", "type": "S", "name": "Deadlift",          "cycle_label": "Strength B - W2/4", "scheme": "4x3 @ 82.5%",           "wu": wu_deadlift(), "str": "Deadlift - 4x3 @ 82.5% 1RM\nRest 3 min between sets.\nProgression from Week 1: same reps, higher intensity.\nFocus on maintaining perfect setup on every rep.", "wod": "DEAD WEIGHT\n5 Rounds for time:\n5 Deadlifts (heavy - 275/185 lb)\n10 Box Jumps (24 in)\n15 Push-ups\n\nRest 90 sec between rounds.\nTarget: 20-26 min.", "tags": ["Barbell", "20-28 min"]},
        {"id": "olympic",  "type": "O", "name": "Power Snatch",      "cycle_label": "Olympic - W2/4",    "scheme": "Heavy single, 5x2@80%",   "wu": wu_snatch(),   "str": "Power Snatch - Build to a heavy single over 15 min.\nThen: 5x2 @ 80% of today's heavy single.\nFocus: bar close to body, aggressive hip extension, fast pull-under.\nWeek 2: snatch focus - alternates with clean in the 4-week cycle.", "wod": "SNATCH & DASH\n10 Rounds for time:\n3 Power Snatches (65/95 lb)\n6 Burpees\n9 Air squats\n\nGo unbroken on snatches every round.\nTarget: 18-24 min.", "tags": ["Barbell", "18-26 min"]},
        {"id": "gymnastics","type":"G", "name": "HSPU - Misfit W2",  "cycle_label": "Misfit HSPU - W2/6","scheme": "HS holds 6 min + ladders","wu": wu_gymnastics(),"str": "Handstand Holds - Accumulate 6 min total (18 min cap)\nFaster than Week 1. Positional focus, push limits.\n\nDB Wall Press: 3x15\nOnly increase weight if Week 1 felt easy.", "wod": "HSPU LADDERS - Week 2\n2 Rounds:\nClimb the strict HSPU ladder by 1s\nRest 90 sec\nClimb the kipping HSPU ladder by 2s\nRest 3 min\n\nKick down before you fail on strict HSPU.\nHandstand hold: 10 x 5-7 sec.", "tags": ["Bodyweight", "Gymnastics", "25-35 min"]},
        {"id": "press",    "type": "S", "name": "Strict Press",      "cycle_label": "Press Cycle - W2/4","scheme": "5x3 @ 75-80%",           "wu": wu_press(),    "str": "Strict Press - 5x3 @ 75-80% 1RM\nRest 2 min between sets.\nWeek 2 of press cycle - strict press after push press volume in W1.\nCues: ribs down, glutes tight, vertical bar path, no layback.", "wod": "SHOULDER COMPLEX\n3 Rounds:\n10 Strict Press (75/105 lb)\n10 Push Press (same)\n10 Push Jerk (same)\n(No rest between movements)\nRest 2 min between rounds\n\nThen: 50 push-up challenge, any sets.\nTarget: approx 20 min.", "tags": ["Barbell", "20-25 min"]},
        {"id": "metcon_a", "type": "M", "name": "KB Storm",          "cycle_label": "MetCon A",          "scheme": "AMRAP 20 min",            "wu": wu_kb(),       "str": None, "wod": "KB STORM\nAMRAP 20 min:\n10 KB Swings (44/70 lb)\n10 Goblet Squats (same KB)\n8 DB Renegade Rows (4 each side, 25/35 lb)\n12 Push-ups\n\nScale: reduce weights. Keep push-ups strict.\nTarget: 6-8 rounds.", "tags": ["KB", "Dumbbell", "20 min AMRAP"]},
        {"id": "metcon_b", "type": "M", "name": "Benchmark - Helen", "cycle_label": "MetCon B - Benchmark","scheme": "3 rounds for time",    "wu": ["90 sec light jog","10 arm circles each direction","5 KB deadlifts, 5 KB swings (light)","5 jumping pull-ups","10 air squats"], "str": None, "wod": "HELEN - benchmark WOD\n3 Rounds for time:\n400m run\n21 KB Swings (35/53 lb)\n12 Pull-ups\n\nRecord time. Compare across future cycles.\nTarget: sub-12 min advanced, sub-18 min intermediate.", "tags": ["KB", "Pull-up bar", "Running", "12-20 min"]},
        {"id": "trail_mid","type": "T", "name": "Trail Run - Fartlek","cycle_label": "Trail Run - Tuesday","scheme": "9 km - fartlek",     "km": "9 km",  "wu": wu_run(), "str": None, "wod": "FARTLEK - 9 km\nEffort: Moderate with unstructured speed surges\n\nkm 0-1.5: easy warm-up\nkm 1.5-7.5: pick a tree/rock and surge to it (10-30 sec), then recover. Aim for 10-15 surges.\nkm 7.5-9: easy cool-down\n\nFartlek means speed play. Run by feel, no watch splits.", "tags": ["Trail", "9 km", "Fartlek", "55-70 min"]},
        {"id": "run_session","type":"E","name": "200m Intervals",    "cycle_label": "Endurance - Wednesday","scheme": "10x200m sprints",   "km": "5 km",  "wu": wu_tempo(), "str": None, "wod": "SPEED LADDER - approx 5 km\n10x200m at 90-95% effort\nRest: walk/jog 200m between reps\n\nThen: Tabata Wall Ball\n8 Rounds: 20 sec max wall ball / 10 sec rest\nCount reps in lowest round as score.\n\nAim for consistent 200m splits within 3 sec.", "tags": ["Running", "5 km", "Wall ball", "35-45 min"]},
    ],
    2: [  # Week 3
        {"id": "squat",    "type": "S", "name": "Back Squat - Peak", "cycle_label": "Strength A - W3/4 PEAK","scheme": "3x3 @ 85-90%",     "wu": wu_squat(),    "str": "Back Squat - 3x3 @ 85-90% 1RM\nRest 3 min between sets.\nPeak week - reduce volume, increase intensity.\nFocus on perfect positioning under heavy load.", "wod": "SQUAT CLINIC\nFor time:\n50 Air squats\n40 Wall Ball shots (14/20 lb)\n30 KB Goblet Squats (44/70 lb)\n20 Front Squats (95/135 lb)\n10 Back Squats (115/185 lb)\n\nAll squats. One theme. Record total time.", "tags": ["Barbell", "KB", "Wall ball", "20-28 min"]},
        {"id": "deadlift", "type": "S", "name": "Deadlift - Peak",   "cycle_label": "Strength B - W3/4 PEAK","scheme": "3x2 @ 87.5%",      "wu": wu_deadlift(), "str": "Deadlift - 3x2 @ 87.5% 1RM\nRest 3-4 min between sets.\nNear-maximal loading. Treat each double as a serious effort.\nThis sets up next week's 1RM test.", "wod": "TRIPLE THREAT\n3 Rounds for time:\n12 Deadlifts (185/275 lb)\n9 Hang Power Cleans (95/135 lb)\n6 Push Jerks (same bar)\n12 Pull-ups\n\nScale loads to 65-70% 1RM.\nTarget: 22-30 min.", "tags": ["Barbell", "Pull-up bar", "24-32 min"]},
        {"id": "olympic",  "type": "O", "name": "Power Clean",       "cycle_label": "Olympic - W3/4",    "scheme": "2RM then 4x2@85%",        "wu": wu_clean(),    "str": "Power Clean - Build to a heavy double (2RM).\nThen: 4x2 @ 85% of today's 2RM.\nFocus: full hip extension, aggressive shrug, fast elbows.\nWeek 3: heavier loading before Clean & Jerk test week.", "wod": "CLEAN SWEEP\nFor time:\n30 Hang Squat Cleans (65/95 lb)\n30 Box Jumps\n20 Hang Squat Cleans\n20 Burpees\n10 Hang Squat Cleans\n10 Toes-to-bar\n\nScale: reduce load to weight you can cycle in sets of 5+.\nTarget: 18-26 min.", "tags": ["Barbell", "20-28 min"]},
        {"id": "gymnastics","type":"G", "name": "HSPU - Misfit W3",  "cycle_label": "Misfit HSPU - W3/6","scheme": "HS holds 7 min + kipping","wu": wu_gymnastics(),"str": "Handstand Holds - Accumulate 7 min total (20 min cap)\nPeak volume week for holds. Push limits every set.\n\nDB Wall Press: 3x15\nOnly increase weight if Week 2 felt easy.", "wod": "UNBROKEN HSPU - Week 3\nClimb the ladder x3\nRest 3:00\nMax rep HSPU:\n  Under 10 reps - count by 1s\n  10-20 reps - count by 2s\n  20+ reps - count by 3s\n\nHandstand hold: 10 x 7-9 sec.\nT-spine peanut rotation cool-down.", "tags": ["Bodyweight", "Gymnastics", "25-35 min"]},
        {"id": "press",    "type": "S", "name": "Push Jerk",         "cycle_label": "Press Cycle - W3/4","scheme": "5x3 - build to heavy triple","wu": wu_press(),  "str": "Push Jerk - Build to a heavy triple. Then 5x3 @ 80% of today's best.\nWeek 3 of press cycle - introducing jerk footwork and power transfer.\nFocus: aggressive dip-drive, punch to lockout, receive feet wide.", "wod": "JERK COMPLEX\n5 Rounds:\n3 Push Jerks (building weight)\n5 Front Squats (same bar)\n7 Push-ups (strict)\n\nRest 90 sec between rounds.\nFinisher: 3x10 DB Z-press.\nTarget: approx 25 min.", "tags": ["Barbell", "22-28 min"]},
        {"id": "metcon_a", "type": "M", "name": "Barbell Complex",   "cycle_label": "MetCon A - CFB Style","scheme": "6 rounds - rest=work", "wu": wu_barbell(),  "str": None, "wod": "THE COMPLEX (CFB Style)\n6 Rounds - rest = work time:\n6 Deadlifts\n5 Hang Power Cleans\n4 Front Squats\n3 Push Press\n2 Hang Squat Cleans\n1 Thruster\n(Same barbell throughout: 75/115 lb)\n\nDo NOT put bar down mid-complex.\nTarget: each round under 90 sec.", "tags": ["Barbell", "20-30 min"]},
        {"id": "metcon_b", "type": "M", "name": "Body Shop Chipper", "cycle_label": "MetCon B - Chipper","scheme": "For time",              "wu": ["3 min easy jog","10 high knees + 10 butt kicks","10 arm circles each direction","10 air squats + 10 push-ups (1 warm-up round)"], "str": None, "wod": "BODY SHOP\nFor time:\n1 mile run\n50 Push-ups\n800m run\n50 Sit-ups\n400m run\n50 Air squats\n200m run\n50 Lunges (alternating)\n\nScale: reduce reps to 30 each or take walk breaks.\nTarget: 30-45 min.", "tags": ["Running", "Bodyweight", "35-50 min"]},
        {"id": "trail_mid","type": "T", "name": "Trail Run - Neg Splits","cycle_label": "Trail Run - Tuesday","scheme": "10 km - negative splits","km": "10 km","wu": wu_run(), "str": None, "wod": "NEGATIVE SPLITS - 10 km\nGoal: every 2 km section faster than the last.\n\nkm 0-2: very easy, hold back\nkm 2-4: comfortable, start to feel the run\nkm 4-6: moderate, building\nkm 6-8: comfortably hard, pushing now\nkm 8-10: strong finish\n\nSkill run: learning to start controlled and finish fast.", "tags": ["Trail", "10 km", "60-75 min"]},
        {"id": "run_session","type":"E","name": "Interval Run",      "cycle_label": "Endurance - Wednesday","scheme": "5x1 km @ tempo + KB", "km": "5 km", "wu": wu_tempo(), "str": None, "wod": "TEMPO + KB - approx 5 km\n5x1 km at tempo effort\nRest: 90 sec easy jog between reps\n\nThen: 3 Rounds\n15 KB Swings (44/70 lb)\n10 Goblet Squats (same)\n10 Dips (chairs/box)\n\nRecord each 1 km split.", "tags": ["Running", "5 km", "KB", "40-50 min"]},
    ],
    3: [  # Week 4
        {"id": "squat",    "type": "S", "name": "Back Squat 1RM Test","cycle_label": "Strength A - W4/4 TEST","scheme": "Work to 1RM",       "wu": wu_squat(),    "str": "Back Squat - Work to a 1RM.\nThen: 2x5 @ 65% (speed squats - move bar explosively).\nThis closes the 4-week strength cycle. Record your number.", "wod": "POST-TEST METCON\n3 Rounds for time:\n10 Front Squats (95/135 lb)\n20 Wall Ball shots (14/20 lb)\n15 Pull-ups\n\nLighter MetCon after heavy strength.\nTarget: 22-30 min.", "tags": ["Barbell", "Wall ball", "24-32 min"]},
        {"id": "deadlift", "type": "S", "name": "Deadlift 1RM Test", "cycle_label": "Strength B - W4/4 TEST","scheme": "Work to 1RM",        "wu": wu_deadlift(), "str": "Deadlift - Build to a 1RM attempt.\nThen: 3x2 @ 90% of today's 1RM.\nRecord your number. This closes the 4-week cycle.\nMinimum 8 warm-up sets. Take your time on the build.", "wod": "FINAL PULL\n3 Rounds for time:\n12 Deadlifts (185/275 lb)\n9 Hang Power Cleans (95/135 lb)\n6 Push Jerks\n12 Pull-ups\n\nScale loads to 65-70% 1RM.\nTarget: 22-30 min.", "tags": ["Barbell", "Pull-up bar", "24-32 min"]},
        {"id": "olympic",  "type": "O", "name": "Clean & Jerk",      "cycle_label": "Olympic - W4/4 TEST","scheme": "Heavy single + 4x1+1@85%","wu": wu_clean(),   "str": "Clean & Jerk - Build to a heavy single over 15 min.\nThen: 4x (1 power clean + 1 split jerk) @ 85% of today's heavy.\nWeek 4: peak of the Olympic cycle. Combine clean + jerk.\nFocus: fast elbows on clean, aggressive dip-drive on jerk.", "wod": "C&J GRIND\n5 Rounds for time:\n5 Clean & Jerks (85/125 lb)\n10 Toes-to-bar\n15 Wall Ball shots (14/20 lb)\n\nTarget: 22-28 min.", "tags": ["Barbell", "Wall ball", "24-30 min"]},
        {"id": "gymnastics","type":"G", "name": "HSPU - Misfit W4",  "cycle_label": "Misfit HSPU - W4/6","scheme": "HS holds 6 min (faster) + test","wu": wu_gymnastics(),"str": "Handstand Holds - Accumulate 6 min total (18 min cap)\nFaster than Week 2. Deload after W3 peak.\n\nDB Wall Press: 3x15 (increase weight only if W3 felt easy).", "wod": "HSPU TEST - Week 4\n2 Rounds:\nClimb the strict HSPU ladder by 1s\nRest 90 sec\nClimb the kipping HSPU ladder by 2s\nRest 3 min\n\nKick down before you fail on strict HSPU.\nHandstand hold: 10 x 9-11 sec.\nCompare scores to Week 2.", "tags": ["Bodyweight", "Gymnastics", "25-35 min"]},
        {"id": "press",    "type": "S", "name": "Push Press 1RM Test","cycle_label": "Press Cycle - W4/4 TEST","scheme": "Work to 1RM",      "wu": wu_press(),    "str": "Push Press - Work to a 1RM.\nThen: 2x5 @ 70% (speed presses).\nThis closes the 4-week press cycle. Record your number.\nOptional: attempt strict press 1RM after 10+ min full rest.", "wod": "PRESS TEST FINISHER\n4 Rounds:\n5 Push Press (@ 70% of today's 1RM)\n10 Pull-ups\n15 Push-ups\n20 Air squats\n\nLight and fast - recover after the heavy press work.\nTarget: 15-20 min.", "tags": ["Barbell", "15-22 min"]},
        {"id": "metcon_a", "type": "M", "name": "KB + Burpees AMRAP","cycle_label": "MetCon A",          "scheme": "AMRAP 20 min",            "wu": wu_kb(),       "str": None, "wod": "BURPEE BOSS\nAMRAP 20 min:\n5 Burpee box jumps (or burpee broad jumps)\n10 KB Swings (44/70 lb)\n15 KB Goblet Squats (same)\n200m run\n\nScale: reduce KB weight, replace box jumps with regular burpees.\nTarget: 5-6+ rounds.", "tags": ["KB", "Running", "20 min AMRAP"]},
        {"id": "metcon_b", "type": "M", "name": "The Closer",        "cycle_label": "MetCon B - Month-End","scheme": "For time",             "wu": ["2 min easy jog","10 arm + hip circles each direction","10 air squats + 10 push-ups + 5 pull-ups","5 wall ball throws + 5 KB swings (light)"], "str": None, "wod": "THE CLOSER - month-end benchmark\nFor time:\n1.5 km run\n50 Wall Ball shots (14/20 lb)\n40 KB Swings (35/53 lb)\n30 Pull-ups\n20 Deadlifts (155/225 lb)\n10 Clean & Jerks (95/135 lb)\n1.5 km run\n\nEvery piece of equipment. One final test.\nScale: reduce all reps by 30% if needed.\nTarget: 38-52 min.", "tags": ["All equipment", "3 km running", "40-55 min"]},
        {"id": "trail_mid","type": "T", "name": "Trail Run - Hill Reps","cycle_label": "Trail Run - Tuesday","scheme": "9 km - hill reps",  "km": "9 km",  "wu": wu_run(), "str": None, "wod": "HILL REPS - 9 km\nEffort: Hard on hills, easy recovery on flat/downhill\n\n2 km easy warm-up jog to your hill\n6 x uphill effort (50-100 m steep section)\n  - Push hard at 90% effort (20-30 sec)\n  - Walk/jog back down (full recovery)\n3 km easy jog home\n\nHill reps build explosive leg power.", "tags": ["Trail", "9 km", "Hill reps", "55-70 min"]},
        {"id": "run_session","type":"E","name": "Tempo Finisher",    "cycle_label": "Endurance - Wednesday","scheme": "4x1 km @ tempo + KB", "km": "5 km", "wu": wu_tempo(), "str": None, "wod": "TEMPO FINISHER - approx 5 km\n4x1 km at tempo effort\nRest: 90 sec easy jog between reps\n\nThen: 3 Rounds\n15 KB Swings (44/70 lb)\n10 Goblet Squats (same)\n10 Dips (chairs/box)\n\nFinal tempo run of the month. Record splits and compare to Week 1.", "tags": ["Running", "5 km", "KB", "38-48 min"]},
    ],
}

# ============================================================
# SERIALISE — base64 is 100% safe: only A-Za-z0-9+/= chars,
# no clash with HTML, CSS, or Python string delimiters.
# ============================================================
_payload = json.dumps({
    "blocks":     {str(k): v for k, v in BLOCKS.items()},
    "weekMeta":   WEEK_META,
    "longTrails": LONG_TRAILS,
    "version":    "v8",
})
APP_DATA_B64 = _b64.b64encode(_payload.encode("utf-8")).decode("ascii")

# ============================================================
# HTML — plain string, data injected with .replace()
# NO f-string used here — zero {{ }} escaping issues.
# ============================================================
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root {
  --bg:#fff; --bg2:#f6f6f4; --tx:#1a1a18; --tx2:#5c5c58; --tx3:#9a9a94;
  --bd:rgba(0,0,0,.08); --bd2:rgba(0,0,0,.18); --rad:8px; --rad2:12px;
  --S-bg:#EEEDFE; --S-t:#3C3489; --O-bg:#FAECE7; --O-t:#712B13;
  --G-bg:#E1F5EE; --G-t:#085041; --M-bg:#FAEEDA; --M-t:#633806;
  --T-bg:#EAF3DE; --T-t:#27500A; --E-bg:#E6F1FB; --E-t:#0C447C;
  --R-bg:#F1EFE8; --R-t:#5F5E5A;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--tx);padding:1rem 1.25rem;font-size:14px;}
.tab-nav{display:flex;gap:4px;margin-bottom:1.25rem;border-bottom:1px solid var(--bd);}
.tab-btn{background:none;border:none;padding:.5rem 1rem;font-size:14px;color:var(--tx2);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;}
.tab-btn.on{color:var(--tx);border-bottom-color:var(--tx);font-weight:500;}
.pane{display:none;} .pane.on{display:block;}
.week-hdr{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:1rem;}
.nav-btn{background:none;border:1px solid var(--bd2);border-radius:var(--rad);padding:4px 14px;font-size:16px;cursor:pointer;color:var(--tx2);}
.nav-btn:hover{background:var(--bg2);}
.wk-lbl{font-size:16px;font-weight:500;}
.cbadges{display:flex;flex-wrap:wrap;gap:5px;margin-top:4px;}
.cb{font-size:10px;padding:2px 7px;border-radius:4px;font-weight:500;}
.km-ctl{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:12px;color:var(--tx3);}
.km-in{width:60px;padding:4px 6px;border:1px solid var(--bd2);border-radius:var(--rad);background:var(--bg);color:var(--tx);font-size:14px;text-align:center;}
.pal-hdr{font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);margin-bottom:8px;}
.palette{display:grid;grid-template-columns:repeat(auto-fill,minmax(145px,1fr));gap:6px;margin-bottom:1.25rem;}
.blk{border-radius:var(--rad);padding:8px 10px;cursor:pointer;border:1.5px solid transparent;}
.blk:hover{border-color:var(--bd2);} .blk.on{border-color:var(--tx);} .blk.done{opacity:.3;pointer-events:none;}
.blk-n{font-size:12px;font-weight:500;} .blk-c{font-size:10px;opacity:.8;margin-top:1px;} .blk-s{font-size:10px;opacity:.65;margin-top:1px;}
.gwrap{overflow-x:auto;}
.wgrid{display:grid;grid-template-columns:repeat(7,minmax(118px,1fr));gap:5px;min-width:700px;}
.dcol{display:flex;flex-direction:column;gap:4px;}
.dhdr{font-size:11px;font-weight:500;color:var(--tx3);text-align:center;padding:3px 0;}
.ddate{font-size:10px;color:var(--tx3);text-align:center;}
.slot{border:1px dashed var(--bd2);border-radius:var(--rad);padding:7px 8px;min-height:60px;cursor:pointer;position:relative;}
.slot:hover{background:var(--bg2);border-color:var(--tx2);}
.slot.rdy{border-color:var(--tx);border-style:solid;background:var(--bg2);}
.slot.lck{cursor:default;border-style:solid;border-color:transparent;}
.slbl{font-size:10px;color:var(--tx3);margin-bottom:3px;}
.sempty{font-size:11px;color:var(--tx3);padding-top:4px;}
.sfill{border-radius:5px;padding:5px 6px;}
.sfill-n{font-size:11px;font-weight:500;} .sfill-s{font-size:10px;margin-top:1px;opacity:.75;}
.rm{position:absolute;top:3px;right:5px;background:none;border:none;cursor:pointer;font-size:13px;color:var(--tx3);line-height:1;padding:0 2px;}
.rm:hover{color:var(--tx);}
.prog{display:flex;gap:16px;flex-wrap:wrap;margin:1rem 0;padding:.75rem 1rem;background:var(--bg2);border-radius:var(--rad);font-size:12px;}
.pi{display:flex;align-items:center;gap:6px;}
.pdot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.det{border:1px solid var(--bd);border-radius:var(--rad2);padding:1.25rem;margin-top:1rem;}
.dtop{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:1rem;}
.dico{width:44px;height:44px;border-radius:var(--rad);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:500;text-align:center;line-height:1.3;flex-shrink:0;}
.dttl{font-size:16px;font-weight:500;} .dsub{font-size:12px;color:var(--tx3);}
.dtags{margin-left:auto;display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;}
.dtag{font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid var(--bd);color:var(--tx2);}
.sec{font-size:11px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--tx3);margin:0 0 6px;}
.wu{border:1px solid var(--bd);border-radius:var(--rad);padding:.5rem .75rem;margin-bottom:1rem;}
.wui{font-size:13px;color:var(--tx2);padding:4px 0;border-bottom:1px solid var(--bd);display:flex;gap:8px;}
.wui:last-child{border:none;}
.wudot{width:5px;height:5px;border-radius:50%;background:var(--bd2);margin-top:7px;flex-shrink:0;}
.box{border-radius:var(--rad);padding:.75rem 1rem;margin-bottom:.75rem;}
.boxt{font-size:13px;line-height:1.75;white-space:pre-line;}
.cal-g{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;}
.cal-dow{font-size:11px;color:var(--tx3);text-align:center;padding:4px 0 6px;}
.cal-d{border:1px solid var(--bd);border-radius:var(--rad);padding:7px 8px;min-height:72px;cursor:pointer;}
.cal-d:hover:not(.cal-r){border-color:var(--bd2);}
.cal-d.cal-s{border:2px solid var(--tx2);}
.cal-d.cal-r{cursor:default;background:var(--bg2);}
.cal-d.cal-e{border:none;background:none;cursor:default;min-height:0;}
.cal-dn{font-size:12px;font-weight:500;color:var(--tx2);}
.cal-b{font-size:10px;padding:2px 5px;border-radius:4px;margin-top:4px;display:inline-block;font-weight:500;}
.cal-n{font-size:10px;color:var(--tx3);margin-top:3px;}
.cal-k{font-size:10px;font-weight:500;margin-top:2px;}
.leg{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1rem;}
</style>
</head>
<body>
<div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px;margin-bottom:.25rem">
  <div>
    <h1 style="font-size:20px;font-weight:500;margin-bottom:2px">May 2026 &mdash; CrossFit + Trail Running</h1>
    <p style="font-size:12px;color:var(--tx3)">Trail: Tue &amp; Sun &nbsp;&#183;&nbsp; 25&ndash;27&nbsp;km/week &nbsp;&#183;&nbsp; 4-week cycles &nbsp;&#183;&nbsp; Rest: Saturday</p>
  </div>
  <span id="ver" style="font-size:10px;padding:2px 8px;border-radius:4px;background:#eee;color:#999;font-family:monospace">...</span>
</div>
<div class="tab-nav">
  <button class="tab-btn on" onclick="tab('planner',this)">Week Planner</button>
  <button class="tab-btn" onclick="tab('calendar',this)">Month Calendar</button>
</div>
<div id="pane-planner" class="pane on">
  <div class="week-hdr">
    <button class="nav-btn" id="bprev" onclick="nav(-1)">&#8592;</button>
    <div><div class="wk-lbl" id="wlbl"></div><div class="cbadges" id="wcyc"></div></div>
    <button class="nav-btn" id="bnext" onclick="nav(1)">&#8594;</button>
    <div class="km-ctl">Weekly target&nbsp;<input class="km-in" id="kmin" type="number" min="10" max="60" onchange="setKm(+this.value)">&nbsp;km</div>
  </div>
  <div class="pal-hdr" id="phdr"></div>
  <div class="palette" id="pal"></div>
  <div class="gwrap"><div class="wgrid" id="grid"></div></div>
  <div class="prog" id="prog"></div>
  <div id="det" style="display:none"></div>
</div>
<div id="pane-calendar" class="pane">
  <div class="leg" id="leg"></div>
  <div class="cal-g" id="calg">
    <div class="cal-dow">Mon</div><div class="cal-dow">Tue</div><div class="cal-dow">Wed</div>
    <div class="cal-dow">Thu</div><div class="cal-dow">Fri</div><div class="cal-dow">Sat</div><div class="cal-dow">Sun</div>
  </div>
  <div id="caldet" style="margin-top:.85rem"></div>
</div>
<textarea id="D" style="display:none">__PAYLOAD__</textarea>
<script>
// ── LOAD DATA ──────────────────────────────────────────────
var BLK, WM, LT;
try {
  var raw = document.getElementById('D').value.trim();
  var d = JSON.parse(atob(raw));
  BLK = d.blocks; WM = d.weekMeta; LT = d.longTrails;
  document.getElementById('ver').textContent = d.version;
} catch(e) {
  document.getElementById('ver').textContent = 'ERR';
  document.getElementById('pane-planner').innerHTML =
    '<p style="color:red;padding:1rem;font-family:monospace">Data error: ' + e + '<br>Raw length: ' +
    document.getElementById('D').value.length + '</p>';
}

// ── CONFIG ─────────────────────────────────────────────────
var TP = {
  S:{l:'Strength',  bg:'var(--S-bg)',tc:'var(--S-t)'},
  O:{l:'Olympic',   bg:'var(--O-bg)',tc:'var(--O-t)'},
  G:{l:'Gymnastics',bg:'var(--G-bg)',tc:'var(--G-t)'},
  M:{l:'MetCon',    bg:'var(--M-bg)',tc:'var(--M-t)'},
  T:{l:'Trail Run', bg:'var(--T-bg)',tc:'var(--T-t)'},
  E:{l:'Endurance', bg:'var(--E-bg)',tc:'var(--E-t)'},
  R:{l:'Rest',      bg:'var(--R-bg)',tc:'var(--R-t)'}
};
var DS = ['mon','tue','wed','thu','fri'];
var DL = ['Mon','Tue','Wed','Thu','Fri'];

// ── STATE ──────────────────────────────────────────────────
var ST = {w:0, km:[25,25,27,26], sl:{}, sel:null};
function sk(d,t){return d+'_'+t;}
function ws(){return ST.sl[ST.w]||(ST.sl[ST.w]={});}
function bfw(w){return (BLK&&BLK[String(w)])||[];}
function pid(){var s=ST.sl[ST.w]||{},r={};Object.keys(s).forEach(function(k){if(s[k])r[s[k]]=true;});return r;}
function fb(id){return bfw(ST.w).find(function(b){return b.id===id;})||null;}
function save(){try{localStorage.setItem('cfpv8',JSON.stringify({w:ST.w,km:ST.km,sl:ST.sl}));}catch(e){}}
function load(){
  try{
    var p=JSON.parse(localStorage.getItem('cfpv8')||'null');
    if(!p)return;
    if(p.w!=null)ST.w=p.w;
    if(p.km)ST.km=p.km;
    if(p.sl)ST.sl=p.sl;
  }catch(e){}
}

// ── TABS ───────────────────────────────────────────────────
function tab(name, btn) {
  document.querySelectorAll('.pane').forEach(function(el){el.classList.remove('on');});
  document.querySelectorAll('.tab-btn').forEach(function(el){el.classList.remove('on');});
  document.getElementById('pane-'+name).classList.add('on');
  btn.classList.add('on');
  if(name==='calendar') buildCal();
}

// ── NAVIGATION ─────────────────────────────────────────────
function nav(d){ST.w=Math.max(0,Math.min(3,ST.w+d));ST.sel=null;save();render();}
function setKm(v){if(v>=10&&v<=60){ST.km[ST.w]=v;save();renderProg();}}

// ── BLOCK ACTIONS ──────────────────────────────────────────
function selB(id){ST.sel=(ST.sel===id)?null:id;renderPal();}
function place(day,t){
  var key=sk(day,t),slots=ws(),cur=slots[key];
  if(cur){var b=fb(cur);if(b)showDet(b);return;}
  if(!ST.sel||pid()[ST.sel])return;
  slots[key]=ST.sel;ST.sel=null;save();render();
}
function rm(day,t){
  var key=sk(day,t),slots=ws(),id=slots[key];
  if(!id)return;
  delete slots[key];ST.sel=null;save();render();
}

// ── RENDER PALETTE ─────────────────────────────────────────
function renderPal(){
  var blks=bfw(ST.w),placed=pid(),h='';
  blks.forEach(function(b){
    var tp=TP[b.type]||TP.S;
    var cls='blk'+(placed[b.id]?' done':'')+(ST.sel===b.id?' on':'');
    h+='<div class="'+cls+'" style="background:'+tp.bg+'" onclick="selB(\''+b.id+'\')">';
    h+='<div class="blk-n" style="color:'+tp.tc+'">'+b.name+'</div>';
    h+='<div class="blk-c" style="color:'+tp.tc+'">'+b.cycle_label+'</div>';
    h+='<div class="blk-s" style="color:'+tp.tc+'">'+b.scheme+'</div>';
    h+='</div>';
  });
  document.getElementById('pal').innerHTML=h;
  var rem=blks.length-Object.keys(placed).length;
  document.getElementById('phdr').textContent=ST.sel
    ?'Block selected \u2014 click an empty slot to place it (click again to deselect)'
    :'Available blocks ('+rem+' remaining) \u2014 click a block, then click a slot';
}

// ── RENDER GRID ────────────────────────────────────────────
function renderGrid(){
  var meta=WM[ST.w],slots=ws(),h='';
  DS.forEach(function(day,di){
    h+='<div class="dcol">';
    h+='<div class="dhdr">'+DL[di]+'</div><div class="ddate">'+meta.dates[di]+'</div>';
    ['am','pm'].forEach(function(t){
      var key=sk(day,t),bid=slots[key],blk=bid?fb(bid):null,rdy=ST.sel&&!bid;
      h+='<div class="slot'+(rdy?' rdy':'')+'" onclick="place(\''+day+'\',\''+t+'\')">';
      h+='<div class="slbl">'+t.toUpperCase()+'</div>';
      if(blk){
        var tp=TP[blk.type]||TP.S;
        h+='<div class="sfill" style="background:'+tp.bg+'">';
        h+='<div class="sfill-n" style="color:'+tp.tc+'">'+blk.name+'</div>';
        h+='<div class="sfill-s" style="color:'+tp.tc+'">'+blk.scheme+'</div></div>';
        h+='<button class="rm" onclick="event.stopPropagation();rm(\''+day+'\',\''+t+'\')">&#215;</button>';
      }else{
        h+='<div class="sempty">'+(rdy?'+ place':'+ add')+'</div>';
      }
      h+='</div>';
    });
    h+='</div>';
  });
  // Sat REST
  h+='<div class="dcol"><div class="dhdr" style="color:var(--R-t)">Sat</div><div class="ddate">'+WM[ST.w].dates[5]+'</div>';
  h+='<div class="slot lck" style="background:var(--R-bg);min-height:128px;display:flex;align-items:center;justify-content:center">';
  h+='<div style="text-align:center"><div style="font-size:13px;font-weight:500;color:var(--R-t)">REST</div>';
  h+='<div style="font-size:11px;color:var(--R-t);opacity:.7;margin-top:4px">Recovery day</div></div></div></div>';
  // Sun trail
  var lt=LT[ST.w];
  h+='<div class="dcol"><div class="dhdr" style="color:var(--T-t)">Sun</div><div class="ddate">'+WM[ST.w].dates[6]+'</div>';
  h+='<div class="slot lck" style="background:var(--T-bg);min-height:128px;cursor:pointer" onclick="showSun('+ST.w+')">';
  h+='<div class="slbl" style="color:var(--T-t)">TRAIL</div>';
  h+='<div class="sfill" style="background:transparent">';
  h+='<div class="sfill-n" style="color:var(--T-t)">'+lt.name+'</div>';
  h+='<div style="font-size:20px;font-weight:500;color:var(--T-t);margin:3px 0">'+lt.km+'</div>';
  h+='<div class="sfill-s" style="color:var(--T-t)">Click for plan</div>';
  h+='</div></div></div>';
  document.getElementById('grid').innerHTML=h;
}

// ── RENDER HEADER ──────────────────────────────────────────
function renderHdr(){
  var w=ST.w,meta=WM[w],c=meta.cycle;
  document.getElementById('wlbl').textContent=meta.label;
  document.getElementById('bprev').disabled=w===0;
  document.getElementById('bnext').disabled=w===3;
  document.getElementById('kmin').value=ST.km[w];
  var cb=[['Squat W'+c+'/4','S'],['Deadlift W'+c+'/4','S'],['Olympic W'+c+'/4','O'],
    ['HSPU W'+c+'/6','G'],['Press W'+c+'/4','S']].map(function(x){
    var tp=TP[x[1]];
    return '<span class="cb" style="background:'+tp.bg+';color:'+tp.tc+'">'+x[0]+'</span>';
  }).join('');
  document.getElementById('wcyc').innerHTML=cb;
}

// ── RENDER PROGRESS ────────────────────────────────────────
function renderProg(){
  var w=ST.w,slots=ST.sl[w]||{};
  var placed=Object.keys(slots).filter(function(k){return!!slots[k];}).length;
  var total=bfw(w).length;
  var twoA=0;DS.forEach(function(d){if(slots[sk(d,'am')]&&slots[sk(d,'pm')])twoA++;});
  var placed2=pid(),kmP=0;
  if(placed2['trail_mid'])kmP+=(w===2?10:9);
  if(placed2['run_session'])kmP+=5;
  kmP+=parseInt(LT[w].km);
  var h='';
  h+='<div class="pi"><div class="pdot" style="background:var(--tx2)"></div><b>'+placed+'/'+total+'</b>&nbsp;blocks placed</div>';
  h+='<div class="pi"><div class="pdot" style="background:var(--S-t)"></div><b>'+twoA+'/4</b>&nbsp;two-a-days</div>';
  h+='<div class="pi"><div class="pdot" style="background:var(--T-t)"></div><b>'+kmP+'/'+ST.km[w]+' km</b>&nbsp;running planned</div>';
  if(placed===total&&twoA>=4)h+='<div class="pi" style="margin-left:auto"><span style="color:var(--T-t);font-weight:500">Week complete \u2713</span></div>';
  document.getElementById('prog').innerHTML=h;
}

// ── SHOW DETAIL ────────────────────────────────────────────
function showDet(b){
  var tp=TP[b.type]||TP.S,h='<div class="det">';
  h+='<div class="dtop">';
  h+='<div class="dico" style="background:'+tp.bg+';color:'+tp.tc+'">'+tp.l.replace(' ','<br>')+'</div>';
  h+='<div><div class="dttl">'+b.name+'</div>';
  h+='<div class="dsub">'+b.cycle_label+(b.km?' &nbsp;&#183; '+b.km:'')+'</div></div>';
  h+='<div class="dtags">'+(b.tags||[]).map(function(t){return'<span class="dtag">'+t+'</span>';}).join('')+'</div>';
  h+='</div>';
  if(b.wu&&b.wu.length){
    h+='<div class="sec" style="margin-top:.25rem">Warm-up &#183; 6&#8211;8 min</div>';
    h+='<div class="wu">'+b.wu.map(function(i){return'<div class="wui"><div class="wudot"></div><div>'+i+'</div></div>';}).join('')+'</div>';
  }
  if(b.str){
    h+='<div class="sec">Strength / Skill work</div>';
    h+='<div class="box" style="background:'+tp.bg+'"><div class="boxt" style="color:'+tp.tc+'">'+b.str+'</div></div>';
  }
  var lbl=b.type==='T'?'Run plan':b.type==='E'?'Endurance WOD':'Workout of the Day';
  h+='<div class="sec">'+lbl+'</div>';
  h+='<div class="box" style="background:var(--bg2);border:1px solid var(--bd)"><div class="boxt" style="color:var(--tx2)">'+b.wod+'</div></div>';
  h+='</div>';
  var el=document.getElementById('det');
  el.innerHTML=h;el.style.display='block';
  el.scrollIntoView({behavior:'smooth',block:'nearest'});
}
function showSun(w){
  var lt=LT[w];
  showDet({name:lt.name,type:'T',cycle_label:'Long Trail Run &#183; Sunday (fixed)',
    km:lt.km,wu:lt.wu,str:null,wod:lt.wod,tags:[lt.km,'Trail','60-90 min']});
}

// ── FULL RENDER ────────────────────────────────────────────
function render(){
  if(!BLK||!WM)return;
  renderHdr();renderPal();renderGrid();renderProg();
}

// ── CALENDAR ───────────────────────────────────────────────
var CAL=[
  [1,'M','KB MetCon',null],[2,'R','Rest',null],[3,'T','Trail Run','10 km'],
  [4,'S','Back Squat','5x5'],[5,'T','Trail Run','9 km'],[6,'E','Tempo Run','~5 km'],
  [7,'O','Hang Power Clean',null],[8,'G','HSPU W1',null],[9,'R','Rest',null],
  [10,'T','Trail Run','11 km'],[11,'S','Deadlift','5x3'],[12,'T','Trail Run','9 km'],
  [13,'E','200m Intervals','~5 km'],[14,'O','Power Snatch',null],[15,'M','KB Storm',null],
  [16,'R','Rest',null],[17,'T','Trail Run','11 km'],[18,'S','Back Squat','3x3'],
  [19,'T','Trail Run','10 km'],[20,'E','Tempo+KB','~5 km'],[21,'O','Power Clean',null],
  [22,'G','HSPU W3',null],[23,'R','Rest',null],[24,'T','Trail Run','12 km'],
  [25,'S','Squat 1RM',null],[26,'T','Trail Run','9 km'],[27,'E','Tempo Finisher','~5 km'],
  [28,'O','Clean & Jerk',null],[29,'S','Deadlift 1RM',null],[30,'R','Rest',null],
  [31,'T','Trail Run','12 km']
];
var cSel=null;
function buildCal(){
  var g=document.getElementById('calg');
  while(g.children.length>7)g.removeChild(g.lastChild);
  document.getElementById('leg').innerHTML=[['S','Strength'],['O','Olympic'],['G','Gymnastics'],
    ['M','MetCon'],['T','Trail Run'],['E','Endurance'],['R','Rest']].map(function(x){
    var tp=TP[x[0]];
    return'<span class="cb" style="background:'+tp.bg+';color:'+tp.tc+'">'+x[1]+'</span>';
  }).join('');
  for(var i=0;i<4;i++){var e=document.createElement('div');e.className='cal-d cal-e';g.appendChild(e);}
  CAL.forEach(function(r){
    var d=r[0],type=r[1],nm=r[2],km=r[3],tp=TP[type];
    var div=document.createElement('div');
    div.className='cal-d'+(type==='R'?' cal-r':'');
    var h='<div class="cal-dn">'+d+'</div>';
    h+='<div class="cal-b" style="background:'+tp.bg+';color:'+tp.tc+'">'+tp.l+'</div>';
    h+='<div class="cal-n">'+nm+'</div>';
    if(km)h+='<div class="cal-k" style="color:'+tp.tc+'">'+km+'</div>';
    div.innerHTML=h;
    if(type!=='R')div.addEventListener('click',(function(day,el){return function(){openCal(day,el);};})(d,div));
    g.appendChild(div);
  });
}
function openCal(d,el){
  if(cSel===el){cSel.classList.remove('cal-s');cSel=null;document.getElementById('caldet').innerHTML='';return;}
  if(cSel)cSel.classList.remove('cal-s');
  cSel=el;el.classList.add('cal-s');
  var wk=d<=10?0:d<=17?1:d<=24?2:3;
  var r=CAL.find(function(x){return x[0]===d;});
  if(!r)return;
  var type=r[1];
  if(type==='T'&&[10,17,24,31].indexOf(d)>=0){
    var savew=ST.w;ST.w=wk;showSun(wk);ST.w=savew;
    // move det to caldet
    var det=document.getElementById('det');
    document.getElementById('caldet').innerHTML=det.innerHTML;
    det.style.display='none';
    return;
  }
  var im={S:'squat',O:'olympic',G:'gymnastics',M:'metcon_a',T:'trail_mid',E:'run_session'};
  if(d===11||d===29)im.S='deadlift';
  var savew=ST.w;ST.w=wk;
  var blk=fb(im[type]);
  ST.w=savew;
  if(blk){
    var savew2=ST.w;ST.w=wk;showDet(blk);ST.w=savew2;
    document.getElementById('caldet').innerHTML=document.getElementById('det').innerHTML;
    document.getElementById('det').style.display='none';
  } else {
    document.getElementById('caldet').innerHTML=
      '<div style="padding:.75rem 1rem;border:1px solid var(--bd);border-radius:8px;margin-top:.5rem">' +
      '<p style="font-size:13px;color:var(--tx2)">Open the Week Planner tab to view full workout details.</p></div>';
  }
  el.scrollIntoView({behavior:'smooth',block:'nearest'});
}

// ── INIT ───────────────────────────────────────────────────
load();
render();
</script>
</body>
</html>"""

FINAL_HTML = HTML.replace("__PAYLOAD__", APP_DATA_B64)
components.html(FINAL_HTML, height=1900, scrolling=True)
