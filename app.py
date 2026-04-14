import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CrossFit + Trail Run Planner — May 2026",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 0; max-width: 960px; }
    header { display: none !important; }
    #MainMenu { display: none; }
    footer { display: none; }
</style>
""", unsafe_allow_html=True)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {
  --bg: #ffffff; --bg2: #f6f6f4; --bg3: #ededea;
  --tx: #1a1a18; --tx2: #5c5c58; --tx3: #9a9a94;
  --bd: rgba(0,0,0,0.09); --bd2: rgba(0,0,0,0.16);
  --rad: 8px; --rad-lg: 12px;
  --str-bg:#EEEDFE;--str-t:#3C3489;
  --oly-bg:#FAECE7;--oly-t:#712B13;
  --gym-bg:#E1F5EE;--gym-t:#085041;
  --met-bg:#FAEEDA;--met-t:#633806;
  --trl-bg:#EAF3DE;--trl-t:#27500A;
  --end-bg:#E6F1FB;--end-t:#0C447C;
  --rst-bg:#F1EFE8;--rst-t:#5F5E5A;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#1c1c1a;--bg2:#252523;--bg3:#2e2e2b;
    --tx:#e6e6e0;--tx2:#a0a09a;--tx3:#666660;
    --bd:rgba(255,255,255,0.09);--bd2:rgba(255,255,255,0.16);
    --str-bg:#26215C;--str-t:#CECBF6;
    --oly-bg:#4A1B0C;--oly-t:#F5C4B3;
    --gym-bg:#04342C;--gym-t:#9FE1CB;
    --met-bg:#412402;--met-t:#FAC775;
    --trl-bg:#173404;--trl-t:#C0DD97;
    --end-bg:#042C53;--end-t:#B5D4F4;
    --rst-bg:#2C2C2A;--rst-t:#D3D1C7;
  }
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--tx);font-size:15px;line-height:1.6;padding:1.5rem;}
h1{font-size:22px;font-weight:500;margin-bottom:2px;}
.sub{font-size:13px;color:var(--tx3);margin-bottom:1.25rem;}
.wk-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:1.25rem;}
.wk-card{background:var(--bg2);border-radius:var(--rad);padding:.65rem .75rem;text-align:center;}
.wk-km{font-size:20px;font-weight:500;color:var(--trl-t);}
.wk-lbl{font-size:11px;color:var(--tx3);margin-top:1px;}
.wk-detail{font-size:11px;color:var(--tx2);margin-top:2px;}
.legend{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1.25rem;}
.badge{font-size:11px;padding:3px 7px;border-radius:5px;font-weight:500;}
.cal{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px;}
.dow{font-size:11px;color:var(--tx3);text-align:center;padding:4px 0 6px;}
.day{border:0.5px solid var(--bd);border-radius:var(--rad);padding:7px 8px;min-height:76px;cursor:pointer;background:var(--bg);transition:border-color .12s;}
.day:hover:not(.rest){border-color:var(--bd2);}
.day.sel{border:1.5px solid var(--tx2);}
.day.rest{cursor:default;background:var(--bg2);}
.day.empty{border:none;background:none;cursor:default;min-height:0;}
.dnum{font-size:12px;font-weight:500;color:var(--tx2);}
.dbadge{font-size:10px;padding:2px 5px;border-radius:4px;margin-top:4px;display:inline-block;font-weight:500;line-height:1.4;}
.dwname{font-size:10px;color:var(--tx3);margin-top:3px;line-height:1.3;}
.dkm{font-size:10px;font-weight:500;margin-top:2px;}
.panel{border:0.5px solid var(--bd);border-radius:var(--rad-lg);padding:1.25rem;margin-top:.85rem;background:var(--bg);}
.ptop{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:1rem;}
.picon{width:44px;height:44px;border-radius:var(--rad);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:500;text-align:center;line-height:1.3;flex-shrink:0;}
.ptitle{font-size:16px;font-weight:500;}
.psub{font-size:12px;color:var(--tx3);}
.ptags{margin-left:auto;display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;}
.ptag{font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid var(--bd);color:var(--tx2);}
.sec{font-size:11px;font-weight:500;letter-spacing:.06em;color:var(--tx3);text-transform:uppercase;margin:0 0 6px;}
.wu{border:0.5px solid var(--bd);border-radius:var(--rad);padding:.5rem .75rem;margin-bottom:1rem;}
.wu-item{font-size:13px;color:var(--tx2);padding:4px 0;border-bottom:0.5px solid var(--bd);display:flex;align-items:flex-start;gap:8px;}
.wu-item:last-child{border-bottom:none;}
.wu-dot{width:5px;height:5px;border-radius:50%;background:var(--bd2);margin-top:7px;flex-shrink:0;}
.box{border-radius:var(--rad);padding:.75rem 1rem;}
.box-text{font-size:13px;line-height:1.7;white-space:pre-line;}
.run-banner{border-radius:var(--rad);padding:.65rem 1rem;margin-bottom:.85rem;display:flex;align-items:center;gap:14px;}
.run-km{font-size:28px;font-weight:500;}
@media(max-width:600px){
  .wk-grid{grid-template-columns:repeat(2,1fr);}
  .cal{gap:3px;}
  .day{min-height:60px;padding:5px 6px;}
  body{padding:1rem .75rem;}
}
</style>
</head>
<body>

<h1>May 2026 — CrossFit + Trail Running</h1>
<p class="sub">Trail runs: Tuesday &amp; Sunday &nbsp;·&nbsp; 3 runs/week &nbsp;·&nbsp; 25–27 km/week &nbsp;·&nbsp; Rest: Saturday</p>

<div class="wk-grid">
  <div class="wk-card"><div class="wk-km">25 km</div><div class="wk-lbl">Week 1 · May 4–10</div><div class="wk-detail">Tue 9 · Wed 5 · Sun 11</div></div>
  <div class="wk-card"><div class="wk-km">25 km</div><div class="wk-lbl">Week 2 · May 11–17</div><div class="wk-detail">Tue 9 · Wed 5 · Sun 11</div></div>
  <div class="wk-card"><div class="wk-km">27 km</div><div class="wk-lbl">Week 3 · May 18–24</div><div class="wk-detail">Tue 10 · Wed 5 · Sun 12</div></div>
  <div class="wk-card"><div class="wk-km">26 km</div><div class="wk-lbl">Week 4 · May 25–31</div><div class="wk-detail">Tue 9 · Wed 5 · Sun 12</div></div>
</div>

<div class="legend">
  <span class="badge" style="background:var(--str-bg);color:var(--str-t)">Strength</span>
  <span class="badge" style="background:var(--oly-bg);color:var(--oly-t)">Olympic</span>
  <span class="badge" style="background:var(--gym-bg);color:var(--gym-t)">Gymnastics</span>
  <span class="badge" style="background:var(--met-bg);color:var(--met-t)">MetCon</span>
  <span class="badge" style="background:var(--trl-bg);color:var(--trl-t)">Trail Run</span>
  <span class="badge" style="background:var(--end-bg);color:var(--end-t)">Endurance</span>
  <span class="badge" style="background:var(--rst-bg);color:var(--rst-t)">Rest</span>
</div>

<div class="cal" id="cal">
  <div class="dow">Mon</div><div class="dow">Tue</div><div class="dow">Wed</div>
  <div class="dow">Thu</div><div class="dow">Fri</div><div class="dow">Sat</div><div class="dow">Sun</div>
</div>
<div id="panel"></div>

<script>
const W = {
1:{t:'M',n:'KB MetCon',
wu:['90 sec jumping jacks','10 hip circles each direction','10 hip hinges (hands slide down shins — groove the hinge pattern)','10 KB deadlifts with light KB','2 min: 10 KB swings + 5 goblet squats (light, preview movements)'],
wod:'KB OPENER\\nAMRAP 20 min:\\n10 KB Swings (♀ 35 lb / ♂ 53 lb)\\n10 Goblet Squats (same KB)\\n8 DB Renegade Rows (4 each side, ♀ 20 lb / ♂ 35 lb)\\n12 Push-ups\\n\\nScale: Reduce weight. Keep push-ups strict.\\nTarget: 6–8 rounds.',
tags:['KB','Dumbbell','20 min AMRAP']},

2:{t:'R',n:'Rest Day',wu:[],
wod:'Full rest or light mobility.\\n\\nOptional (20–25 min):\\n• 2 min couch stretch each hip\\n• 2 min pigeon pose each side\\n• 10 cat-cow flows\\n• 2 min thoracic foam roll\\n\\nHydrate, sleep well, and get ready for your first long trail run tomorrow.',
tags:['Recovery']},

3:{t:'T',n:'Trail Run — Easy',km:'10 km',
wu:['3 min: Brisk walk then easy jog from home to trail','10 high knees + 10 butt kicks','10 leg swings front/back each leg','8 walking lunges each leg','4 × 20 sec build-up strides (70–80% effort), easy jog back'],
wod:'EASY TRAIL — 10 km\\nEffort: Zone 2 (conversational pace — full sentences throughout)\\nTerrain: Mixed trail, light elevation\\n\\nStructure:\\n→ km 0–3: settle in, warm up the legs, very easy\\n→ km 3–8: steady comfortable pace, enjoy the terrain\\n→ km 8–10: slight pick-up if feeling good\\n\\nFocus: smooth cadence (~170 spm), relaxed shoulders, eyes on terrain.\\nThis is the start of the month — keep it easy, more work ahead.',
tags:['Trail','10 km','~60–80 min']},

4:{t:'S',n:'Back Squat',
wu:['90 sec jumping jacks or jump rope','10 hip circles each direction','10 slow air squats — focus on depth and knee tracking','10 leg swings front/back each leg','Empty-bar warm-up: 3 × 5 back squats, building to 50% working weight'],
str:'Back Squat — 5 × 5 @ 75–80% 1RM\\nRest 2–3 min between sets.\\nCues: big breath and brace before descent, drive knees out, chest stays tall.',
wod:'SQUAT OPENER\\nFor time — 21–15–9:\\nBack Squats (♀ 95 lb / ♂ 135 lb)\\nBurpees\\n\\nThen: 2 × max-rep air squats (rest 90 sec between sets)\\n\\nScale: Reduce barbell load to 50–60% 1RM.\\nTarget: sub-12 min for 21-15-9.',
tags:['Barbell','15–20 min']},

5:{t:'T',n:'Trail Run — Hills',km:'9 km',
wu:['3 min: Easy jog from home to trail / hill','10 high knees + 10 butt kicks','8 walking lunges each leg','10 leg swings front/back each leg','4 × 15 sec uphill strides (80% effort) to activate glutes and calves'],
wod:'HILL TRADER — 9 km\\nEffort: Moderate with hill surges\\n\\nStructure:\\n→ km 0–2: easy warm-up pace, find rhythm\\n→ km 2–7: 5 × hill efforts — push hard uphill (20–30 sec), recover on downhill and flat\\n→ km 7–9: steady cool-down effort back\\n\\nTip: Shorten stride and lean forward on climbs — use your arms.\\nPower hiking steep sections is fine. No shame in walking uphills.\\nWeek 1 running: Run 1/3 · Cumulative this week: ~9 km of 25 km target.',
tags:['Trail','9 km','Hills','~55–70 min']},

6:{t:'E',n:'Run + Wall Ball',km:'~5 km',
wu:['2 min easy jog at conversational pace','10 high knees + 10 butt kicks (2 sets)','10 walking lunges each leg','10 leg swings front and back each leg','30 sec calf stretch each side'],
wod:'WALL ROAD — ~5 km running\\nFor time:\\n2 km run\\n30 Wall Ball shots (♀ 14 lb / ♂ 20 lb to 10 ft)\\n2 km run\\n20 Wall Ball shots\\n1 km run\\n10 Wall Ball shots\\n\\nKeep wall ball sets unbroken where possible.\\nScale: Reduce distances or reps by 20%.\\nTarget: 30–38 min.',
tags:['Wall ball','Running','~5 km','30–40 min']},

7:{t:'O',n:'Hang Power Clean',
wu:['90 sec: Jump rope or light jog','10 arm circles + 10 hip circles each direction','PVC: 10 pass-throughs, 10 overhead squats','Empty bar: 5 hang muscle cleans → 5 hang power cleans — 2 sets','Practice front rack: elbows high, bar on shoulders'],
str:'Hang Power Clean — Build to a heavy triple (3RM).\\nThen: 3 × 3 @ 85% of today\'s heavy triple.\\nFocus: explosive hip extension, fast elbow turnover, solid catch.',
wod:'CLEAN MACHINE\\n4 Rounds for time:\\n12 Hang Power Cleans (♀ 75 lb / ♂ 115 lb)\\n12 Burpees\\n15 Pull-ups\\n\\nRest 60 sec between rounds.\\nScale: Reduce load, sub ring rows for pull-ups.\\nTarget: 22–30 min.',
tags:['Barbell','Pull-up bar','22–30 min']},

8:{t:'G',n:'Pull-ups + Push-ups',
wu:['60 sec: Light jog in place','10 shoulder circles each direction','10 scap push-ups (elbows flared, retract shoulder blades)','20 sec dead hang on pull-up bar','10 kipping swings — find rhythm','10 push-ups (3-sec descent, pause at bottom, press up)'],
wod:'BAR & FLOOR\\n5 Rounds for time:\\n7 Pull-ups\\n7 Push-ups (strict)\\n7 Sit-ups\\n7 Air squats\\n\\nThen: EMOM 8 min\\nOdd min: max pull-ups (stop 1 rep before failure)\\nEven min: max push-ups (same rule)\\n\\nRecord totals. Scale pull-ups: banded or ring rows.\\nTarget: 5 rounds in sub-18 min.',
tags:['Pull-up bar','Bodyweight','25–35 min']},

9:{t:'R',n:'Rest Day',wu:[],
wod:'Full rest — Week 1 complete.\\n\\nWeek 1 running check:\\n✔ Tue 9 km · Wed 5 km · Sun 10 km = 24 km\\n(Optional: short 20 min easy walk today to top up to 25 km)\\n\\nFocus on: sleep, protein, and hydration.\\nWeek 2 is identical in structure — build confidence in the routine.',
tags:['Recovery']},

10:{t:'T',n:'Trail Run — Long',km:'11 km',
wu:['3 min: Walk to trail then easy jog','10 high knees + 10 butt kicks','10 walking lunges each leg','10 leg swings each direction','4 × 20 sec build-up strides, ease back into easy pace'],
wod:'LONG TRAIL — 11 km\\nEffort: Easy to moderate (Zone 2 mostly, Zone 3 on climbs)\\n\\nStructure:\\n→ km 0–3: pure easy, find your trail legs\\n→ km 3–9: steady effort, let terrain dictate pace\\n→ km 9–11: gradual build, finish feeling strong not spent\\n\\nFocus: proprioception — look ahead, pick foot placement, stay relaxed.\\nElite tip: Walk technical sections. Running efficiently beats running carelessly.\\nWeek 1 running: Run 3/3 · Weekly total: ~25 km ✓',
tags:['Trail','11 km','~70–85 min']},

11:{t:'S',n:'Deadlift',
wu:['90 sec: Jumping jacks or easy row','10 good mornings with PVC or empty bar','10 slow hip hinge RDLs with empty bar','Warm-up sets: 5 @ 40%, 3 @ 60%, 2 @ 75%, 1 @ 85% of working weight'],
str:'Deadlift — 5 × 3 @ 80–85% 1RM\\nRest 3 min between sets.\\nCues: hips back, chest tall, lat engagement before lift, bar drags up shins.',
wod:'DEAD SPRINT\\nFor time — 21–15–9:\\nDeadlifts (♀ 155 lb / ♂ 225 lb)\\nBox Jumps (24 in or broad jumps)\\n\\nRest 3 min, then 3 Rounds:\\n15 KB Swings (♀ 35 lb / ♂ 53 lb)\\n15 Push-ups\\n\\nTarget: sub-10 min for 21-15-9.',
tags:['Barbell','KB','18–28 min']},

12:{t:'T',n:'Trail Run — Fartlek',km:'9 km',
wu:['3 min: Easy jog to trail entrance','10 leg swings front/back each leg','10 high knees + 10 butt kicks','8 walking lunges each leg','2 × 30 sec easy stride to open up legs'],
wod:'FARTLEK — 9 km\\nEffort: Moderate with unstructured speed surges\\n\\nStructure:\\n→ km 0–1.5: easy warm-up\\n→ km 1.5–7.5: fartlek play — pick a tree/rock/corner and surge to it (10–30 sec), then settle back to easy. Aim for 10–15 surges.\\n→ km 7.5–9: easy cool-down\\n\\nFartlek = "speed play" in Swedish. No watch splits — run by feel.\\nBuilds speed without the pressure of structured intervals.\\nWeek 2 running: Run 1/3 · Cumulative this week: ~9 km of 25 km target.',
tags:['Trail','9 km','Fartlek','~55–70 min']},

13:{t:'E',n:'Tempo Run',km:'~5 km',
wu:['2 min: Easy jog, progressive','10 high knees + 10 butt kicks','10 leg swings each leg','4 × 20 sec build-up strides to tempo pace','60 sec easy jog shakeout'],
wod:'TEMPO GRIND — ~5 km\\n5 × 1 km at tempo pace (comfortably hard — short phrases only)\\nJog 90 sec between km reps\\n\\nThen immediately:\\n3 Rounds:\\n15 Push-ups\\n15 Sit-ups\\n15 Air squats\\n(No rest between rounds)\\n\\nTempo pace = effort where you can answer a question but not hold a conversation.\\nTotal run including warm-up: ~6 km.',
tags:['Running','~5 km','Bodyweight','35–45 min']},

14:{t:'O',n:'Power Snatch',
wu:['90 sec: Jump rope','10 large arm circles each direction','PVC: 10 overhead squats, 10 snatch-grip deadlifts','Empty bar: 3 × 5 hang muscle snatches → 3 × 3 hang power snatches','5 reps: "starfish" — fast drop into catch position'],
str:'Power Snatch — Build to a heavy single over 15 min.\\nThen: 5 × 2 @ 80% of today\'s heavy single.\\nFocus: bar close to body, aggressive hip extension, pull under fast.',
wod:'SNATCH & DASH\\n10 Rounds for time:\\n3 Power Snatches (♀ 65 lb / ♂ 95 lb)\\n6 Burpees\\n9 Air squats\\n\\nGo unbroken on snatches every round.\\nScale: Keep load light enough to not break singles.\\nTarget: 18–24 min.',
tags:['Barbell','20–26 min']},

15:{t:'M',n:'KB / DB MetCon',
wu:['90 sec: Jumping jacks','10 hip hinges (slow, hands on shins)','10 KB deadlifts with light KB','10 arm swings each direction','2 min: 10 KB swings + 5 goblet squats (light)'],
wod:'KB STORM\\nAMRAP 20 min:\\n10 KB Swings (♀ 44 lb / ♂ 70 lb)\\n10 Goblet Squats (same KB)\\n8 DB Renegade Rows (4 each side, ♀ 25 lb / ♂ 35 lb)\\n12 Push-ups\\n\\nScale: Reduce weights. Keep push-ups strict.\\nTarget: 6–8 rounds. Note: active recovery for legs after Tuesday trail run.',
tags:['Kettlebell','Dumbbell','20 min AMRAP']},

16:{t:'R',n:'Rest Day',wu:[],
wod:'Full rest — Week 2 complete.\\n\\nWeek 2 running check:\\n✔ Tue 9 km · Wed 5 km · Sun 11 km = 25 km ✓\\n\\nGreat consistency. Week 3 has the highest running volume (27 km).\\n\\nFocus on:\\n• Sleep (8+ hrs)\\n• Protein intake (1.6–2g per kg body weight)\\n• Hydration\\n• Light foam rolling or yoga if desired',
tags:['Recovery']},

17:{t:'T',n:'Trail Run — Recovery',km:'11 km',
wu:['3 min: Walk then very easy jog to trail','8 leg swings front/back each leg','8 hip circles each direction','2 min: easy jog, check in with your body — legs may feel heavy today'],
wod:'RECOVERY TRAIL — 11 km\\nEffort: Easy throughout (Zone 1–2). If legs feel tired, that is expected.\\n\\nStructure:\\n→ Full run at conversational pace — you should be able to sing\\n→ Walk any section that feels tight or technical\\n→ Treat this as moving meditation, not training\\n\\nThis follows a hard training week. Its purpose is blood flow and recovery.\\nPost-run: 5 min easy walk + 5–10 min stretch — hip flexors, calves, hamstrings.\\nWeek 3 running: Run 3/3 · Weekly total: ~25 km (of 27 km target — rest makes up the difference)',
tags:['Trail','11 km','Recovery','~65–80 min']},

18:{t:'S',n:'Front Squat',
wu:['90 sec: Jumping jacks','10 hip circles each direction','10 air squats — 3 sec pause at bottom','10 wrist circles + front rack stretch with PVC against wall','Empty bar: 3 × 5 front squats — build to 50% working weight'],
str:'Front Squat — 4 × 4 @ 78–83% 1RM\\nRest 2 min between sets.\\nCues: elbows high throughout, upright torso, knees track toes aggressively.',
wod:'FRONT LOADED\\n3 Rounds for time:\\n10 Front Squats (♀ 95 lb / ♂ 135 lb)\\n20 Wall Ball shots (♀ 14 lb / ♂ 20 lb)\\n15 Pull-ups\\n\\nScale: Reduce front squat load. Break wall balls into 10+10.\\nTarget: 22–30 min.',
tags:['Barbell','Wall ball','Pull-up bar','24–32 min']},

19:{t:'T',n:'Trail Run — Neg. Splits',km:'10 km',
wu:['3 min: Walk then easy jog to trail','10 high knees + 10 butt kicks','10 walking lunges each leg','4 × 15 sec building strides (60% → 70% → 80% → 90% effort)'],
wod:'NEGATIVE SPLITS — 10 km\\nGoal: every 2 km section is faster than the last.\\n\\nPacing plan:\\n→ km 0–2: very easy, hold back (feels almost too slow)\\n→ km 2–4: comfortable, start to feel the run\\n→ km 4–6: moderate effort, building confidence\\n→ km 6–8: comfortably hard, pushing now\\n→ km 8–10: strong finish, leave it all on the trail\\n\\nThis is a skill run — learning to start controlled and finish fast.\\nExpect the last 2 km to feel hard. That is the point.\\nWeek 3 running: Run 1/3 · Cumulative this week: ~10 km of 27 km target.',
tags:['Trail','10 km','Progression','~60–75 min']},

20:{t:'E',n:'Interval Run',km:'~5 km',
wu:['3 min: Easy jog progressive','4 × 20 sec strides at 85% effort with 40 sec easy jog','5 high knees, 5 butt kicks','30 sec calf stretch each side'],
wod:'SPEED LADDER — ~5 km\\n10 × 200m at 90–95% effort\\nRest: walk/jog 200m between reps (total ~4 km + warm-up jog)\\n\\nThen: Tabata Wall Ball\\n8 Rounds: 20 sec max wall ball shots / 10 sec rest\\nCount reps in lowest round as score.\\n\\nAim for consistent 200m splits — record each one.\\nTarget: same split ±3 sec across all 10 reps.',
tags:['Running','~5 km','Wall ball','35–45 min']},

21:{t:'O',n:'Clean & Jerk',
wu:['90 sec: Jump rope or light jog','10 arm circles + 10 hip circles each direction','PVC: 10 overhead squats, 5 tall jerks (footwork drill)','Empty bar: 3 × 3 hang power clean + push jerk → 2 × 2 clean + split jerk'],
str:'Clean & Jerk — Build to a heavy single over 15 min.\\nThen: 4 × 1+1 (1 power clean + 1 split jerk) @ 85% of today\'s heavy single.\\nFocus: fast elbows on clean, aggressive dip-drive on jerk.',
wod:'C&J GRIND\\n5 Rounds for time:\\n5 Clean & Jerks (♀ 85 lb / ♂ 125 lb)\\n10 Toes-to-bar (sub: hanging knee raises)\\n15 Wall Ball shots (♀ 14 lb / ♂ 20 lb)\\n\\nTarget: 22–28 min.',
tags:['Barbell','Wall ball','24–30 min']},

22:{t:'G',n:'HSPU + Pull-ups',
wu:['60 sec: Light jog','10 shoulder circles each direction','10 scap push-ups + 10 band pull-aparts','10 kipping swings on pull-up bar','5 strict pull-ups (slow up, slow down)','Handstand hold against wall: 20 sec × 2 (or pike push-up hold)'],
wod:'GYMNASTY\\n5 Rounds for time:\\n5 Strict Pull-ups\\n5 Strict Handstand Push-ups (sub: pike push-ups or Z-press with DB)\\n10 Ring Rows (or 10 kipping pull-ups)\\n10 Push-ups (feet elevated on box if available)\\n\\nSkill finisher: EMOM 6 min\\nOdd: max strict pull-up hold (chin over bar)\\nEven: max wall handstand hold time\\n\\nTarget: 5 rounds in 20–26 min.',
tags:['Pull-up bar','Bodyweight','25–35 min']},

23:{t:'R',n:'Rest Day',wu:[],
wod:'Full rest — Week 3 complete.\\n\\nWeek 3 running check:\\n✔ Tue 10 km · Wed 5 km · Sun 11 km = 26 km\\nPlus MetCon running (~1–2 km in WODs) = ~27–28 km ✓\\n\\nThis was your highest volume running week.\\nTomorrow is your longest single trail run of the month (12 km).\\nPrioritise dinner tonight: carbs + protein for fuel.',
tags:['Recovery']},

24:{t:'T',n:'Trail Run — Long',km:'12 km',
wu:['3 min: Walk then easy jog to trail','10 high knees + 10 butt kicks','10 walking lunges each leg','10 leg swings each direction','4 × 20 sec easy strides — do not go too hard, you have 12 km ahead'],
wod:'LONG TRAIL — 12 km\\nYour longest single run of the month. Approach with patience.\\nEffort: Easy-moderate (Zone 2 with Zone 3 on climbs)\\n\\nStructure:\\n→ km 0–3: fully easy, let body warm into it\\n→ km 3–9: comfortable sustainable effort, enjoy the scenery\\n→ km 9–11: build slightly if feeling good\\n→ km 11–12: easy cool-down, bring heart rate down on the way home\\n\\nNutrition: carry water and a gel/dates if going over 75 min.\\nFocus: breathing rhythm (inhale 3 steps, exhale 2), forward lean, quick feet on technical ground.\\nWeek 4 running: Run 3/3 · Weekly total: ~26 km ✓',
tags:['Trail','12 km','Long run','~75–100 min']},

25:{t:'S',n:'Push Press',
wu:['90 sec: Arm circles, shoulder rolls, jumping jacks','10 PVC pass-throughs','10 strict overhead press with PVC','5 push press with empty bar — focus on dip-drive-press timing','2 × 5 push press @ 40% then 50% working weight'],
str:'Push Press — 5 × 5 @ 75–80% 1RM\\nRest 2 min between sets.\\nCues: vertical dip (no forward lean), explosive leg drive, press to lockout, ribs down on return.',
wod:'PRESS OR DIE\\n21–15–9 for time:\\nPush Press (♀ 75 lb / ♂ 115 lb)\\nBurpees\\n\\nImmediately into: 5 min AMRAP\\n5 DB Push Press (♀ 35 lb / ♂ 50 lb each)\\n10 Push-ups\\n\\nTarget: sub-12 min for 21-15-9.',
tags:['Barbell','Dumbbell','18–25 min']},

26:{t:'T',n:'Trail Run — Hill Reps',km:'9 km',
wu:['3 min: Easy jog to trail / hill','10 high knees + 10 butt kicks','8 walking lunges each leg','4 × 20 sec easy uphill strides to activate glutes and calves'],
wod:'HILL REPS — 9 km\\nEffort: Hard on hills, easy recovery on downhill/flat\\n\\nStructure:\\n→ 2 km easy warm-up jog to your hill\\n→ 6 × uphill effort (find a 50–100 m steep section)\\n  - Push hard uphill at 90% effort (~20–30 sec)\\n  - Walk/jog back down (full recovery)\\n→ 3 km easy jog home\\n\\nHill reps build explosive leg power that transfers directly to CrossFit squats and cleans.\\nLean forward and drive knees up — short fast strides on the climb.\\nWeek 4 running: Run 1/3 · Cumulative this week: ~9 km of 26 km target.',
tags:['Trail','9 km','Hill reps','~55–70 min']},

27:{t:'E',n:'Tempo + KB',km:'~5 km',
wu:['3 min easy jog progressive','4 × 20 sec strides at 80–85% effort','60 sec easy shakeout','10 KB deadlifts (light — preview movements)'],
wod:'TEMPO FINISHER — ~5 km\\n4 × 1 km at tempo effort\\nRest: 90 sec easy jog between reps\\n\\nThen: 3 Rounds\\n15 KB Swings (♀ 44 lb / ♂ 70 lb)\\n10 Goblet Squats (same KB)\\n10 Dips (chairs/box)\\n\\nRecord each 1 km split. Aim to run km 4 faster than km 1.\\nWeek 4 running: Run 2/3 · Cumulative this week: ~14 km of 26 km target.',
tags:['Running','~5 km','KB','38–48 min']},

28:{t:'M',n:'Barbell Complex',
wu:['90 sec: Arm circles, hip openers, jumping jacks','10 PVC pass-throughs','5 empty-bar deadlifts → 5 hang cleans → 5 front squats → 5 push press (one complex)','Rest 60 sec, repeat with light load'],
wod:'THE COMPLEX\\n6 Rounds — record each round time (rest = work time):\\n6 Deadlifts\\n5 Hang Power Cleans\\n4 Front Squats\\n3 Push Press\\n2 Hang Squat Cleans\\n1 Thruster\\n(Same barbell ♀ 75 lb / ♂ 115 lb)\\n\\nDo NOT put bar down mid-complex. Rest only at top of lift.\\nScale: Reduce load — technique over weight here.\\nTarget: each round under 90 sec.',
tags:['Barbell','20–30 min']},

29:{t:'S',n:'Deadlift — Heavy',
wu:['90 sec: Jumping jacks or easy row','10 good mornings with PVC','10 slow RDLs — empty bar','Warm-up sets: 5@40%, 3@60%, 2@75%, 1@85%, 1@90%'],
str:'Deadlift — Build to a heavy double (2RM attempt).\\nThen: 3 × 2 @ 90% of today\'s double.\\nThis is your strongest pull of the month — honour it with perfect setup.',
wod:'FINAL PULL\\n3 Rounds for time:\\n12 Deadlifts (♀ 185 lb / ♂ 275 lb)\\n9 Hang Power Cleans (♀ 95 lb / ♂ 135 lb)\\n6 Push Jerks\\n12 Pull-ups\\n\\nScale all barbell loads to 65–70% 1RM.\\nTarget: 22–30 min.',
tags:['Barbell','Pull-up bar','24–32 min']},

30:{t:'R',n:'Rest Day',wu:[],
wod:'Final Saturday rest of the month.\\n\\nWeek 4 running so far:\\n✔ Tue 9 km · Wed 5 km = 14 km\\nSunday adds 12 km → weekly total ~26 km ✓\\n\\nTwo training days left — finish strong.\\n\\nOptional: 20 min mobility\\n• Hip flexor stretch 2 min each side\\n• Achilles and calf stretch (essential post-hill reps)\\n• Downward dog flow × 10',
tags:['Recovery']},

31:{t:'T',n:'Trail Run — Final',km:'12 km',
wu:['3 min: Walk then easy jog — savour the start of this last run','10 high knees + 10 butt kicks','10 walking lunges each leg','10 leg swings each direction'],
wod:'FINAL TRAIL — 12 km\\nThe last run of the month. Run it your way.\\n\\nOptions:\\n→ Run it easy and celebrate — you have earned this\\n→ Go by feel — push the second half if legs are good\\n→ Try for a personal best on your favourite trail segment\\n\\nMonth complete. Look back on what you have achieved:\\n✔ ~102 km of running across the month\\n✔ Strength cycles: squat, deadlift, press\\n✔ Olympic lifting: clean, jerk, snatch\\n✔ Gymnastics progressions\\n✔ MetCon conditioning\\n\\nYou showed up every time. That is what counts.',
tags:['Trail','12 km','Celebration','~70–90 min']}
};

const TYPE = {
  S:{l:'Strength',bg:'var(--str-bg)',tc:'var(--str-t)'},
  O:{l:'Olympic',bg:'var(--oly-bg)',tc:'var(--oly-t)'},
  G:{l:'Gymnastics',bg:'var(--gym-bg)',tc:'var(--gym-t)'},
  M:{l:'MetCon',bg:'var(--met-bg)',tc:'var(--met-t)'},
  T:{l:'Trail Run',bg:'var(--trl-bg)',tc:'var(--trl-t)'},
  E:{l:'Endurance',bg:'var(--end-bg)',tc:'var(--end-t)'},
  R:{l:'Rest',bg:'var(--rst-bg)',tc:'var(--rst-t)'}
};

let sel = null;
const cal = document.getElementById('cal');
const panel = document.getElementById('panel');

for (let i = 0; i < 4; i++) {
  const e = document.createElement('div');
  e.className = 'day empty';
  cal.appendChild(e);
}

for (let d = 1; d <= 31; d++) {
  const w = W[d], tp = TYPE[w.t];
  const div = document.createElement('div');
  div.className = 'day' + (w.t === 'R' ? ' rest' : '');
  div.innerHTML = `<div class="dnum">${d}</div>
    <div class="dbadge" style="background:${tp.bg};color:${tp.tc}">${tp.l}</div>
    <div class="dwname">${w.n}</div>
    ${w.km ? `<div class="dkm" style="color:${tp.tc}">${w.km}</div>` : ''}`;
  if (w.t !== 'R') div.onclick = () => openDay(d, div);
  cal.appendChild(div);
}

function openDay(d, el) {
  if (sel === el) {
    sel.classList.remove('sel');
    sel = null;
    panel.innerHTML = '';
    return;
  }
  if (sel) sel.classList.remove('sel');
  sel = el;
  el.classList.add('sel');
  const w = W[d], tp = TYPE[w.t];
  const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const dayName = days[(d + 3) % 7];
  let h = `<div class="panel">`;
  h += `<div class="ptop">
    <div class="picon" style="background:${tp.bg};color:${tp.tc}">${tp.l.replace(' ','<br>')}</div>
    <div><div class="ptitle">May ${d} — ${dayName}</div>
    <div class="psub">${tp.l}${w.km ? ' · ' + w.km : ''}</div></div>
    <div class="ptags">${(w.tags||[]).map(t=>`<span class="ptag">${t}</span>`).join('')}</div>
  </div>`;
  if (w.km) {
    h += `<div class="run-banner" style="background:${tp.bg}">
      <div class="run-km" style="color:${tp.tc}">${w.km}</div>
      <div style="font-size:13px;color:${tp.tc};opacity:.85">${tp.l === 'Trail Run' ? 'Trail run · shoes on · head up' : 'Running component — pace by effort'}</div>
    </div>`;
  }
  if (w.wu && w.wu.length) {
    h += `<div class="sec" style="margin-top:.5rem">Warm-up · 6–8 min</div>
    <div class="wu">${w.wu.map(i=>`<div class="wu-item"><div class="wu-dot"></div><div>${i}</div></div>`).join('')}</div>`;
  }
  if (w.str) {
    h += `<div class="sec">Strength / Skill work</div>
    <div class="box" style="background:${tp.bg};margin-bottom:.85rem">
    <div class="box-text" style="color:${tp.tc}">${w.str}</div></div>`;
  }
  h += `<div class="sec">${w.t==='T'?'Run plan':w.t==='E'?'Endurance WOD':w.t==='R'?'Recovery':'Workout of the Day'}</div>
  <div class="box" style="background:var(--bg2);border:0.5px solid var(--bd)">
  <div class="box-text" style="color:var(--tx2)">${w.wod}</div></div>`;
  h += `</div>`;
  panel.innerHTML = h;
  panel.scrollIntoView({behavior:'smooth', block:'nearest'});
}
</script>
</body>
</html>"""

components.html(HTML, height=1800, scrolling=True)
