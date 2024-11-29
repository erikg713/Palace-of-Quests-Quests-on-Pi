from app.models import User, PremiumBenefit, db
from datetime import datetime, timedelta

def apply_premium_benefit(user_id, benefit_id):
    benefit = PremiumBenefit.query.get(benefit_id)
    user = User.query.get(user_id)
    
    if benefit.benefit_type == "xp_boost":
        user.xp_boost_expires = datetime.utcnow() + timedelta(days=benefit.duration_days)
    elif benefit.benefit_type == "item":
        # Add exclusive item to user inventory (pseudo code)
        user.inventory.append(benefit.name)
    elif benefit.benefit_type == "guild_access":
        user.guild_access_expires = datetime.utcnow() + timedelta(days=benefit.duration_days)

    db.session.commit()

from app.models import User, PremiumBenefit, db
from datetime import datetime, timedelta

def apply_premium_benefit(user_id, benefit_id):
    benefit = PremiumBenefit.query.get(benefit_id)
    user = User.query.get(user_id)
    
    if benefit.benefit_type == "xp_boost":
        user.xp_boost_expires = datetime.utcnow() + timedelta(days=benefit.duration_days)
    elif benefit.benefit_type == "item":
        user.inventory.append(benefit.name)  # Replace with actual inventory handling logic
    elif benefit.benefit_type == "guild_access":
        user.guild_access_expires = datetime.utcnow() + timedelta(days=benefit.duration_days)

    db.session.commit()
