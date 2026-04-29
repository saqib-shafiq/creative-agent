import json
import re
from openai import OpenAI

class CreativeAgent:
    """AI Agent that handles the prompt chaining for campaign generation"""
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def run_strategist(self, product_name, product_desc, target_audience, brand_voice, is_arabic_output):
        """Agent 1: Strategic Analyst - Analyzes the brief and returns strategic insights"""
        
        # Arabic prompt strategy
        if is_arabic_output:
            language_instruction = """
اكتب بالعربية فقط. استخدم اللغة العربية العامية السعودية الطبيعية (ليست الفصحى).
لا تستخدم أي كلمات إنجليزية إطلاقاً.
استخدم اسلوب تحليلي موجز.
"""
        else:
            language_instruction = "Output in English"
        
        # Englihs prompt Stregegy 
        system_prompt = f"""
You are a senior creative strategist specializing in consumer psychology and culturally relevant marketing in Saudi Arabia.

{language_instruction}

Analyze the product and return a JSON strategic brief with:
1. Core emotional tension (what struggle or desire does the target audience feel?)
2. Key Saudi cultural moment (specific time/place/situation in Saudi daily life)
3. Sensory hook (what can they see, feel, taste, smell?)
4. Unspoken desire (what do they really want but don't say?)

Output format:
{{
  "emotional_tension": "",
  "saudi_moment": "",
  "sensory_hook": "",
  "unspoken_desire": ""
}}
"""
        # Invoking ML call
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.8,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": (
                    f"Product Name: {product_name}\n"
                    f"Description: {product_desc}\n"
                    f"Target Audience: {target_audience}\n"
                    f"Brand Voice: {brand_voice}"
                )},
            ],
        )
        
        return json.loads(response.choices[0].message.content)
    
    def run_copywriter(self, strategic_brief, product_name, brand_voice, is_arabic_output):
        """Agent 2: Copywriter - Creates the campaign narrative from strategic brief"""

        # Arabic prompt copy_write         
        if is_arabic_output:
            system_prompt = f"""أنت كاتب إعلانات سعودي محترف، معروف بقدرتك على كتابة قصص حسية وواقعية بالعامية السعودية.

**قواعد مهمة جداً:**
- اكتب بالعربية ONLY - لا تستخدم أي كلمات إنجليزية نهائياً
- استخدم العامية السعودية الطبيعية (زي كلامنا في الرياض وجدة)
- خلي الكتابة مثل محادثة حقيقية
- اسم المنتج هو: {product_name} - استخدم هذا الاسم بالضبط في الخاتمة
- ممنوع إطلاقًا استخدام أي كلمات إنجليزية في النص العربي الناتج – يجب ترجمة كل شيء بالكامل.

**البنية المطلوبة بالضبط (يجب اتباع هذا الهيكل بالكامل):**

[السطر الأول: الopening hook - جملة افتتاحية قصيرة قوية تنتهي بثلاث نقاط "..."] 
[ثم سطر فارغ]
[الفقرة الأولى: جملتان كحد أقصى فقط لوصف اللحظة والمكان والشعور، بشكل متصل بدون انقطاع، ويجب ألا تتجاوز 40 كلمة.فواصل]
[ثم سطر فارغ]
[الفقرة الثانية: 1 جمل فقط - تصف التجربة الحسية والمقارنة - تكون جمل متصلة بدون فواصل]
[ثم سطر فارغ]
[السطر الأخير: اسم المنتج بالضبط "{product_name}" + فائدته - جملة قصيرة]

**مثال على البنية الصحيحة:**

يا جماعة تخيلوا معي...

الساعة ٢ الظهر، حر الرياض اللي ما يرحم، وتوك طالع من الجامعة أو الدوام ومحتار. تحتاج شي يبرد على قلبك ويصححك... بس بنفس الوقت مالك خلق السكريات والخرابيط اللي تحسسك بتأنيب الضمير بعد أول رشفة.

تفتح الثلاجة... وتشوفه قدامك. علبة باردة، عليها قطرات موية، تعدك بالانتعاش اللي يضرب في الراس... طبيعي وخفيف. بعيد عن المشروبات الثقيلة والمحليات الصناعية.

{product_name}. انتعاشك اللي يروق مزاجك.

**تعليمات إضافية مهمة:**
- لا تضع أي كلمات أو جمل بعد اسم المنتج في السطر الأخير
- الفقرة الأولى والثانية يجب أن تكون كل فقرة 1-2 جمل كاملة
- لا تقطع الكلمة بين سطرين (مثل arti/ficiality)
- لا تكتب فقرات طويلة جداً
- يجب ألا يتجاوز الرد 100 كلمة.

**أخرج JSON فقط بهذا الشكل:**
{{"narrative": "النص الكامل هنا مع سطرين فارغين بين الأجزاء"}}
"""
        else:
            # English prompt copy_write
            system_prompt = f"""You are an award-winning copywriter known for vivid, sensory storytelling.

**CRITICAL RULES:**
- Product name is: {product_name} - Use this EXACT name in the closing line
- Do NOT invent or change the product name
- The closing line should be: "{product_name}. [short benefit phrase]"

**Required Structure (must follow exactly):**

[Opening hook line - a VERY SHORT phrase ending with "..."]
[THEN a blank line]
[Paragraph 1: 1-2 sentences ONLY - describe the moment, setting, feeling - continuous sentences without breaks - MUST NOT exceed 40 words]
[THEN a blank line]
[Paragraph 2: 1 sentences ONLY - describe sensory experience and comparison - continuous sentences without breaks]
[THEN a blank line]
[Closing line: EXACTLY "{product_name}. [short benefit]" - nothing more]


**Example of CORRECT structure:**

Picture this...

The sun blazing down at 2 PM, you just finished work and you're exhausted. You need something to cool you down and refresh you... but you don't want the guilt that comes with sugary drinks after that first sip.

You open the fridge and there it is. A cold can with water droplets, promising refreshment that hits just right. Natural, light, and nothing like the artificial taste of sodas or energy drinks.

{product_name}. Your refreshment that lifts your mood.

**CRITICAL RULES:**
- The opening hook is ONLY the first phrase ending with "...", nothing else on that line
- Paragraph 1 must be 1-2 complete sentences, no line breaks inside
- Paragraph 2 must be 1-2 complete sentences, no line breaks inside
- Do NOT split words across lines (no "arti/ficiality")
- The closing line has the product name FIRST, then benefit - nothing else
- Do NOT add extra sentences after the product name
- The response MUST NOT exceed 100 words.

**Output ONLY JSON:**
{{"narrative": "full text here with blank lines between sections"}}
"""
        # invoking ML call
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.85,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": (
                    f"Strategic Brief: {json.dumps(strategic_brief, indent=2, ensure_ascii=False)}\n\n"
                    f"IMPORTANT: The product name is '{product_name}'. Use this exact name in the closing line. Do not change it.\n"
                    f"Brand Voice: {brand_voice}\n\n"
                    f"Remember: opening hook on first line, then blank line, then paragraph 1 (3-4 sentences), then blank line, then paragraph 2 (3-4 sentences), then blank line, then closing line with '{product_name}'."
                    if is_arabic_output else
                    f"IMPORTANT: The product name is '{product_name}'. Use this exact name in the closing line. Do not invent a different name.\n\n"
                    f"Follow the structure exactly: hook..., blank line, paragraph 1 (3-4 sentences), blank line, paragraph 2 (3-4 sentences), blank line, closing line with '{product_name}'."
                )},
            ],
        )
        
        return json.loads(response.choices[0].message.content)
    
    def enforce_structure(self, text, product_name, is_arabic):
        """Enforce the 4-part structure with proper line breaks and correct product name"""
        
        # Fix product name if it's incorrect
        if product_name.lower() not in text.lower():
            # Try to find where product name should be in closing line
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if 'juice' in line.lower() or 'drink' in line.lower() or 'burst' in line.lower():
                    # Replace with correct product name
                    lines[i] = product_name + line[line.find('.'):] if '.' in line else product_name
            text = '\n'.join(lines)
        
        # Split by double newlines
        parts = text.split('\n\n')
        
        # Clean up parts
        clean_parts = []
        for part in parts:
            part = part.strip()
            if part:
                # Remove any line breaks inside paragraphs
                part = part.replace('\n', ' ')
                clean_parts.append(part)
        
        # Ensure we have at least 4 parts
        if len(clean_parts) >= 4:
            # Make sure closing line starts with product name
            closing = clean_parts[3]
            if not closing.startswith(product_name):
                # Extract benefit after product name
                if '.' in closing:
                    benefit = closing[closing.find('.'):]
                    closing = product_name + benefit
                else:
                    closing = product_name + ". " + closing
                clean_parts[3] = closing
            
            return f"{clean_parts[0]}\n\n{clean_parts[1]}\n\n{clean_parts[2]}\n\n{clean_parts[3]}"
        
        # If we have 3 parts (missing one paragraph)
        if len(clean_parts) == 3:
            # Assume hook, paragraph, closing
            hook = clean_parts[0]
            closing = clean_parts[2]
            # Split the middle into two paragraphs
            middle = clean_parts[1]
            sentences = re.split(r'(?<=[.!?])\s+', middle)
            if len(sentences) >= 6:
                mid_point = len(sentences) // 2
                para1 = ' '.join(sentences[:mid_point])
                para2 = ' '.join(sentences[mid_point:])
                return f"{hook}\n\n{para1}\n\n{para2}\n\n{closing}"
        
        # If text is one block, try to parse
        if len(clean_parts) == 1:
            full_text = clean_parts[0]
            
            # Find opening hook (first sentence or phrase ending with ...)
            hook_match = re.match(r'^([^.!?]*[.…]{1,3})', full_text)
            if hook_match:
                hook = hook_match.group(1).strip()
                remaining = full_text[len(hook):].strip()
            else:
                # Take first 40 chars as hook
                hook = full_text[:40] + "..."
                remaining = full_text[40:].strip()
            
            # Find closing line (should contain product name or near the end)
            sentences = re.split(r'(?<=[.!?])\s+', remaining)
            if len(sentences) >= 3:
                closing = sentences[-1]
                # Ensure closing has product name
                if product_name.lower() not in closing.lower():
                    closing = f"{product_name}. {closing}"
                
                # Middle sentences as paragraphs
                middle_sentences = sentences[:-1]
                
                # Split into two paragraphs
                mid_point = len(middle_sentences) // 2
                para1 = ' '.join(middle_sentences[:mid_point])
                para2 = ' '.join(middle_sentences[mid_point:])
                
                return f"{hook}\n\n{para1}\n\n{para2}\n\n{closing}"
        
        return text
    
    def generate_campaign(self, product_name, product_desc, target_audience, brand_voice, output_language):
        """
        Main method that chains both agents to generate a complete campaign
        
        Args:
            product_name (str): Name of the product
            product_desc (str): Description of the product
            target_audience (str): Target audience description
            brand_voice (str): Comma-separated brand voice attributes
            output_language (str): "English" or "Arabic"
        
        Returns:
            dict: Contains strategic_brief and campaign_narrative
        """
        is_arabic_output = (output_language == "Arabic")
        
        # Run Agent 1: Strategist
        strategic_brief = self.run_strategist(
            product_name, product_desc, target_audience, 
            brand_voice, is_arabic_output
        )
        
        # Run Agent 2: Copywriter
        campaign = self.run_copywriter(
            strategic_brief, product_name, brand_voice, is_arabic_output
        )
        
        narrative = campaign.get("narrative", "")
        
        # Enforce the 4-part structure with correct product name
        narrative = self.enforce_structure(narrative, product_name, is_arabic_output)
        
        return {
            "strategic_brief": strategic_brief,
            "campaign_narrative": narrative
        }