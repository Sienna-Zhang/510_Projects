# Week 1 Lab Manual: Welcome to Agentic Coding

## Table of Contents

- [Learning Objectives](#learning-objectives)
- [Component A: Staff Interview](#component-a-staff-interview)
- [Component B: Lab](#component-b-lab)
- [Component C: System Architecture & Design](#component-c-system-architecture--design)
- [Component D: Testing & Validation](#component-d-testing--validation)
- [Component E: Applied Challenge — The GIX Wayfinder](#component-e-applied-challenge--the-gix-wayfinder)
- [Troubleshooting Matrix](#troubleshooting-matrix)
- [Submission](#submission)

---

## Learning Objectives

By the end of this lab, you will be able to:

1. **Set up a development environment** including Git, Python, and Cursor
2. **Conduct a structured user interview** and synthesize findings into a problem statement
3. **Use agentic coding to build a web application** by writing natural language prompts in Cursor's Composer mode
4. **Read and modify AI-generated code** by identifying what a function does and making a deliberate change by hand
5. **Articulate the difference between generating code and understanding code**
6. **Sketch a system diagram** showing how your app's components connect (user input, Streamlit, Python logic, data) using boxes and arrows
7. **Verify that your app produces correct output** by manually testing 2 edge cases (e.g., empty input, unexpected characters) and documenting the results


---

## Component A: Staff Interview

> Before building your first app, you will listen to a GIX staff member describe a genuine problem. 

### Guest

**Dorothy, Program Coordinator** — Student Purchasing

### Focus

Dorothy manages purchase requests for GIX programs. Her pain point: finding an easier, user-friendly way to submit and track purchase requests so she can easily see who submitted what, what they want to order, and from which class. 

### Format

Class discuss and synthesize interview questions collectively. These questions should aim to solicitate information from staff member to inform how your solution might look like.
**Every student takes their own individual notes.**

### During the Interview

As you listen, capture:

- **Direct quotes** -- write down 1-2 exact phrases the Coordinator uses
- **Surprises** -- what did you not expect to hear?
- **Current workarounds** -- how is the problem being handled today (spreadsheets, email, memory, signs)?
- **What success looks like** -- in the interviewee's own words

> **Observe the User Journey:** As the staff member describes their current process, trace the steps they follow from start to finish. Write down each action in order, as if you were drawing a timeline. For example:
>
> 1. New student emails the Coordinator asking about room booking
> 2. Coordinator opens their inbox, reads the email
> 3. Coordinator opens the room booking spreadsheet
> 4. Coordinator looks up availability
> 5. Coordinator replies with instructions
> 6. Student follows instructions (or asks a follow-up question)
>
> For each step, note if possible/applicable:
> - **How long does this step take?** (seconds, minutes, hours, days)
> - **Where does the information live?** (email, spreadsheet, someone's memory, a sign on a wall)
> - **What could go wrong at this step?** (lost email, outdated spreadsheet, staff member is out sick)
>
> This user journey map will help you identify which steps your app should address and which are out of scope.

### Synthesis Artifact: Problem Statement

After the interview, write one sentence in this format:

> "When **[people]** needs to **[task]**, they currently **[workaround]**, which causes **[pain]**."

**Example:** "When a new GIX student needs to find out how to book a meeting room, they currently ask the Facilities Coordinator by email, which causes a 1-2 day delay and adds to the Coordinator's inbox load."

### Your Task

Your problem statement becomes the subject of the app you build in Component B. 

### Deliverable

- Individual interview notes (and the class question list if you captured it)
- One problem statement in the format above

---

## Component B: Lab

### Warm-up — Level 1: Tool Awareness

**Agentic Coding Kickoff:** Before opening Cursor, try this quick experiment.

1. Think of a simple app idea (e.g., "a checklist for new students at GIX")
2. Describe it in one paragraph of plain English
3. Paste that paragraph into [ChatGPT](https://chat.openai.com) or [Claude](https://claude.ai), or other LLMs of your choice, and ask it to generate the code
4. Now keep that same paragraph ready (you will paste it into Cursor Composer shortly)

**Compare:** Which response felt more "buildable": A chatbot gives you code in a text window, or Cursor writes files directly into your project?

---

### Level 1: Environment Setup

This section walks you through installing every tool you need. If you already have a tool installed, skip to the verification step.

#### Step 1.1: Install Git

Git is a version control system. Think of it as "Track Changes" for code -- it records every change you make so you can go back in time and maintain a clean history of your work.

**macOS:**
Open the Terminal app (search "Terminal" in Spotlight) and type:

```bash
git --version
```

If Git is installed, you will see a version number like `git version 2.43.0`. You are done with this step.

If it is not installed, macOS will prompt you to install the Command Line Developer Tools. Click "Install" and wait for it to finish (this may take a few minutes). Then run `git --version` again to confirm.

**Windows:**
Download Git from [https://git-scm.com/download/win](https://git-scm.com/download/win). Run the installer and accept all default settings. Once installed, open "Git Bash" from your Start menu and type:

```bash
git --version
```

You should see a version number. Keep Git Bash open -- you will use it throughout this lab.

**Verification:** Running `git --version` prints a version number (2.30 or higher is fine).

#### Step 1.2: Create a GitHub Account

GitHub is a website that hosts your Git projects online. You will use it to store and share all your coursework. If you already have a GitHub account, skip this step.

1. Go to [https://github.com](https://github.com)
2. Click "Sign up" and follow the prompts
3. Choose a professional username -- this will be on your resume
4. Verify your email address

#### Step 1.3: Install Python 3.11+

Python is the programming language we use for the first half of this course. Streamlit, the web app framework we start with, is a Python library.

**macOS:**

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest stable Python release
3. Run the installer. **Important:** Check the box that says "Add Python to PATH" if you see it.

Verify by opening Terminal and typing:

```bash
python3 --version
```

**Windows:**

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest stable Python release
3. Run the installer. **Important:** Check the box that says "Add python.exe to PATH" at the bottom of the first installer screen. Then click "Install Now."

Verify by opening Git Bash (or Command Prompt) and typing:

```bash
python --version
```

If that does not work, try `python3 --version`.

#### Step 1.4: Install Cursor

Cursor is an AI-native code editor. It looks and feels like VS Code (a popular editor), and it has built-in AI capabilities that let you generate, edit, and understand code through natural language conversation.

1. Go to [https://cursor.com](https://cursor.com)
2. Download the installer for your operating system
3. Run the installer
4. Open Cursor. It will ask you to sign in or create an account -- do so.
5. When prompted, you can import VS Code settings if you already use VS Code. Otherwise, accept the defaults.

> **Pro tip:** Cursor's free tier gives you a limited number of AI requests per month. This is enough for this lab. If you want unlimited requests, the Pro plan is $20/month. Your student account may provide you one year of access to the Pro plan for free.

#### Step 1.5: Set Up a Virtual Environment and Install Streamlit

Open your terminal (Terminal on macOS, Git Bash on Windows) and run:

```bash
# Navigate to your project folder first (this is just an example, use the path on your device!)
mkdir -p ~/Documents/techin510
cd ~/Documents/techin510

# Create a virtual environment
python3 -m venv .venv

# Activate it (macOS / Linux)
source .venv/bin/activate

# Activate it (Windows PowerShell)
# .venv\Scripts\Activate.ps1

# Activate it (Windows Command Prompt / Git Bash)
# .venv\Scripts\activate.bat
```

You should see `(.venv)` at the beginning of your terminal prompt. This means the virtual environment is active.

After creating the virtual environment, your project folder looks like this:

```
techin510/
├── .venv/          ← Created by python3 -m venv (do NOT edit files inside here)
│   ├── bin/        ← Contains the activate script and installed commands
│   ├── lib/        ← Where pip installs packages (e.g., streamlit)
│   └── ...
└── (your project files will go here)
```

Now install Streamlit inside the virtual environment:

```bash
pip install streamlit
```

If that does not work, try:

```bash
pip3 install streamlit
```

Verify the installation:

```bash
streamlit --version
```

**Verification:** Running `streamlit --version` prints a version number (1.30 or higher). You see `(.venv)` in your terminal prompt.

> **Important:** Every time you open a new terminal window to work on this project, you must activate the virtual environment first: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate.bat` (Windows). If you forget, `streamlit` will not be found.

---

### Level 2: Build Your First Streamlit App with Cursor

You will use Cursor's AI capabilities to build a working web application that addresses the problem you identified in Component A.

#### Step 2.1: Create a New Project Folder

In your terminal, create a folder for your app and activate your virtual environment:

```bash
# Create this week's project folder. This is just an example, use your path instead!
mkdir -p ~/Documents/techin510/my-first-app
cd ~/Documents/techin510/my-first-app

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS / Linux
# .venv\Scripts\activate.bat  # Windows

# Create a requirements file so anyone can reproduce your setup
echo "streamlit>=1.30.0" > requirements.txt
pip install -r requirements.txt
```

Also create a `.gitignore` file to keep secrets and environment files out of GitHub:

```bash
echo -e ".venv/\n__pycache__/\n.env\n.streamlit/secrets.toml" > .gitignore
```

Open this folder in Cursor

#### Step 2.2: Open Cursor

Cursor has several AI modes. For building a new app from scratch, we use **Agent** (also called Agent mode):

- Open the Composer panel
- You should see a text input where you can type a prompt

#### Step 2.3: Write Your First Prompt

Your prompt should describe an app that addresses the onboarding problem from your interview. Use your problem statement as a starting point.

> **Before you type:** Take time to answer this question: *"Who would use this app, and for what?"* Write one sentence. For example: "A new GIX student who needs to find facility information without emailing the Coordinator." 

Here is an example:

```
Build a Streamlit app called "GIX New Student Guide" that helps incoming students find answers to common onboarding questions. Organize information into categories (e.g., Facilities, Equipment, Room Booking, Printing, Parking). Include a search bar that filters questions and answers as the user types. Use a clean, simple layout. Populate it with 10-15 sample FAQ entries based on common new-student questions.
```

**Adapt this prompt to match YOUR interview findings.** If the interviewee mentioned specific pain points (e.g., room booking confusion, equipment checkout process), make those the focus of your app. Work with your agent to solve the problem in Component A.

Press Enter (or click the send button) to submit your prompt.

#### Step 2.4: Watch and Review

Cursor will generate code for your app. Watch what happens:

- It may create one or more Python files
- It may ask clarifying questions (answer them if possible)
- It will show you the code it is writing

When Cursor finishes generating, **do not accept blindly.** Review the generated code. You do not need to understand every line yet, but notice the overall structure. 
During your code review, ask your AI agent to explain some unclear parts for you.

Click "Accept" (or "Apply") to save the generated code.

#### Step 2.5: Run Your App

Open the terminal inside Cursor (go to **View > Terminal**) and type:

```bash
streamlit run app.py
```

(Replace `app.py` with whatever filename Cursor created. It is usually `app.py` or `main.py`.) If you do not know how to run the app, simply ask your agent!

Your default web browser should open with your app running. You should see an interactive web page with the features you described.

**What success looks like:** A Streamlit app opens in your browser. You can interact with it -- search, click, see content update.

> **If the app does not run or shows an error:** Copy the error message, go back to agent, paste the error, and ask: "I got this error when running the app. Please fix it." This is a normal part of the agentic coding workflow. 

---

### Level 3: Add a Feature

Now that your app works, use Cursor to iterate on it. Open agent again (`Cmd+I`) and add a feature that makes the app more useful. Here are some example ideas:

- "Add a sidebar where users can select a category to filter the FAQ entries"
- "Add a 'Was this helpful?' button below each answer that tracks feedback"
- "Add a contact card at the bottom with the Facilities Coordinator's office hours and email"
- "Add a dark mode toggle to the sidebar"

Accept the changes if you like them and re-run the app (Streamlit usually auto-reloads, but if not, stop with `Ctrl+C` and restart with `streamlit run app.py`).

**Log your AI interactions.** For each prompt you give Cursor, write down:

1. What you asked for (the prompt)
2. What Cursor produced (brief description)
3. Whether it worked on the first try, or what you had to fix

You will submit this log as part of your deliverables.

---

### Accessibility Baseline Check

Before moving on, run two quick checks on your Streamlit app. 

**Check 1: Color Contrast**

**What is color contrast?** It is the difference in brightness between text and its background. Low contrast (light gray text on a white background) is hard to read for many users, not just those with vision impairments. The WCAG (Web Content Accessibility Guidelines) standard recommends a contrast ratio of at least 4.5:1 for normal text.

1. Open your running Streamlit app in the browser
2. Right-click on any text in your app and select "Inspect" (or press F12)
3. In the DevTools panel, look at the "Styles" tab for the text color and background color
4. Copy both colors (e.g., `#333333` and `#FFFFFF`) and paste them into the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
5. Does the ratio pass at least 4.5:1? If not, note which text fails

If you used Streamlit's default theme, your contrast likely passes. If you customized colors in Level 5, double-check those custom colors.

**Check 2: Semantic Headings**

**What are semantic headings?** Headings communicate the structure of your page -- like a table of contents. Screen readers (software used by visually impaired users) use headings to navigate a page. In Streamlit:

- `st.title()` produces an `<h1>` heading -- use it once per page for the main title
- `st.header()` produces an `<h2>` heading -- use it for major sections
- `st.subheader()` produces an `<h3>` heading -- use it for subsections
- `st.write()` or `st.markdown()` produces plain paragraph text -- do NOT use it for section titles

Review your `app.py` and confirm:
- [ ] You have exactly one `st.title()` at the top of your app
- [ ] Section headings use `st.header()` or `st.subheader()`, not `st.write("## My Section")`
- [ ] Headings follow a logical order (you do not skip from `st.title()` directly to `st.subheader()` without a `st.header()` in between)

**Why this matters:** Using proper heading functions instead of manual markdown formatting ensures that your page structure is accessible to all users and is correctly interpreted by assistive technologies. It also improves the visual consistency of your app.

**Record your results.** Note whether your app passed both checks. If something failed, fix it now.

---

### Level 4: Understand and Modify Code

Generating code with AI is powerful, but it is only half the skill. The other half is understanding what was generated.

#### Step 4.1: Pick a Function or Component

Look at your generated code. Find one specific section that interests you. Good candidates:

- A function that filters or searches data
- A section that creates the user interface layout
- The part that handles user input (text boxes, dropdowns, buttons)

#### Step 4.2: Ask Cursor to Explain It

Select (highlight) the code you picked. Then:

1. Open Cursor Chat
2. Type: "Explain this code to me line by line. I am a beginner."

Read the explanation carefully. Does it make sense? If something is unclear, ask a follow-up question in the same chat.

Now close the Chat panel and try to explain the code in your own words. **The goal is not to memorize code. This is to build a mental model of what the code does and why.**

#### Step 4.3: Make a Change by Hand

Without using AI, make a small deliberate change to the code. Ideas:

- Change a text label (e.g., change "Search" to "Find an answer")
- Change the number of columns in a layout
- Add a new FAQ entry to the data by hand
- Add a new line of text using `st.write("Your text here")`

Save the file and check that the app still works. If it breaks, read the error message and try to fix it yourself first. If you are stuck, ask Cursor Chat for help.

#### Step 4.4: Write an Explanation Comment

At the top of your main Python file, write a comment in your own words describing what the code does. For example:

```python
# This app is a GIX New Student Guide built with Streamlit.
# It organizes onboarding FAQs into categories and lets users
# search for answers instead of emailing the Facilities Coordinator.
# I manually changed the search label from "Search" to "Find an answer."
```

---

### Level 5: Stretch Goals

Implement one of these challenges. Each has a specific goal and a checkpoint so you know when you are done.

**Add a Second Page**
- **Goal:** Use `st.sidebar` and `st.radio` to create a navigation that switches between your main app and a new "About" page.
- **Guiding prompt for Cursor:** "Add a sidebar with a radio button that lets the user switch between 'Home' and 'About' pages. The About page should show a description of the project and a link to the GIX website."
- **Checkpoint:** You can click between pages using the sidebar, and each page shows different content.
- **Hint:** If `st.sidebar` or `st.radio` are new to you, search the [Streamlit docs](https://docs.streamlit.io) for each component. Reading the docs is a normal part of development.

**Style with Themes**
- **Goal:** Add a `.streamlit/config.toml` file to customize the look of your app (colors, fonts).
- **Guiding prompt for Cursor:** "Create a Streamlit config.toml file that changes the primary color to blue and uses a sans-serif font."
- **Checkpoint:** Your app uses the custom theme when you reload the page.
- **Hint:** See the [Streamlit theming docs](https://docs.streamlit.io/develop/concepts/configuration/theming) for the available options.

---

### Push to GitHub

Before you finish, push your project to a GitHub repository. Make sure your README contains clear information about your project along with instructions on how to reproduce all results.

---

## Component C: System Architecture & Design



### Architecture Concept: What Is a System?

#### The Big Idea

Every application is a **system**. A system is anything that takes input, processes it, and produces output. 
In today's lab, you built a Streamlit app from an interview finding. That app has a clear Input-Process-Output structure:

- **Input:** The user interacts with your app (searches, clicks, types)
- **Process:** Your Python code filters data, formats text, or makes decisions
- **Output:** Streamlit displays the result in the browser

Understanding this structure helps you communicate with AI tools more effectively. When your prompt says "build an app that shows FAQ entries filtered by category," you are describing all three layers: the input (category selection), the process (filtering), and the output (filtered list).

---

### Diagramming Exercise: Draw I/P/O for Your Streamlit App

#### Instructions

Draw an Input-Process-Output diagram for the Streamlit app you built today. You can draw this on paper, on a whiteboard, or digitally.

#### Step-by-Step

1. **Draw three boxes** in a row, connected by arrows pointing left to right.
2. **Label the boxes** "Input," "Process," and "Output."
3. **Fill in each box** with specifics from YOUR app:
   - **Input box:** List every way a user provides information to your app (search text, button clicks, dropdown selections, etc.)
   - **Process box:** List what your Python code does with that input (filters a list, looks up a match, formats data, etc.)
   - **Output box:** List what the user sees as a result (filtered FAQ list, a message, a chart, etc.)
4. **Add one arrow from Output back to Input** (a feedback loop) -- label it with what the user does after seeing the output (e.g., "refines search," "clicks another category").


#### What to Include

- Every user interaction that feeds into the app (inputs)
- The core logic your Python code performs (process)
- Everything the user sees as a result (outputs)
- At least one feedback arrow showing how output leads to new input

---

### Design Decision Log

#### The Template

Every week, you will record one design decision using this template. This builds the habit of thinking about trade-offs: the core of architectural thinking.

| Field | Your Entry |
|-------|------------|
| **Decision** | What did you decide? |
| **Alternatives considered** | What else could you have done? |
| **Why you chose this** | What constraint drove it? |
| **Trade-off** | What did you give up? |
| **When would you choose differently?** | Under what conditions? |

#### Respond to the Decision Prompt

> **"Why did you put everything in one file (app.py) instead of splitting it into multiple files?"**

If you DID split into multiple files, flip the question: why did you choose to split?

Think about:
- How many lines of code does your app have? At what point does a single file become hard to navigate?
- What would change if you needed to add five more features next week?
- What did the AI tool (Cursor) produce -- one file or many? Did you accept that structure, or did you change it?
---

## Component D: Testing & Validation


### Validation Exercise: Smoke Test

A **smoke test** is the simplest form of testing: you turn the thing on and check whether smoke comes out. 

In software, a smoke test answers one question: **does the application start up and perform its most basic functions without crashing?** It is not thorough. It is not detailed. It is the absolute minimum bar -- and it is the first thing professional teams run after every code change.


#### Why this matters

- Every deployed application in the software industry goes through smoke testing before it reaches users
- Smoke tests are fast and catch the most catastrophic problems early
- Even apps built entirely by AI can fail smoke tests -- the AI might generate code that looks correct but crashes on startup due to a missing import or a typo in a variable name

#### Instructions

You just built your first Streamlit app in Component B. Now you will systematically verify that it works and document exactly what you tested and what happened. Casually clicking here and there does not count as valid tests.

**Step 1: Start your app** (if it is not already running)

```bash
streamlit run app.py
```

Confirm the app opens in your browser without any error messages in the terminal or on the page.

**Step 2: Identify 3 features to test**

Look at your app and pick 3 distinct features. A "feature" is anything the user can interact with or see. Examples:

- A search bar that filters results
- A sidebar with category selection
- A button that triggers an action
- A data table that displays information
- A metric card showing a number

**Step 3: Test each feature and record the results**

For each feature, perform a specific action and write down what happened. Use the recording template below.

#### Recording Template

Copy this table into your submission document and fill it in:

| # | Feature Tested | Action You Took | Expected Result | Actual Result | Pass/Fail |
|---|---------------|-----------------|-----------------|---------------|-----------|
| 1 | _e.g., Search bar_ | _Typed "room booking"_ | _Shows only FAQ entries about room booking_ | _Showed 2 matching entries_ | _Pass_ |
| 2 | _e.g., Category filter_ | _Selected "Facilities" from sidebar_ | _Shows only Facilities entries_ | _All entries still visible (filter not working)_ | _Fail_ |
| 3 | _e.g., Page title_ | _Loaded the app_ | _Title says "GIX Student Guide"_ | _Title says "GIX Student Guide"_ | _Pass_ |

**Step 4: Take a screenshot**

Take a screenshot of your running app that shows at least one of the features you tested. This screenshot is part of your submission.

**Step 5: Fix any failures**

If any feature failed the smoke test, try to fix it. Paste the error or unexpected behavior into Cursor and ask for help. If you fix it, re-test and update your table.

#### Quality Gate Checklist

Use this checklist before submission:

- [ ] Smoke test table completed with 3 tested features
- [ ] Any failed test is either fixed and re-tested, or clearly documented
- [ ] Screenshot of the running app included
- [ ] Accessibility baseline results recorded (color contrast + semantic headings)


---

## Component E: Applied Challenge — The GIX Wayfinder

### The Problem

New GIX students can't find campus resources — the makerspace, bike storage, free printing, quiet study nooks. No single digital resource exists; students rely on word of mouth and outdated PDFs. Build a wayfinding prototype that solves this.

> This component is required and part of your Week 1 submission.

### What You Build

- A Streamlit app with a set of campus resources stored in a data structure you design
- Search and filtering functionality
- A display showing matching resources with relevant details
- An I/P/O (Input/Process/Output) architecture diagram (hand-drawn is fine)

### Part 1: Architecture & Design

Draw an **I/P/O diagram** for your app. For each section (Input, Process, Output), describe what happens and what data flows through.

Label your data source and draw an arrow showing data flow from source → processing logic → UI.

### Part 2: Implementation

Build your Streamlit app:
- Design a data structure for GIX campus resources — decide what fields each resource needs
- Implement search and filtering using appropriate Streamlit components
- Display results in a clear, usable format
- Consider what happens when no results match the user's query

### Part 3: Testing & Validation

1. **Edge cases:** Document 2 edge cases you identified and tested. Explain why each is an important case to handle.
2. **Assert statement:** Write 1 `assert` statement verifying your data integrity
3. **Prompt log:** Copy your initial AI prompt and one refinement you made to it. Explain what changed and why.

---

## Troubleshooting Matrix

### Python Installation Issues

**"python is not recognized as a command" (Windows):**
Python was not added to your system PATH during installation. The easiest fix: re-run the Python installer, and this time check the "Add python.exe to PATH" box. Alternatively, try using `py` instead of `python`.

**"pip is not recognized":**
Try `pip3` instead of `pip`. If that does not work either, run: `python -m pip install streamlit` (or `python3 -m pip install streamlit`).

**Multiple Python versions installed:**
If `python --version` shows Python 2.x, use `python3` and `pip3` for all commands in this course.

### Cursor Issues

**Cursor is not generating code:**
Make sure you are signed in to Cursor (check the bottom-left corner). The free tier has a limited number of requests -- if you have hit the limit, try again in a few minutes or upgrade to Pro.

**Cursor is slow or unresponsive:**
Close other heavy applications. Cursor's AI features require an internet connection -- check your wifi. Try closing and reopening Cursor.

**"Model not available" or similar error:**
Cursor periodically updates its available models. If you see this error, try selecting a different model from the model dropdown in the Composer panel.

### Streamlit Issues

**"streamlit: command not found":**
Streamlit may not be on your PATH. Try running: `python -m streamlit run app.py` (or `python3 -m streamlit run app.py`).

**App opens but shows an error:**
Read the error message in the terminal and in the browser. Common issues:
- **ModuleNotFoundError:** A library is missing. Install it with `pip install <library_name>`.
- **SyntaxError:** There is a typo in the code. Look at the line number in the error, find that line in your code, and check for missing colons, parentheses, or quotation marks.
- **IndentationError:** Python is sensitive to spacing. Make sure code inside functions and `if` blocks is indented consistently (use 4 spaces).

Copy the full error message and paste it into Cursor Composer with the prompt: "I got this error. Please fix it." This is the standard agentic debugging workflow.

### Git and GitHub Issues

**"Permission denied" when pushing to GitHub:**
You need to authenticate. The most common fix: set up a personal access token or configure SSH keys. Ask a TA for help if you are stuck.

**"fatal: not a git repository":**
You are in the wrong folder. Make sure you `cd` into your project folder before running Git commands. Run `pwd` to see what folder you are in.

**"Updates were rejected because the remote contains work...":**
This means GitHub has changes you do not have locally. Run `git pull` first, then try `git push` again. If you just created the repo and this happens, you may have accidentally initialized it with a README on GitHub. The simplest fix: delete the GitHub repo, recreate it without a README, and push again.

**Merge conflict:**
For now, do not worry about this. If you see a merge conflict message, ask a TA. We will cover conflict resolution in a later week.

---

## Submission

All deliverables are **individual**. Submit your Github link on Canvas. Your Github repo should be well organized. Results should be reproducible with clear instructions on how to run the code. Make sure your repo contains a pdf report with the following information:

Your repo must include your Streamlit source code, `requirements.txt`, and a README with clear run instructions.

### Component A Deliverables


1. **Interview notes** 
2. **Problem statement**: 1 sentence in the template 

### Component B Deliverables

1. **AI Usage Log**: Document at least 3 interactions with AI tools (include Cursor prompts from build/iteration). For each, write:
   - the prompt you gave
   - what the AI produced
   - whether it worked on the first try, and what you fixed if it did not
2. **Accessibility baseline results**: Briefly report:
   - color contrast check result (pass/fail and any fix)
   - semantic headings check result (pass/fail and any fix)

### Component C Deliverables
1. **Architecture diagram** 
2. **Design Decision Log**

### Component D Deliverables
1. **Validation results** (the completed smoke-test table)
2. **Screenshot** of your running app showing at least one tested feature
3. **Quality gate checklist** (completed)

### Component E Deliverables
1. **Wayfinder app implementation** in your repo (code and data structure)
2. **I/P/O diagram** for the Wayfinder app
3. **Edge-case validation notes** for 2 edge cases (with why they matter)
4. **One `assert` statement** for data integrity (include it in code and mention where)
5. **Prompt log excerpt**: initial prompt + one refinement, with a brief note on what changed and why

### Reflection Deliverables

Before you leave, take a few minutes to write 3-5 sentences addressing the following questions. Submit these as part of your Component B deliverables.

1. **What surprised you about AI-assisted coding?** Was it easier or harder than you expected? What moment made you think "wow" or "wait, that is not right"?

2. **What did the AI get wrong?** Did you encounter errors, unexpected behavior, or code that did not match what you asked for? How did you fix it?

3. **Could you explain your code?** Pick one section of your app -- could you walk a classmate through what it does, line by line, without looking at Cursor's explanation?

4. **What did you learn from the interview?** How did talking to Dorothy (Program Coordinator, Student Purchasing) change what you built, compared to what you might have built without that conversation?
