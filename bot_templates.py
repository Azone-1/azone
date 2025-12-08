# bot_templates.py
# Pre-built bot templates for quick setup
# Organized by platform: Telegram, Facebook, YouTube, TikTok

BOT_TEMPLATES = {
    # ==================== TELEGRAM TEMPLATES ====================
    'telegram_support_myanmar': {
        'platform': 'telegram',
        'name': 'မြန်မာ Telegram Support Bot',
        'description': 'Telegram အတွက် မြန်မာဘာသာဖြင့် Customer Support Bot. Telegram Bot Token လိုအပ်ပါသည်။',
        'integration_guide': 'Telegram Bot Token ရယူရန်: @BotFather သို့ /newbot command ပို့ပါ။ Token ကို Dashboard ရှိ Telegram Integration section တွင် ထည့်သွင်းပါ။',
        'initial_greeting': 'မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ Customer Support ကို ကြိုဆိုပါသည်။ ဘာကူညီပေးရမလဲ?',
        'steps': [
            {
                'type': 'message',
                'content': 'ကျေးဇူးတင်ပါသည်! ကျွန်ုပ်တို့သည် သင့်အား ကူညီရန် ဤနေရာတွင် ရှိနေပါသည်။'
            },
            {
                'type': 'question',
                'content': 'သင့်နာမည် ဘယ်လိုခေါ်လဲ?',
                'variables': {'user_name': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'user_name'}]
            },
            {
                'type': 'message',
                'content': '{user_name} ရေ၊ နှုတ်ခွန်းဆက်ပါတယ်! ဘာကူညီပေးရမလဲ?'
            },
            {
                'type': 'question',
                'content': 'သင့်ပြဿနာ သို့မဟုတ် မေးခွန်းကို ဖော်ပြပါ:',
                'variables': {'issue_description': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'issue_description'}]
            },
            {
                'type': 'message',
                'content': 'ကျေးဇူးတင်ပါသည်! သင့်မေးခွန်းကို ကျွန်ုပ်တို့ Support Team သို့ ပို့ဆောင်ထားပါပြီ။ မကြာမီ ဆက်သွယ်ပါမည်။'
            }
        ]
    },
    'telegram_lead_capture': {
        'platform': 'telegram',
        'name': 'Telegram Lead Capture Bot',
        'description': 'Telegram အတွက် Lead အချက်အလက်များ စုဆောင်းသော Bot. Telegram Bot Token လိုအပ်ပါသည်။',
        'integration_guide': 'Telegram Bot Token ရယူရန်: @BotFather သို့ /newbot command ပို့ပါ။ Token ကို Dashboard ရှိ Telegram Integration section တွင် ထည့်သွင်းပါ။',
        'initial_greeting': 'မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ ဝန်ဆောင်မှုများအကြောင်း ပိုမိုလေ့လာလိုပါသလား?',
        'steps': [
            {
                'type': 'message',
                'content': 'ကောင်းပါတယ်! အချက်အလက်အချို့ကို စုဆောင်းပါမယ်။'
            },
            {
                'type': 'question',
                'content': 'သင့်နာမည် အပြည့်အစုံ ဘာလဲ?',
                'variables': {'lead_name': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_name'}]
            },
            {
                'type': 'question',
                'content': 'သင့် Email လိပ်စာ ဘာလဲ?',
                'variables': {'lead_email': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_email'}]
            },
            {
                'type': 'question',
                'content': 'ဖုန်းနံပါတ် ဘာလဲ?',
                'variables': {'lead_phone': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_phone'}]
            },
            {
                'type': 'message',
                'content': 'ကျေးဇူးတင်ပါသည် {lead_name}! သင့်အချက်အလက်ကို ရရှိပါပြီ။ ကျွန်ုပ်တို့ Team မှ {lead_email} သို့ မကြာမီ ဆက်သွယ်ပါမည်။'
            }
        ]
    },
    'telegram_order_tracker': {
        'platform': 'telegram',
        'name': 'Telegram Order Tracker Bot',
        'description': 'Telegram အတွက် Order Tracking Bot. API integration လိုအပ်ပါသည်။',
        'integration_guide': '1. Telegram Bot Token: @BotFather မှ token ရယူပါ\n2. API Integration: Order tracking API endpoint ကို configure လုပ်ပါ\n3. Dashboard ရှိ Telegram Integration section တွင် token ထည့်သွင်းပါ',
        'initial_greeting': 'မင်္ဂလာပါ! သင့် order ကို track လုပ်ရန် ကူညီပေးနိုင်ပါသည်။',
        'steps': [
            {
                'type': 'message',
                'content': 'Order tracking အတွက် order number လိုအပ်ပါသည်။'
            },
            {
                'type': 'question',
                'content': 'သင့် order number ကို ထည့်သွင်းပါ:',
                'variables': {'order_number': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'order_number'}]
            },
            {
                'type': 'message',
                'content': 'Order {order_number} ကို စစ်ဆေးနေပါသည်...'
            },
            {
                'type': 'api_call',
                'content': 'Checking order status...',
                'api_config': {
                    'url': 'https://api.example.com/orders/{{order_number}}',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_API_TOKEN", "Content-Type": "application/json"}',
                    'body': '{}'
                },
                'response_template': 'Order {order_number} status: {{api_response.status}}. Estimated delivery: {{api_response.delivery_date}}'
            }
        ]
    },
    'telegram_simple_greeting': {
        'platform': 'telegram',
        'name': 'Telegram Simple Greeting Bot',
        'description': 'Telegram အတွက် ရိုးရှင်းသော Greeting Bot. Beginners အတွက် သင့်တော်ပါသည်။',
        'integration_guide': 'Telegram Bot Token ရယူရန်: @BotFather သို့ /newbot command ပို့ပါ။',
        'initial_greeting': 'မင်္ဂလာပါ! ကျွန်ုပ်တို့၏ service ကို ကြိုဆိုပါသည်။',
        'steps': [
            {
                'type': 'message',
                'content': 'ကျေးဇူးတင်ပါသည်! ဘာကူညီပေးရမလဲ?'
            }
        ]
    },
    
    # ==================== FACEBOOK TEMPLATES ====================
    'facebook_messenger_support': {
        'platform': 'facebook',
        'name': 'Facebook Messenger Support Bot',
        'description': 'Facebook Messenger အတွက် Customer Support Bot. Facebook Page Access Token လိုအပ်ပါသည်။',
        'integration_guide': 'Facebook Integration:\n1. Facebook Developer Console တွင် App ဖန်တီးပါ\n2. Messenger Product ကို add လုပ်ပါ\n3. Page Access Token ကို generate လုပ်ပါ\n4. Webhook URL: https://yourdomain.com/webhook/facebook\n5. Verify Token ကို set လုပ်ပါ',
        'initial_greeting': 'Hello! Welcome to our Facebook Messenger support. How can I help you today?',
        'steps': [
            {
                'type': 'message',
                'content': 'Thank you for contacting us! I\'m here to help you with any questions or issues.'
            },
            {
                'type': 'question',
                'content': 'What is your name?',
                'variables': {'user_name': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'user_name'}]
            },
            {
                'type': 'message',
                'content': 'Nice to meet you, {user_name}! What can I help you with today?'
            },
            {
                'type': 'question',
                'content': 'Please describe your issue or question:',
                'variables': {'issue_description': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'issue_description'}]
            },
            {
                'type': 'message',
                'content': 'Thank you! Our support team will review your request and get back to you soon via Messenger.'
            }
        ]
    },
    'facebook_lead_generator': {
        'platform': 'facebook',
        'name': 'Facebook Lead Generator Bot',
        'description': 'Facebook Messenger အတွက် Lead Generation Bot. Facebook Lead Ads integration လိုအပ်ပါသည်။',
        'integration_guide': 'Facebook Lead Ads Integration:\n1. Facebook Ads Manager တွင် Lead Ad campaign ဖန်တီးပါ\n2. Lead Form ကို configure လုပ်ပါ\n3. Webhook URL: https://yourdomain.com/webhook/facebook/leads\n4. Page Access Token ကို Dashboard တွင် configure လုပ်ပါ',
        'initial_greeting': 'Hi! Interested in learning more? Let\'s get started!',
        'steps': [
            {
                'type': 'message',
                'content': 'Great! I\'d love to help you. Let me collect some information.'
            },
            {
                'type': 'question',
                'content': 'What is your full name?',
                'variables': {'lead_name': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_name'}]
            },
            {
                'type': 'question',
                'content': 'What is your email address?',
                'variables': {'lead_email': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_email'}]
            },
            {
                'type': 'question',
                'content': 'What is your phone number?',
                'variables': {'lead_phone': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'lead_phone'}]
            },
            {
                'type': 'message',
                'content': 'Thank you, {lead_name}! We\'ve received your information. Someone from our team will contact you at {lead_email} soon.'
            }
        ]
    },
    'facebook_product_catalog': {
        'platform': 'facebook',
        'name': 'Facebook Product Catalog Bot',
        'description': 'Facebook Messenger အတွက် Product Catalog Bot. Facebook Catalog API integration လိုအပ်ပါသည်။',
        'integration_guide': 'Facebook Catalog Integration:\n1. Facebook Business Manager တွင် Catalog ဖန်တီးပါ\n2. Products ကို add လုပ်ပါ\n3. Catalog API endpoint ကို configure လုပ်ပါ\n4. Webhook: https://yourdomain.com/webhook/facebook/catalog',
        'initial_greeting': 'Hello! Browse our products and get instant information.',
        'steps': [
            {
                'type': 'message',
                'content': 'I can help you find products, check prices, and answer questions!'
            },
            {
                'type': 'question',
                'content': 'What product are you looking for?',
                'variables': {'product_name': '{answer}'},
                'actions': [{'type': 'save_answer', 'variable': 'product_name'}]
            },
            {
                'type': 'api_call',
                'content': 'Searching for {product_name}...',
                'api_config': {
                    'url': 'https://graph.facebook.com/v18.0/your_catalog_id/products?search={{product_name}}',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_PAGE_ACCESS_TOKEN"}',
                    'body': '{}'
                },
                'response_template': 'Found products: {{api_response.data}}. Price: {{api_response.price}}'
            }
        ]
    },
    
    # ==================== YOUTUBE TEMPLATES ====================
    'youtube_comment_moderator': {
        'platform': 'youtube',
        'name': 'YouTube Comment Moderator Bot',
        'description': 'YouTube comments ကို moderate လုပ်သော Bot. YouTube Data API v3 လိုအပ်ပါသည်။',
        'integration_guide': 'YouTube API Integration:\n1. Google Cloud Console တွင် project ဖန်တီးပါ\n2. YouTube Data API v3 ကို enable လုပ်ပါ\n3. OAuth 2.0 credentials ကို create လုပ်ပါ\n4. API Key ကို Dashboard တွင် configure လုပ်ပါ\n5. Webhook: https://yourdomain.com/webhook/youtube/comments',
        'initial_greeting': 'YouTube Comment Moderation Bot is active.',
        'steps': [
            {
                'type': 'message',
                'content': 'Monitoring comments on your YouTube channel...'
            },
            {
                'type': 'webhook',
                'content': 'Processing new comment...',
                'webhook_config': {
                    'url': 'https://yourdomain.com/webhook/youtube/comments',
                    'method': 'POST',
                    'headers': '{"Authorization": "Bearer YOUR_YOUTUBE_API_KEY", "Content-Type": "application/json"}',
                    'body': '{"videoId": "{{video_id}}", "commentId": "{{comment_id}}", "text": "{{comment_text}}"}'
                },
                'response_template': 'Comment processed: {{webhook_response.status}}'
            },
            {
                'type': 'api_call',
                'content': 'Checking comment sentiment...',
                'api_config': {
                    'url': 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={{video_id}}',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_YOUTUBE_API_KEY"}',
                    'body': '{}'
                },
                'response_template': 'Comment moderation result: {{api_response.moderation_status}}'
            }
        ]
    },
    'youtube_engagement_bot': {
        'platform': 'youtube',
        'name': 'YouTube Engagement Bot',
        'description': 'YouTube channel engagement ကို မြှင့်တင်သော Bot. YouTube Analytics API လိုအပ်ပါသည်။',
        'integration_guide': 'YouTube Analytics Integration:\n1. Google Cloud Console တွင် project ဖန်တီးပါ\n2. YouTube Analytics API ကို enable လုပ်ပါ\n3. OAuth 2.0 credentials ကို create လုပ်ပါ\n4. Channel ID ကို configure လုပ်ပါ\n5. Webhook: https://yourdomain.com/webhook/youtube/analytics',
        'initial_greeting': 'YouTube Engagement Bot is monitoring your channel.',
        'steps': [
            {
                'type': 'message',
                'content': 'Tracking video performance and engagement metrics...'
            },
            {
                'type': 'api_call',
                'content': 'Fetching channel analytics...',
                'api_config': {
                    'url': 'https://youtubeanalytics.googleapis.com/v2/reports?ids=channel=={{channel_id}}&metrics=views,likes,comments&dimensions=video',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_OAUTH_TOKEN"}',
                    'body': '{}'
                },
                'response_template': 'Channel stats: Views: {{api_response.views}}, Likes: {{api_response.likes}}, Comments: {{api_response.comments}}'
            }
        ]
    },
    
    # ==================== TIKTOK TEMPLATES ====================
    'tiktok_comment_moderator': {
        'platform': 'tiktok',
        'name': 'TikTok Comment Moderator Bot',
        'description': 'TikTok comments ကို moderate လုပ်သော Bot. TikTok Open API လိုအပ်ပါသည်။',
        'integration_guide': 'TikTok API Integration:\n1. TikTok for Developers portal တွင် app ဖန်တီးပါ\n2. Open API access ကို request လုပ်ပါ\n3. Client Key & Client Secret ကို generate လုပ်ပါ\n4. OAuth 2.0 flow ကို implement လုပ်ပါ\n5. Webhook: https://yourdomain.com/webhook/tiktok/comments',
        'initial_greeting': 'TikTok Comment Moderation Bot is active.',
        'steps': [
            {
                'type': 'message',
                'content': 'Monitoring comments on your TikTok videos...'
            },
            {
                'type': 'webhook',
                'content': 'Processing new comment...',
                'webhook_config': {
                    'url': 'https://yourdomain.com/webhook/tiktok/comments',
                    'method': 'POST',
                    'headers': '{"Authorization": "Bearer YOUR_TIKTOK_ACCESS_TOKEN", "Content-Type": "application/json"}',
                    'body': '{"video_id": "{{video_id}}", "comment_id": "{{comment_id}}", "text": "{{comment_text}}"}'
                },
                'response_template': 'Comment processed: {{webhook_response.status}}'
            }
        ]
    },
    'tiktok_engagement_tracker': {
        'platform': 'tiktok',
        'name': 'TikTok Engagement Tracker Bot',
        'description': 'TikTok video engagement metrics ကို track လုပ်သော Bot. TikTok Analytics API လိုအပ်ပါသည်။',
        'integration_guide': 'TikTok Analytics Integration:\n1. TikTok for Developers portal တွင် app ဖန်တီးပါ\n2. Analytics API access ကို request လုပ်ပါ\n3. OAuth 2.0 credentials ကို configure လုပ်ပါ\n4. Webhook: https://yourdomain.com/webhook/tiktok/analytics',
        'initial_greeting': 'TikTok Engagement Tracker is monitoring your account.',
        'steps': [
            {
                'type': 'message',
                'content': 'Tracking video performance: views, likes, shares, comments...'
            },
            {
                'type': 'api_call',
                'content': 'Fetching video analytics...',
                'api_config': {
                    'url': 'https://open.tiktokapis.com/v2/research/video/query/?fields=video_id,view_count,like_count,share_count,comment_count',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_TIKTOK_ACCESS_TOKEN"}',
                    'body': '{}'
                },
                'response_template': 'Video stats: Views: {{api_response.view_count}}, Likes: {{api_response.like_count}}, Shares: {{api_response.share_count}}'
            }
        ]
    },
    'tiktok_hashtag_tracker': {
        'platform': 'tiktok',
        'name': 'TikTok Hashtag Tracker Bot',
        'description': 'TikTok hashtag performance ကို track လုပ်သော Bot. TikTok Research API လိုအပ်ပါသည်။',
        'integration_guide': 'TikTok Research API Integration:\n1. TikTok for Developers portal တွင် Research API access ကို apply လုပ်ပါ\n2. Client credentials ကို generate လုပ်ပါ\n3. Access token ကို obtain လုပ်ပါ\n4. Webhook: https://yourdomain.com/webhook/tiktok/hashtags',
        'initial_greeting': 'TikTok Hashtag Tracker is monitoring trending hashtags.',
        'steps': [
            {
                'type': 'message',
                'content': 'Tracking hashtag performance and trends...'
            },
            {
                'type': 'api_call',
                'content': 'Fetching hashtag data...',
                'api_config': {
                    'url': 'https://open.tiktokapis.com/v2/research/hashtag/query/?hashtag_name={{hashtag}}',
                    'method': 'GET',
                    'headers': '{"Authorization": "Bearer YOUR_TIKTOK_ACCESS_TOKEN"}',
                    'body': '{}'
                },
                'response_template': 'Hashtag stats: {{api_response.hashtag_name}} - Views: {{api_response.view_count}}'
            }
        ]
    }
}

def get_template(template_id):
    """Get a bot template by ID"""
    return BOT_TEMPLATES.get(template_id)

def list_templates(platform=None):
    """List all available templates, optionally filtered by platform"""
    templates = []
    for template_id, template in BOT_TEMPLATES.items():
        if platform is None or template.get('platform') == platform:
            templates.append({
                'id': template_id,
                'name': template['name'],
                'description': template['description'],
                'platform': template.get('platform', 'general'),
                'integration_guide': template.get('integration_guide', '')
            })
    return templates

def get_templates_by_platform():
    """Get templates organized by platform"""
    platforms = {
        'telegram': [],
        'facebook': [],
        'youtube': [],
        'tiktok': []
    }
    
    for template_id, template in BOT_TEMPLATES.items():
        platform = template.get('platform', 'general')
        if platform in platforms:
            platforms[platform].append({
                'id': template_id,
                'name': template['name'],
                'description': template['description'],
                'integration_guide': template.get('integration_guide', '')
            })
    
    return platforms

def create_bot_from_template(template_id, bot_name=None):
    """Create a bot configuration from a template"""
    template = get_template(template_id)
    if not template:
        return None
    
    bot_config = {
        'bot_name': bot_name or template['name'],
        'initial_greeting': template['initial_greeting'],
        'steps': template['steps']
    }
    
    return bot_config
