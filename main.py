```python:disable-run
from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

# =============================================
# LATENT RECURSION SYSTEM v11.0 – FINAL FIXED VERSION
# 70 questions (all visible, including Stability); grammar fixed; selected option green; page scrolls to top; back button; top 3 patterns with root/symptom/action; biome with circle trees & red currents
# =============================================

questions = [
    # Vitality (1-10)
    {"id": 1, "element": "Vitality", "text": "In general, would you say your health is?", "options": ["Excellent", "Very good", "Good", "Fair", "Poor"]},
    {"id": 2, "element": "Vitality", "text": "During the past 4 weeks, how much did pain interfere with your normal work?", "options": ["Not at all", "A little bit", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 3, "element": "Vitality", "text": "During the past 4 weeks, did you have a lot of energy?", "options": ["All of the time", "Most of the time", "Some of the time", "A little of the time", "None of the time"]},
    {"id": 4, "element": "Vitality", "text": "During the past 4 weeks, to what degree did you experience mental exhaustion?", "options": ["Not at all", "A little bit", "Somewhat", "Quite a bit", "Very much"]},
    {"id": 5, "element": "Vitality", "text": "During the past 4 weeks, how would you rate your sleep quality overall?", "options": ["Very good", "Fairly good", "Fairly bad", "Very bad"]},
    {"id": 6, "element": "Vitality", "text": "How often do you feel unable to control important things in your life?", "options": ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]},
    {"id": 7, "element": "Vitality", "text": "I am able to adapt when changes occur.", "options": ["Not true at all", "Rarely true", "Sometimes true", "Often true", "True nearly all the time"]},
    {"id": 8, "element": "Vitality", "text": "I am often cheerful and in good spirits.", "options": ["At no time", "Some of the time", "Less than half the time", "More than half the time", "All of the time"]},
    {"id": 9, "element": "Vitality", "text": "I have felt calm and relaxed.", "options": ["At no time", "Some of the time", "Less than half the time", "More than half the time", "All of the time"]},
    {"id": 10, "element": "Vitality", "text": "I have enough physical and mental energy to fully engage in work, family, friends, and hobbies.", "options": ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]},

    # Connection (11-20)
    {"id": 11, "element": "Connection", "text": "How often do you feel that you lack companionship?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 12, "element": "Connection", "text": "How often do you feel left out among family, friends, or at work?", "options": ["Hardly ever", "Some of the time", "Often"]},
    {"id": 13, "element": "Connection", "text": "I'm afraid that I will lose my partner's love.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 14, "element": "Connection", "text": "I prefer not to show a partner how I feel deep down.", "options": ["Strongly disagree", "Disagree", "Slightly disagree", "Neutral", "Slightly agree", "Agree", "Strongly agree"]},
    {"id": 15, "element": "Connection", "text": "I can count on my friends/family when things go wrong.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 16, "element": "Connection", "text": "When I feel lonely, there are people I can talk to.", "options": ["Definitely false", "Probably false", "Probably true", "Definitely true"]},
    {"id": 17, "element": "Connection", "text": "I have healthy relationships with my neighbours and colleagues.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 18, "element": "Connection", "text": "Social media negatively impacts my mental health.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 19, "element": "Connection", "text": "I am in control of my screen time.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 20, "element": "Connection", "text": "My digital habits support my productivity.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Environment (21-30)
    {"id": 21, "element": "Environment", "text": "How safe do you feel in your neighborhood?", "options": ["Very poor", "Poor", "Fair", "Good", "Very good"]},
    {"id": 22, "element": "Environment", "text": "How clean and well-maintained is your neighbourhood?", "options": ["Very poor", "Poor", "Fair", "Good", "Very good"]},
    {"id": 23, "element": "Environment", "text": "I have access to park/garden/green space around my neighborhood.", "options": ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]},
    {"id": 24, "element": "Environment", "text": "How clean and well-maintained is your home?", "options": ["Very poor", "Poor", "Fair", "Good", "Very good"]},
    {"id": 25, "element": "Environment", "text": "I have enough private space in my home.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 26, "element": "Environment", "text": "I feel safe and comfortable in my home.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 27, "element": "Environment", "text": "How often does clutter or disorganization affect your daily life?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 28, "element": "Environment", "text": "Rate your workplace's overall comfortability and functionality.", "options": ["Poor", "Fair", "Good", "Very good", "Excellent"]},
    {"id": 29, "element": "Environment", "text": "Transit from my home to work and city is often comfortable.", "options": ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]},
    {"id": 30, "element": "Environment", "text": "My home/work space/neighbourhood positively impacts my well-being.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Growth (31-40)
    {"id": 31, "element": "Growth", "text": "I have found a meaningful career.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 32, "element": "Growth", "text": "My work is aligned with my career goals.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 33, "element": "Growth", "text": "I actively seek opportunities for career growth within my workspace.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 34, "element": "Growth", "text": "I actively seek opportunities to learn new skills.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 35, "element": "Growth", "text": "I actively seek opportunities to switch jobs for higher pay and designation.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 36, "element": "Growth", "text": "Setbacks do not discourage me.", "options": ["Not like me at all", "Not much like me", "Somewhat like me", "Mostly like me", "Very much like me"]},
    {"id": 37, "element": "Growth", "text": "I always manage to solve problems and get things done.", "options": ["Not at all true", "Hardly true", "Moderately true", "Exactly true"]},
    {"id": 38, "element": "Growth", "text": "I am confident I could deal efficiently with unexpected events like loss of job.", "options": ["Not at all true", "Hardly true", "Moderately true", "Exactly true"]},
    {"id": 39, "element": "Growth", "text": "Challenges motivate me to grow.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 40, "element": "Growth", "text": "How strong is your ability to prepare for the future?", "options": ["Not strong", "Slightly strong", "Moderately strong", "Very strong", "Strongest"]},

    # Stability (41-50) – now visible
    {"id": 41, "element": "Stability", "text": "How often have you had trouble paying bills?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 42, "element": "Stability", "text": "How often do you wonder if you are earning enough money?", "options": ["Never", "Rarely", "Sometimes", "Often", "Very often"]},
    {"id": 43, "element": "Stability", "text": "How often do you feel anxious about your current financial situation?", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 44, "element": "Stability", "text": "I worry about my/my family’s spending habits.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 45, "element": "Stability", "text": "I feel stressed about my debts.", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
    {"id": 46, "element": "Stability", "text": "I could handle a major unexpected expense like a hospital bill.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]},
    {"id": 47, "element": "Stability", "text": "I know what my financial goals are.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 48, "element": "Stability", "text": "I have a clear financial plan for the next 1-5 years.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 49, "element": "Stability", "text": "I regularly set aside money for long term savings.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 50, "element": "Stability", "text": "I am actively securing my financial future.", "options": ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]},

    # Meaning (51-60)
    {"id": 51, "element": "Meaning", "text": "I am engaged and interested in my daily activities.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 52, "element": "Meaning", "text": "In life, I have clear goals and aims.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 53, "element": "Meaning", "text": "My relationships are genuine.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 54, "element": "Meaning", "text": "I feel genuinely interested in lives of people around me.", "options": ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 55, "element": "Meaning", "text": "I personally know some people who earnestly try to make positive difference in the world.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 56, "element": "Meaning", "text": "I contribute to society with act of service/food donations/financial help.", "options": ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]},
    {"id": 57, "element": "Meaning", "text": "I don't hold grudges, I find it easy to forgive and move on.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 58, "element": "Meaning", "text": "My life has a clear sense of purpose.", "options": ["Absolutely untrue", "Mostly untrue", "Somewhat untrue", "Can't say", "Somewhat true", "Mostly true", "Absolutely true"]},
    {"id": 59, "element": "Meaning", "text": "I try to lead a purposeful and meaningful life.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},
    {"id": 60, "element": "Meaning", "text": "I am optimistic about my future.", "options": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]},

    # Recursion (61-70)
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

# Element Groups for Scoring
element_groups = {
    "Vitality": [q for q in questions if q["element"] == "Vitality"],
    "Connection": [q for q in questions if q["element"] == "Connection"],
    "Environment": [q for q in questions if q["element"] == "Environment"],
    "Growth": [q for q in questions if q["element"] == "Growth"],
    "Stability": [q for q in questions if q["element"] == "Stability"],
    "Meaning": [q for q in questions if q["element"] == "Meaning"],
    "Recursion": [q for q in questions if q["element"] == "Recursion"]
}

# 50 Recursive Patterns with Root, Symptom, Action
recursions = [
    {"name": "Fixed Mindset", "root": "Growing up with labels rather than praise for effort", "symptom": "Avoiding challenges; giving up easily when things get hard", "action": "The \"Not Yet\" Technique. When you struggle, add \"yet\" to the end of the sentence. \"I don't understand this... yet.\" Praise yourself for the process of learning, not the grade/result."},
    {"name": "Good-Child Syndrome", "root": "Survival depended on being obedient, quiet, helpful, never angry, never needy", "symptom": "Can’t say no, rage turns inward (depression, autoimmune issues), perfectionism + resentment", "action": "Low-Stakes Disappointment. Practice saying \"no\" to something small (e.g., declining a receipt, choosing a different restaurant than your friend) to teach your nervous system that you are safe even if you aren't compliant."},
    {"name": "Frozen Grief / Uncried Tears", "root": "Was not allowed to cry or grieve (death, divorce, abuse, moves) → emotions got locked in the body", "symptom": "Sudden crying spells decades later, unexplained sadness, psychosomatic pain, “emotional constipation”", "action": "Scheduled Grief. Set a timer for 10 minutes to sit in silence, listen to sad music, or look at a photo, specifically allowing the feeling to rise. When the timer hits, get up and physically shake out your body."},
    {"name": "Abandonment Fear", "root": "Separation, divorce, or inconsistent caregivers in formative years", "symptom": "Clinginess, testing partners, staying in toxic relationships to avoid being alone, pre-emptive leaving (\"I'll leave you before you leave me\").", "action": "Self-Soothing Mantra. When panic rises, place a hand on your heart and say, \"I am here with you. I am not leaving you.\" You must become the consistent caregiver you didn't have."},
    {"name": "Emotional Neglect Echo", "root": "Physical needs were met, but emotional needs were ignored or minimized", "symptom": "Difficulty identifying feelings (alexithymia), feeling flawed or empty, believing one’s needs do not matter.", "action": "The Emotion Wheel. Print an emotion wheel. Three times a day, force yourself to point to exactly what you are feeling (e.g., \"I am not just bad, I am lonely\"). Naming it tames it."},
    {"name": "Trust Deficit", "root": "Betrayal by primary caregivers or Adverse Childhood Experiences (ACEs)", "symptom": "Hyper-vigilance, testing people, interpreting neutral actions as malicious, isolating to ensure safety.", "action": "Fact-Checking. When you suspect someone’s motive, ask yourself: \"Do I have evidence for this thought, or is this my past fear talking?\" Look for alternative, benign explanations."},
    {"name": "Self-Worth Wound", "root": "History of humiliation, verbal abuse, or being treated as a burden", "symptom": "Self-deprecation, settling for less than deserved in career/love, inability to accept compliments.", "action": "Esteemable Acts. Self-esteem comes from doing esteemable things. Keep a daily promise to yourself (e.g., making your bed) to rebuild trust in your own worthiness."},
    {"name": "Chaos Adaptation", "root": "Growing up in an unstable, unpredictable, or volatile home environment", "symptom": "Feeling bored or anxious during times of peace, subconsciously manufacturing drama or crisis to feel \"normal.\"", "action": "Re-framing Boredom. When things are calm and you feel an itch for drama, tell yourself: \"This isn't boredom; this is safety.\" Practice sitting in \"boring\" safety for 5 minutes."},
    {"name": "Perfectionism Trap", "root": "Relentless criticism or high expectations where love was conditional on success", "symptom": "Procrastination (fear of starting), burnout, paralysis, harsh inner critic.", "action": "B- Work. Intentionally do a task at 80% effort. Send the email without the third proofread. Leave the bed slightly messy. Observe that the world does not end."},
    {"name": "Failure Aversion", "root": "Excessive punishment or shaming for making simple mistakes in childhood", "symptom": "Playing small, refusing to try new things, hiding errors rather than fixing them, stagnation.", "action": "Redefining Failure. View every \"fail\" as data collection. Ask: \"What did I learn?\" rather than \"What is wrong with me?\""},
    {"name": "Identity Confusion", "root": "Constant invalidation of preferences/thoughts (\"You don't think that,\" \"You're cold, put a jacket on\")", "symptom": "Chameleon behavior (changing personality to fit the room), indecision, feeling like a stranger to oneself.", "action": "Values Sorting. Write down 5 things that matter to you (not your parents/society). Make one small decision today based solely on one of those values."},
    {"name": "Emotional Suppression", "root": "Emotions were dismissed, mocked, or punished (\"Stop crying or I'll give you something to cry about\")", "symptom": "Numbness, sudden explosive outbursts (volcano effect), psychosomatic illness, emotional unavailability.", "action": "Somatic Release. If you can't cry/speak, use the body. Scream into a pillow, punch a mattress, or sprint for 30 seconds to move the energy out."},
    {"name": "Financial Anxiety Loop", "root": "Childhood poverty, witnessing parental panic over bills, foreclosure/eviction trauma", "symptom": "Hoarding resources, guilt when spending on necessities, panic attacks regarding financial security regardless of actual wealth.", "action": "Neutral Money Monitoring. Check your bank account daily—not to judge, but to normalize looking at the numbers without panic. Desensitize the trigger."},
    {"name": "People-Pleasing Circuit", "root": "Love and safety were conditional on compliant, \"happy\" behavior", "symptom": "Inability to say no, over-apologizing, resentment toward others for \"taking advantage,\" loss of self.", "action": "The Pause. Never say \"yes\" immediately. Implement a mandatory rule: \"I need to check my calendar, I'll let you know in an hour.\" This buys you time to find your true \"no.\""},
    {"name": "Hyper-Independence", "root": "Had to fend for self too early due to negligent or absent parents", "symptom": "Viewing help as weakness, isolation during struggles, burnout from carrying everything alone.", "action": "Micro-Asks. Ask for help with something inconsequential today (e.g., \"Can you pass the salt?\" or \"What time is it?\"). Retrain the brain that receiving is safe."},
    {"name": "Guilt-Shame Spiral", "root": "Being the \"scapegoat\" for family problems or parents' emotional states", "symptom": "Compulsive apologizing, feeling responsible for others' moods, deep sense of being intrinsically \"wrong.\"", "action": "Responsibility Pie Chart. Draw a circle. Assign how much of a problem is actually yours vs. timing, other people, or luck. Rarely is it 100% you."},
    {"name": "Catastrophizing Habit", "root": "Living in an environment of unpredictable violence or chaos", "symptom": "High anxiety, inability to relax, constantly scanning for threats, \"waiting for the other shoe to drop.\"", "action": "Best/Worst/Likely. When spiraling, write down: 1) The Worst Case, 2) The Best Case, 3) The Most Likely Case. Focus on the third."},
    {"name": "Chronic Self-Doubt", "root": "Constant \"never good enough\" messages or comparison to siblings/others", "symptom": "Analysis paralysis, constantly seeking external validation before making decisions, second-guessing.", "action": "Evidence Log. Keep a list of \"Wins.\" Write down 3 things you handled well today. Consult this list when doubt creeps in."},
    {"name": "Boundary Collapse", "root": "Enmeshment, lack of privacy, or parents treating the child as an extension of themselves", "symptom": "Oversharing, taking on others' emotions as one's own, inability to distinguish where \"I\" end and \"You\" begin.", "action": "The \"I\" Statement. Practice saying \"I feel [x] when you do [y].\" Establish a physical boundary, like closing a door or not answering a text after 9 PM."},
    {"name": "Savior Complex", "root": "Parentification (child had to parent their own parents or siblings)", "symptom": "Attracting broken partners to \"fix,\" neglecting own needs to solve others' crises, basing self-worth on utility.", "action": "Detachment with Love. When someone complains, say, \"That sounds hard. What do you plan to do about it?\" Resist the urge to offer a solution."},
    {"name": "Impostor Syndrome", "root": "Praise received only for innate talent or achievement, not effort", "symptom": "Overworking to prove worth, attributing success to luck, dread of being \"found out.\"", "action": "Own the Success. When praised, say only \"Thank you.\" Do not deflect (\"Oh, it was nothing\"). Sit with the discomfort of receiving credit."},
    {"name": "Rejection Sensitivity", "root": "Frequent exclusion, ridicule, or bullying by peers/family", "symptom": "Misinterpreting neutral cues as rejection, social withdrawal, emotional volatility in relationships.", "action": "Check the Story. Ask yourself: \"Did they actually reject me, or are they just busy/tired?\" Assume positive intent until proven otherwise."},
    {"name": "Control Obsession", "root": "Experience of profound helplessness or powerlessness in childhood", "symptom": "Rigidity, panic when plans change, inability to delegate, high stress when not in charge.", "action": "Delegation Experiment. Let someone else plan dinner or drive the car. Practice the mantra: \"I can handle it if things go wrong.\""},
    {"name": "Numbness / Dissociation Loop", "root": "Overwhelming trauma where \"leaving the body\" was the only safety", "symptom": "Feeling unreal or foggy, poor memory, \"zoning out\" during stress, lack of physical sensation.", "action": "5-4-3-2-1 Grounding. Acknowledge 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. This pulls you back into the present moment."},
    {"name": "Approval Addiction", "root": "Love was withheld unless performing (sports, grades, looks)", "symptom": "Depression when not receiving praise, changing views to match the crowd, \"performing\" rather than living.", "action": "Secret Hobby. Do something creative or active purely for yourself and do not share it on social media. Keep the joy for you."},
    {"name": "Chronic Over-Responsibility", "root": "Became the emotional caretaker or surrogate spouse to a parent too young", "symptom": "Feeling responsible for everyone’s happiness, heaviness, inability to be playful or lighthearted.", "action": "\"Not Mine\" Mantra. Visualize a heavy backpack. Consciously take it off and say, \"This is not my burden to carry.\""},
    {"name": "Self-Sabotage Pattern", "root": "Success was associated with danger (envy, punishment, or abandonment)", "symptom": "Quitting right before the finish line, destroying healthy relationships, procrastination when close to a goal.", "action": "Upper Limit Awareness. When things are going well and you feel the urge to ruin it, stop and say, \"I am expanding my capacity for good.\" Breathe through the anxiety of happiness."},
    {"name": "Existential Emptiness", "root": "No modeling of meaning, purpose, or spiritual connection in the home", "symptom": "Chronic boredom, apathy, lack of direction, feeling that life is \"pointless.\"", "action": "Service. Meaning is often found in contribution. Do one small act of kindness (holding a door, listening intently) to feel connected to the whole."},
    {"name": "Fear of Success", "root": "Success brought unwanted responsibility, visibility, or alienation from family", "symptom": "Turning down promotions, playing small (\"Tall Poppy Syndrome\"), anxiety when things go well.", "action": "Visualize Safety. Visualize succeeding, but also visualize your family/friends still loving you (or you surviving their envy)."},
    {"name": "Fear of Rejection", "root": "Avoidance of requests/opportunities to prevent hearing \"no\"", "symptom": "Not asking for raises, not approaching potential partners, isolation, resentment of missed chances.", "action": "Rejection Therapy. Intentionally ask for something ridiculous (e.g., a 10% discount on a coffee) just to hear the word \"No\" and realize you don't die."},
    {"name": "Fear of Making Wrong Decision", "root": "Analysis paralysis stemming from fear of punishment for wrong choices", "symptom": "Stagnation, letting others decide for you, ruminating on past choices, inability to move forward.", "action": "The 2-Minute Rule. If a decision is reversible (e.g., what to eat, what to wear), give yourself 2 minutes max to decide. Trust your gut."},
    {"name": "Fear of Other People's Opinions (FOPO)", "root": "Conforming to strict social norms to avoid criticism or shame", "symptom": "Hiding true self, anxiety about reputation, suppression of unique traits, \"What will the neighbors think?\" mentality.", "action": "The Hula Hoop. Imagine a hula hoop around you. Everything inside (your thoughts, actions) is your business. Everything outside (their opinions) is their business. Stay in your hoop."},
    {"name": "Fear of Responsibility", "root": "Adulting = overwhelming burden", "symptom": "Underachievement, reliance on others for basic needs, avoidance of \"adulting.\"", "action": "One Adult Task. Do not try to fix your whole life. Do one adult task today (e.g., book the dentist). Celebration follows completion."},
    {"name": "Fear of Commitment", "root": "Witnessed trapped/unhappy marriages", "symptom": "Serial dating, job hopping, sabotaging relationships when they get serious, feeling suffocated by expectations.", "action": "Daily Choice. Remind yourself: \"I am choosing this relationship today. I am free to leave if it becomes abusive.\" Remind yourself you are not trapped."},
    {"name": "Fear of Unknown/Change", "root": "Change historically = danger", "symptom": "Staying in toxic comfort zone, refusal to adapt, anxiety when routine is disrupted.", "action": "Micro-Novelty. Brush your teeth with the other hand. Take a different route to work. Teach your brain that small changes are safe."},
    {"name": "Fear of Vulnerability", "root": "Openness was mocked or weaponised", "symptom": "Superficial relationships, armoured heart, loneliness despite being around people.", "action": "The 10% Rule. Share just 10% more than you normally would with a safe person. \"I'm actually having a tough day\" instead of \"I'm fine.\""},
    {"name": "Fear of Conflict", "root": "Arguments were explosive/dangerous", "symptom": "Passive-aggression, silent treatment, internalized anger, relationships that lack depth/honesty.", "action": "The Sandwich Method. Address an issue by sandwiching the critique between two positive statements. \"I love how we work together. I need you to be on time. I value our partnership.\""},
    {"name": "Procrastination", "root": "Overwhelm/fear caused by high pressure or lack of guidance", "symptom": "Last-minute rushes, guilt-stress-relief cycle, missed deadlines.", "action": "5-Minute Start. Agree to do the thing for only 5 minutes. If you want to stop after 5 minutes, you can. Usually, the friction is just in starting."},
    {"name": "Negative Self-Talk", "root": "Internalized voice of a critical parent or authority figure", "symptom": "Constant self-attack, eroding confidence, talking oneself out of opportunities, depression.", "action": "Name the Critic. Give that negative voice a silly name (e.g., \"Grumpy Gertie\"). When it starts, say, \"Thanks for your input, Gertie, but I've got this.\""},
    {"name": "Blaming Others/Circumstances", "root": "Attributing failures externally to protect a fragile ego", "symptom": "Lack of personal accountability, repeating the same mistakes, feeling powerless to change life.", "action": "Radical Responsibility. Ask: \"What was my role in this?\" Even if it’s only 1%, owning your part gives you the power to change it."},
    {"name": "Lack of Prioritization", "root": "Busy with non-important tasks to avoid facing the big scary tasks", "symptom": "\"Busy but not productive,\" exhaustion without achievement, clutter (mental and physical).", "action": "Eisenhower Matrix. Categorize tasks: Urgent/Important vs. Not Urgent/Not Important. Do the hardest thing first (Eat the Frog)."},
    {"name": "Mindless Consumption/Distraction", "root": "Using food, screens, substances to soothe distress without addressing underlying emotional issues", "symptom": "Doomscrolling, binge-eating/watching, brain fog, loss of time, shame cycle.", "action": "Urge Surfing. When you want to pick up the phone/eat, wait 10 minutes. \"Surf\" the urge like a wave. It often peaks and subsides."},
    {"name": "Overcommitment (FOMO)", "root": "Saying yes to too much to avoid missing out or disappointing others", "symptom": "Flaking on plans, exhaustion, resentment, half-finished projects.", "action": "JOMO (Joy of Missing Out). Intentionally skip one event to stay home and rest. Savor the feeling of reclaiming your time."},
    {"name": "Self-Isolation", "root": "\"I'm a burden\" or \"no one understands\"", "symptom": "Deepening depression, loss of social skills, feedback loop of loneliness.", "action": "Opposite Action. If your depression says \"stay in bed,\" the opposite action is \"call a friend\" or \"go outside.\" Do the opposite of what the mood dictates."},
    {"name": "Ignoring Personal Needs", "root": "Putting others first was the only way to be \"good\" or safe", "symptom": "Physical illness, exhaustion, resentment outbursts, not knowing what one actually likes or needs.", "action": "HALT Check. Before helping anyone else, ask: Am I Hungry, Angry, Lonely, or Tired? Address your HALT first."},
    {"name": "All-or-Nothing Thinking", "root": "Viewing situations in extremes (perfect or failure) due to rigid parenting", "symptom": "Quitting a habit after one slip-up, rigid rules, judgment of self and others, inability to see nuance.", "action": "The Grey Zone. Replace \"always\" and \"never\" with \"sometimes\" and \"often.\" Allow for a partial success (e.g., a 10-minute workout is better than 0)."},
    {"name": "Living in the Past/Ruminating", "root": "Trauma or regret that was never processed or forgiven", "symptom": "Bitterness, missing the present moment, re-playing old arguments, inability to move on.", "action": "Sensory Interrupt. When replaying a past argument, physically clap your hands loudly and say \"Stop.\" Then name 3 blue things in the room."},
    {"name": "Focusing on What is Lacking", "root": "Concentrating on inadequacies (e.g., lack of time, money, skills) instead of leveraging existing strengths and opportunities", "symptom": "Chronic pessimism, ungratefulness, jealousy/envy, inability to enjoy success.", "action": "Gratitude Rampage. Spend 60 seconds listing everything that is working right now (lungs breathing, electricity on, coffee warm). Shift the lens."},
    {"name": "Waiting for the Perfect Time", "root": "Believing there is an ideal moment to start a new venture, which is a form of procrastination that ensures nothing ever begins", "symptom": "\"I'll do it when...\" syndrome, dreaming but not doing, life passing by while waiting for conditions to be ideal.", "action": "Imperfect Action. Do the thing badly today rather than perfectly tomorrow. Start the project with a messy draft."},
    {"name": "Comparison Trap", "root": "Being constantly compared to siblings/peers by parents or teachers", "symptom": "Feeling behind in life, bitterness toward others' success, diminishing own achievements.", "action": "Compare to Past Self. Only compare who you are today to who you were last year. Are you kinder? wiser? stronger? That is the only metric that matters."},
    {"name": "Scarcity / Deprivation Loop", "root": "Growing up with “there’s never enough” (money, food, love, time, attention)", "symptom": "Hoarding, under-charging, inability to receive, saying \"it’s fine\" when it’s not", "action": "Notice one thing you have in abundance (air, sunlight) and feel grateful."},
    {"name": "Good-Girl / Good-Boy Syndrome", "root": "Survival depended on being obedient, quiet, helpful, never angry, never needy", "symptom": "Can’t say no, rage turns inward (depression, autoimmune issues), perfectionism + resentment", "action": "Practice small safe 'no's daily."},
    {"name": "Frozen Grief / Uncried Tears", "root": "Was not allowed to cry or grieve (death, divorce, abuse, moves) → emotions got locked in the body", "symptom": "Sudden crying spells decades later, unexplained sadness, psychosomatic pain", "action": "Scheduled Grief + shake out."}
]

# Calculate element scores
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
            val_num = len(q["options"]) - 1 - idx if negative else idx
            total += val_num
            count += 1
        max_val = len(q["options"]) - 1 if count else 1
        scores[el] = round((total / (count * max_val)) * 100) if count else 50
    return scores

# Detect top 3 patterns from 50
def detect_recursions(responses, scores):
    ace = sum(1 for i in range(61,68) if responses.get(str(i)) == "Yes")
    emo_neglect = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("71","Rarely true"))
    phys_abuse = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("72","Rarely true"))
    fin_struggle = ["Never true","Rarely true","Sometimes true","Often true","Very often true"].index(responses.get("76","Rarely true"))
    v,c,e,g,s,m = (scores.get(k,50) for k in ["Vitality","Connection","Environment","Growth","Stability","Meaning"])

    candidates = []
    for pattern in recursions:
        strength = 40
        if "Fixed Mindset" in pattern["name"]:
            strength += emo_neglect * 5 + (100 - g) * 0.7 + (100 - m) * 0.3
        elif "Good-Child" in pattern["name"]:
            strength += emo_neglect * 10 + (100 - c) * 0.5 + (100 - v) * 0.3
        elif "Frozen Grief" in pattern["name"]:
            strength += emo_neglect * 8 + phys_abuse * 5 + (100 - v) * 0.6 + (100 - m) * 0.4
        elif "Abandonment Fear" in pattern["name"]:
            strength += ace * 8 + emo_neglect * 5 + (100 - c) * 0.8 + (100 - m) * 0.6
        elif "Emotional Neglect Echo" in pattern["name"]:
            strength += emo_neglect * 10 + (100 - m) * 0.5 + (100 - v) * 0.3
        elif "Trust Deficit" in pattern["name"]:
            strength += ace * 10 + (100 - c) * 0.5 + (100 - e) * 0.3
        elif "Self-Worth Wound" in pattern["name"]:
            strength += emo_neglect * 8 + phys_abuse * 8 + (100 - g) * 0.5 + (100 - v) * 0.3
        elif "Chaos Adaptation" in pattern["name"]:
            strength += fin_struggle * 8 + ace * 8 + (100 - s) * 0.5 + (100 - e) * 0.3
        elif "Perfectionism Trap" in pattern["name"]:
            strength += emo_neglect * 7 + phys_abuse * 5 + (100 - g) * 0.5 + (100 - s) * 0.3
        elif "Failure Aversion" in pattern["name"]:
            strength += phys_abuse * 10 + fin_struggle * 5 + (100 - g) * 0.5 + (100 - s) * 0.3
        elif "Identity Confusion" in pattern["name"]:
            strength += emo_neglect * 8 + ace * 6 + (100 - m) * 0.5 + (100 - g) * 0.3
        elif "Emotional Suppression" in pattern["name"]:
            strength += emo_neglect * 10 + phys_abuse * 5 + (100 - v) * 0.5 + (100 - c) * 0.3
        elif "Financial Anxiety Loop" in pattern["name"]:
            strength += fin_struggle * 10 + ace * 5 + (100 - s) * 0.5 + (100 - g) * 0.3
        elif "People-Pleasing Circuit" in pattern["name"]:
            strength += emo_neglect * 10 + (100 - c) * 0.5 + (100 - g) * 0.3
        elif "Hyper-Independence" in pattern["name"]:
            strength += ace * 7 + emo_neglect * 7 + (100 - c) * 0.5
        elif "Guilt-Shame Spiral" in pattern["name"]:
            strength += emo_neglect * 9 + phys_abuse * 6 + (100 - g) * 0.5
        elif "Catastrophizing Habit" in pattern["name"]:
            strength += ace * 8 + phys_abuse * 6 + (100 - v) * 0.5
        elif "Chronic Self-Doubt" in pattern["name"]:
            strength += emo_neglect * 10 + (100 - g) * 0.6
        elif "Boundary Collapse" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - c) * 0.6
        elif "Savior Complex" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - g) * 0.5 + (100 - c) * 0.3
        elif "Impostor Syndrome" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - g) * 0.6
        elif "Rejection Sensitivity" in pattern["name"]:
            strength += ace * 7 + emo_neglect * 5 + (100 - c) * 0.6
        elif "Control Obsession" in pattern["name"]:
            strength += ace * 8 + (100 - s) * 0.6
        elif "Numbness / Dissociation Loop" in pattern["name"]:
            strength += phys_abuse * 10 + emo_neglect * 7 + (100 - v) * 0.6
        elif "Approval Addiction" in pattern["name"]:
            strength += emo_neglect * 9 + (100 - c) * 0.5
        elif "Chronic Over-Responsibility" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - g) * 0.5
        elif "Self-Sabotage Pattern" in pattern["name"]:
            strength += ace * 6 + phys_abuse * 8 + (100 - g) * 0.6
        elif "Existential Emptiness" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - m) * 0.7
        elif "Fear of Success" in pattern["name"]:
            strength += ace * 6 + (100 - g) * 0.6
        elif "Fear of Rejection" in pattern["name"]:
            strength += ace * 7 + (100 - c) * 0.6
        elif "Fear of Making Wrong Decision" in pattern["name"]:
            strength += phys_abuse * 8 + (100 - g) * 0.6
        elif "Fear of Other People's Opinions" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - c) * 0.5
        elif "Fear of Responsibility" in pattern["name"]:
            strength += emo_neglect * 6 + (100 - s) * 0.6
        elif "Fear of Commitment" in pattern["name"]:
            strength += ace * 7 + (100 - s) * 0.6
        elif "Fear of Unknown/Change" in pattern["name"]:
            strength += ace * 8 + (100 - g) * 0.5
        elif "Fear of Vulnerability" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - c) * 0.6
        elif "Fear of Conflict" in pattern["name"]:
            strength += phys_abuse * 7 + (100 - c) * 0.5
        elif "Procrastination" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - g) * 0.6
        elif "Negative Self-Talk" in pattern["name"]:
            strength += emo_neglect * 9 + (100 - v) * 0.5
        elif "Blaming Others/Circumstances" in pattern["name"]:
            strength += emo_neglect * 6 + (100 - g) * 0.5
        elif "Lack of Prioritization" in pattern["name"]:
            strength += emo_neglect * 5 + (100 - g) * 0.5
        elif "Mindless Consumption/Distraction" in pattern["name"]:
            strength += emo_neglect * 6 + (100 - v) * 0.5
        elif "Overcommitment (FOMO)" in pattern["name"]:
            strength += emo_neglect * 5 + (100 - s) * 0.5
        elif "Self-Isolation" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - c) * 0.5
        elif "Ignoring Personal Needs" in pattern["name"]:
            strength += emo_neglect * 8 + (100 - v) * 0.5
        elif "All-or-Nothing Thinking" in pattern["name"]:
            strength += emo_neglect * 6 + (100 - g) * 0.5
        elif "Living in the Past/Ruminating" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - m) * 0.5
        elif "Focusing on What is Lacking" in pattern["name"]:
            strength += fin * 8 + (100 - s) * 0.5
        elif "Waiting for Perfect Time" in pattern["name"]:
            strength += emo_neglect * 6 + (100 - g) * 0.5
        elif "Comparison Trap" in pattern["name"]:
            strength += emo_neglect * 7 + (100 - g) * 0.5
        elif "Scarcity / Deprivation Loop" in pattern["name"]:
            strength = 40 + fin*10 + (100 - s)*0.6 + (100 - v)*0.4
        elif "Good-Girl / Good-Boy Syndrome" in pattern["name"]:
            strength = 40 + emo*10 + (100 - c)*0.5 + (100 - g)*0.3
        elif "Frozen Grief / Uncried Tears" in pattern["name"]:
            strength = 40 + emo*8 + phys*5 + (100 - v)*0.6 + (100 - m)*0.4

        strength = min(100, strength)
        if strength > 40:
            affected = [el for el, sc in scores.items() if sc < 65]
            candidates.append({
                "name": pat["name"],
                "root": pat["root"],
                "symptom": pat["symptom"],
                "action": pat["action"],
                "strength": strength,
                "affected_elements": affected or ["None – minimal impact"]
            })

    return sorted(candidates, key=lambda x: x["strength"], reverse=True)[:3] or [{"name": "No major recursion detected", "root": "", "symptom": "", "action": "", "strength": 0, "affected_elements": []}]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.get_json()
    if len(data) < 70:
        return jsonify({"error": "Please answer all 70 questions."}), 400
    scores = calculate_element_scores(data)
    recursions = detect_recursions(data, scores)
    avg = sum(r["strength"] for r in recursions) / max(1, len(recursions))
    return jsonify({"scores": scores, "recursions": recursions, "avg_recursion": avg})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Latent Recursion System</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
  <style>
    .tree {{ transition: all 1.5s ease; }}
    .ring {{ transition: all 1.5s ease; }}
    input[type="radio"]:checked + span {{
      color: #22c55e;  /* Green for selected option */
    }}
  </style>
</head>
<body class="bg-gradient-to-br from-slate-950 to-slate-900 text-white min-h-screen">
  <div class="container mx-auto p-6 max-w-5xl">
    <h1 class="text-5xl font-bold text-center text-teal-400 mt-8 mb-2">Latent Recursion System</h1>
    <p class="text-center text-gray-300 mb-12 text-xl">Discover hidden patterns from your past that keep you stuck today.</p>
    <div class="text-center mb-12">
      <div class="w-full bg-gray-800 rounded-full h-3">
        <div id="progress" class="bg-teal-500 h-3 rounded-full transition-all duration-1000" style="width:0%"></div>
      </div>
      <p class="mt-4 text-gray-400" id="progress-text">0/70</p>
    </div>
    <div id="assessment" class="space-y-12"></div>
    <div id="biome-container" class="my-16 text-center hidden">
      <h2 class="text-3xl font-bold mb-8">Your Personal Biome</h2>
      <canvas id="biome" width="600" height="600" class="mx-auto border-4 border-teal-600 rounded-2xl shadow-2xl"></canvas>
    </div>
    <div id="results" class="hidden mt-12 p-8 bg-slate-800 rounded-2xl shadow-2xl space-y-8"></div>
  </div>
  <script>
    const questions = {json.dumps(questions)};
    const order = {json.dumps(element_order)};
    let responses = {{}}, current = 0;
    let scene, camera, renderer, trees = [], ring, userFigure, currents = [];

    function initBiome() {{
      const canvas = document.getElementById('biome');
      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0f172a);
      camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
      renderer = new THREE.WebGLRenderer({{canvas, antialias: true}});
      renderer.setSize(600, 600);
      // Central Individual
      const geo = new THREE.DodecahedronGeometry(0.5, 0);
      const mat = new THREE.MeshBasicMaterial({{color: 0x00ffaa, wireframe: true}});
      userFigure = new THREE.Mesh(geo, mat);
      userFigure.position.y = 0.5;
      scene.add(userFigure);
      // Undercurrent Ring
      const ringGeo = new THREE.TorusGeometry(4, 0.15, 16, 100);
      const ringMat = new THREE.MeshBasicMaterial({{color: 0xff0066}});
      ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2;
      scene.add(ring);
      camera.position.z = 10;
      animate();
    }}
    function animate() {{
      requestAnimationFrame(animate);
      ring.rotation.z += 0.01;
      userFigure.rotation.y += 0.01;
      renderer.render(scene, camera);
    }}
    function updateBiome(scores, avg_recursion, affected) {{
      trees.forEach(t => scene.remove(t));
      trees = [];
      currents.forEach(c => scene.remove(c));
      currents = [];
      const config = [
        {{el: 'Vitality', x: -3.5, color: 0x00ff88, title: "Vitality Tree"}},
        {{el: 'Connection', x: -1.8, color: 0x4488ff, title: "Connection Tree"}},
        {{el: 'Environment', x: 0, color: 0xffaa00, title: "Environment Tree"}},
        {{el: 'Growth', x: 1.8, color: 0xff00ff, title: "Growth Tree"}},
        {{el: 'Stability', x: 3.5, color: 0xffff00, title: "Stability Tree"}},
        {{el: 'Meaning', x: 3.5, color: 0xff0088, title: "Meaning Tree"}}
      ];
      config.forEach(c => {{
        const h = (scores[c.el] || 50) / 100 * 4 + 0.5;
        const geo = new THREE.CylinderGeometry(0.4, 0.6, h, 8);
        const mat = new THREE.MeshBasicMaterial({{color: c.color}});
        const tree = new THREE.Mesh(geo, mat);
        tree.position.set(c.x, h/2, 0);
        scene.add(tree);
        trees.push(tree);
        // Title
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 256; canvas.height = 64;
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 24px Arial';
        ctx.fillText(c.title, 10, 40);
        const texture = new THREE.CanvasTexture(canvas);
        const sprite = new THREE.Sprite(new THREE.SpriteMaterial({{map: texture}}));
        sprite.position.set(c.x, h + 1, 0);
        sprite.scale.set(3, 0.75, 1);
        scene.add(sprite);
        // Red current if affected
        if (affected.includes(c.el)) {{
          const currentGeo = new THREE.CylinderGeometry(0.1, 0.1, 4, 8);
          const currentMat = new THREE.MeshBasicMaterial({{color: 0xff0000}});
          const current = new THREE.Mesh(currentGeo, currentMat);
          current.position.set(c.x, 0, 0);
          scene.add(current);
          currents.push(current);
        }}
      }});
      const constriction = avg_recursion / 100;
      ring.scale.set(1 + constriction, 1 + constriction, 1);
      ring.material.color.setHex(constriction > 0.5 ? 0xff0000 : 0x00ff66);
    }}

    // === ASSESSMENT FLOW ===
    function loadElement() {{
      const el = elements[currentElement];
      const qs = element_groups[el];
      const container = document.getElementById('assessment');
      container.innerHTML = `<h2 class="text-3xl font-bold text-teal-400 mb-8">${el}</h2>`;
      qs.forEach(q => {{
        const div = document.createElement('div');
        div.className = 'bg-slate-800 p-5 rounded-xl mb-4';
        div.innerHTML = `<p class="font-medium mb-3">${q.id}. ${q.text}</p>`;
        const optsDiv = document.createElement('div');
        optsDiv.className = 'grid grid-cols-1 md:grid-cols-5 gap-3';
        q.options.forEach((opt, i) => {{
          const label = document.createElement('label');
          label.className = 'flex items-center p-3 bg-slate-700 rounded hover:bg-teal-600 cursor-pointer transition';
          label.innerHTML = `
            <input type="radio" name="q${q.id}" value="${opt}" class="mr-3">
            <span>${opt}</span>
          `;
          optsDiv.appendChild(label);
        }});
        div.appendChild(optsDiv);
        container.appendChild(div);
      }});
      const nextBtn = document.createElement('button');
      nextBtn.textContent = currentElement < 6 ? 'Next Element →' : 'See My Results';
      nextBtn.className = 'w-full p-5 bg-teal-600 hover:bg-teal-500 rounded-xl font-bold text-xl mt-8';
      nextBtn.onclick = () => {{
        qs.forEach(q => {{
          const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
          if (selected) responses[q.id] = selected.value;
        }});
        currentElement++;
        if (currentElement < 7) loadElement();
        else submit();
      }};
      container.appendChild(nextBtn);
      document.getElementById('progress-text').innerText = `${el} – ${Object.keys(responses).length}/70`;
    }}
    function submit() {{
      if (Object.keys(responses).length < 70) {{
        alert("Please answer all 70 questions for accurate results.");
        return;
      }}
      fetch('/assess', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify(responses)
      }})
      .then(r => r.json())
      .then(data => {{
        document.getElementById('assessment').classList.add('hidden');
        document.getElementById('biome-container').classList.remove('hidden');
        updateBiome(data.scores, data.avg_recursion);
        let html = `<h2 class="text-4xl font-bold text-center text-teal-400 mb-8">Your Top 3 Latent Recursions</h2>`;
        if (data.recursions[0].strength === 0) {{
          html += `<p class="
```
