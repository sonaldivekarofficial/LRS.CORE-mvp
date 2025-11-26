from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

questions = [
    # 1-10 Vitality
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

    # 11-20 Connection
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

    # 21-30 Environment
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

    # 31-40 Growth
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

    # 41-50 Stability (hidden from UI but scored)
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

    # 51-60 Meaning
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

    # 61-76 Recursion (trauma & childhood)
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

recursions_defs = { ... }  # unchanged — full version in the final code

# ... [all functions exactly as in the previous working version with the fixed parentheses] ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
