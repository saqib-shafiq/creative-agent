# ✦ Creative Agent — AI-Powered Marketing Studio

> A prompt-chaining AI agent that transforms product briefs into campaign narratives using OpenAI's GPT-4o-mini. Features strategic analysis, copywriting, and bilingual support (English/Arabic).

## Architecture

The agent uses a **sequential prompt-chaining architecture** with two specialized agents:

| Agent | Role | Output |
|-------|------|--------|
| **Strategist** | Analyzes product brief and extracts strategic insights | JSON with emotional tension, cultural moment, sensory hook, unspoken desire |
| **Copywriter** | Transforms strategic brief into immersive narrative ad | Structured narrative with opening hook, 2 paragraphs, closing line |


User Brief
↓
Agent 1: Strategist (GPT-4o-mini)
↓
Strategic Brief JSON
↓
Agent 2: Copywriter (GPT-4o-mini)
↓
Campaign Narrative (4-part structure)
↓
Final Output + Strategic Brief (collapsible)

## Features

- **Dual-Agent Architecture** — Strategist + Copywriter working in sequence
- **Bilingual Interface** — Toggle between English and Arabic UI instantly
- **Bilingual Output** — Generate campaigns in English or Saudi Arabic dialect
- **4-Part Narrative Structure** — Opening hook → Paragraph 1 → Paragraph 2 → Closing line
- **Dynamic Product Name** — Uses exact product name provided in closing line
- **Saudi Cultural Context** — Strategist prompts include Saudi-specific cultural moments
- **No Inline Styling** — Clean Streamlit native components only

## Output Structure

Every campaign follows this proven format:

[Opening hook - short phrase ending with "..."]
[blank line]
[Paragraph 1: 3-4 sentences describing the moment/setting]
[blank line]
[Paragraph 2: 3-4 sentences describing sensory experience]
[blank line]
[Product Name. Benefit statement.]


## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Language | Python 3.9+ |
| API | OpenAI API |

## File Structure

creative-agent/
├── app.py # Streamlit UI with language toggle
├── agent.py # AI Agent logic (Strategist + Copywriter)
├── requirements.txt # Python dependencies
└── .streamlit/
└── secrets.toml # API keys (not in repo)


## Setup & Installation

### 1. Clone the repository

git clone https://github.com/yourusername/creative-agent.git
cd creative-agent

### 2. Create virtual environment

## Windows (PowerShell):

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

## macOS/Linux:

bash
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependiencies

pip install -r requirements.txt

### 4. Set up API key

Create .streamlit/secrets.toml:

toml
OPENAI_API_KEY = "your-openai-api-key-here"

### 5. Run the app
streamlit run app.py


### Deployment on Streamlit Cloud 

1. Push code to GitHub repository
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Set main file: app.py
5. Add secret: OPENAI_API_KEY

### Environment Variables
Variable	Required	Description
OPENAI_API_KEY	Yes	Your OpenAI API key

### Example Usage
1. Toggle Language — Click 🌐 button to switch between English/Arabic UI
2. Enter Product Info — Product name, description, target audience
3. Select Brand Voice — Choose 1+ brand voice attributes (Youthful, Fun, Natural, etc.)
4. Generate Campaign — Click submit, agent chain runs automatically
5. View Results — Campaign narrative displayed with strategic brief in expandable section

### Example Input
Field	            Example
- Product Name	    Mint & Lemon
- Product Description	Natural mint and lemon drink, no sugar, refreshing
- Target Audience	    University students & young professionals, 18-30, health-conscious
- Brand Voice	        Refreshing, Natural

### Example Output (English)
Picture this...

The sun blazing down at 2 PM, you just finished work and you're exhausted. You need something to cool you down and refresh you... but you don't want the guilt that comes with sugary drinks.

You open the fridge and there it is. A cold can with water droplets, promising refreshment that hits just right. Natural, light, and nothing artificial.

Mint & Lemon. Your refreshment that lifts your mood.

### Example Output (Arabic)
يا جماعة تخيلوا معي...

الساعة ٢ الظهر، حر الرياض اللي ما يرحم، وتوك طالع من الجامعة أو الدوام ومحتار. تحتاج شي يبرد على قلبك ويصححك... بس بنفس الوقت مالك خلق السكريات والخرابيط.

تفتح الثلاجة... وتشوفه قدامك. علبة باردة، عليها قطرات موية، تعدك بالانتعاش اللي يضرب في الراس... طبيعي وخفيف.

نعناع وليمون. انتعاشك اللي يروق مزاجك.

### Key Design Decisions
Decision	                            Rationale
- Two-agent architecture	                Separates strategic thinking from creative writing for better outputs
- GPT-4o-mini	                            Cost-effective while maintaining quality for marketing copy
- Exact product name enforcement	        Ensures brand consistency in closing line
- No inline styling	                    Keeps UI clean and maintainable
- Language toggle with immediate rerun	Instant UI language switching without page reload
- Saudi dialect focus 	                Authentic Khaleeji Arabic, not formal MSA

### Troubleshooting
Language doesn't switch immediately
Click the 🌐 toggle button again — st.rerun() forces immediate refresh.

### Output has wrong product name
The enforce_structure function in agent.py automatically corrects this.

### API key errors
Ensure .streamlit/secrets.toml has correct OPENAI_API_KEY format.

### Output has broken words (arti/ficiality)
The prompt explicitly instructs the model to avoid splitting words across lines.

### License
MIT

### Author
Creative Agent Team