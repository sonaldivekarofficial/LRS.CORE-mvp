from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

# === ALL 70 QUESTIONS (complete, no typos) ===
questions = [
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

    # Stability 41–50 (hidden but scored)
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

    # Meaning 51–60
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

    # Recursion 61–76
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

element_groups = {
    "Vitality": questions[0:10],
    "Connection": questions[10:20],
    "Environment": questions[20:30],
    "Growth": questions[30:40],
    "Stability": questions[40:50],
    "Meaning": questions[50:60],
    "Recursion": questions[60:70]
}

recursions_defs = {
    "abandonment_fear":{"title":"Abandonment Fear","desc":"Fear of being left or rejected, recurring from early instability."},
    "emotional_neglect_echo":{"title":"Emotional Neglect Echo","desc":"Persistent emptiness from unmet emotional needs in childhood."},
    "trust_deficit":{"title":"Trust Deficit","desc":"Difficulty trusting others due to early betrayal or inconsistency."},
    "self_worth_wound":{"title":"Self-Worth Wound","desc":"Deep feeling of unworthiness from early humiliation or criticism."},
    "chaos_adaptation":{"title":"Chaos Adaptation","desc":"Attraction to unstable situations as they feel familiar."},
    "perfectionism_trap":{"title":"Perfectionism Trap","desc":"Relentless drive for flawlessness causing burnout."},
    "failure_aversion":{"title":"Failure Aversion","desc":"Extreme fear of failing, limiting risk-taking."},
    "identity_confusion":{"title":"Identity Confusion","desc":"Struggle with self-identity from early invalidation."},
    "emotional_suppression":{"title":"Emotional Suppression","desc":"Habit of suppressing emotions from dismissive early environments."},
    "financial_anxiety_loop":{"title":"Financial Anxiety Loop","desc":"Ongoing fear of poverty from childhood financial struggle."}
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
            negative = any(k in q["text"].lower() for k in ["pain","exhaustion","unable","lack","left out","negatively","clutter","poor","never","trouble","worry","anxious","stressed","interfere"])
            val_num = len(q["options"])-1 - idx if negative else idx
            total += val_num
            count += 1
        if count == 0:
            scores[el] = 50
        else:
            scores[el] = round((total / (count * (len(q["options"])-1))) * 100)
    return scores

def detect_recursions(responses, element_scores):
    ace = sum(1 for i in range(61,68) if responses.get(str(i)) == "Yes")
    emo = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("71","Rarely true"))
    phys = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("72","Rarely true"))
    fin = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("76","Rarely true"))
    v,c,e,g,s,m = (element_scores.get(k,50) for k in ["Vitality","Connection","Environment","Growth","Stability","Meaning"])
    cand = []
    for k,r in recursions_defs.items():
        score = 0
        if k=="abandonment_fear": score = 40 + ace*8 + emo*5 + (100-c)*0.8 + (100-m)*0.6
        elif k=="emotional_neglect_echo": score = 40 + emo*14 + (100-m)*0.9 + (100-c)*0.5
        elif k=="trust_deficit": score = 40 + ace*12 + (100-c)*0.9
        elif k=="self_worth_wound": score = 40 + emo*10 + phys*10 + (100-g)*0.8
        elif k=="chaos_adaptation": score = 40 + fin*10 + ace*8 + (100-s)*0.9
        elif k=="perfectionism_trap": score = 40 + emo*12 + (100-g)*0.9
        elif k=="failure_aversion": score = 40 + phys*12 + (100-g)*0.9
        elif k=="identity_confusion": score = 40 + emo*12 + (100-m)*0.9
        elif k=="emotional_suppression": score = 40 + emo*14 + (100-v)*0.8
        elif k=="financial_anxiety_loop": score = 40 + fin*16 + (100-s)*0.9
        score = min(100, int(score))
        if score > 45:
            cand.append({"title":r["title"],"description":r["desc"],"strength":score,"affected_elements":[x for x,y in element_scores.items() if y<65]})
    return sorted(cand, key=lambda x: x["strength"], reverse=True)[:3] or [{"title":"No major recursion detected","description":"Your biome is balanced and expanding.","strength":0,"affected_elements":[]}]

@app.route('/')
def index():
    return render_template_string_string(HTML_TEMPLATE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.get_json()
    scores = calculate_element_scores(data)
    recursions = detect_recursions(data, scores)
    avg = sum(r["strength"] for r in recursions)/max(1,len(recursions))
    return jsonify({"scores":scores, "recursions":recursions, "avg_recursion":avg})

HTML_TEMPLATE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><title>Latent Recursion System</title>
<script src="https://cdn.tailwindcss.com"></script><script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
<style>.tree{transition:all 1.5s ease}</style></head><body class="bg-gradient-to-br from-slate-950 to-slate-900 text-white min-h-screen">
<div class="container mx-auto p-6 max-w-5xl"><h1 class="text-5xl font-bold text-center text-teal-400 mt-8 mb-2">Latent Recursion System</h1>
<p class="text-center text-gray-300 mb-12 text-xl">Discover hidden patterns from your past that keep you stuck today.</p>
<div class="text-center mb-12"><div class="w-full bg-gray-800 rounded-full h-3"><div id="progress" class="bg-teal-500 h-3 rounded-full transition-all duration-1000" style="width:0%"></div></div>
<p class="mt-4 text-gray-400" id="progress-text">0/70</p></div><div id="assessment" class="space-y-12"></div>
<div id="biome-container" class="my-16 text-center hidden"><h2 class="text-3xl font-bold mb-8">Your Personal Biome</h2>
<canvas id="biome" width="600" height="600" class="mx-auto border-4 border-teal-600 rounded-2xl shadow-2xl"></canvas></div>
<div id="results" class="hidden mt-12 p-8 bg-slate-800 rounded-2xl shadow-2xl space-y-8"></div></div>
<script>
const elements = ['Vitality','Connection','Environment','Growth','Stability','Meaning','Recursion'];
const questions = """ + json.dumps(questions) + """;
let responses = {}, current = 0;
let scene, camera, renderer, trees=[], ring;
function initBiome(){const c=document.getElementById('biome');scene=new THREE.Scene();scene.background=new THREE.Color(0x0f172a);
camera=new THREE.PerspectiveCamera(60,1,0.1,1000);renderer=new THREE.WebGLRenderer({canvas:c,antialias:true});renderer.setSize(600,600);
const geo=new THREE.DodecahedronGeometry(0.5,0);const mat=new THREE.MeshBasicMaterial({color:0x00ffaa,wireframe:true});
const user=new THREE.Mesh(geo,mat);user.position.y=0.5;scene.add(user);
const ringGeo=new THREE.TorusGeometry(4,0.15,16,100);const ringMat=new THREE.MeshBasicMaterial({color:0xff0066});
ring=new THREE.Mesh(ringGeo,ringMat);ring.rotation.x=Math.PI/2;scene.add(ring);camera.position.z=10;animate();}
function animate(){requestAnimationFrame(animate);ring.rotation.z+=0.01;renderer.render(scene,camera);}
function updateBiome(s,r){trees.forEach(t=>scene.remove(t));trees=[];
const cfg=[{el:'Vitality',x:-3.5,c:0x00ff88},{el:'Connection',x:-1.8,c:0x4488ff},{el:'Environment',x:0,c:0xffaa00},
{el:'Growth',x:1.8,c:0xff00ff},{el:'Stability',x:3.5,c:0xffff00},{el:'Meaning',x:3.5,c:0xff0088}];
cfg.forEach(o=>{const h=(s[o.o el]||50)/100*4+0.5;const geo=new THREE.CylinderGeometry(0.4,0.6,h,8);
const mat=new THREE.MeshBasicMaterial({color:o.c});const tree=new THREE.Mesh(geo,mat);
tree.position.set(o.x,h/2,0);scene.add(tree);trees.push(tree);});
const con=r/100;ring.scale.set(1+con,1+con,1);ring.material.color.setHex(con>0.5?0xff0000:0x00ff66);}
function load(){const el=elements[current];const qs=element_groups[el]||[];
document.getElementById('assessment').innerHTML=`<h2 class="text-3xl font-bold text-teal-400 mb-8">${el}</h2>`;
qs.forEach(q=>{const d=document.createElement('div');d.className='bg-slate-800 p-5 rounded-xl mb-4';
d.innerHTML=`<p class="font-medium mb-3">${q.id}. ${q.text}</p><div class="grid grid-cols-1 md:grid-cols-5 gap-3" id="opts${q.id}"></div>`;
const opts=document.getElementById(`opts${q.id}`);
q.options.forEach(o=>{const l=document.createElement('label');l.className='flex items-center p-3 bg-slate-700 rounded hover:bg-teal-600 cursor-pointer';
l.innerHTML=`<input type="radio" name="q${q.id}" value="${o}" class="mr-3"><span>${o}</span>`;opts.appendChild(l);});
document.getElementById('assessment').appendChild(d);});
const btn=document.createElement('button');btn.textContent=current<6?'Next →':'See Results';
btn.className='w-full p-5 bg-teal-600 hover:bg-teal-500 rounded-xl font-bold text-xl mt-8';
btn.onclick=()=>{qs.forEach(q=>{const sel=document.querySelector(`input[name="q${q.id}"]:checked`);if(sel)responses[q.id]=sel.value;});
current++;if(current<7)load();else submit();};document.getElementById('assessment').appendChild(btn);
document.getElementById('progress-text').innerText=`${el} – ${Object.keys(responses).length}/70`;}
function submit(){fetch('/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(responses)})
.then(r=>r.json()).then(d=>{document.getElementById('assessment').classList.add('hidden');
document.getElementById('biome-container').classList.remove('hidden');updateBiome(d.scores,d.avg_recursion);
let html=`<h2 class="text-4xl font-bold text-center text-teal-400 mb-8">Your Latent Recursions</h2>`;
if(d.recursions[0].strength===0)html+=`<p class="text-xl text-center text-green-400">No major recursion detected.</p>`;
else d.recursions.forEach((r,i)=>{html+=`<div class="p-6 bg-red-950/50 rounded-xl border border-red-600">
<p class="text-2xl font-bold">${i+1}. ${r.title}</p><p class="text-4xl font-bold text-red-400 mb-4">${r.strength}%</p>
<p class="text-lg">${r.description}</p></div>`;});
html+=`<h2 class="text-4xl font-bold text-center text-teal-400 mb-8">30-Day Plan</h2><div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="p-6 bg-slate-800 rounded-xl"><p class="font-bold text-xl">Week 1–2: Awareness & Mapping</p><p>Journal daily triggers and origins.</p></div>
<div class="p-6 bg-slate-800 rounded-xl"><p class="font-bold text-xl">Week 3–4: Replace & Track</p><p>New habits + weekly review.</p></div></div>`;
document.getElementById('results').innerHTML=html;document.getElementById('results').classList.remove('hidden');});}
initBiome();load();
</script></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
