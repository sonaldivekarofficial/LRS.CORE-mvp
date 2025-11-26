from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

# =============================================
# LATENT RECURSION SYSTEM – FINAL WORKING VERSION
# =============================================

questions = [
    # Vitality 1-10
    {"id": 1, "element": "Vitality", "text": "In general, would you say your health is?", "options": ["Excellent","Very good","Good","Fair","Poor"]},
    {"id": 2, "element": "Vitality", "text": "During the past 4 weeks, how much did pain interfere with your normal work?", "options": ["Not at all","A little bit","Moderately","Quite a bit","Extremely"]},
    {"id": 3, "element": "Vitality", "text": "During the past 4 weeks, did you have a lot of energy?", "options": ["All of the time","Most of the time","Some of the time","A little of the time","None of the time"]},
    {"id": 4, "element": "Vitality", "text": "During the past 4 weeks, to what degree did you experience mental exhaustion?", "options": ["Not at all","A little bit","Somewhat","Quite a bit","Very much"]},
    {"id": 5, "element": "Vitality", "text": "During the past 4 weeks, how would you rate your sleep quality overall?", "options": ["Very good","Fairly good","Fairly bad","Very bad"]},
    {"id": 6, "element": "Vitality", "text": "How often do you feel unable to control important things in your life?", "options": ["Never","Almost never","Sometimes","Fairly often","Very often"]},
    {"id": 7, "element": "Vitality", "text": "I am able to adapt when changes occur.", "options": ["Not true at all","Rarely true","Sometimes true","Often true","True nearly all the time"]},
    {"id": 8, "element": "Vitality", "text": "I am often cheerful and in good spirits.", "options": ["At no time","Some of the time","Less than half the time","More than half the time","All of the time"]},
    {"id": 9, "element": "Vitality", "text": "I have felt calm and relaxed.", "options": ["At no time","Some of the time","Less than half the time","More than half the time","All of the time"]},
    {"id":10, "element": "Vitality", "text": "I have enough physical and mental energy to fully engage in work, family, friends, and hobbies.", "options": ["Never","Almost never","Sometimes","Fairly often","Very often"]},

    # Connection 11-20
    {"id":11, "element":"Connection","text":"How often do you feel that you lack companionship?","options":["Hardly ever","Some of the time","Often"]},
    {"id":12, "element":"Connection","text":"How often do you feel left out among family, friends, or at work?","options":["Hardly ever","Some of the time","Often"]},
    {"id":13, "element":"Connection","text":"I fear losing my partner’s love or approval.","options":["Strongly disagree","Disagree","Slightly disagree","Neutral","Slightly agree","Agree","Strongly agree"]},
    {"id":14, "element":"Connection","text":"I prefer not to show my partner how I truly feel deep down.","options":["Strongly disagree","Disagree","Slightly disagree","Neutral","Slightly agree","Agree","Strongly agree"]},
    {"id":15, "element":"Connection","text":"I can count on my friends or family when things go wrong.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":16, "element":"Connection","text":"When I feel lonely, there are people I can talk to.","options":["Definitely false","Probably false","Probably true","Definitely true"]},
    {"id":17, "element":"Connection","text":"I have healthy relationships with neighbors and colleagues.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":18, "element":"Connection","text":"Social media negatively impacts my mental health.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":19, "element":"Connection","text":"I am in control of my screen time.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":20, "element":"Connection","text":"My digital habits support my productivity and well-being.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Environment 21-30
    {"id":21, "element":"Environment","text":"How safe do you feel in your neighborhood?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":22, "element":"Environment","text":"How clean and well-maintained is your neighborhood?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":23, "element":"Environment","text":"I have easy access to a park, garden, or green space in my neighborhood.","options":["Strongly disagree","Disagree","Agree","Strongly agree"]},
    {"id":24, "element":"Environment","text":"How clean and well-maintained is your home?","options":["Very poor","Poor","Fair","Good","Very good"]},
    {"id":25, "element":"Environment","text":"I have enough private space in my home.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":26, "element":"Environment","text":"I feel safe and comfortable in my home.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":27, "element":"Environment","text":"How often does clutter or disorganization affect your daily life?","options":["Never","Rarely","Sometimes","Often","Always"]},
    {"id":28, "element":"Environment","text":"How would you rate your workplace’s overall comfort and functionality?","options":["Poor","Fair","Good","Very good","Excellent"]},
    {"id":29, "element":"Environment","text":"My commute from home to work or the city is generally comfortable.","options":["Strongly disagree","Disagree","Agree","Strongly agree"]},
    {"id":30, "element":"Environment","text":"My home, workspace, and neighborhood positively impact my well-being.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Growth 31-40
    {"id":31, "element":"Growth","text":"I have found a meaningful career.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":32, "element":"Growth","text":"My current work aligns with my long-term career goals.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":33, "element":"Growth","text":"I actively seek opportunities for career growth in my current role.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":34, "element":"Growth","text":"I actively seek opportunities to learn new skills.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":35, "element":"Growth","text":"I am open to switching jobs for better pay and designation.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":36, "element":"Growth","text":"Setbacks do not discourage me for long.","options":["Not like me at all","Not much like me","Somewhat like me","Mostly like me","Very much like me"]},
    {"id":37, "element":"Growth","text":"I can always find a way to solve problems and get things done.","options":["Not at all true","Hardly true","Moderately true","Exactly true"]},
    {"id":38, "element":"Growth","text":"I am confident I could handle unexpected events like job loss.","options":["Not at all true","Hardly true","Moderately true","Exactly true"]},
    {"id":39, "element":"Growth","text":"Challenges motivate me to grow.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":40, "element":"Growth","text":"How strong is your ability to prepare for the future?","options":["Not strong","Slightly strong","Moderately strong","Very strong","Strongest"]},

    # Meaning 51-60
    {"id":51, "element":"Meaning","text":"I am engaged and interested in my daily activities.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":52, "element":"Meaning","text":"In life, I have clear goals and aims.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":53, "element":"Meaning","text":"My relationships feel genuine and meaningful.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":54, "element":"Meaning","text":"I feel genuinely interested in the lives of people around me.","options":["Very slightly or not at all","A little","Moderately","Quite a bit","Extremely"]},
    {"id":55, "element":"Meaning","text":"I personally know people who earnestly try to make a positive difference in the world.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":56, "element":"Meaning","text":"I contribute to society through acts of service, donations, or help.","options":["Very slightly or not at all","A little","Moderately","Quite a bit","Extremely"]},
    {"id":57, "element":"Meaning","text":"I find it easy to forgive and let go of grudges.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":58, "element":"Meaning","text":"My life has a clear sense of purpose.","options":["Absolutely untrue","Mostly untrue","Somewhat untrue","Can't say","Somewhat true","Mostly true","Absolutely true"]},
    {"id":59, "element":"Meaning","text":"I actively try to lead a purposeful and meaningful life.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},
    {"id":60, "element":"Meaning","text":"I am optimistic about my future.","options":["Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]},

    # Recursion 61-70
    {"id":61,"element":"Recursion","text":"Before age 18: Did a parent or adult often swear at, insult, or humiliate you?","options":["Yes","No"]},
    {"id":62,"element":"Recursion","text":"Before age 18: Did you often feel no one in your family understood you?","options":["Yes","No"]},
    {"id":63,"element":"Recursion","text":"Before age 18: Did you live with a substance abuser or alcoholic adult?","options":["Yes","No"]},
    {"id":64,"element":"Recursion","text":"Before age 18: Did you live with a household member who was depressed or mentally ill?","options":["Yes","No"]},
    {"id":65,"element":"Recursion","text":"Before age 18: Were your parents separated or divorced?","options":["Yes","No"]},
    {"id":66,"element":"Recursion","text":"Before age 18: Did you witness your mother or father being pushed, grabbed, or slapped?","options":["Yes","No"]},
    {"id":67,"element":"Recursion","text":"Before age 18: Did an adult ever touch or fondle you sexually, or make you touch them?","options":["Yes","No"]},
    {"id":68,"element":"Recursion","text":"Before age 18: I felt emotionally neglected by my family.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":69,"element":"Recursion","text":"Before age 18: I was physically hit so hard it left marks or bruises.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]},
    {"id":70,"element":"Recursion","text":"Before age 18: My household struggled financially and we often had difficulty making ends meet.","options":["Never true","Rarely true","Sometimes true","Often true","Very often true"]}
]

element_groups = {
    "Vitality": questions[0:10],
    "Connection": questions[10:20],
    "Environment": questions[20:30],
    "Growth": questions[30:40],
    "Meaning": questions[50:60],
    "Recursion": questions[60:70]
}

recursions_defs = {
    "abandonment_fear": {"title": "Abandonment Fear", "desc": "A recurring pattern of fearing loss or rejection, often leading to isolation or clinginess in relationships."},
    "emotional_neglect_echo": {"title": "Emotional Neglect Echo", "desc": "Lingering feelings of emptiness or unworthiness from not having emotional needs met in childhood."},
    "trust_deficit": {"title": "Trust Deficit", "desc": "Difficulty trusting others due to early experiences of betrayal, inconsistency, or harm."},
    "self_worth_wound": {"title": "Self-Worth Wound", "desc": "Persistent feelings of being unworthy or inadequate, rooted in early humiliation or neglect."},
    "chaos_adaptation": {"title": "Chaos Adaptation", "desc": "Unconscious attraction to instability or drama, as it feels familiar from a chaotic childhood."}
}

def calculate_element_scores(responses):
    scores = {}
    for el, qs in element_groups.items():
        if el == "Recursion": continue
        total = count = 0
        for q in qs:
            val = responses.get(str(q["id"]))
            if not val or not q["options"]: continue
            idx = q["options"].index(val)
            # Reverse scoring for negatively worded items
            negative = any(word in q["text"].lower() for word in ["pain","exhaustion","unable","lack","left out","negatively","clutter","trouble"])
            score = (len(q["options"]) - 1 - idx) if negative else idx
            total += score + 1
            count += 1
        max_possible = count * len(q["options"]) if count else 1
        scores[el] = round((total / max_possible) * 100)
    return scores

def detect_recursions(responses, element_scores):
    ace = sum(1 for i in range(61,68) if responses.get(str(i)) == "Yes")
    emo = responses.get("68", "Rarely true")
    phys = responses.get("69", "Rarely true")
    fin = responses.get("70", "Rarely true")
    emo_score = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(emo) + 1
    phys_score = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(phys) + 1
    fin_score = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(fin) + 1

    candidates = []
    weak = [e for e, s in element_scores.items() if s < 65]

    for key, r in recursions_defs.items():
        strength = 0
        affected = []
        if key == "abandonment_fear":
            strength = 40 + ace*9
            if "Connection" in weak: strength += 25; affected.append("Connection")
            if "Meaning" in weak: strength += 15; affected.append("Meaning")
        elif key == "emotional_neglect_echo":
            strength = 40 + emo_score*12
            if "Meaning" in weak: strength += 30; affected.append("Meaning")
            if "Connection" in weak: strength += 20; affected.append("Connection")
        elif key == "trust_deficit":
            strength = 40 + ace*10
            if "Connection" in weak: strength += 30; affected.append("Connection")
        elif key == "self_worth_wound":
            strength = 40 + emo_score*10 + phys_score*10
            if "Growth" in weak: strength += 25; affected.append("Growth")
            if "Vitality" in weak: strength += 20; affected.append("Vitality")
        elif key == "chaos_adaptation":
            strength = 40 + fin_score*12 + ace*6
            if "Environment" in weak: strength += 25; affected.append("Environment")

        strength = min(100, strength)
        if strength > 50:
            candidates.append({
                "title": r["title"],
                "description": r["desc"],
                "strength": strength,
                "affected_elements": affected or weak[:2]
            })

    return sorted(candidates, key=lambda x: x["strength"], reverse=True)[:3] or [{
        "title": "No major recursion detected",
        "description": "Your biome is balanced and expanding.",
        "strength": 0,
        "affected_elements": []
    }]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.get_json() or {}
    scores = calculate_element_scores(data)
    recursions = detect_recursions(data, scores)
    avg_recursion = sum(r["strength"] for r in recursions) / len(recursions)
    return jsonify({"scores": scores, "recursions": recursions, "avg_recursion": avg_recursion})

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Latent Recursion System</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
  <style>.tree,.ring{{transition:all 1.5s ease}}</style>
</head>
<body class="bg-gradient-to-br from-slate-950 to-slate-900 text-white min-h-screen">
  <div class="container mx-auto p-6 max-w-5xl">
    <h1 class="text-5xl font-bold text-center text-teal-400 mt-8 mb-2">Latent Recursion System</h1>
    <p class="text-center text-gray-300 mb-12 text-xl">
      Discover hidden patterns from your past that keep you stuck today. Like an MRI scan for your life, it shows how these patterns affect your personal biome — the six key areas of your life — and provides a plan to break free and live fully.
    </p>
    <div class="text-center mb-12">
      <div class="w-full bg-gray-800 rounded-full h-3"><div id="progress" class="bg-teal-500 h-3 rounded-full transition-all duration-1000" style="width:0%"></div></div>
      <p class="mt-4 text-gray-400" id="progress-text">Vitality – 0/70</p>
    </div>
    <div id="assessment" class="space-y-12"></div>

    <div id="biome-container" class="my-16 text-center hidden">
      <h2 class="text-3xl font-bold mb-8">Your Personal Biome</h2>
      <canvas id="biome" width="600" height="600" class="mx-auto border-4 border-teal-600 rounded-2xl shadow-2xl"></canvas>
      <p class="mt-4 text-gray-400">Central orb = You · Trees = Six life elements · Ring = Latent recursion (tight/red = active, loose/green = resolved)</p>
    </div>

    <div id="results" class="hidden mt-12 p-8 bg-slate-800 rounded-2xl shadow-2xl space-y-8"></div>
  </div>

  <script>
    const elements = ['Vitality','Connection','Environment','Growth','Meaning','Recursion'];
    const questions = {json.dumps(questions)};
    const elementGroups = {json.dumps({k: [q["id"] for q in v] for k,v in element_groups.items()})};
    let responses = {{}};
    let current = 0;

    let scene, camera, renderer, trees=[], ring, userFigure;
    function initBiome() {{
      const c = document.getElementById('biome');
      scene = new THREE.Scene(); scene.background = new THREE.Color(0x0f172a);
      camera = new THREE.PerspectiveCamera(60,1,0.1,1000);
      renderer = new THREE.WebGLRenderer({{canvas:c, antialias:true}}); renderer.setSize(600,600);
      const geo = new THREE.DodecahedronGeometry(0.5,0);
      const mat = new THREE.MeshBasicMaterial({{color:0x00ffaa, wireframe:true}});
      userFigure = new THREE.Mesh(geo,mat); userFigure.position.y=0.5; scene.add(userFigure);
      const rg = new THREE.TorusGeometry(4,0.15,16,100);
      const rm = new THREE.MeshBasicMaterial({{color:0xff0066}});
      ring = new THREE.Mesh(rg,rm); ring.rotation.x=Math.PI/2; scene.add(ring);
      camera.position.z=10; animate();
    }}
    function animate(){{requestAnimationFrame(animate); ring.rotation.z+=0.01; userFigure.rotation.y+=0.01; renderer.render(scene,camera);}}
    function updateBiome(scores, rec){{
      trees.forEach(t=>scene.remove(t)); trees=[];
      const cfg = [
        {{el:'Vitality',x:-3.5,c:0x00ff88,t:"Vitality Tree"}},
        {{el:'Connection',x:-1.8,c:0x4488ff,t:"Connection Tree"}},
        {{el:'Environment',x:0,c:0xffaa00,t:"Environment Tree"}},
        {{el:'Growth',x:1.8,c:0xff00ff,t:"Growth Tree"}},
        {{el:'Meaning',x:3.5,c:0xff0088,t:"Meaning Tree"}}
      ];
      cfg.forEach(o=>{{ const h=(scores[o.el]||50)/100*4+0.5;
        const tree = new THREE.Mesh(new THREE.CylinderGeometry(0.4,0.6,h,8), new THREE.MeshBasicMaterial({{color:o.c}}));
        tree.position.set(o.x,h/2,0); scene.add(tree); trees.push(tree);
        const canvas=document.createElement('canvas'); const ctx=canvas.getContext('2d');
        canvas.width=256; canvas.height=64; ctx.fillStyle='#fff'; ctx.font='bold 24px Arial'; ctx.fillText(o.t,10,40);
        const sprite=new THREE.Sprite(new THREE.SpriteMaterial({{map:new THREE.CanvasTexture(canvas)}}));
        sprite.position.set(o.x,h+1,0); sprite.scale.set(3,0.75,1); scene.add(sprite);
      }});
      const con=rec/100; ring.scale.set(1+con,1+con,1);
      ring.material.color.setHex(con>0.5?0xff0000:0x00ff66);
    }}

    function loadElement() {{
      const el = elements[current];
      const ids = elementGroups[el];
      const container = document.getElementById('assessment');
      container.innerHTML = `<h2 class="text-3xl font-bold text-teal-400 mb-8">${{el}}</h2>`;
      questions.filter(q=>ids.includes(q.id)).forEach(q=>{{
        const div=document.createElement('div'); div.className='bg-slate-800 p-5 rounded-xl mb-4';
        div.innerHTML=`<p class="font-medium mb-3">${{q.id}}. ${{q.text}}</p><div class="grid grid-cols-1 md:grid-cols-5 gap-3"></div>`;
        const opts=div.querySelector('div');
        q.options.forEach(opt=>{{
          const label=document.createElement('label');
          label.className='flex items-center p-3 bg-slate-700 rounded hover:bg-teal-600 cursor-pointer transition';
          label.innerHTML=`<input type="radio" name="q${{q.id}}" value="${{opt}}" class="mr-3"><span>${{opt}}</span>`;
          opts.appendChild(label);
        }});
        container.appendChild(div);
      }});
      const btn=document.createElement('button');
      btn.textContent = current<5 ? 'Next Element →' : 'See My Results';
      btn.className='w-full p-5 bg-teal-600 hover:bg-teal-500 rounded-xl font-bold text-xl mt-8';
      btn.onclick=()=>{{
        ids.forEach(id=>{{
          const sel=document.querySelector(`input[name="q${{id}}"]:checked`);
          if(sel) responses[id]=sel.value;
        }});
        current++;
        if(current<6) loadElement();
        else submit();
      }};
      container.appendChild(btn);
      document.getElementById('progress-text').textContent = `${{el}} – ${{Object.keys(responses).length}}/70`;
      document.getElementById('progress').style.width = `${{(Object.keys(responses).length/70*100).toFixed(0)}}%`;
    }}

    function submit() {{
      fetch('/assess',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(responses)}})
      .then(r=>r.json()).then(data=>{{
        document.getElementById('assessment').classList.add('hidden');
        document.getElementById('biome-container').classList.remove('hidden');
        updateBiome(data.scores, data.avg_recursion);
        let html=`<h2 class="text-4xl font-bold text-center text-teal-400 mb-8">Your Latent Recursions</h2>`;
        if(data.recursions[0].strength===0){{
          html+=`<p class="text-2xl text-center text-green-400">No major recursion detected. Your biome is free to expand.</p>`;
        }}else{{
          data.recursions.forEach((r,i)=>{{
            html+=`<div class="p-6 bg-red-950/50 rounded-xl border border-red-600">
              <p class="text-2xl font-bold">${{i+1}}. ${{r.title}}</p>
              <p class="text-4xl font-bold text-red-400 mb-4">${{r.strength}}%</p>
              <p class="text-lg">${{r.description}}</p>
              ${{(r.affected_elements.length?`<p class="text-sm text-gray-400 mt-4">Pulling on: ${{r.affected_elements.join(' · ')}}</p>`:'')}}</div>`;
          }});
        }}
        html+=`<h2 class="text-4xl font-bold text-center text-teal-400 my-8">Your 30-Day Transformation Plan</h2>
        <div class="grid md:grid-cols-2 gap-6 text-left">
          <div class="p-5 bg-slate-800 rounded-xl"><p class="font-bold text-teal-400">Week 1 – Acknowledgement</p><p>Daily: Write one example of your pattern showing up.</p></div>
          <div class="p-5 bg-slate-800 rounded-xl"><p class="font-bold text-teal-400">Week 2 – Deep Analysis</p><p>Map the childhood root + your current role in keeping it alive.</p></div>
          <div class="p-5 bg-slate-800 rounded-xl"><p class="font-bold text-teal-400">Week 3 – Radical Acceptance</p><p>Practice “It was not my fault, but it is my responsibility now.”</p></div>
          <div class="p-5 bg-slate-800 rounded-xl"><p class="font-bold text-teal-400">Week 4 – New Pathways</p><p>Take one new action daily that contradicts the old pattern.</p></div>
        </div>`;
        document.getElementById('results').innerHTML=html;
        document.getElementById('results').classList.remove('hidden');
      }});
    }}

    initBiome();
    loadElement();
  </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
