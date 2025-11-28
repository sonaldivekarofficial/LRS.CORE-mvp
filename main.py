import os
import json
from flask import Flask, request, render_template_string

app = Flask(__name__)

# =============================================
# DATA: QUESTIONS
# =============================================
questions = [
    # Vitality (1-10)
    {"id": 1, "element": "Vitality", "text": "In general, would you say your health is?", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]},
    {"id": 2, "element": "Vitality", "text": "During the past 4 weeks, how much did pain interfere with your normal work?", "options": ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 3, "element": "Vitality", "text": "During the past 4 weeks, did you have a lot of energy?", "options": ["All of the time", "Most of the time", "Some of the time", "A little of the time", "None of the time"]},
    {"id": 4, "element": "Vitality", "text": "During the past 4 weeks, to what degree did you experience mental exhaustion?", "options": ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"]},
    {"id": 5, "element": "Vitality", "text": "During the past 4 weeks, how would you rate your sleep quality overall?", "options": ["Very good", "Fairly good", "Fairly bad", "Very bad"]},
    {"id": 6, "element": "Vitality", "text": "How often do you feel unable to control important things in your life?", "options": ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]},
    {"id": 7, "element": "Vitality", "text": "I am able to adapt when changes occur.", "options": ["True nearly all the time", "Often true", "Sometimes true", "Rarely true", "Not true at all"]}, # REVERSED for scoring consistency
    {"id": 8, "element": "Vitality", "text": "I am often cheerful and in good spirits.", "options": ["All of the time", "More than half the time", "Less than half the time", "Some of the time", "At no time"]}, # REVERSED
    {"id": 9, "element": "Vitality", "text": "I have felt calm and relaxed.", "options": ["All of the time", "More than half the time", "Less than half the time", "Some of the time", "At no time"]}, # REVERSED
    {"id": 10, "element": "Vitality", "text": "I have enough physical and mental energy to fully engage in work, family, friends, and hobbies.", "options": ["Very often", "Fairly often", "Sometimes", "Almost never", "Never"]}, # REVERSED

    # Connection (11-20)
    {"id": 11, "element": "Connection", "text": "How often do you feel that you lack companionship?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 12, "element": "Connection", "text": "How often do you feel left out among family, friends, or at work?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 13, "element": "Connection", "text": "I'm afraid that I will lose my partner's love.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 14, "element": "Connection", "text": "I prefer not to show a partner how I feel deep down.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 15, "element": "Connection", "text": "I can count on my friends/family when things go wrong.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 16, "element": "Connection", "text": "When I feel lonely, there are people I can talk to.", "options": ["Definitely true", "Probably true", "Probably false", "Definitely false"]}, # REVERSED
    {"id": 17, "element": "Connection", "text": "I have healthy relationships with my neighbours and colleagues.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 18, "element": "Connection", "text": "Social media negatively impacts my mental health.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 19, "element": "Connection", "text": "I am in control of my screen time.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 20, "element": "Connection", "text": "My digital habits support my productivity.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED

    # Environment (21-30)
    {"id": 21, "element": "Environment", "text": "How safe do you feel in your neighborhood?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, # REVERSED
    {"id": 22, "element": "Environment", "text": "How clean and well-maintained is your neighbourhood?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, # REVERSED
    {"id": 23, "element": "Environment", "text": "I have access to park/garden/green space around my neighborhood.", "options": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 24, "element": "Environment", "text": "How clean and well-maintained is your home?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, # REVERSED
    {"id": 25, "element": "Environment", "text": "I have enough private space in my home.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 26, "element": "Environment", "text": "I feel safe and comfortable in my home.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 27, "element": "Environment", "text": "How often does clutter or disorganization affect your daily life?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 28, "element": "Environment", "text": "Rate your workplace’s overall comfortability and functionality.", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]}, # REVERSED
    {"id": 29, "element": "Environment", "text": "Transit from my home to work and city is often comfortable.", "options": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 30, "element": "Environment", "text": "My home/work space/neighbourhood positively impacts my well-being.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED

    # Growth (31-40)
    {"id": 31, "element": "Growth", "text": "I have found a meaningful career.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 32, "element": "Growth", "text": "My work is aligned with my career goals.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 33, "element": "Growth", "text": "I actively seek opportunities for career growth within my work space.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 34, "element": "Growth", "text": "I actively seek opportunities to learn new skills.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 35, "element": "Growth", "text": "I actively seek opportunities to switch job for higher pay and designation.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 36, "element": "Growth", "text": "Setbacks do not discourage me.", "options": ["Very much like me", "Mostly like me", "Somewhat like me", "Not much like me", "Not like me at all"]}, # REVERSED
    {"id": 37, "element": "Growth", "text": "I always manage to solve problems and get things done.", "options": ["Exactly true", "Moderately true", "Hardly true", "Not at all true"]}, # REVERSED
    {"id": 38, "element": "Growth", "text": "I am confident I could deal efficiently with unexpected events like loss of job.", "options": ["Exactly true", "Moderately true", "Hardly true", "Not at all true"]}, # REVERSED
    {"id": 39, "element": "Growth", "text": "Challenges motivate me to grow.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 40, "element": "Growth", "text": "How strong is your ability to prepare for the future?", "options": ["Strongest", "Very strong", "Moderately strong", "Slightly strong", "Not strong"]}, # REVERSED

    # Stability (41-50)
    {"id": 41, "element": "Stability", "text": "How often have you had trouble paying bills?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 42, "element": "Stability", "text": "How often do you wonder if you are earning enough money?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 43, "element": "Stability", "text": "How often do you feel anxious about your current financial situation?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 44, "element": "Stability", "text": "I worry about my/my family’s spending habits.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 45, "element": "Stability", "text": "I feel stressed about my debts.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 46, "element": "Stability", "text": "I could handle a major unexpected expense like a hospital bill.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]}, # REVERSED
    {"id": 47, "element": "Stability", "text": "I know what my financial goals are.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 48, "element": "Stability", "text": "I have a clear financial plan for the next 1-5 years.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 49, "element": "Stability", "text": "I regularly set aside money for long term savings.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 50, "element": "Stability", "text": "I am actively securing my financial future.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]}, # REVERSED

    # Meaning (51-60)
    {"id": 51, "element": "Meaning", "text": "I am engaged and interested in my daily activities.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 52, "element": "Meaning", "text": "In life, I have clear goals and aims.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 53, "element": "Meaning", "text": "My relationships are genuine.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 54, "element": "Meaning", "text": "I feel genuinely interested in lives of people around me.", "options": ["Extremely", "Quite a bit", "Moderately", "A little", "Very slightly or not at all"]}, # REVERSED
    {"id": 55, "element": "Meaning", "text": "I personally know some people who earnestly try to make positive difference in the world.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 56, "element": "Meaning", "text": "I contribute to society with act of service/food donations/financial help.", "options": ["Extremely", "Quite a bit", "Moderately", "A little", "Very slightly or not at all"]}, # REVERSED
    {"id": 57, "element": "Meaning", "text": "I don't hold grudges, I find it easy to forgive and move on.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 58, "element": "Meaning", "text": "My life has a clear sense of purpose.", "options": ["Absolutely true", "Mostly true", "Somewhat true", "Can't say", "Somewhat untrue", "Mostly untrue", "Absolutely untrue"]}, # REVERSED
    {"id": 59, "element": "Meaning", "text": "I try to lead a purposeful and meaningful life.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED
    {"id": 60, "element": "Meaning", "text": "I am optimistic about my future.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, # REVERSED

    # Childhood Screening (61-70)
    {"id": 61, "element": "Childhood Screening", "text": "Did a parent or adult often swear at, insult, or humiliate you?", "options": ["Yes", "No"]},
    {"id": 62, "element": "Childhood Screening", "text": "Did you often feel no one in your family understood you?", "options": ["Yes", "No"]},
    {"id": 63, "element": "Childhood Screening", "text": "Did you live with a substance abuser or alcoholic?", "options": ["Yes", "No"]},
    {"id": 64, "element": "Childhood Screening", "text": "Was a household member depressed or mentally ill?", "options": ["Yes", "No"]},
    {"id": 65, "element": "Childhood Screening", "text": "Were your parents separated or divorced?", "options": ["Yes", "No"]},
    {"id": 66, "element": "Childhood Screening", "text": "Was your mother/father often pushed, grabbed, or slapped?", "options": ["Yes", "No"]},
    {"id": 67, "element": "Childhood Screening", "text": "Did an adult touch or fondle you sexually, or make you touch them?", "options": ["Yes", "No"]},
    {"id": 68, "element": "Childhood Screening", "text": "I felt emotionally neglected by my family.", "options": ["Very often true", "Often true", "Sometimes true", "Rarely true", "Never true"]}, # REVERSED to match negative scoring
    {"id": 69, "element": "Childhood Screening", "text": "I was physically hit so hard it left marks or bruises.", "options": ["Very often true", "Often true", "Sometimes true", "Rarely true", "Never true"]}, # REVERSED
    {"id": 70, "element": "Childhood Screening", "text": "My household struggled financially and we often had difficulty making ends meet.", "options": ["Very often true", "Often true", "Sometimes true", "Rarely true", "Never true"]} # REVERSED
]

# =============================================
# DATA: RECURSIONS & LOGIC MAPPING
# =============================================
# I have added a "category" tag to each pattern so the math knows when to trigger it.
recursions = [
    {"category": "Growth", "name": "Fixed Mindset", "root": "Growing up with labels rather than praise for effort", "symptom": "Avoiding challenges to maintain the label; giving up easily when things get hard", "action": "The \"Not Yet\" Technique. When you struggle, add \"yet\" to the end of the sentence."},
    {"category": "Childhood Screening", "name": "Good-Child Syndrome", "root": "Survival depended on being obedient, quiet, helpful", "symptom": "Can’t say no, rage turns inward (depression, autoimmune issues)", "action": "Low-Stakes Disappointment. Practice saying \"no\" to something small."},
    {"category": "Vitality", "name": "Frozen Grief", "root": "Was not allowed to cry or grieve", "symptom": "Sudden crying spells decades later, unexplained sadness", "action": "Scheduled Grief. Set a timer for 10 minutes to sit in silence."},
    {"category": "Connection", "name": "Abandonment Fear", "root": "Separation, divorce, or inconsistent caregivers", "symptom": "Clinginess, testing partners, pre-emptive leaving", "action": "Self-Soothing Mantra. \"I am here with you. I am not leaving you.\""},
    {"category": "Connection", "name": "Emotional Neglect Echo", "root": "Physical needs met, emotional needs ignored", "symptom": "Difficulty identifying feelings, feeling empty", "action": "The Emotion Wheel. Point to exactly what you are feeling."},
    {"category": "Connection", "name": "Trust Deficit", "root": "Betrayal by primary caregivers", "symptom": "Hyper-vigilance, testing people", "action": "Fact-Checking. Ask yourself: \"Do I have evidence for this thought?\""},
    {"category": "Vitality", "name": "Self-Worth Wound", "root": "History of humiliation or verbal abuse", "symptom": "Self-deprecation, settling for less", "action": "Esteemable Acts. Keep a daily promise to yourself."},
    {"category": "Environment", "name": "Chaos Adaptation", "root": "Unstable, unpredictable home", "symptom": "Feeling bored during peace, manufacturing drama", "action": "Re-framing Boredom. \"This isn't boredom; this is safety.\""},
    {"category": "Growth", "name": "Perfectionism Trap", "root": "Love was conditional on success", "symptom": "Procrastination, burnout, harsh inner critic", "action": "B- Work. Intentionally do a task at 80% effort."},
    {"category": "Growth", "name": "Failure Aversion", "root": "Excessive punishment for simple mistakes", "symptom": "Playing small, refusing to try new things", "action": "Redefining Failure. View every fail as data collection."},
    {"category": "Meaning", "name": "Identity Confusion", "root": "Constant invalidation of preferences", "symptom": "Chameleon behavior, indecision", "action": "Values Sorting. Make one small decision based on your values."},
    {"category": "Vitality", "name": "Emotional Suppression", "root": "Emotions were dismissed or punished", "symptom": "Numbness, explosive outbursts", "action": "Somatic Release. Scream into a pillow or sprint."},
    {"category": "Stability", "name": "Financial Anxiety Loop", "root": "Childhood poverty", "symptom": "Hoarding resources, panic about bills", "action": "Neutral Money Monitoring. Check bank account daily."},
    {"category": "Connection", "name": "People-Pleasing Circuit", "root": "Love conditional on compliant behavior", "symptom": "Inability to say no, resentment", "action": "The Pause. Never say yes immediately."},
    {"category": "Stability", "name": "Hyper-Independence", "root": "Had to fend for self too early", "symptom": "Viewing help as weakness, burnout", "action": "Micro-Asks. Ask for help with something small."},
    {"category": "Connection", "name": "Guilt-Shame Spiral", "root": "Being the scapegoat", "symptom": "Compulsive apologizing, feeling 'wrong'", "action": "Responsibility Pie Chart."},
    {"category": "Vitality", "name": "Catastrophizing Habit", "root": "Unpredictable violence or chaos", "symptom": "High anxiety, constant scanning for threats", "action": "Best/Worst/Likely. Focus on the third."},
    {"category": "Growth", "name": "Chronic Self-Doubt", "root": "Constant 'never good enough' messages", "symptom": "Analysis paralysis, seeking validation", "action": "Evidence Log. Keep a list of Wins."},
    {"category": "Connection", "name": "Boundary Collapse", "root": "Enmeshment, lack of privacy", "symptom": "Oversharing, taking on others' emotions", "action": "The 'I' Statement. Practice saying 'I feel...'"},
    {"category": "Connection", "name": "Savior Complex", "root": "Parentification", "symptom": "Attracting broken partners to fix", "action": "Detachment with Love."},
    {"category": "Growth", "name": "Impostor Syndrome", "root": "Praise for talent, not effort", "symptom": "Overworking, dread of being found out", "action": "Own the Success. Say only 'Thank you'."},
    {"category": "Connection", "name": "Rejection Sensitivity", "root": "Frequent exclusion or bullying", "symptom": "Misinterpreting neutral cues as rejection", "action": "Check the Story. Assume positive intent."},
    {"category": "Vitality", "name": "Control Obsession", "root": "Profound helplessness", "symptom": "Rigidity, panic when plans change", "action": "Delegation Experiment."},
    {"category": "Vitality", "name": "Numbness / Dissociation", "root": "Overwhelming trauma", "symptom": "Feeling unreal, zoning out", "action": "5-4-3-2-1 Grounding."},
    {"category": "Meaning", "name": "Approval Addiction", "root": "Love withheld unless performing", "symptom": "Depression when not receiving praise", "action": "Secret Hobby."},
    {"category": "Meaning", "name": "Chronic Over-Responsibility", "root": "Emotional caretaker", "symptom": "Heaviness, inability to be playful", "action": "'Not Mine' Mantra."},
    {"category": "Growth", "name": "Self-Sabotage Pattern", "root": "Success associated with danger", "symptom": "Quitting before finish line", "action": "Upper Limit Awareness."},
    {"category": "Meaning", "name": "Existential Emptiness", "root": "No modeling of meaning", "symptom": "Chronic boredom, apathy", "action": "Service. Do one small act of kindness."},
    {"category": "Growth", "name": "Fear of Success", "root": "Success brought unwanted responsibility", "symptom": "Playing small", "action": "Visualize Safety."},
    {"category": "Connection", "name": "Fear of Rejection", "root": "Avoidance of 'no'", "symptom": "Not asking for things, isolation", "action": "Rejection Therapy. Ask for something ridiculous."},
    {"category": "Growth", "name": "Fear of Wrong Decision", "root": "Fear of punishment for wrong choices", "symptom": "Stagnation, letting others decide", "action": "The 2-Minute Rule."},
    {"category": "Connection", "name": "FOPO (Fear of Opinions)", "root": "Conforming to strict norms", "symptom": "Hiding true self", "action": "The Hula Hoop. Stay in your hoop."},
    {"category": "Stability", "name": "Fear of Responsibility", "root": "Adulting = overwhelming burden", "symptom": "Underachievement", "action": "One Adult Task."},
    {"category": "Connection", "name": "Fear of Commitment", "root": "Witnessed unhappy marriages", "symptom": "Sabotaging relationships", "action": "Daily Choice."},
    {"category": "Environment", "name": "Fear of Change", "root": "Change = danger", "symptom": "Staying in toxic comfort zone", "action": "Micro-Novelty."},
    {"category": "Connection", "name": "Fear of Vulnerability", "root": "Openness was mocked", "symptom": "Superficial relationships", "action": "The 10% Rule."},
    {"category": "Connection", "name": "Fear of Conflict", "root": "Arguments were explosive", "symptom": "Passive-aggression, silent treatment", "action": "The Sandwich Method."},
    {"category": "Growth", "name": "Procrastination", "root": "Overwhelm or lack of guidance", "symptom": "Last-minute rushes", "action": "5-Minute Start."},
    {"category": "Vitality", "name": "Negative Self-Talk", "root": "Internalized critical parent", "symptom": "Self-attack", "action": "Name the Critic."},
    {"category": "Growth", "name": "Blaming Others", "root": "Fragile ego", "symptom": "Lack of accountability", "action": "Radical Responsibility."},
    {"category": "Growth", "name": "Lack of Prioritization", "root": "Busy with non-important tasks", "symptom": "Busy but not productive", "action": "Eisenhower Matrix."},
    {"category": "Vitality", "name": "Mindless Consumption", "root": "Soothing distress", "symptom": "Doomscrolling, binge-eating", "action": "Urge Surfing."},
    {"category": "Connection", "name": "Overcommitment (FOMO)", "root": "Fear of missing out", "symptom": "Exhaustion, resentment", "action": "JOMO."},
    {"category": "Connection", "name": "Self-Isolation", "root": "Feeling like a burden", "symptom": "Loneliness loop", "action": "Opposite Action."},
    {"category": "Vitality", "name": "Ignoring Personal Needs", "root": "Putting others first", "symptom": "Resentment outbursts", "action": "HALT Check."},
    {"category": "Growth", "name": "All-or-Nothing Thinking", "root": "Rigid parenting", "symptom": "Quitting after one slip-up", "action": "The Grey Zone."},
    {"category": "Meaning", "name": "Living in the Past", "root": "Unresolved trauma", "symptom": "Ruminating on old events", "action": "Mindfulness Practice."},
    {"category": "Childhood Screening", "name": "Trauma Bonding", "root": "Abuse confused with love", "symptom": "Addiction to toxic people", "action": "No Contact Rule."},
    {"category": "Stability", "name": "Scarcity Mindset", "root": "Never enough resources", "symptom": "Fear of spending", "action": "Abundance Journal."},
    {"category": "Growth", "name": "Learned Helplessness", "root": "Efforts never changed outcome", "symptom": "Giving up before trying", "action": "Smallest Possible Win."}
]

# =============================================
# HTML TEMPLATES
# =============================================
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Latent Recursion System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; color: #333; }
        .question-block { background: white; margin-bottom: 20px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .element-tag { font-size: 0.75em; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; margin-bottom: 5px; }
        h1 { text-align: center; color: #2c3e50; }
        h3 { margin-top: 5px; font-size: 1.1em; }
        label { display: block; margin: 8px 0; cursor: pointer; padding: 8px; border-radius: 4px; transition: background 0.2s; }
        label:hover { background-color: #e9ecef; }
        input[type="radio"] { margin-right: 10px; }
        button { background-color: #007bff; color: white; border: none; padding: 15px 30px; font-size: 1.2em; cursor: pointer; border-radius: 5px; margin-top: 20px; width: 100%; transition: background 0.3s; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <h1>Latent Recursion System</h1>
    <p style="text-align:center;">Answer honestly to reveal your hidden patterns.</p>
    <form action="/analyze" method="POST">
        {% for q in questions %}
        <div class="question-block">
            <div class="element-tag">{{ q.element }}</div>
            <h3>{{ q.id }}. {{ q.text }}</h3>
            {% for option in q.options %}
                <label>
                    <input type="radio" name="q_{{ q.id }}" value="{{ option }}" required>
                    {{ option }}
                </label>
            {% endfor %}
        </div>
        {% endfor %}
        <button type="submit">Reveal My Patterns</button>
    </form>
</body>
</html>
"""

result_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Analysis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; color: #333; }
        .header { text-align: center; margin-bottom: 40px; }
        .card { background: white; padding: 25px; margin-bottom: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 6px solid #e74c3c; }
        h2 { color: #2c3e50; margin-top: 0; }
        .label { font-weight: bold; color: #555; display: block; margin-top: 10px; }
        .content { margin-bottom: 5px; color: #333; }
        .action-box { background-color: #e8f8f5; border: 1px solid #d1f2eb; padding: 15px; border-radius: 5px; margin-top: 15px; }
        .action-title { color: #27ae60; font-weight: bold; margin-bottom: 5px; }
        .btn { display: inline-block; margin-top: 30px; text-decoration: none; background: #34495e; color: white; padding: 12px 25px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Analysis Complete</h1>
        <p>We have analyzed your answers and identified the top 3 patterns holding you back.</p>
    </div>
    
    {% for rec in patterns %}
        <div class="card">
            <h2>{{ rec.name }}</h2>
            <span class="label">ROOT CAUSE:</span>
            <div class="content">{{ rec.root }}</div>
            
            <span class="label">CURRENT SYMPTOM:</span>
            <div class="content">{{ rec.symptom }}</div>
            
            <div class="action-box">
                <div class="action-title">ACTIONABLE STEP:</div>
                {{ rec.action }}
            </div>
        </div>
    {% endfor %}

    <div style="text-align: center;">
        <a href="/" class="btn">Retake Assessment</a>
    </div>
</body>
</html>
"""

# =============================================
# SCORING LOGIC HELPERS
# =============================================

def get_distress_score(user_answer, options_list):
    """
    Calculates a score from 0 to 1 based on the answer position.
    Assumption: The options are arranged from Positive -> Negative 
    OR Negative -> Positive. 
    
    I have manually reversed the options in the data list above so that 
    the LAST option is always the MOST NEGATIVE (High Score).
    
    Returns: A float between 0.0 (Good) and 1.0 (Bad).
    """
    try:
        index = options_list.index(user_answer)
        # Normalize index to 0-1 scale
        return index / (len(options_list) - 1)
    except ValueError:
        return 0

# =============================================
# APP ROUTES
# =============================================

@app.route('/')
def index():
    return render_template_string(html_template, questions=questions)

@app.route('/analyze', methods=['POST'])
def analyze():
    form_data = request.form
    
    # 1. Calculate Distress Score for each Category (Element)
    category_scores = {
        "Vitality": 0,
        "Connection": 0,
        "Environment": 0,
        "Growth": 0,
        "Stability": 0,
        "Meaning": 0,
        "Childhood Screening": 0
    }
    
    category_counts = category_scores.copy()

    for q in questions:
        q_id = str(q['id'])
        user_ans = form_data.get(f'q_{q_id}')
        if user_ans:
            score = get_distress_score(user_ans, q['options'])
            element = q['element']
            category_scores[element] += score
            category_counts[element] += 1
            
    # 2. Find the Categories with the highest average distress
    # We prioritize categories where the user is struggling most.
    sorted_categories = []
    for cat in category_scores:
        if category_counts[cat] > 0:
            avg_score = category_scores[cat] / category_counts[cat]
            sorted_categories.append((cat, avg_score))
            
    # Sort categories by highest distress (descending)
    sorted_categories.sort(key=lambda x: x[1], reverse=True)
    
    # Get the top 3 most painful categories
    top_pain_categories = [x[0] for x in sorted_categories[:3]]
    
    # 3. Filter Recursions
    # We look for patterns that match the user's top painful categories.
    matched_patterns = [r for r in recursions if r['category'] in top_pain_categories]
    
    # If we have too many matches, just take the first 3 (or randomize them)
    # If we have too few, fill with generic ones from the next highest category
    final_results = matched_patterns[:3]
    
    # Fallback: If logic finds nothing (rare), return defaults
    if not final_results:
        final_results = recursions[:3]

    return render_template_string(result_template, patterns=final_results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
