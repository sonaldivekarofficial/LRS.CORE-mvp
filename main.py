from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

# =============================================
# LATENT RECURSION SYSTEM v6.0 – FINAL WORKING MVP
# Only 70 questions total (60 + 10 recursion)
# =============================================

questions = [
    # Vitality (1-10)
    {"id": 1, "element": "Vitality", "text": "In general, would you say your health is?", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]},
    {"id": 2, "element": "Vitality", "text": "During the past 4 weeks, how much did pain interfere with your normal work?", "options": ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 3, "element": "Vitality", "text": "Did you have a lot of energy?", "options": ["All of the time", "Most of the time", "Some of the time", "A little of the time", "None of the time"]},
    {"id": 4, "element": "Vitality", "text": "To what degree did you experience fatigue?", "options": ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"]},
    {"id": 5, "element": "Vitality", "text": "How often have you felt unable to control important things in your life?", "options": ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]},
    {"id": 6, "element": "Vitality", "text": "I am able to adapt when changes occur.", "options": ["Not true at all", "Rarely true", "Sometimes true", "Often true", "True nearly all the time"]},
    {"id": 7, "element": "Vitality", "text": "During the past month, how would you rate your sleep quality overall?", "options": ["Very good", "Fairly good", "Fairly bad", "Very bad"]},
    {"id": 8, "element": "Vitality", "text": "I have felt cheerful and in good spirits.", "options": ["At no time", "Some of the time", "Less than half", "More than half", "All of the time"]},
    {"id": 9, "element": "Vitality", "text": "I have felt calm and relaxed.", "options": ["At no time", "Some of the time", "Less than half", "More than half", "All of the time"]},
    {"id": 10, "element": "Vitality", "text": "I woke up feeling fresh and rested.", "options": ["At no time", "Some of the time", "Less than half", "More than half", "All of the time"]},

    # Connection (11-20)
    {"id": 11, "element": "Connection", "text": "I feel distant from people.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 12, "element": "Connection", "text": "How often do you feel that you lack companionship?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 13, "element": "Connection", "text": "How often do you feel left out?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 14, "element": "Connection", "text": "I'm afraid that I will lose my partner's love.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 15, "element": "Connection", "text": "I prefer not to show a partner how I feel deep down.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 16, "element": "Connection", "text": "There are several people I trust to help solve my problems.", "options": ["Definitely false", "Probably false", "Probably true", "Definitely true"]},
    {"id": 17, "element": "Connection", "text": "When I feel lonely, there are people I can talk to.", "options": ["Definitely false", "Probably false", "Probably true", "Definitely true"]},
    {"id": 18, "element": "Connection", "text": "There is someone I can turn to for advice.", "options": ["Definitely false", "Probably false", "Probably true", "Definitely true"]},
    {"id": 19, "element": "Connection", "text": "There is a special person around when I am in need.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 20, "element": "Connection", "text": "I can count on my friends when things go wrong.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Environment (21-30)
    {"id": 21, "element": "Environment", "text": "How safe do you feel in your neighborhood?", "options": ["Very poor", "Poor", "Fair", "Good", "Very good"]},
    {"id": 22, "element": "Environment", "text": "How clean and well-maintained is your home?", "options": ["Very poor", "Poor", "Fair", "Good", "Very good"]},
    {"id": 23, "element": "Environment", "text": "My workplace is physically comfortable.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 24, "element": "Environment", "text": "Rate your home's overall safety and functionality.", "options": ["Poor", "Fair", "Good", "Very good", "Excellent"]},
    {"id": 25, "element": "Environment", "text": "How often does clutter or disorganization affect your daily life?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 26, "element": "Environment", "text": "I feel in control of my screen time.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 27, "element": "Environment", "text": "There are sidewalks on most streets in my neighborhood.", "options": ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]},
    {"id": 28, "element": "Environment", "text": "It is easy to walk to a transit stop from my home.", "options": ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]},
    {"id": 29, "element": "Environment", "text": "My digital habits support my productivity.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 30, "element": "Environment", "text": "Social media positively impacts my well-being.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Growth (31-40)
    {"id": 31, "element": "Growth", "text": "I actively seek opportunities to learn new things.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 32, "element": "Growth", "text": "How strong is your ability to adapt when changes occur?", "options": ["Not strong", "Slightly strong", "Moderately strong", "Very strong", "Strongest"]},
    {"id": 33, "element": "Growth", "text": "I have found a meaningful career.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 34, "element": "Growth", "text": "Setbacks don't discourage me.", "options": ["Not like me at all", "Not much like me", "Somewhat like me", "Mostly like me", "Very much like me"]},
    {"id": 35, "element": "Growth", "text": "I am a hard worker.", "options": ["Not like me at all", "Not much like me", "Somewhat like me", "Mostly like me", "Very much like me"]},
    {"id": 36, "element": "Growth", "text": "I can always manage to solve difficult problems if I try hard enough.", "options": ["Not at all true", "Hardly true", "Moderately true", "Exactly true"]},
    {"id": 37, "element": "Growth", "text": "I am confident I could deal efficiently with unexpected events.", "options": ["Not at all true", "Hardly true", "Moderately true", "Exactly true"]},
    {"id": 38, "element": "Growth", "text": "Challenges motivate me to grow.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 39, "element": "Growth", "text": "How strong is your ability to prepare for the future?", "options": ["Not strong", "Slightly strong", "Moderately strong", "Very strong", "Strongest"]},
    {"id": 40, "element": "Growth", "text": "My work helps me better understand myself.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Stability (41-50)
    {"id": 41, "element": "Stability", "text": "I could handle a major unexpected expense.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]},
    {"id": 42, "element": "Stability", "text": "I am securing my financial future.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]},
    {"id": 43, "element": "Stability", "text": "How often have you had trouble paying bills?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 44, "element": "Stability", "text": "How often do you worry about money?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 45, "element": "Stability", "text": "I regularly set aside money for savings.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 46, "element": "Stability", "text": "I have a clear financial plan for the next year.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 47, "element": "Stability", "text": "I feel anxious about my financial situation.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 48, "element": "Stability", "text": "I worry about money.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 49, "element": "Stability", "text": "I feel stressed about my personal finances.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 50, "element": "Stability", "text": "I feel overwhelmed by my financial situation.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},

    # Meaning (51-60)
    {"id": 51, "element": "Meaning", "text": "I understand my life's meaning.", "options": ["Absolutely untrue", "Mostly untrue", "Somewhat untrue", "Can't say", "Somewhat true", "Mostly true", "Absolutely true"]},
    {"id": 52, "element": "Meaning", "text": "My life has a clear sense of purpose.", "options": ["Absolutely untrue", "Mostly untrue", "Somewhat untrue", "Can't say", "Somewhat true", "Mostly true", "Absolutely true"]},
    {"id": 53, "element": "Meaning", "text": "I find meaning in my relationships.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 54, "element": "Meaning", "text": "Contributing to society makes my life meaningful.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 55, "element": "Meaning", "text": "In life, I have clear goals and aims.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 56, "element": "Meaning", "text": "Interested.", "options": ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 57, "element": "Meaning", "text": "Inspired.", "options": ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 58, "element": "Meaning", "text": "I lead a purposeful and meaningful life.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 59, "element": "Meaning", "text": "I am engaged and interested in my daily activities.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 60, "element": "Meaning", "text": "I am optimistic about my future.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Recursion – ONLY 10 questions (61-70)
    {"id":61,"element":"Recursion","text":"Did a parent or adult often swear at, insult, or humiliate you?","options":["Yes","No"]},
    {"id":62,"element":"Recursion","text":"Did you often feel no one in your family loved you?","options":["Yes","No"]},
    {"id":63,"element":"Recursion","text":"Did you live with a substance abuser or alcoholic?","options":["Yes","No"]},
    {"id":64,"element":"Recursion","text":"Was a household member depressed or mentally ill?","options":["Yes","No"]},
    {"id":65,"element":"Recursion","text":"Were your parents separated or divorced?","options":["Yes","No"]},
    {"id":66,"element":"Recursion","text":"Was your mother/father often pushed, grabbed, or slapped?","options":["Yes","No"]},
    {"id":67,"element":"Recursion","text":"Did an adult touch or fondle you sexually or make me touch them?","options":["Yes","No"]},
    {"id":71,"element":"Recursion","text":"I felt emotionally neglected by my family.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":72,"element":"Recursion","text":"I was hit so hard it left marks or bruises.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":76,"element":"Recursion","text":"My household struggled financially and we barely had enough to make ends meet.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]}
]

# Group questions by element
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
    "abandonment_fear": {"title": "Abandonment Fear", "desc": "Recurring fear of being left that leads to isolation and self-sabotage."},
    "emotional_neglect_echo": {"title": "Emotional Neglect Echo", "desc": "Lingering emptiness from childhood emotional absence."},
    "self_doubt_cycle": {"title": "Self-Doubt Cycle", "desc": "Persistent inner critic blocking decisions and self-expression."},
    "trust_deficit": {"title": "Trust Deficit", "desc": "Deep difficulty trusting others from betrayal or inconsistency."},
    "failure_phobia": {"title": "Failure Phobia", "desc": "Terror of failing that paralyzes action."}
}

def calculate_element_scores(responses):
    scores = {}
    for el, qs in element_groups.items():
        if el == "Recursion": continue
        total = count = 0
        max_val = len(qs[0]["options"]) if qs and qs[0]["options"] else 5
        for q in qs:
            val = responses.get(str(q["id"]))
            if val and q["options"]:
                total += q["options"].index(val)
                count += 1
        scores[el] = round((total / (count * (max_val - 1)) * 100)) if count else 50
    return scores

def detect_recursions(responses, element_scores):
    ace = sum(1 for i in range(61,68) if responses.get(str(i)) == "Yes")
    emo_neglect = ["Often true","Very often true"].count(responses.get("71",""))
    phys_abuse = ["Often true","Very often true"].count(responses.get("72",""))
    fin_struggle = ["Often true","Very often true"].count(responses.get("76",""))

    candidates = []
    for key, r in recursions_defs.items():
        score = 20
        reasons = []
        if key == "abandonment_fear":
            score += ace * 10
            if element_scores.get("Connection",100) < 65: score += 30
            if element_scores.get("Meaning",100) < 65: score += 20
        elif key == "emotional_neglect_echo":
            score += emo_neglect * 25 + ace * 8
            if element_scores.get("Meaning",100) < 65: score += 30
        elif key == "self_doubt_cycle":
            score += emo_neglect * 20 + phys_abuse * 15
            if element_scores.get("Growth",100) < 65: score += 30
        elif key == "trust_deficit":
            score += ace * 12
            if element_scores.get("Connection",100) < 65: score += 35
        elif key == "failure_phobia":
            score += phys_abuse * 20 + fin_struggle * 15
            if element_scores.get("Growth",100) < 65: score += 30
            if element_scores.get("Stability",100) < 65: score += 20

        score = min(100, score)
        if score > 45:
            affected = [e for e, s in element_scores.items() if s < 65]
            candidates.append({
                "title": r["title"],
                "description": r["desc"],
                "strength": score,
                "currently_pulling": affected or ["None – largely resolved"],
                "reasons": reasons
            })
    return candidates[:3] or [{"title":"No major recursion detected","description":"Your biome is free and expanding.","strength":0,"currently_pulling":[],"reasons":[]}]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.json
    scores = calculate_element_scores(data)
    recursions = detect_recursions(data, scores)
    avg_rec = sum(r["strength"] for r in recursions) / max(1, len(recursions))
    return jsonify({"scores": scores, "recursions": recursions, "avg_recursion": avg_rec})

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Find My Latent Pattern</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
  <style>.tree{{transition:all 1.5s}}.ring{{transition:all 1.5s}}</style>
</head>
<body class="bg-gradient-to-br from-slate-950 to-slate-900 text-white min-h-screen">
  <div class="container mx-auto p-6 max-w-5xl">
    <h1 class="text-6xl font-bold text-center text-teal-400 mt-12 mb-4">Find My Latent Pattern</h1>
    <p class="text-center text-gray-300 text-xl mb-12">The MRI Scan of Your Personal Biome</p>
    <div class="text-center mb-12">
      <div class="w-full bg-gray-800 rounded-full h-4"><div id="progress" class="bg-teal-500 h-4 rounded-full transition-all" style="width:0%"></div></div>
      <p class="mt-4 text-gray-400" id="progress-text">0/70</p>
    </div>
    <div id="assessment" class="space-y-12"></div>
    <div id="biome-container" class="my-16 text-center hidden">
      <h2 class="text-4xl font-bold mb-8 text-teal-400">Your Personal Biome</h2>
      <canvas id="biome" width="700" height="700" class="mx-auto border-4 border-teal-600 rounded-3xl shadow-2xl"></canvas>
      <p class="mt-6 text-lg text-gray-400">Ring tightens when recursions are active</p>
    </div>
    <div id="results" class="hidden mt-16 space-y-12"></div>
  </div>

  <script>
    const elements = ['Vitality','Connection','Environment','Growth','Stability','Meaning','Recursion'];
    const allQuestions = {json.dumps(questions)};
    const elementGroups = {{Vitality: allQuestions.filter(q=>q.element==='Vitality'), Connection: allQuestions.filter(q=>q.element==='Connection'), Environment: allQuestions.filter(q=>q.element==='Environment'), Growth: allQuestions.filter(q=>q.element==='Growth'), Stability: allQuestions.filter(q=>q.element==='Stability'), Meaning: allQuestions.filter(q=>q.element==='Meaning'), Recursion: allQuestions.filter(q=>q.element==='Recursion')}};
    let responses = {{}}, current = 0;
    let scene, camera, renderer, trees=[], ring;

    function initBiome() {{
      const canvas = document.getElementById('biome');
      scene = new THREE.Scene(); scene.background = new THREE.Color(0x0f172a);
      camera = new THREE.PerspectiveCamera(60,1,0.1,1000);
      renderer = new THREE.WebGLRenderer({{canvas, antialias:true}}); renderer.setSize(700,700);
      const geo = new THREE.DodecahedronGeometry(0.6);
      const mat = new THREE.MeshBasicMaterial({{color:0x00ffaa, wireframe:true}});
      const user = new THREE.Mesh(geo, mat); user.position.y = 0.6; scene.add(user);
      const ringGeo = new THREE.TorusGeometry(5,0.2,16,100);
      const ringMat = new THREE.MeshBasicMaterial({{color:0xff0066}});
      ring = new THREE.Mesh(ringGeo, ringMat); ring.rotation.x = Math.PI/2; scene.add(ring);
      camera.position.z = 12;
      animate();
    }}
    function animate(){{ requestAnimationFrame(animate); ring.rotation.z += 0.008; renderer.render(scene,camera); }}
    function updateBiome(scores, avg){{
      trees.forEach(t=>scene.remove(t)); trees=[];
      const config = [
        {{el:"Vitality",x:-4.5,c:0x00ff88}},{{el:"Connection",x:-2.5,c:0x4488ff}},
        {{el:"Environment",x:-0.5,c:0xffaa00}},{{el:"Growth",x:1.5,c:0xff00ff}},
        {{el:"Stability",x:3.5,c:0xffff00}},{{el:"Meaning",x:5.5,c:0xff0088}}
      ];
      config.forEach(p=>{{ const h = (scores[p.el]||50)/100*5 + 0.8;
        const geo = new THREE.CylinderGeometry(0.5,0.7,h,8);
        const mat = new THREE.MeshBasicMaterial({{color:p.c}});
        const tree = new THREE.Mesh(geo,mat); tree.position.set(p.x,h/2,0); scene.add(tree); trees.push(tree);
      }});
      const con = 1 + (avg/100)*0.6; ring.scale.set(con,con,1);
      ring.material.color.setHex(avg>60?0xff0033:avg>30?0xff8800:0x00ff88);
    }}
    function updateProgress(){{ const answered = Object.keys(responses).length;
      document.getElementById('progress').style.width = (answered/70*100)+'%';
      document.getElementById('progress-text').innerText = elements[current] + ' – ' + answered + '/70';
    }}
    function loadElement() {{
      const el = elements[current];
      const qs = elementGroups[el];
      const div = document.getElementById('assessment'); div.innerHTML = `<h2 class="text-4xl font-bold text-teal-400 mb-10">${{el}}</h2>`;
      qs.forEach(q=>{{ const block = document.createElement('div'); block.className = 'bg-slate-800 p-6 rounded-2xl mb-6';
        block.innerHTML = `<p class="font-medium text-lg mb-4">${{q.id}}. ${{q.text}}</p>`;
        if(q.options.length>0){{
          const opts = document.createElement('div'); opts.className = 'grid grid-cols-1 md:grid-cols-5 gap-3';
          q.options.forEach(opt=>{{ const label = document.createElement('label');
            label.className = 'flex items-center p-3 bg-slate-700 rounded hover:bg-teal-600 cursor-pointer transition';
            label.innerHTML = `<input type="radio" name="q${{q.id}}" value="${{opt}}" class="mr-3"><span>${{opt}}</span>`;
            opts.appendChild(label);
          }});
          block.appendChild(opts);
        }} else {{
          const ta = document.createElement('textarea'); ta.className = 'w-full p-4 bg-slate-700 rounded text-white';
          ta.placeholder = 'Your answer...'; block.appendChild(ta);
        }}
        div.appendChild(block);
      }});
      const btn = document.createElement('button');
      btn.textContent = current<6?'Next Element →':'Generate My Biome & Recursions';
      btn.className = 'w-full py-6 bg-teal-600 hover:bg-teal-500 rounded-2xl font-bold text-2xl mt-10';
      btn.onclick = () => {{
        qs.forEach(q=>{{ if(q.options.length>0){{
          const sel = document.querySelector(`input[name="q${{q.id}}"]:checked`);
          if(sel) responses[q.id] = sel.value;
        }} else {{
          const ta = div.querySelector('textarea');
          if(ta) responses[q.id] = ta.value.trim();
        }}}});
        updateProgress(); current++;
        if(current<7) loadElement(); else submit();
      }};
      div.appendChild(btn);
    }}
    function submit() {{
      fetch('/assess',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(responses)}})
      .then(r=>r.json()).then(d=>{{
        document.getElementById('assessment').classList.add('hidden');
        document.getElementById('biome-container').classList.remove('hidden');
        updateBiome(d.scores, d.avg_recursion);
        let html = `<h2 class="text-5xl font-bold text-center text-teal-400 mb-12">Your Latent Recursions</h2>`;
        if(d.recursions[0].strength===0){{
          html += `<p class="text-2xl text-center text-green-400 font-bold">No major recursion detected.<br>Your biome is free and expanding.</p>`;
        }} else {{
          d.recursions.forEach((r,i)=>{{
            const pull = r.currently_pulling.length ? r.currently_pulling.join(", ") : "None – largely resolved";
            html += `
            <div class="p-8 bg-gradient-to-br from-red-950 to-purple-950 rounded-3xl border ${{r.strength>70?'border-red-500':'border-orange-500'}}">
              <p class="text-3xl font-bold">${{i+1}}. ${{r.title}}</p>
              <p class="text-5xl font-bold my-4 ${{r.strength>70?'text-red-400':'text-orange-400'}}">${{r.strength}}% Active</p>
              <p class="text-lg mb-6">${{r.description}}</p>
              <p class="text-xl font-semibold text-yellow-300">Currently pulling on: ${{pull}}</p>
            </div>`;
          }});
        }}
        html += `<h2 class="text-5xl font-bold text-center text-teal-400 mt-20 mb-10">Your 30-Day Journey</h2>
        <div class="bg-slate-800 p-10 rounded-3xl text-lg space-y-4">
          <p>Days 1–5: Daily journaling of repeating patterns</p>
          <p>Days 6–10: Map causes and cycles</p>
          <p>Days 11–15: Radical self-honesty</p>
          <p>Days 16–30: Re-design and daily action</p>
        </div>`;
        document.getElementById('results').innerHTML = html;
        document.getElementById('results').classList.remove('hidden');
      }});
    }}
    initBiome(); loadElement();
  </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
