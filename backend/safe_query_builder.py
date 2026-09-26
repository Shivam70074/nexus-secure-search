import random
from typing import List, Dict, Any

# Mock Data Generation Helpers
FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Shaurya", "Atharv", "Advik", "Pranav", "Kabir", "Ritvik", "Rudra", "Aryan", "Ansh", "Dhruv", "Sita", "Gita", "Ria", "Nia", "Priya", "Anjali", "Kavya", "Sneha", "Neha", "Pooja", "Swati", "Meera", "Tara", "Roshni", "Ananya", "Diya", "Isha", "Aditi", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Victor", "Peggy"]
LAST_NAMES = ["Sharma", "Singh", "Gupta", "Patel", "Khan", "Kumar", "Reddy", "Rao", "Das", "Mukherjee", "Nair", "Iyer", "Joshi", "Bose", "Chawla", "Yadav", "Mishra", "Pandey", "Verma", "Chauhan"]
ROLES_SKILLS = [
    ("Android Developer", ["Android", "Kotlin", "Java", "Firebase", "Jetpack Compose"]),
    ("Flutter Developer", ["Flutter", "Dart", "Firebase", "Provider", "BLoC"]),
    ("iOS Developer", ["iOS", "Swift", "Objective-C", "CoreData", "SwiftUI"]),
    ("ML Engineer", ["Python", "TensorFlow", "PyTorch", "NLP", "Transformers", "Scikit-Learn"]),
    ("Full Stack Developer", ["React", "Node.js", "MongoDB", "Express", "TypeScript"]),
    ("Frontend Developer", ["React", "Vue", "Angular", "CSS", "HTML", "JavaScript"]),
    ("Backend Developer", ["Python", "Django", "FastAPI", "PostgreSQL", "Docker"]),
    ("DevOps Engineer", ["AWS", "Kubernetes", "Docker", "CI/CD", "Terraform"]),
    ("Data Scientist", ["Python", "Pandas", "SQL", "Machine Learning", "Data Visualization"]),
    ("Cybersecurity Analyst", ["Security", "Network", "Pen Testing", "Cryptography", "WAF"]),
    ("Blockchain Developer", ["Solidity", "Web3.js", "Ethereum", "Smart Contracts", "Rust"])
]
CITIES = ["Lucknow", "Delhi", "Mumbai", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Jaipur"]
ACTIVITIES = [
    "Committed to open-source project",
    "Published a new package",
    "Updated model weights",
    "Deployed to production",
    "Fine-tuned LLM",
    "Participated in a hackathon",
    "Resolved critical security bug",
    "Merged PR #452",
    "Wrote technical blog post",
    "Attended tech meetup",
    "Refactored legacy code"
]

MOCK_DATABASE = []
random.seed(42) # For reproducibility
for i in range(1, 151):
    role_skill = random.choice(ROLES_SKILLS)
    role = role_skill[0]
    skills = random.sample(role_skill[1], min(3, len(role_skill[1])))
    MOCK_DATABASE.append({
        "id": i,
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "role": role,
        "city": random.choice(CITIES),
        "bio": f"Passionate {role} with 5+ years of experience. Always learning and building.",
        "skills": skills,
        "recent_activity": random.choice(ACTIVITIES)
    })

# Ensure the examples from the original prompt are always matched exactly for demos
MOCK_DATABASE.insert(0, {"id": 1001, "name": "Alice Sharma", "role": "Android Developer", "city": "Lucknow", "bio": "Building scalable Android apps.", "skills": ["Android", "Kotlin", "Java"], "recent_activity": "Committed to nexus-android"})
MOCK_DATABASE.insert(1, {"id": 1002, "name": "Bob Singh", "role": "Flutter Developer", "city": "Lucknow", "bio": "Cross-platform mobile dev.", "skills": ["Flutter", "Dart", "Firebase"], "recent_activity": "Published new package"})
MOCK_DATABASE.insert(2, {"id": 1003, "name": "Charlie Gupta", "role": "ML Engineer", "city": "Delhi", "bio": "Training models for security.", "skills": ["Python", "TensorFlow", "PyTorch"], "recent_activity": "Updated model weights"})


class SafeQueryBuilder:
    def extract_intent(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        intent = {}
        
        # Robust mock intent extraction for the prototype
        roles_to_match = ["android", "flutter", "ios", "ml", "full stack", "frontend", "backend", "devops", "data scientist", "cybersecurity", "blockchain", "developer", "engineer"]
        for r in roles_to_match:
            if r in query_lower:
                intent["role"] = r
                break
                
        for c in [city.lower() for city in CITIES]:
            if c in query_lower:
                intent["city"] = c
                break
                
        return intent

    def execute_safe_query(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for record in MOCK_DATABASE:
            match = True
            for key, val in intent.items():
                if val.lower() not in record.get(key, "").lower():
                    match = False
                    break
            if match:
                # Enforce schema allowlist
                safe_record = {k: v for k, v in record.items() if k in ["id", "name", "role", "city", "bio", "skills", "recent_activity"]}
                results.append(safe_record)
        return results

query_builder = SafeQueryBuilder()
