# Configuration file (optional)

COLORS = {
    'primary': '#2C3E50',
    'secondary': '#18BC9C',
    'background': '#F8F9FA',
    'text': '#2C3E50',
    'chart_colors': ['#18BC9C', '#3498DB', '#E74C3C', '#F39C12', '#9B59B6']
}

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")