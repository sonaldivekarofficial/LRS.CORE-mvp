import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# =============================================
# DATA: QUESTIONS (Remains the same for reference)
# =============================================
questions = [
    # Vitality (1-10)
    {"id": 1, "element": "Vitality", "text": "In general, would you say your health is?", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]},
    {"id": 2, "element": "Vitality", "text": "During the past 4 weeks, how much did pain interfere with your normal work?", "options": ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 3, "element": "Vitality", "text": "During the past 4 weeks, did you have a lot of energy?", "options": ["All of the time", "Most of the time", "Some of the time", "A little of the time", "None of the time"]},
    {"id": 4, "element": "Vitality", "text": "During the past 4 weeks, to what degree did you experience mental exhaustion?", "options": ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"]},
    {"id": 5, "element": "Vitality", "text": "During the past 4 weeks, how would you rate your sleep quality overall?", "options": ["Very good", "Fairly good", "Fairly bad", "Very bad"]},
    {"id": 6, "element": "Vitality", "text": "How often do you feel unable to control important things in your life?", "options": ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]},
    {"id": 7, "element": "Vitality", "text": "I am able to adapt when changes occur.", "options": ["True nearly all the time", "Often true", "Sometimes true", "Rarely true", "Not true at all"]}, 
    {"id": 8, "element": "Vitality", "text": "I am often cheerful and in good spirits.", "options": ["All of the time", "More than half the time", "Less than half the time", "Some of the time", "At no time"]}, 
    {"id": 9, "element": "Vitality", "text": "I have felt calm and relaxed.", "options": ["All of the time", "More than half the time", "Less than half the time", "Some of the time", "At no time"]}, 
    {"id": 10, "element": "Vitality", "text": "I have enough physical and mental energy to fully engage in work, family, friends, and hobbies.", "options": ["Very often", "Fairly often", "Sometimes", "Almost never", "Never"]}, 

    # Connection (11-20)
    {"id": 11, "element": "Connection", "text": "How often do you feel that you lack companionship?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 12, "element": "Connection", "text": "How often do you feel left out among family, friends, or at work?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 13, "element": "Connection", "text": "I'm afraid that I will lose my partner's love.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 14, "element": "Connection", "text": "I prefer not to show a partner how I feel deep down.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 15, "element": "Connection", "text": "I can count on my friends/family when things go wrong.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 16, "element": "Connection", "text": "When I feel lonely, there are people I can talk to.", "options": ["Definitely true", "Probably true", "Probably false", "Definitely false"]}, 
    {"id": 17, "element": "Connection", "text": "I have healthy relationships with my neighbours and colleagues.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 18, "element": "Connection", "text": "Social media negatively impacts my mental health.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 19, "element": "Connection", "text": "I am in control of my screen time.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 20, "element": "Connection", "text": "My digital habits support my productivity.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 

    # Environment (21-30)
    {"id": 21, "element": "Environment", "text": "How safe do you feel in your neighborhood?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, 
    {"id": 22, "element": "Environment", "text": "How clean and well-maintained is your neighbourhood?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, 
    {"id": 23, "element": "Environment", "text": "I have access to park/garden/green space around my neighborhood.", "options": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]}, 
    {"id": 24, "element": "Environment", "text": "How clean and well-maintained is your home?", "options": ["Very good", "Good", "Fair", "Poor", "Very poor"]}, 
    {"id": 25, "element": "Environment", "text": "I have enough private space in my home.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 26, "element": "Environment", "text": "I feel safe and comfortable in my home.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 27, "element": "Environment", "text": "How often does clutter or disorganization affect your daily life?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 28, "element": "Environment", "text": "Rate your workplace’s overall comfortability and functionality.", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]}, 
    {"id": 29, "element": "Environment", "text": "Transit from my home to work and city is often comfortable.", "options": ["Strongly agree", "Agree", "Disagree", "Strongly disagree"]}, 
    {"id": 30, "element": "Environment", "text": "My home/work space/neighbourhood positively impacts my well-being.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 

    # Growth (31-40)
    {"id": 31, "element": "Growth", "text": "I have found a meaningful career.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 32, "element": "Growth", "text": "My work is aligned with my career goals.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 33, "element": "Growth", "text": "I actively seek opportunities for career growth within my work space.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 34, "element": "Growth", "text": "I actively seek opportunities to learn new skills.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 35, "element": "Growth", "text": "I actively seek opportunities to switch job for higher pay and designation.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 36, "element": "Growth", "text": "Setbacks do not discourage me.", "options": ["Very much like me", "Mostly like me", "Somewhat like me", "Not much like me", "Not like me at all"]}, 
    {"id": 37, "element": "Growth", "text": "I always manage to solve problems and get things done.", "options": ["Exactly true", "Moderately true", "Hardly true", "Not at all true"]}, 
    {"id": 38, "element": "Growth", "text": "I am confident I could deal efficiently with unexpected events like loss of job.", "options": ["Exactly true", "Moderately true", "Hardly true", "Not at all true"]}, 
    {"id": 39, "element": "Growth", "text": "Challenges motivate me to grow.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 40, "element": "Growth", "text": "How strong is your ability to prepare for the future?", "options": ["Strongest", "Very strong", "Moderately strong", "Slightly strong", "Not strong"]}, 

    # Stability (41-50)
    {"id": 41, "element": "Stability", "text": "How often have you had trouble paying bills?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 42, "element": "Stability", "text": "How often do you wonder if you are earning enough money?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 43, "element": "Stability", "text": "How often do you feel anxious about your current financial situation?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 44, "element": "Stability", "text": "I worry about my/my family’s spending habits.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 45, "element": "Stability", "text": "I feel stressed about my debts.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 46, "element": "Stability", "text": "I could handle a major unexpected expense like a hospital bill.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]}, 
    {"id": 47, "element": "Stability", "text": "I know what my financial goals are.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 48, "element": "Stability", "text": "I have a clear financial plan for the next 1-5 years.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 49, "element": "Stability", "text": "I regularly set aside money for long term savings.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 50, "element": "Stability", "text": "I am actively securing my financial future.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]}, 

    # Meaning (51-60)
    {"id": 51, "element": "Meaning", "text": "I am engaged and interested in my daily activities.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 52, "element": "Meaning", "text": "In life, I have clear goals and aims.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 53, "element": "Meaning", "text": "My relationships are genuine.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 54, "element": "Meaning", "text": "I feel genuinely interested in lives of people around me.", "options": ["Extremely", "Quite a bit", "Moderately", "A little", "Very slightly or not at all"]}, 
    {"id": 55, "element": "Meaning", "text": "I personally know some people who earnestly try to make positive difference in the world.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 56, "element": "Meaning", "text": "I contribute to society with act of service/food donations/financial help.", "options": ["Extremely", "Quite a bit", "Moderately", "A little", "Very slightly or not at all"]}, 
    {"id": 57, "element": "Meaning", "text": "I don't hold grudges, I find it easy to forgive and move on.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 58, "element": "Meaning", "text": "My life has a clear sense of purpose.", "options": ["Absolutely true", "Mostly true", "Somewhat true", "Can't say", "Somewhat untrue", "Mostly untrue", "Absolutely untrue"]}, 
    {"id": 59, "element": "Meaning", "text": "I try to lead a purposeful and meaningful life.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 
    {"id": 60, "element": "Meaning", "text": "I am optimistic about my future.", "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]}, 

    # Childhood Screening (61-70)
    {"id": 61, "element": "Childhood Screening", "text": "Did a parent or adult often swear at, insult, or humiliate you?", "options": ["Yes", "No"]},
    {"id": 62, "element": "Childhood Screening", "text": "Did you often feel no one in your family understood you?", "options": ["Yes", "No"]},
    {"id": 63, "element": "Childhood Screening", "text": "Did you live with a substance abuser or alcoholic?", "options": ["Yes", "No"]},
    {"id": 64, "element": "Childhood Screening", "text": "Was a household member depressed or mentally ill?", "options": ["Yes", "No"]},
    {"id": 65, "element": "Childhood Screening", "text": "Were your parents separated or divorced?", "options": ["Yes", "No"]},
    {"id": 66, "element": "Childhood Screening", "text": "Was your mother/father often pushed, grabbed, or slapped?", "options": ["Yes", "No"]},
    {"id": 67, "element": "Childhood Screening", "text": "Did an adult touch or fondle you sexually, or make you touch them?", "options": ["Yes", "No"]},
    {"id": "68_r", "element": "Childhood Screening", "text": "I felt emotionally neglected by my family.", "options": ["Never true", "Rarely true", "Sometimes true", "Often true", "Very often true"]}, 
    {"id": "69_r", "element": "Childhood Screening", "text": "I was physically hit so hard it left marks or bruises.", "options": ["Never true", "Rarely true", "Sometimes true", "Often true", "Very often true"]}, 
    {"id": "70_r", "element": "Childhood Screening", "text": "My household struggled financially and we often had difficulty making ends meet.", "options": ["Never true", "Rarely true", "Sometimes true", "Often true", "Very often true"]} 
]

# Map Q-IDs for easier lookup (since we used strings for reversed questions)
Q_MAP = {str(q['id']): q for q in questions if type(q['id']) is int}
Q_MAP.update({'68_r': questions[67], '69_r': questions[68], '70_r': questions[69]})
Q_MAP_ID_TO_OPTIONS = {id: q['options'] for id, q in Q_MAP.items()}

# =============================================
# DATA: RECURSIONS & THE NEW QUESTION MAPPING (CRITICAL)
# Each pattern is now mapped to specific Question IDs (q_ids) that trigger it.
# =============================================
recursions = [
    # Patterns from Screenshot (for testing continuity)
    {"name": "Fixed Mindset", "q_ids": ["36", "37", "39"], "root": "Growing up with labels rather than praise for effort", "symptom": "Avoiding challenges to maintain the label; giving up easily when things get hard", "action": "The \"Not Yet\" Technique. When you struggle, add \"yet\" to the end of the sentence. \"I don't understand this... yet.\""},
    {"name": "Good-Child Syndrome", "q_ids": ["61", "68_r", "15"], "root": "Survival depended on being obedient, quiet, helpful, never angry", "symptom": "Can’t say no, rage turns inward (depression, autoimmune issues)", "action": "Low-Stakes Disappointment. Practice saying \"no\" to something small."},
    {"name": "Perfectionism Trap", "q_ids": ["31", "32", "36"], "root": "Love was conditional on success", "symptom": "Procrastination, burnout, harsh inner critic", "action": "B- Work. Intentionally do a task at 80% effort."},
    
    # Other Patterns (with logical mappings to specific Qs)
    {"name": "Frozen Grief", "q_ids": ["9", "4", "62"], "root": "Was not allowed to cry or grieve -> emotions locked in body", "symptom": "Sudden crying spells, unexplained sadness", "action": "Scheduled Grief. Set a timer for 10 minutes to sit in silence."},
    {"name": "Abandonment Fear", "q_ids": ["13", "12", "11"], "root": "Separation or inconsistent caregivers", "symptom": "Clinginess, testing partners, pre-emptive leaving", "action": "Self-Soothing Mantra. \"I am here with you. I am not leaving you.\""},
    {"name": "Emotional Neglect Echo", "q_ids": ["68_r", "51", "58"], "root": "Physical needs met, emotional needs ignored", "symptom": "Difficulty identifying feelings, feeling empty", "action": "The Emotion Wheel. Point to exactly what you are feeling."},
    {"name": "Trust Deficit", "q_ids": ["14", "15", "16"], "root": "Betrayal by primary caregivers", "symptom": "Hyper-vigilance, testing people", "action": "Fact-Checking. Ask: \"Do I have evidence for this thought?\""},
    {"name": "Self-Worth Wound", "q_ids": ["61", "59", "57"], "root": "Humiliation or verbal abuse", "symptom": "Self-deprecation, settling for less", "action": "Esteemable Acts. Keep a daily promise to yourself."},
    {"name": "Chaos Adaptation", "q_ids": ["26", "27", "6"], "root": "Unstable, unpredictable home", "symptom": "Feeling bored during peace, manufacturing drama", "action": "Re-framing Boredom. Tell yourself: \"This isn't boredom; this is safety.\""},
    {"name": "Failure Aversion", "q_ids": ["36", "38", "37"], "root": "Punishment for simple mistakes", "symptom": "Playing small, hiding errors", "action": "Redefining Failure. View every fail as data collection."},
    {"name": "Identity Confusion", "q_ids": ["52", "59", "51"], "root": "Constant invalidation of preferences", "symptom": "Chameleon behavior, indecision", "action": "Values Sorting. Make one small decision based on your values."},
    {"name": "Emotional Suppression", "q_ids": ["9", "4", "8"], "root": "Emotions were dismissed or punished", "symptom": "Numbness, explosive outbursts", "action": "Somatic Release. Scream into a pillow or sprint."},
    {"name": "Financial Anxiety Loop", "q_ids": ["41", "43", "45"], "root": "Childhood poverty", "symptom": "Hoarding resources, panic about bills", "action": "Neutral Money Monitoring. Check bank account daily without judgment."},
    {"name": "People-Pleasing Circuit", "q_ids": ["15", "16", "17"], "root": "Safety conditional on compliant behavior", "symptom": "Inability to say no, resentment", "action": "The Pause. Never say yes immediately."},
    {"name": "Hyper-Independence", "q_ids": ["15", "17", "46"], "root": "Had to fend for self too early", "symptom": "Viewing help as weakness, burnout", "action": "Micro-Asks. Ask for help with something small."},
    {"name": "Guilt-Shame Spiral", "q_ids": ["61", "68_r", "57"], "root": "Being the scapegoat", "symptom": "Compulsive apologizing, feeling intrinsically wrong", "action": "Responsibility Pie Chart. Assign how much of a problem is actually yours."},
    {"name": "Catastrophizing Habit", "q_ids": ["6", "43", "38"], "root": "Unpredictable violence or chaos", "symptom": "High anxiety, scanning for threats", "action": "Best/Worst/Likely. Focus on the most likely outcome."},
    {"name": "Chronic Self-Doubt", "q_ids": ["37", "38", "58"], "root": "Constant 'never good enough' messages", "symptom": "Analysis paralysis, seeking validation", "action": "Evidence Log. Keep a list of wins."},
    {"name": "Boundary Collapse", "q_ids": ["14", "17", "18"], "root": "Enmeshment or lack of privacy", "symptom": "Oversharing, taking on others' emotions", "action": "The 'I' Statement. Practice saying 'I feel X when you do Y'."},
    {"name": "Savior Complex", "q_ids": ["66", "17", "15"], "root": "Parentification", "symptom": "Attracting broken partners to fix", "action": "Detachment with Love. Don't offer solutions immediately."},
    {"name": "Impostor Syndrome", "q_ids": ["32", "33", "31"], "root": "Praise for talent, not effort", "symptom": "Overworking, dread of being found out", "action": "Own the Success. Say only 'Thank you'."},
    {"name": "Rejection Sensitivity", "q_ids": ["12", "11", "13"], "root": "Frequent exclusion or bullying", "symptom": "Misinterpreting neutral cues as rejection", "action": "Check the Story. Assume positive intent."},
    {"name": "Control Obsession", "q_ids": ["6", "7", "27"], "root": "Profound helplessness", "symptom": "Rigidity, panic when plans change", "action": "Delegation Experiment. Let someone else plan."},
    {"name": "Numbness / Dissociation", "q_ids": ["4", "9", "51"], "root": "Overwhelming trauma", "symptom": "Feeling unreal, zoning out", "action": "5-4-3-2-1 Grounding."},
    {"name": "Approval Addiction", "q_ids": ["59", "51", "15"], "root": "Love withheld unless performing", "symptom": "Depression without praise", "action": "Secret Hobby. Do something just for you."},
    {"name": "Chronic Over-Responsibility", "q_ids": ["10", "56", "54"], "root": "Emotional caretaker to parent", "symptom": "Heaviness, inability to be playful", "action": "'Not Mine' Mantra. Visualize taking off the backpack."},
    {"name": "Self-Sabotage Pattern", "q_ids": ["36", "38", "40"], "root": "Success associated with danger", "symptom": "Quitting before finish line", "action": "Upper Limit Awareness. Breathe through the anxiety of happiness."},
    {"name": "Existential Emptiness", "q_ids": ["58", "52", "51"], "root": "No modeling of meaning", "symptom": "Chronic boredom, apathy", "action": "Service. Do one small act of kindness."},
    {"name": "Fear of Success", "q_ids": ["32", "35", "36"], "root": "Success brought unwanted responsibility", "symptom": "Playing small", "action": "Visualize Safety."},
    {"name": "Fear of Rejection", "q_ids": ["11", "12", "13"], "root": "Avoidance of 'no'", "symptom": "Not asking for things", "action": "Rejection Therapy. Ask for something ridiculous."},
    {"name": "Fear of Wrong Decision", "q_ids": ["7", "6", "37"], "root": "Fear of punishment for wrong choices", "symptom": "Stagnation, letting others decide", "action": "The 2-Minute Rule. Decide quickly on small things."},
    {"name": "FOPO (Fear of People's Opinions)", "q_ids": ["18", "19", "53"], "root": "Conforming to strict norms", "symptom": "Hiding true self", "action": "The Hula Hoop. Stay in your hoop."},
    {"name": "Fear of Responsibility", "q_ids": ["47", "48", "40"], "root": "Adulting = burden", "symptom": "Underachievement", "action": "One Adult Task."},
    {"name": "Fear of Commitment", "q_ids": ["13", "14", "53"], "root": "Witnessed unhappy marriages", "symptom": "Sabotaging relationships", "action": "Daily Choice."},
    {"name": "Fear of Change", "q_ids": ["7", "6", "26"], "root": "Change = danger", "symptom": "Staying in toxic comfort zone", "action": "Micro-Novelty."},
    {"name": "Fear of Vulnerability", "q_ids": ["14", "53", "16"], "root": "Openness was mocked", "symptom": "Superficial relationships", "action": "The 10% Rule. Share a little more."},
    {"name": "Fear of Conflict", "q_ids": ["61", "17", "15"], "root": "Arguments were explosive", "symptom": "Passive-aggression", "action": "The Sandwich Method."},
    {"name": "Procrastination", "q_ids": ["4", "10", "34"], "root": "Overwhelm or lack of guidance", "symptom": "Last-minute rushes", "action": "5-Minute Start."},
    {"name": "Negative Self-Talk", "q_ids": ["8", "9", "4"], "root": "Internalized critical parent", "symptom": "Self-attack", "action": "Name the Critic."},
    {"name": "Blaming Others", "q_ids": ["37", "38", "57"], "root": "Fragile ego", "symptom": "Lack of accountability", "action": "Radical Responsibility."},
    {"name": "Lack of Prioritization", "q_ids": ["20", "52", "59"], "root": "Avoiding big tasks", "symptom": "Busy but not productive", "action": "Eisenhower Matrix."},
    {"name": "Mindless Consumption", "q_ids": ["18", "19", "20"], "root": "Soothing distress via screens/food", "symptom": "Doomscrolling", "action": "Urge Surfing."},
    {"name": "Overcommitment (FOMO)", "q_ids": ["10", "17", "33"], "root": "Fear of missing out", "symptom": "Exhaustion", "action": "JOMO."},
    {"name": "Self-Isolation", "q_ids": ["11", "12", "16"], "root": "Feeling like a burden", "symptom": "Loneliness loop", "action": "Opposite Action."},
    {"name": "Ignoring Personal Needs", "q_ids": ["10", "4", "3"], "root": "Putting others first to be safe", "symptom": "Resentment outbursts", "action": "HALT Check."},
    {"name": "All-or-Nothing Thinking", "q_ids": ["36", "37", "57"], "root": "Rigid parenting", "symptom": "Quitting after one slip-up", "action": "The Grey Zone."},
    {"name": "Living in the Past", "q_ids": ["62", "68_r", "58"], "root": "Unresolved trauma", "symptom": "Ruminating on old events", "action": "Mindfulness Practice."},
    {"name": "Trauma Bonding", "q_ids": ["66", "67", "13"], "root": "Abuse confused with love", "symptom": "Addiction to toxic people", "action": "No Contact Rule."},
    {"name": "Scarcity Mindset", "q_ids": ["42", "44", "49"], "root": "Never enough resources", "symptom": "Fear of spending", "action": "Abundance Journal."},
    {"name": "Learned Helplessness", "q_ids": ["6", "38", "37"], "root": "Efforts never changed outcome", "symptom": "Giving up before trying", "action": "Smallest Possible Win."}
]

# =============================================
# HTML TEMPLATES (Unchanged for aesthetics)
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
    0.0 (Good/No Distress) to 1.0 (Bad/Max Distress).
    """
    try:
        index = options_list.index(user_answer)
        # Normalize index to 0-1 scale
        return index / (len(options_list) - 1)
    except ValueError:
        # Should not happen if required fields are filled, but safety catch
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
    
    # 1. Calculate Distress Scores for ALL 50 patterns
    scored_patterns = []
    
    for pattern in recursions:
        pattern_score_sum = 0
        q_count = 0
        
        # Iterate through the specific questions mapped to this pattern
        for q_id in pattern['q_ids']:
            # The name attribute in the form is 'q_X'
            form_key = f'q_{q_id}'
            user_ans = form_data.get(form_key)
            
            # Find the original options list for scoring
            options_list = Q_MAP_ID_TO_OPTIONS.get(q_id)
            
            if user_ans and options_list:
                # Get the distress score for this specific question
                score = get_distress_score(user_ans, options_list)
                pattern_score_sum += score
                q_count += 1
                
        # 2. Calculate the Average Distress for this specific pattern
        if q_count > 0:
            avg_pattern_score = pattern_score_sum / q_count
            
            # Create a new structure containing the pattern and its score
            scored_patterns.append({
                'score': avg_pattern_score,
                'name': pattern['name'],
                'root': pattern['root'],
                'symptom': pattern['symptom'],
                'action': pattern['action']
            })

    # 3. Sort ALL 50 patterns by score (Highest score = highest priority)
    scored_patterns.sort(key=lambda x: x['score'], reverse=True)
    
    # 4. Select the Top 3 patterns with the highest distress scores
    final_results = scored_patterns[:3]
    
    # Fallback to defaults if no scores calculated (e.g., if user skipped all questions, though required=True should prevent this)
    if not final_results:
        final_results = recursions[:3]

    return render_template_string(result_template, patterns=final_results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
