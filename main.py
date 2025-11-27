from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

questions = [
    # Vitality (1-10)
    {"id":1,"element":"Vitality","text":"In general, would you say your health is?","options":["Excellent","Very good","Good","Fair","Poor"]},
    {"id":2,"element":"Vitality","text":"During the past 4 weeks, how much did pain interfere with your normal work?","options":["Not at all","A little bit","Moderately","Quite a bit","Extremely"]},
    {"id":3,"element":"Vitality","text":"During the past 4 weeks, did you have a lot of energy?","options":["All of the time","Most of the time","Some of the time","A little of the time","None of the time"]},
    {"id":4,"element":"Vitality","text":"During the past 4 weeks, to what degree did you experience mental exhaustion?","options":["Not at all","A little bit","Somewhat","Quite a bit","Very much"]},
    {"id":5,"element":"Vitality","text":"During the past 4 weeks, how would you rate your sleep quality overall?","options":["Very good","Fairly good","Fairly bad","Very bad"]},
    {"id":6,"element":"Vitality","text":"How often do you feel unable to control important things in your life?","options":["Never","Almost never","Sometimes","Fairly often","Very often"]},
    {"id":7,"element":"Vitality","text":"I am able to adapt when changes occur.","options":["Not true at all","Rarely true","Sometimes true","Often true","True nearly all the time"]},
    {"id":8,"element":"Vitality","text":"I am often cheerful and in good spirits.","options":["At no time","Some of the time","Less than half the time","More than half the time","All of the time"]},
    {"id":9,"element":"Vitality","text":"I have felt calm and relaxed.","options":["At no time","Some of the time","Less than half the time","More than half the time","All of the time"]},
    {"id":10,"element":"Vitality","text":"I have enough physical and mental energy to fully engage in work, family, friends, and hobbies.","options":["Never","Almost never","Sometimes","Fairly often","Very often"]},

    # Connection (11-20)
    {"id":11,"element":"Connection","text":"How often do you feel that you lack companionship?","options":["Hardly ever","Some of the time","Often"]},
    {"id":12,"element":"Connection","text":"How often do you feel left out among family, friends, or at work?","options":["Hardly ever","Some of the time","Often"]},
    {"id":13,"element":"Connection","text":"I'm afraid that I will lose my partner's love.","options":["Strongly disagree","Disagree","Slightly disagree","Neutral","Slightly agree","Agree","Strongly agree"]},
    {"id":14,"element":"Connection","text":"I prefer not to show a partner how I feel deep down.","options":["Strongly disagree","Disagree","Slightly disagree","Neutral","Slightly agree","Agree","Strongly agree"]},
    {"id":15,"element":"Connection","text":"I can count on my friends/family when things go wrong.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":16,"element":"Connection","text":"When I feel lonely, there are people I can talk to.","options":["Definitely false","Probably false","Probably true","Definitely true"]},
    {"id":17,"element":"Connection","text":"I have healthy relationships with my neighbours and colleagues.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":18,"element":"Connection","text":"Social media negatively impacts my mental health.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":19,"element":"Connection","text":"I am in control of my screen time.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":20,"element":"Connection","text":"My digital habits support my productivity.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Environment (21-30)
    {"id":21,"element":"Environment","text":"How safe do you feel in your neighborhood?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":22,"element":"Environment","text":"How clean and well-maintained is your neighbourhood?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":23,"element":"Environment","text":"I have access to park/garden/green space around my neighborhood.","options":["Strongly disagree","Disagree","Agree","Strongly agree"]},
    {"id":24,"element":"Environment","text":"How clean and well-maintained is your home?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":25,"element":"Environment","text":"I have enough private space in my home","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":26,"element":"Environment","text":"I feel safe and comfortable in my home","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":27,"element":"Environment","text":"How often does clutter or disorganization affect your daily life?","options":["Never","Rarely","Sometimes","Often","Always"]},
    {"id":28,"element":"Environment","text":"Rate your work place’s overall comfortability and functionality.","options":["Poor","Fair","Good","Very good","Excellent"]},
    {"id":29,"element":"Environment","text":"Transit from my home to work and city is often comfortable.","options":["Strongly disagree","Disagree","Agree","Strongly agree"]},
    {"id":30,"element":"Environment","text":"My home/work space/ neighbourhood positively impacts my well-being.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Growth (31-40)
    {"id":31,"element":"Growth","text":"I have found a meaningful career.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":32,"element":"Growth","text":"My work is aligned with my career goals.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":33,"element":"Growth","text":"I actively seek opportunities for career growth within my work space.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":34,"element":"Growth","text":"I actively seek opportunities to learn new skills.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":35,"element":"Growth","text":"I actively seek opportunities to switch job for higher pay and designation.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":36,"element":"Growth","text":"Setbacks don't discourage me.","options":["Not like me at all","Not much like me","Somewhat like me","Mostly like me","Very much like me"]},
    {"id":37,"element":"Growth","text":"I always manage to solve problems and get things done","options":["Not at all true","Hardly true","Moderately true","Exactly true"]},
    {"id":38,"element":"Growth","text":"I am confident I could deal efficiently with unexpected events like loss of job.","options":["Not at all true","Hardly true","Moderately true","Exactly true"]},
    {"id":39,"element":"Growth","text":"Challenges motivate me to grow.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":40,"element":"Growth","text":"How strong is your ability to prepare for the future?","options":["Not strong","Slightly strong","Moderately strong","Very strong","Strongest"]},

    # Stability (41-50) — NOW VISIBLE
    {"id":41,"element":"Stability","text":"I feel financially secure most of the time.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":42,"element":"Stability","text":"I have a reliable safety net (savings, insurance, support).","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":43,"element":"Stability","text":"My income covers my needs comfortably.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":44,"element":"Stability","text":"I rarely worry about money.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":45,"element":"Stability","text":"I live in a stable and predictable environment.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":46,"element":"Stability","text":"My relationships feel secure and dependable.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":47,"element":"Stability","text":"I have consistent routines that support my well-being.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":48,"element":"Stability","text":"Unexpected events rarely derail my life.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":49,"element":"Stability","text":"I trust that tomorrow will be okay.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":50,"element":"Stability","text":"Overall, my life feels steady and grounded.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Meaning (51-60)
    {"id":51,"element":"Meaning","text":"I am engaged and interested in my daily activities.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":52,"element":"Meaning","text":"In life, I have clear goals and aims.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":53,"element":"Meaning","text":"My relationships are genuine.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":54,"element":"Meaning","text":"I feel genuinely interested in lives of people around me.","options":["Very slightly or not at all","A little","Moderately","Quite a bit","Extremely"]},
    {"id":55,"element":"Meaning","text":"I personally know some people who earnestly try to make positive difference in the world","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":56,"element":"Meaning","text":"I contribute to society with act of service/food donations/financial help.","options":["Very slightly or not at all","A little","Moderately","Quite a bit","Extremely"]},
    {"id":57,"element":"Meaning","text":"I don't hold grudges, I find it easy to forgive and move on","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":58,"element":"Meaning","text":"My life has a clear sense of purpose.","options":["Absolutely untrue","Mostly untrue","Somewhat untrue","Can't say","Somewhat true","Mostly true","Absolutely true"]},
    {"id":59,"element":"Meaning","text":"I try to lead a purposeful and meaningful life.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":60,"element":"Meaning","text":"I am optimistic about my future.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Recursion (61-70) — trauma questions
    {"id":61,"element":"Recursion","text":"Did a parent or adult often swear at, insult, or humiliate you?","options":["Yes","No"]},
    {"id":62,"element":"Recursion","text":"Did you often feel no one in your family understood you?","options":["Yes","No"]},
    {"id":63,"element":"Recursion","text":"Did you live with a substance abuser or alcoholic?","options":["Yes","No"]},
    {"id":64,"element":"Recursion","text":"Was a household member depressed or mentally ill?","options":["Yes","No"]},
    {"id":65,"element":"Recursion","text":"Were your parents separated or divorced?","options":["Yes","No"]},
    {"id":66,"element":"Recursion","text":"Was your mother/father often pushed, grabbed, or slapped?","options":["Yes","No"]},
    {"id":67,"element":"Recursion","text":"Did an adult touch or fondle you sexually or make you touch them?","options":["Yes","No"]},
    {"id":71,"element":"Recursion","text":"I felt emotionally neglected by my family.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":72,"element":"Recursion","text":"I was hit so hard it left marks or bruises.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":76,"element":"Recursion","text":"My household struggled financially and we barely had enough to make ends meet.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]}
]

# Group by element
element_groups = {
    "Vitality": [q for q in questions if q["element"] == "Vitality"],
    "Connection": [q for q in questions if q["element"] == "Connection"],
    "Environment": [q for q in questions if q["element"] == "Environment"],
    "Growth": [q for q in questions if q["element"] == "Growth"],
    "Stability": [q for q in questions if q["element"] == "Stability"],
    "Meaning": [q for q in questions if q["element"] == "Meaning"],
    "Recursion": [q for q in questions if q["element"] == "Recursion"]
}

recursions_defs = {
    "abandonment_fear": {"title":"Abandonment Fear","desc":"Fear of being left or rejected, recurring from early instability."},
    "emotional_neglect_echo": {"title":"Emotional Neglect Echo","desc":"Persistent emptiness from unmet emotional needs in childhood."},
    "trust_deficit": {"title":"Trust Deficit","desc":"Difficulty trusting others due to early betrayal or inconsistency."},
    "self_worth_wound": {"title":"Self-Worth Wound","desc":"Deep feeling of unworthiness from early humiliation or criticism."},
    "chaos_adaptation": {"title":"Chaos Adaptation","desc":"Attraction to unstable situations as they feel familiar."},
    "perfectionism_trap": {"title":"Perfectionism Trap","desc":"Relentless drive for flawlessness causing burnout."},
    "failure_aversion": {"title":"Failure Aversion","desc":"Extreme fear of failing, limiting risk-taking."},
    "identity_confusion": {"title":"Identity Confusion","desc":"Struggle with self-identity from early invalidation."},
    "emotional_suppression": {"title":"Emotional Suppression","desc":"Habit of suppressing emotions from dismissive early environments."},
    "financial_anxiety_loop": {"title":"Financial Anxiety Loop","desc":"Ongoing fear of poverty from childhood financial struggle."}
}

def calculate_element_scores(responses):
    scores = {}
    for el, qs in element_groups.items():
        if el == "Recursion": continue
        total = count = 0
        for q in qs:
            val = responses.get(str(q["id"]))
            if not val: continue
            idx = q["options"].index(val)
            negative = any(k in q["text"].lower() for k in ["pain","exhaustion","unable","lack","left out","negatively","clutter","poor","never","worry","stressed","interfere"])
            val_num = len(q["options"])-1 - idx if negative else idx
            total += val_num
            count += 1
        max_val = len(q["options"])-1 if count else 1
        scores[el] = round((total / (count * max_val)) * 100) if count else 50
    return scores

def detect_recursions(responses, scores):
    ace = sum(1 for i in range(61,68) if responses.get(str(i)) == "Yes")
    emo = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("71","Rarely true"))
    phys = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("72","Rarely true"))
    fin = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("76","Rarely true"))
    v,c,e,g,s,m = (scores.get(k,50) for k in ["Vitality","Connection","Environment","Growth","Stability","Meaning"])

    candidates = []
    for key, r in recursions_defs.items():
        sc = 0
        if key=="abandonment_fear": sc = 35 + ace*9 + emo*6 + (100-c)*0.8 + (100-m)*0.6
        elif key=="emotional_neglect_echo": sc = 35 + emo*15 + (100-m)*0.9
        elif key=="trust_deficit": sc = 35 + ace*12 + (100-c)*0.9
        elif key=="self_worth_wound": sc = 35 + emo*10 + phys*10 + (100-g)*0.8
        elif key=="chaos_adaptation": sc = 35 + fin*10 + ace*8 + (100-s)*0.9
        elif key=="perfectionism_trap": sc = 35 + emo*12 + (100-g)*0.9
        elif key=="failure_aversion": sc = 35 + phys*12 + (100-g)*0.9
        elif key=="identity_confusion": sc = 35 + emo*12 + (100-m)*0.9
        elif key=="emotional_suppression": sc = 35 + emo*14 + (100-v)*0.8
        elif key=="financial_anxiety_loop": sc = 35 + fin*16 + (100-s)*0.9
        sc = min(100, int(sc))
        if sc > 45:
            affected = [el for el,score in scores.items() if score < 65]
            candidates.append({"title":r["title"],"desc":r["desc"],"strength":sc,"affected":affected or ["None"]})
    return sorted(candidates, key=lambda x: x["strength"], reverse=True)[:2]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.get_json()
    if len(data) < 70:
        return jsonify({"error": "Please answer all 70 questions for accurate results."}), 400
    scores = calculate_element_scores(data)
    recursions = detect_recursions(data, scores)
    avg = sum(r["strength"] for r in recursions)/len(recursions) if recursions else 0
    return jsonify({"scores": scores, "recursions": recursions, "avg_recursion": avg})

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/><title>Latent Recursion System</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
</head><body class="bg-gradient-to-br from-slate-950 to-slate-900 text-white min-h-screen">
<div class="container mx-auto p-6 max-w-5xl">
<h1 class="text-5xl font-bold text-center text-teal-400 mt-8 mb-2">Latent Recursion System</h1>
<p class="text-center text-gray-300 mb-12 text-xl">Discover hidden patterns from your past that keep you stuck today.</p>
<div class="text-center mb-12"><div class="w-full bg-gray-800 rounded-full h-3">
<div id="progress" class="bg-teal-500 h-3 rounded-full transition-all duration-1000" style="width:0%"></div></div>
<p class="mt-4 text-gray-400" id="progress-text">0/70</p></div>
<div id="assessment" class="space-y-12"></div>
<div id="biome-container" class="my-16 text-center hidden"><h2 class="text-3xl font-bold mb-8">Your Personal Biome</h2>
<canvas id="biome" width="600" height="600" class="mx-auto border-4 border-teal-600 rounded-2xl shadow-2xl"></canvas></div>
<div id="results" class="hidden mt-12 p-8 bg-slate-800 rounded-2xl shadow-2xl space-y-8"></div>
</div>

<script>
const questions = {json.dumps(questions)};
const groups = {json.dumps({k: [q["id"] for q in v] for k,v in element_groups.items()})};
const order = ['Vitality','Connection','Environment','Growth','Stability','Meaning','Recursion'];
let responses = {{}}, current = 0;
let scene, camera, renderer, trees = [], ring, userOrb;

function initBiome() {{
  const canvas = document.getElementById('biome');
  scene = new THREE.Scene(); scene.background = new THREE.Color(0x0f172a);
  camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({{canvas, antialias:true}}); renderer.setSize(600,600);
  const geo = new THREE.DodecahedronGeometry(0.6,0);
  const mat = new THREE.MeshBasicMaterial({{color:0x00ffaa, wireframe:true}});
  userOrb = new THREE.Mesh(geo, mat); userOrb.position.y = 0.6; scene.add(userOrb);
  const ringGeo = new THREE.TorusGeometry(4.5, 0.2, 16, 100);
  const ringMat = new THREE.MeshBasicMaterial({{color:0xff0066}});
  ring = new THREE.Mesh(ringGeo, ringMat); ring.rotation.x = Math.PI/2; scene.add(ring);
  camera.position.z = 12; animate();
}}
function animate() {{ requestAnimationFrame(animate); ring.rotation.z += 0.008; userOrb.rotation.y += 0.005; renderer.render(scene,camera); }}

function updateBiome(scores, avg) {{
  trees.forEach(t => scene.remove(t)); trees = [];
  const cfg = [
    {{el:'Vitality', a:0, c:0x00ff88}}, {{el:'Connection', a:Math.PI*0.33, c:0x4488ff}},
    {{el:'Environment', a:Math.PI*0.66, c:0xffaa00}}, {{el:'Growth', a:Math.PI, c:0xff00ff}},
    {{el:'Stability', a:Math.PI*1.33, c:0xffff00}}, {{el:'Meaning', a:Math.PI*1.66, c:0xff0088}}
  ];
  cfg.forEach(o => {{
    const h = (scores[o.el]||50)/100*4 + 0.5;
    const geo = new THREE.CylinderGeometry(0.4,0.6,h,8);
    const mat = new THREE.MeshBasicMaterial({{color:o.c}});
    const tree = new THREE.Mesh(geo,mat);
    tree.position.set(Math.cos(o.a)*4, h/2, Math.sin(o.a)*4);
    scene.add(tree); trees.push(tree);
  }});
  const con = avg/100;
  ring.scale.set(1+con*1.5,1+con*1.5,1);
  ring.material.color.setHex(con > 0.5 ? 0xff0000 : 0x00ff66);
}}

function loadElement() {{
  const el = order[current];
  const ids = groups[el];
  const qs = questions.filter(q => ids.includes(q.id));
  const cont = document.getElementById('assessment');
  cont.innerHTML = `<h2 class="text-3xl font-bold text-teal-400 mb-8">${{el}}</h2>`;
  qs.forEach(q => {{
    const div = document.createElement('div');
    div.className = 'bg-slate-800 p-6 rounded-xl mb-6';
    div.innerHTML = `<p class="font-medium mb-4">${{q.id}}. ${{q.text}}</p><div class="grid grid-cols-1 md:grid-cols-${{Math.min(5,q.options.length)}} gap-4"></div>`;
    const opts = div.lastChild;
    q.options.forEach(opt => {{
      const lbl = document.createElement('label');
      lbl.className = 'flex items-center p-3 bg-slate-700 rounded hover:bg-teal-600 cursor-pointer transition';
      lbl.innerHTML = `<input type="radio" name="q${{q.id}}" value="${{opt}}" class="mr-3"><span>${{opt}}</span>`;
      opts.appendChild(lbl);
    }});
    cont.appendChild(div);
  }});
  const btn = document.createElement('button');
  btn.textContent = current < 6 ? 'Next Element →' : 'See My Results';
  btn.className = 'w-full p-5 bg-teal-600 hover:bg-teal-500 rounded-xl font-bold text-xl mt-8';
  btn.onclick = () => {{
    qs.forEach(q => {{ const sel = document.querySelector(`input[name="q${{q.id}}"]:checked`); if(sel) responses[q.id] = sel.value; }});
    if (Object.keys(responses).length < 70) {{ alert("Please answer all 70 questions for accurate results."); return; }}
    current < 6 ? (current++, loadElement()) : submit();
  }};
  cont.appendChild(btn);
  document.getElementById('progress').style.width = `${{Object.keys(responses).length/70*100}}%`;
  document.getElementById('progress-text').innerText = `${{el}} – ${{Object.keys(responses).length}}/70`;
}}

function submit() {{
  fetch('/assess', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body:JSON.stringify(responses)}})
  .then(r => r.json()).then(d => {{
    if(d.error) {{ alert(d.error); return; }}
    document.getElementById('assessment').classList.add('hidden');
    document.getElementById('biome-container').classList.remove('hidden');
    updateBiome(d.scores, d.avg_recursion);
    let html = `<h2 class="text-4xl font-bold text-center text-teal-400 mb-8">Your Top 2 Latent Recursions</h2>`;
    if(d.recursions.length === 0 || d.recursions[0].strength === 0) {{
      html += `<p class="text-2xl text-center text-green-400">No major recursion detected. Your biome is free and expanding.</p>`;
    }} else {{
      d.recursions.forEach((r,i) => {{
        html += `<div class="p-6 bg-red-950/50 rounded-xl border border-red-600 mb-6">
          <p class="text-2xl font-bold">${{i+1}}. ${{r.title}} – ${{r.strength}}%</p>
          <p class="text-lg mt-2">${{r.desc}}</p>
          <p class="text-sm text-gray-400 mt-4">Strongly affecting: ${{r.affected.join(' · ')}}</p>
        </div>`;
      }});
    }}
    document.getElementById('results').innerHTML = html;
    document.getElementById('results').classList.remove('hidden');
  }});
}}

initBiome(); loadElement();
</script></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
