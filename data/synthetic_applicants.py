import random
from datetime import datetime
import pandas as pd

def get_base_score(income, job_history, collateral_pct, credit_clean, gender, location, age):
    score = 0
    # INCOME
    if income >= 1000000:
        score += 30
    elif income >= 500000:
        score += 20
    elif income >= 250000:
        score += 10
    
    # JOB STABILITY
    if job_history >= 5:
        score += 25
    elif job_history >= 3:
        score += 15
    elif job_history >= 1:
        score += 8
    else:
        score += 2
        
    # COLLATERAL
    if collateral_pct >= 0.6:
        score += 25
    elif collateral_pct >= 0.4:
        score += 15
    elif collateral_pct >= 0.2:
        score += 8
        
    # CREDIT HISTORY
    if credit_clean == 'Clean':
        score += 20
    elif credit_clean == '1 Default':
        score += 10
    elif credit_clean == '2-3 Defaults':
        score += 5
    else:  # Recent defaults
        score -= 15
        
    # DEMOGRAPHIC BONUS
    if gender == 'Female':
        score += 2
    if location == 'Rural':
        score += 2
    if 25 <= age <= 45:
        score += 1
        
    return min(100, max(0, score))


def generate_realistic_name(gender):
    male_names = ['Rajesh', 'Amit', 'Anil', 'Sunil', 'Vijay', 'Rahul', 'Sanjay', 'Manoj', 'Prakash', 'Arun']
    female_names = ['Priya', 'Fatima', 'Pooja', 'Neha', 'Anjali', 'Kavita', 'Geeta', 'Rekha', 'Sunita', 'Aarti']
    last_names = ['Kumar', 'Sharma', 'Singh', 'Patel', 'Yadav', 'Gupta', 'Verma', 'Khan', 'Mishra', 'Chauhan']
    
    if gender == 'Male':
        return f"{random.choice(male_names)} {random.choice(last_names)[0]}."
    else:
        return f"{random.choice(female_names)} {random.choice(last_names)[0]}."

def generate_synthetic_applicants(n=500):
    """
    Generate realistic, diverse applicants with intentional biases.
    """
    applicants = []
    
    # Set seed for reproducibility during generation
    random.seed(42)
    
    for i in range(n):
        # Demographics
        gender = random.choice(['Male', 'Female'])
        location = random.choice(['Urban', 'Rural'])
        age = random.randint(18, 70)
        
        # Financial
        base_income = random.gauss(500000, 200000)
        income = max(150000, base_income)  # ₹ 150K minimum
        
        job_history = random.gauss(3.5, 2)
        job_history = round(max(0, min(job_history, 20)), 1)  # 0-20 years
        
        collateral_pct = random.gauss(0.35, 0.15)
        collateral_pct = round(max(0, min(collateral_pct, 1.0)), 2)  # 0-100%
        
        credit_roll = random.random()
        if credit_roll > 0.3:
            credit_clean = 'Clean'
        elif credit_roll > 0.15:
            credit_clean = '1 Default'
        elif credit_roll > 0.05:
            credit_clean = '2-3 Defaults'
        else:
            credit_clean = 'Recent defaults'
        
        # Intentional bias patterns
        if location == 'Rural':
            income *= 0.85  # Rural applicants earn ~15% less
        
        if gender == 'Female':
            collateral_pct *= 0.9  # Women have less collateral
        
        if gender == 'Female' and location == 'Rural':
            income *= 0.95  # Intersectional burden
        
        # Score
        score = get_base_score(income, job_history, collateral_pct, credit_clean, gender, location, age)
        
        # Decision
        if score >= 70:
            status = 'APPROVED'
        elif score >= 50:
            status = 'UNDER REVIEW'
        else:
            status = 'DENIED'
            
        # Add intentional bias: artificially alter status based on demographics
        # to test bias detection engines.
        if location == 'Rural' and random.random() < 0.15 and status == 'APPROVED':
            status = 'UNDER REVIEW'
            
        if location == 'Rural' and gender == 'Female' and random.random() < 0.10 and status == 'UNDER REVIEW':
            status = 'DENIED'
            
        applicants.append({
            'id': f'{i+1:04d}',
            'name': generate_realistic_name(gender),
            'gender': gender,
            'age': age,
            'location': location,
            'income': round(income),
            'job_history': job_history,
            'collateral_pct': collateral_pct,
            'credit_history': credit_clean,
            'score': score,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
    
    return pd.DataFrame(applicants)

if __name__ == "__main__":
    df = generate_synthetic_applicants(500)
    df.to_csv('seed_data.csv', index=False)
    print("Generated 500 applicants and saved to seed_data.csv")
