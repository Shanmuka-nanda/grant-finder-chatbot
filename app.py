from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Grant database
GRANTS_DATABASE = [
    {
        "id": 1,
        "title": "National Science Foundation Research Grant",
        "description": "Funding for innovative research projects in science and technology. Supports early-career researchers and established scientists.",
        "amount": "$50,000 - $500,000",
        "deadline": "2024-12-15",
        "category": "Research",
        "eligibility": "Universities, research institutions, individual researchers with PhD",
        "keywords": ["research", "science", "technology", "innovation", "academic", "university"]
    },
    {
        "id": 2,
        "title": "Small Business Innovation Grant",
        "description": "Financial support for small businesses to develop new products and services. Focus on technology startups and innovative solutions.",
        "amount": "$25,000 - $250,000",
        "deadline": "2024-11-30",
        "category": "Business",
        "eligibility": "Small businesses (under 50 employees), startups, entrepreneurs",
        "keywords": ["business", "startup", "small business", "entrepreneur", "innovation", "commercial"]
    },
    {
        "id": 3,
        "title": "Education Enhancement Fund",
        "description": "Grants for educational programs, school improvements, and student support initiatives. Supports K-12 and higher education.",
        "amount": "$10,000 - $100,000",
        "deadline": "2025-01-20",
        "category": "Education",
        "eligibility": "Schools, educational nonprofits, teachers, educational organizations",
        "keywords": ["education", "school", "student", "learning", "teaching", "academic", "nonprofit"]
    },
    {
        "id": 4,
        "title": "Environmental Conservation Grant",
        "description": "Funding for environmental protection, conservation projects, and sustainability initiatives.",
        "amount": "$30,000 - $300,000",
        "deadline": "2024-12-01",
        "category": "Environment",
        "eligibility": "Environmental nonprofits, conservation groups, research institutions",
        "keywords": ["environment", "conservation", "sustainability", "green", "climate", "ecology"]
    },
    {
        "id": 5,
        "title": "Arts and Culture Development Fund",
        "description": "Support for artists, cultural organizations, and creative projects that enrich community life.",
        "amount": "$5,000 - $75,000",
        "deadline": "2025-02-15",
        "category": "Arts",
        "eligibility": "Individual artists, arts organizations, cultural nonprofits, museums",
        "keywords": ["arts", "culture", "creative", "artist", "museum", "theater", "music"]
    },
    {
        "id": 6,
        "title": "Healthcare Innovation Grant",
        "description": "Funding for healthcare research, medical technology development, and public health initiatives.",
        "amount": "$40,000 - $400,000",
        "deadline": "2024-11-15",
        "category": "Healthcare",
        "eligibility": "Hospitals, medical research institutions, healthcare nonprofits, medical professionals",
        "keywords": ["healthcare", "medical", "health", "hospital", "medicine", "public health"]
    },
    {
        "id": 7,
        "title": "Community Development Grant",
        "description": "Support for local community projects, neighborhood improvements, and social services.",
        "amount": "$15,000 - $150,000",
        "deadline": "2025-01-10",
        "category": "Community",
        "eligibility": "Community organizations, local nonprofits, neighborhood groups",
        "keywords": ["community", "local", "neighborhood", "social", "development", "nonprofit"]
    },
    {
        "id": 8,
        "title": "Technology Innovation Award",
        "description": "Grants for developing cutting-edge technology solutions, software development, and digital innovation.",
        "amount": "$35,000 - $350,000",
        "deadline": "2024-12-20",
        "category": "Technology",
        "eligibility": "Tech companies, software developers, technology startups, IT professionals",
        "keywords": ["technology", "tech", "software", "digital", "innovation", "IT", "computer"]
    },
    {
        "id": 9,
        "title": "Nonprofit Capacity Building Grant",
        "description": "Funding to help nonprofits strengthen their operations, expand services, and improve organizational effectiveness.",
        "amount": "$20,000 - $200,000",
        "deadline": "2025-02-01",
        "category": "Nonprofit",
        "eligibility": "Registered 501(c)(3) nonprofits, charitable organizations",
        "keywords": ["nonprofit", "charity", "charitable", "501c3", "organization", "foundation"]
    },
    {
        "id": 10,
        "title": "Youth Development Program Grant",
        "description": "Support for programs that help young people develop skills, access opportunities, and achieve their potential.",
        "amount": "$12,000 - $120,000",
        "deadline": "2025-01-05",
        "category": "Youth",
        "eligibility": "Youth organizations, after-school programs, mentoring organizations",
        "keywords": ["youth", "children", "teen", "student", "young", "mentoring", "after-school"]
    }
]


def calculate_relevance_score(grant, query):
    """Calculate how relevant a grant is to the search query"""
    score = 0
    query_lower = query.lower()
    
    # Check title
    if query_lower in grant["title"].lower():
        score += 10
    
    # Check description
    description_lower = grant["description"].lower()
    matches = len(re.findall(r'\b' + re.escape(query_lower) + r'\b', description_lower))
    score += matches * 3
    
    # Check keywords
    for keyword in grant["keywords"]:
        if keyword.lower() in query_lower:
            score += 5
        if query_lower in keyword.lower():
            score += 3
    
    # Check category
    if grant["category"].lower() in query_lower or query_lower in grant["category"].lower():
        score += 8
    
    # Check eligibility
    if query_lower in grant["eligibility"].lower():
        score += 2
    
    return score


def search_grants(query):
    """Search grants based on query with AI-like relevance scoring"""
    if not query or len(query.strip()) < 2:
        return []
    
    query = query.strip()
    
    # Calculate relevance scores
    scored_grants = []
    for grant in GRANTS_DATABASE:
        score = calculate_relevance_score(grant, query)
        if score > 0:
            scored_grants.append((grant, score))
    
    # Sort by relevance score (highest first)
    scored_grants.sort(key=lambda x: x[1], reverse=True)
    
    # Return top matches (limit to 5 most relevant)
    return [grant for grant, score in scored_grants[:5]]


def generate_ai_response(query, results):
    """Generate AI-like response based on search results"""
    if len(results) == 0:
        responses = [
            f"I couldn't find any grants matching '{query}'. Try searching for specific categories like 'education', 'research', 'business', 'healthcare', or 'nonprofit' grants.",
            f"No grants found for '{query}'. You might want to try different keywords such as 'small business', 'environmental', 'arts', or 'community development'.",
            f"I don't have any grants matching '{query}' in my database. Consider searching by category: Research, Business, Education, Healthcare, Arts, Environment, or Community grants."
        ]
        return responses[hash(query) % len(responses)]
    
    elif len(results) == 1:
        return f"I found 1 grant that matches your search for '{query}':"
    else:
        return f"I found {len(results)} grants that match your search for '{query}':"


@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for grant search"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Please provide a search query',
                'grants': []
            }), 400
        
        # Handle help commands
        query_lower = query.lower()
        if query_lower in ['help', 'what can you do', 'how to use', 'commands', 'examples']:
            help_message = """I can help you find grants! Here's how to use me:

**Search by Category:**
• Education grants
• Business/startup funding
• Research grants
• Healthcare innovation
• Environmental conservation
• Arts and culture
• Community development
• Technology grants
• Nonprofit grants
• Youth programs

**Search Tips:**
• Be specific: "education grants for nonprofits"
• Use keywords: "small business", "research", "innovation"
• Try different terms if no results appear

**Example Queries:**
• "education grants"
• "small business funding"
• "nonprofit grants"
• "research grants for universities"
• "healthcare innovation grants"

Click the suggestion chips above or type your query to get started!"""
            
            return jsonify({
                'success': True,
                'message': help_message,
                'grants': [],
                'query': query,
                'is_help': True
            })
        
        # Search for grants
        results = search_grants(query)
        
        # Generate AI response
        ai_message = generate_ai_response(query, results)
        
        return jsonify({
            'success': True,
            'message': ai_message,
            'grants': results,
            'query': query
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}',
            'grants': []
        }), 500


@app.route('/api/grants', methods=['GET'])
def get_all_grants():
    """Get all available grants"""
    return jsonify({
        'success': True,
        'grants': GRANTS_DATABASE,
        'total': len(GRANTS_DATABASE)
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all grant categories"""
    categories = list(set([grant['category'] for grant in GRANTS_DATABASE]))
    return jsonify({
        'success': True,
        'categories': sorted(categories)
    })


@app.route('/')
def index():
    """Serve the main HTML page"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

