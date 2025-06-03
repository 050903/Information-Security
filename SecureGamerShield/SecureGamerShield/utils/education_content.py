"""
Education content and quiz questions for privacy learning modules
"""

def get_education_modules():
    """Return structured education modules for privacy learning"""
    
    modules = {
        "Understanding Gaming Privacy": {
            "icon": "🎮",
            "description": "Learn the fundamentals of privacy in gaming environments",
            "difficulty": "Beginner",
            "duration": "15 minutes",
            "objectives": [
                "Understand what data games collect about you",
                "Learn about different types of privacy risks in gaming",
                "Identify common privacy threats in online gaming",
                "Recognize the importance of gaming privacy protection"
            ],
            "content": [
                {
                    "title": "What is Gaming Privacy?",
                    "content": """
Gaming privacy refers to the protection of personal information and behavioral data collected while playing video games. Modern games collect extensive information including:

**Personal Data:**
- Account information (email, username, age)
- Payment and billing information
- Communication logs (chat, voice)
- Friend lists and social connections

**Behavioral Data:**
- Gameplay patterns and preferences
- Time spent playing
- In-game purchases and transactions
- Performance metrics and statistics

**Technical Data:**
- Device information and specifications
- Location data (when enabled)
- Network information and IP addresses
- System performance and crash reports

Understanding what data is collected is the first step toward protecting your privacy while gaming.
                    """,
                    "interactive": {
                        "type": "checklist",
                        "items": [
                            "I understand what personal data games collect",
                            "I know what behavioral data means",
                            "I'm aware of technical data collection",
                            "I recognize the importance of gaming privacy"
                        ]
                    }
                },
                {
                    "title": "Common Privacy Risks",
                    "content": """
Gaming environments present unique privacy challenges:

**Identity Exposure:**
- Real names and personal information shared accidentally
- Profile information visible to strangers
- Location data revealing physical address

**Communication Risks:**
- Voice chat recordings stored indefinitely
- Text messages monitored and analyzed
- Personal conversations with strangers

**Data Breaches:**
- Gaming companies targeted by hackers
- Account credentials stolen and sold
- Payment information compromised

**Tracking and Profiling:**
- Behavioral patterns analyzed for marketing
- Cross-platform tracking across games
- Data sold to third-party advertisers

Being aware of these risks helps you make informed decisions about your gaming privacy settings.
                    """,
                    "interactive": {
                        "type": "scenario",
                        "scenario": "You're playing an online multiplayer game and a stranger asks for your real name and city. They seem friendly and want to meet up.",
                        "choices": [
                            "Share your real name but not your city",
                            "Give a fake name and general region",
                            "Politely decline to share personal information",
                            "Block the player immediately"
                        ],
                        "correct": "Politely decline to share personal information",
                        "explanation": "Never share personal information with strangers online, regardless of how friendly they seem. Politely declining maintains social interaction while protecting your privacy."
                    }
                }
            ],
            "resources": [
                {
                    "type": "Article",
                    "title": "Gaming Privacy Best Practices",
                    "description": "Comprehensive guide to protecting privacy while gaming",
                    "url": "https://www.eff.org/deeplinks/2019/03/how-protect-your-privacy-while-gaming"
                },
                {
                    "type": "Guide",
                    "title": "Understanding Game Data Collection",
                    "description": "What data games collect and how it's used"
                }
            ]
        },
        
        "Password Security for Gamers": {
            "icon": "🔐",
            "description": "Master password security for your gaming accounts",
            "difficulty": "Beginner",
            "duration": "20 minutes",
            "objectives": [
                "Create strong, unique passwords for gaming accounts",
                "Understand the importance of two-factor authentication",
                "Learn about password managers and their benefits",
                "Recognize signs of compromised accounts"
            ],
            "content": [
                {
                    "title": "Strong Password Fundamentals",
                    "content": """
Strong passwords are your first line of defense against account takeovers:

**Password Requirements:**
- Minimum 12 characters (longer is better)
- Mix of uppercase and lowercase letters
- Include numbers and special characters
- Avoid dictionary words and personal information
- Unique password for each gaming account

**Common Mistakes to Avoid:**
- Using the same password across multiple accounts
- Including birthdays, names, or pet names
- Using simple keyboard patterns (123456, qwerty)
- Sharing passwords with friends or family
- Writing passwords down in unsecure locations

**Password Creation Tips:**
- Use passphrases with random words
- Substitute letters with numbers and symbols
- Create memorable but unpredictable combinations
- Use password generators for maximum security

Remember: A strong password is only effective if it's unique to each account.
                    """
                },
                {
                    "title": "Two-Factor Authentication (2FA)",
                    "content": """
Two-factor authentication adds an essential second layer of security:

**How 2FA Works:**
1. Enter your username and password (first factor)
2. Provide a second verification method (second factor)
3. Gain access only when both factors are verified

**Types of 2FA:**
- **SMS Text Messages:** Codes sent to your phone
- **Authenticator Apps:** Time-based codes from apps like Google Authenticator
- **Hardware Keys:** Physical security keys (most secure)
- **Biometric:** Fingerprint or facial recognition

**Benefits of 2FA:**
- Protects against password breaches
- Prevents unauthorized access even with stolen passwords
- Alerts you to login attempts
- Required by many competitive gaming platforms

**Setting Up 2FA:**
Most gaming platforms support 2FA in their security settings. Enable it on all your gaming accounts, especially those with payment information or valuable in-game items.
                    """,
                    "interactive": {
                        "type": "checklist",
                        "items": [
                            "I understand how 2FA protects my accounts",
                            "I know the different types of 2FA available",
                            "I will enable 2FA on my gaming accounts",
                            "I understand authenticator apps are more secure than SMS"
                        ]
                    }
                }
            ]
        },
        
        "Social Gaming Privacy": {
            "icon": "👥",
            "description": "Navigate privacy in social gaming environments",
            "difficulty": "Intermediate",
            "duration": "25 minutes",
            "objectives": [
                "Manage friend requests and social connections safely",
                "Configure voice and text chat privacy settings",
                "Control sharing of gaming activity and achievements",
                "Handle harassment and inappropriate behavior"
            ],
            "content": [
                {
                    "title": "Social Connection Safety",
                    "content": """
Social gaming creates unique privacy challenges that require careful management:

**Friend Request Management:**
- Only accept requests from people you know or trust
- Review profiles before accepting unknown requests
- Use privacy settings to limit who can send requests
- Remove inactive or suspicious connections regularly

**Profile Information Control:**
- Limit personal information in gaming profiles
- Use gaming-specific usernames, not real names
- Control visibility of your gaming activity
- Manage who can see your friend lists

**Communication Privacy:**
- Be cautious about sharing personal details in chat
- Use privacy-focused communication platforms when possible
- Understand that game chat may be monitored or recorded
- Report inappropriate behavior immediately

**Group and Guild Considerations:**
- Research groups before joining
- Understand group privacy policies
- Be selective about shared group activities
- Maintain boundaries between gaming and personal life
                    """
                }
            ]
        },
        
        "Data Rights and Control": {
            "icon": "📊",
            "description": "Understand and exercise your data rights as a gamer",
            "difficulty": "Intermediate",
            "duration": "30 minutes",
            "objectives": [
                "Know your data rights under GDPR and CCPA",
                "Learn how to request your gaming data",
                "Understand data portability and deletion rights",
                "Navigate privacy policies and terms of service"
            ],
            "content": [
                {
                    "title": "Your Legal Data Rights",
                    "content": """
Modern privacy laws grant you significant rights over your personal data:

**GDPR Rights (EU Residents):**
- **Right to Access:** Request copies of your personal data
- **Right to Rectification:** Correct inaccurate information
- **Right to Erasure:** Request deletion of your data
- **Right to Portability:** Transfer data between services
- **Right to Object:** Opt out of certain data processing

**CCPA Rights (California Residents):**
- Right to know what data is collected
- Right to delete personal information
- Right to opt out of data sales
- Right to non-discrimination for exercising rights

**How to Exercise Your Rights:**
1. Contact the gaming company's privacy team
2. Submit formal data requests through their portals
3. Provide necessary identification verification
4. Follow up if responses are delayed
5. File complaints with regulators if needed

**Important Considerations:**
- Rights may vary by jurisdiction
- Some data may be retained for legal or security reasons
- Deletion may affect your gaming experience
- Keep records of your requests and responses
                    """
                }
            ]
        }
    }
    
    return modules

def get_quiz_questions(module_name):
    """Return quiz questions for a specific module"""
    
    quiz_questions = {
        "Understanding Gaming Privacy": [
            {
                "question": "Which type of data do modern games typically collect?",
                "type": "multiple_choice",
                "options": ["Only gameplay statistics", "Personal and behavioral data", "Just account information", "Only payment details"],
                "correct": "Personal and behavioral data",
                "explanation": "Modern games collect extensive personal, behavioral, and technical data to improve gameplay and for business purposes."
            },
            {
                "question": "Sharing your real name with strangers in online games is always safe.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct": "False",
                "explanation": "Sharing personal information with strangers online poses privacy and safety risks, regardless of the platform."
            },
            {
                "question": "What is the biggest risk of data breaches in gaming?",
                "type": "multiple_choice",
                "options": ["Losing game progress", "Identity theft and financial fraud", "Getting banned from games", "Slower internet connection"],
                "correct": "Identity theft and financial fraud",
                "explanation": "Data breaches can expose personal and payment information, leading to serious identity theft and financial risks."
            }
        ],
        
        "Password Security for Gamers": [
            {
                "question": "What is the minimum recommended length for a secure password?",
                "type": "multiple_choice",
                "options": ["8 characters", "10 characters", "12 characters", "16 characters"],
                "correct": "12 characters",
                "explanation": "Security experts recommend at least 12 characters for strong password protection against modern attack methods."
            },
            {
                "question": "Two-factor authentication only works with SMS text messages.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct": "False",
                "explanation": "2FA can use SMS, authenticator apps, hardware keys, or biometric methods. Authenticator apps are generally more secure than SMS."
            },
            {
                "question": "Which is the most secure type of two-factor authentication?",
                "type": "multiple_choice",
                "options": ["SMS text messages", "Email codes", "Authenticator apps", "Hardware security keys"],
                "correct": "Hardware security keys",
                "explanation": "Hardware security keys provide the highest level of 2FA security as they're resistant to phishing and SIM swapping attacks."
            }
        ],
        
        "Social Gaming Privacy": [
            {
                "question": "You should accept friend requests from all players to build a large network.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct": "False",
                "explanation": "Only accept friend requests from people you know or trust to maintain your privacy and security."
            },
            {
                "question": "What information should you avoid sharing in gaming profiles?",
                "type": "multiple_choice",
                "options": ["Gaming achievements", "Real name and location", "Favorite games", "Gaming statistics"],
                "correct": "Real name and location",
                "explanation": "Personal identifying information like real names and locations should be kept private to protect your safety and privacy."
            }
        ],
        
        "Data Rights and Control": [
            {
                "question": "Under GDPR, you have the right to request deletion of your personal data.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct": "True",
                "explanation": "GDPR grants EU residents the 'right to erasure' allowing them to request deletion of their personal data under certain circumstances."
            },
            {
                "question": "What should you do if a gaming company doesn't respond to your data request?",
                "type": "multiple_choice",
                "options": ["Give up and accept it", "File a complaint with regulators", "Create a new account", "Stop playing games"],
                "correct": "File a complaint with regulators",
                "explanation": "If companies don't respond to legitimate data requests, you can file complaints with data protection authorities who can investigate and enforce compliance."
            }
        ]
    }
    
    return quiz_questions.get(module_name, [])