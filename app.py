from flask import Flask, request, render_template, redirect, session, flash
from surveys import Question, Survey, satisfaction_survey
app =Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "123@45#"


responses =[]
RESPONSES =""


@app.route('/')
def home_page():
    title =satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template("index.html", title = title, instructions = instruction)

@app.route('/start',methods = ["POST"])
def start_survey():
    session[RESPONSES] = []  
    return redirect("/questions/0")

@app.route("/questions/<int:nums>")
def questions(nums):
    if (len(responses) == len(satisfaction_survey.questions)):
          return redirect("/done")
    if (len(responses)!=nums):
        flash(f"Invalid question id: {nums}.")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[nums]
    return render_template("form.html", question =question, num = nums)

@app.route("/survey", methods=["POST"])
def submit_survey():
    resp = request.form['answer']
    responses.append(resp)
    session[RESPONSES] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/done")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/done")
def submit():
    return render_template('thank.html',resp=session[RESPONSES])    

    
