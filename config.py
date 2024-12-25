class Config:
    WEBSITE_NAME = 'My Website'
    YEAR = 2024
    TEMPLATE_PATHS = {
        'home': 'components/main.html',
        # Add other page templates here if needed
    }
    RESERVATION_TYPES = [
        ('orientation', 'Orientation'),
        ('resume_help', 'Resume Help'),
        ('computer_skills', 'Computer Skills'),
        ('skills_in_demand', 'Skills in Demand'),
        ('web_development', 'Web Development'),
        ('networking', 'Networking'),
    ]
    DATA_CSV = 'data.csv'