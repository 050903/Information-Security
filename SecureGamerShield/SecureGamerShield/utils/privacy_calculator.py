"""
Privacy calculation utilities for gaming privacy assessment
"""

def calculate_risk_score(responses):
    """
    Calculate privacy risk score based on user responses
    Returns: (risk_score, risk_level, category_scores)
    """
    
    # Scoring weights for different categories
    scoring_weights = {
        'gaming_habits': 0.2,
        'account_security': 0.25,
        'privacy_awareness': 0.25,
        'data_sharing': 0.3
    }
    
    # Initialize category scores
    category_scores = {
        'Gaming Habits': 0,
        'Account Security': 0,
        'Privacy Awareness': 0,
        'Data Sharing Control': 0
    }
    
    # Gaming habits scoring
    gaming_frequency_scores = {
        "Rarely": 10,
        "Weekly": 25,
        "Daily": 50,
        "Multiple times daily": 80
    }
    
    multiplayer_scores = {
        "Never": 0,
        "Occasionally": 20,
        "Frequently": 50,
        "Always": 80
    }
    
    voice_chat_scores = {
        "Never": 0,
        "With friends only": 15,
        "With strangers sometimes": 45,
        "Frequently with strangers": 80
    }
    
    streaming_scores = {
        "Never": 0,
        "Rarely": 10,
        "Regularly": 40,
        "Professionally": 70
    }
    
    gaming_habits_score = (
        gaming_frequency_scores.get(responses['gaming_frequency'], 0) * 0.3 +
        multiplayer_scores.get(responses['multiplayer_gaming'], 0) * 0.3 +
        voice_chat_scores.get(responses['voice_chat'], 0) * 0.3 +
        streaming_scores.get(responses['streaming'], 0) * 0.1
    )
    
    category_scores['Gaming Habits'] = min(100, gaming_habits_score)
    
    # Account security scoring
    account_sharing_scores = {
        "Never": 0,
        "With family": 20,
        "With friends": 50,
        "With strangers": 90
    }
    
    password_scores = {
        "Unique strong passwords": 0,
        "Some unique passwords": 30,
        "Similar passwords": 60,
        "Same password everywhere": 90
    }
    
    two_factor_scores = {
        "On all accounts": 0,
        "On some accounts": 25,
        "On few accounts": 60,
        "Never": 90
    }
    
    account_security_score = (
        account_sharing_scores.get(responses['account_sharing'], 0) * 0.3 +
        password_scores.get(responses['password_practices'], 0) * 0.4 +
        two_factor_scores.get(responses['two_factor_auth'], 0) * 0.3
    )
    
    category_scores['Account Security'] = min(100, account_security_score)
    
    # Privacy awareness scoring
    privacy_check_scores = {
        "Regularly": 0,
        "When reminded": 25,
        "Rarely": 60,
        "Never": 90
    }
    
    data_awareness_scores = {
        "Very aware": 0,
        "Somewhat aware": 30,
        "Not very aware": 60,
        "Not aware at all": 90
    }
    
    permission_scores = {
        "Always": 0,
        "Usually": 20,
        "Sometimes": 50,
        "Never": 80
    }
    
    privacy_awareness_score = (
        privacy_check_scores.get(responses['privacy_settings_check'], 0) * 0.4 +
        data_awareness_scores.get(responses['data_collection_awareness'], 0) * 0.3 +
        permission_scores.get(responses['permission_review'], 0) * 0.3
    )
    
    category_scores['Privacy Awareness'] = min(100, privacy_awareness_score)
    
    # Data sharing control scoring
    personal_info_scores = {
        "Never": 0,
        "Rarely": 20,
        "Sometimes": 60,
        "Frequently": 90
    }
    
    third_party_scores = {
        "Never": 0,
        "Rarely": 25,
        "Sometimes": 50,
        "Frequently": 80
    }
    
    data_sharing_score = (
        personal_info_scores.get(responses['personal_info_sharing'], 0) * 0.6 +
        third_party_scores.get(responses['third_party_connections'], 0) * 0.4
    )
    
    category_scores['Data Sharing Control'] = min(100, data_sharing_score)
    
    # Calculate overall risk score
    overall_risk = (
        category_scores['Gaming Habits'] * scoring_weights['gaming_habits'] +
        category_scores['Account Security'] * scoring_weights['account_security'] +
        category_scores['Privacy Awareness'] * scoring_weights['privacy_awareness'] +
        category_scores['Data Sharing Control'] * scoring_weights['data_sharing']
    )
    
    # Determine risk level
    if overall_risk >= 70:
        risk_level = "High"
    elif overall_risk >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return int(overall_risk), risk_level, category_scores

def get_risk_recommendations(responses, category_scores):
    """
    Generate personalized recommendations based on risk assessment
    """
    
    recommendations = []
    
    # Account Security recommendations
    if category_scores['Account Security'] >= 60:
        if responses['two_factor_auth'] in ["Never", "On few accounts"]:
            recommendations.append({
                'title': 'Enable Two-Factor Authentication',
                'priority': 'High',
                'description': 'Add an extra layer of security to your gaming accounts with 2FA',
                'steps': [
                    'Log into your gaming platform accounts',
                    'Go to Security or Account Settings',
                    'Enable Two-Factor Authentication',
                    'Use an authenticator app for better security',
                    'Save backup codes in a secure location'
                ]
            })
        
        if responses['password_practices'] in ["Similar passwords", "Same password everywhere"]:
            recommendations.append({
                'title': 'Improve Password Security',
                'priority': 'High',
                'description': 'Use unique, strong passwords for each gaming account',
                'steps': [
                    'Install a reputable password manager',
                    'Generate unique passwords for each account',
                    'Use passwords with 12+ characters',
                    'Include numbers, symbols, and mixed case',
                    'Change passwords if they\'ve been reused'
                ]
            })
    
    # Privacy Awareness recommendations
    if category_scores['Privacy Awareness'] >= 50:
        if responses['privacy_settings_check'] in ["Rarely", "Never"]:
            recommendations.append({
                'title': 'Review Privacy Settings Regularly',
                'priority': 'Medium',
                'description': 'Stay on top of your privacy settings across all gaming platforms',
                'steps': [
                    'Set a monthly reminder to check privacy settings',
                    'Review settings after platform updates',
                    'Check what data is being collected',
                    'Adjust sharing and visibility preferences',
                    'Document your preferred settings'
                ]
            })
        
        if responses['data_collection_awareness'] in ["Not very aware", "Not aware at all"]:
            recommendations.append({
                'title': 'Learn About Data Collection',
                'priority': 'Medium',
                'description': 'Understand what data games collect and how it\'s used',
                'steps': [
                    'Read privacy policies of your favorite games',
                    'Use privacy transparency tools',
                    'Learn about different types of data collection',
                    'Understand your data rights',
                    'Complete privacy education modules'
                ]
            })
    
    # Data Sharing recommendations
    if category_scores['Data Sharing Control'] >= 50:
        if responses['personal_info_sharing'] in ["Sometimes", "Frequently"]:
            recommendations.append({
                'title': 'Limit Personal Information Sharing',
                'priority': 'High',
                'description': 'Be more cautious about sharing personal details in games',
                'steps': [
                    'Avoid sharing real name, age, or location',
                    'Use gaming-specific usernames',
                    'Be cautious in voice and text chat',
                    'Don\'t share social media profiles',
                    'Educate yourself about social engineering'
                ]
            })
        
        if responses['third_party_connections'] in ["Sometimes", "Frequently"]:
            recommendations.append({
                'title': 'Audit Social Media Connections',
                'priority': 'Medium',
                'description': 'Review and limit connections between gaming and social accounts',
                'steps': [
                    'Review connected social media accounts',
                    'Disconnect unnecessary integrations',
                    'Control what gaming activity is shared',
                    'Adjust auto-posting settings',
                    'Review friend sync settings'
                ]
            })
    
    # Gaming Habits recommendations
    if category_scores['Gaming Habits'] >= 60:
        if responses['voice_chat'] == "Frequently with strangers":
            recommendations.append({
                'title': 'Secure Voice Chat Practices',
                'priority': 'Medium',
                'description': 'Protect your privacy during voice communications',
                'steps': [
                    'Use push-to-talk instead of open mic',
                    'Be cautious about background noise revealing location',
                    'Don\'t share personal information in voice chat',
                    'Use voice changers if desired for anonymity',
                    'Report inappropriate behavior'
                ]
            })
        
        if responses['streaming'] in ["Regularly", "Professionally"]:
            recommendations.append({
                'title': 'Streaming Privacy Protection',
                'priority': 'Medium',
                'description': 'Protect your privacy while streaming gameplay',
                'steps': [
                    'Use streaming-specific privacy settings',
                    'Hide personal information from screen',
                    'Be careful about showing emails or messages',
                    'Use separate accounts for streaming',
                    'Control chat and interaction settings'
                ]
            })
    
    # Sort recommendations by priority
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return recommendations

def calculate_comprehensive_score(user_data):
    """
    Calculate a comprehensive privacy score based on multiple factors
    """
    
    # This would integrate with actual user data in a real application
    # For now, return a calculated score based on typical privacy factors
    
    base_score = 65
    
    # Factors that could improve the score
    if user_data.get('two_factor_enabled', False):
        base_score += 10
    
    if user_data.get('unique_passwords', False):
        base_score += 8
    
    if user_data.get('privacy_settings_reviewed', False):
        base_score += 7
    
    if user_data.get('limited_data_sharing', False):
        base_score += 10
    
    return min(100, base_score)
