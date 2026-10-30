import os
import json
from flask import Flask, render_template, request, abort

app = Flask(__name__)

# JSON ফাইল লোড করার হেল্পার ফাংশন
def load_json(filename):
    filepath = os.path.join(app.root_path, 'data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ১. হোমপেজ (সব চ্যাপ্টারের লিস্ট)
@app.route('/')
def index():
    meta = load_json('chapters.json')
    chapters = meta.get('chapters', [])
    return render_template('index.html', chapters=chapters)

# ২. চ্যাপ্টার পেজ (নোট বা স্টাডি মেটেরিয়াল)
@app.route('/chapter/<slug>')
def chapter(slug):
    meta = load_json('chapters.json')
    chapters = meta.get('chapters', [])
    
    # slug দিয়ে চ্যাপ্টার খোঁজা
    chapter_info = next((c for c in chapters if c['slug'] == slug), None)
    if not chapter_info:
        abort(404)
    
    # চ্যাপ্টারের ডেটা ফাইল ম্যাপিং
    file_map = {
        "companies-act-1994": "chapter1_companies.json",
        "negotiable-instruments-act-1881": "chapter2_negotiable.json",
        "partnership-act-1932": "chapter3_partnership.json",
        "contract-act-sale-of-goods": "chapter4_contract.json"
    }
    
    chapter_data = load_json(file_map.get(slug, ""))
    sections = chapter_data.get('sections', [])
    
    return render_template('chapter.html', chapter=chapter_info, sections=sections)

# ৩. কুইজ পেজ
@app.route('/quiz/<slug>')
def quiz(slug):
    meta = load_json('chapters.json')
    chapter_info = next((c for c in meta.get('chapters', []) if c['slug'] == slug), None)
    
    if not chapter_info:
        abort(404)
        
    quiz_files = {
        "companies-act-1994": "quiz_companies.json",
        "negotiable-instruments-act-1881": "quiz_negotiable.json",
        "partnership-act-1932": "quiz_partnership.json",
        "contract-act-sale-of-goods": "quiz_contract.json"
    }
    
    quiz_data = load_json(quiz_files.get(slug, ""))
    questions = quiz_data.get('questions', [])
    
    return render_template('quiz.html', chapter=chapter_info, questions=questions)

# ৪. অ্যাডভান্সড সার্চ ফাংশনালিটি (এক বা একাধিক শব্দ দিয়ে সার্চ)
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    results = []
    
    if query:
        # ইউজার একাধিক শব্দ লিখলে স্পেস দিয়ে আলাদা করা হচ্ছে
        search_terms = query.split()
        
        file_map = {
            "companies-act-1994": "chapter1_companies.json",
            "negotiable-instruments-act-1881": "chapter2_negotiable.json",
            "partnership-act-1932": "chapter3_partnership.json",
            "contract-act-sale-of-goods": "chapter4_contract.json"
        }
        
        for slug, filename in file_map.items():
            data = load_json(filename)
            for section in data.get('sections', []):
                heading = section.get('heading', '').lower()
                content = section.get('content', '').lower()
                keywords = [kw.lower() for kw in section.get('keywords', [])]
                
                # চেক করা হচ্ছে সার্চের সবগুলো শব্দ সেকশনটিতে আছে কিনা
                match = True
                for term in search_terms:
                    if not (term in heading or term in content or any(term in kw for kw in keywords)):
                        match = False
                        break
                
                if match:
                    results.append({
                        "chapter_slug": slug,
                        "chapter_title": data.get('title'),
                        "section_id": section.get('id'),
                        "heading": section.get('heading'),
                        "snippet": section.get('content', '')[:200] + "..."
                    })
                    
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    import os
# ... (আপনার অন্যান্য কোড)

if __name__ == '__main__':
    # Render নিজেই পোর্ট ঠিক করে দেয়, তাই লোকালহোস্টে ৫০০০ এবং Render-এ ডাইনামিক পোর্ট ব্যবহার হবে
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)