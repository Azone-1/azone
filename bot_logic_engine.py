# bot_logic_engine.py
# Advanced Bot Logic Engine with Intent Recognition, Context Awareness, and Conditional Logic
import re
import json
import requests
from datetime import datetime
from urllib.parse import urlparse

class BotLogicEngine:
    """Advanced bot logic engine with intent recognition and context awareness"""
    
    def __init__(self, bot_config):
        self.bot_config = bot_config
        self.steps = bot_config.get('steps', [])
        self.initial_greeting = bot_config.get('initial_greeting', '')
        
    def recognize_intent(self, user_message):
        """
        Recognize user intent from message
        Returns: (intent, confidence, matched_keywords)
        """
        user_msg_lower = user_message.lower().strip()
        
        # Common intents and their keywords
        intent_patterns = {
            'greeting': ['မင်္ဂလာပါ', 'hello', 'hi', 'hey', 'ဟေး', 'နေကောင်းလား', 'ဘာတွေလုပ်နေလဲ'],
            'question': ['ဘာ', 'ဘယ်', 'ဘယ်လို', 'ဘယ်သူ', 'ဘယ်နေရာ', 'what', 'where', 'when', 'who', 'how', 'why', '?'],
            'affirmation': ['ဟုတ်ကဲ့', 'ဟုတ်ပါ', 'ရပါတယ်', 'ဖြစ်ပါတယ်', 'ok', 'yes', 'yeah', 'sure', 'okay'],
            'negation': ['မဟုတ်ပါ', 'မဟုတ်ဘူး', 'no', 'not', 'မဖြစ်ဘူး'],
            'command': ['လုပ်ပေးပါ', 'ပြပေးပါ', 'ရှာပေးပါ', 'ဖွင့်ပေးပါ', 'do', 'show', 'open', 'get', 'find'],
            'farewell': ['ကျေးဇူးတင်ပါတယ်', 'ပြန်တွေ့မယ်', 'bye', 'goodbye', 'see you', 'thanks', 'thank you']
        }
        
        matched_intent = None
        max_confidence = 0
        matched_keywords = []
        
        for intent, keywords in intent_patterns.items():
            matches = [kw for kw in keywords if kw in user_msg_lower]
            if matches:
                confidence = len(matches) / len(keywords) if keywords else 0
                if confidence > max_confidence:
                    max_confidence = confidence
                    matched_intent = intent
                    matched_keywords = matches
        
        # If no intent matched, try to match with step content
        if not matched_intent:
            for step in self.steps:
                step_content = step.get('content', '').lower()
                step_keywords = [w for w in step_content.split() if len(w) > 3]
                matches = [kw for kw in step_keywords if kw in user_msg_lower]
                if matches:
                    matched_intent = 'step_match'
                    max_confidence = len(matches) / max(len(step_keywords), 1)
                    matched_keywords = matches
                    break
        
        return matched_intent or 'unknown', max_confidence, matched_keywords
    
    def extract_variables(self, text, session_data):
        """Extract and replace variables in text (e.g., {user_name}, {date}, {time})"""
        if not text:
            return text
        
        # Get current date/time
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        # Replace common variables using regex to replace ALL occurrences
        text = re.sub(r'\{date\}', date_str, text)
        text = re.sub(r'\{time\}', time_str, text)
        text = re.sub(r'\{datetime\}', datetime_str, text)
        
        # Replace session variables (support both {var} and {{var}} formats)
        # Use regex to find and replace ALL occurrences of each variable
        if 'variables' in session_data and isinstance(session_data['variables'], dict):
            for key, value in session_data['variables'].items():
                if key and value is not None:
                    # Escape special regex characters in the key
                    escaped_key = re.escape(key)
                    value_str = str(value)
                    
                    # Replace {variable} format - match {key} exactly
                    # Use word boundaries or ensure we match the full variable name
                    pattern_single = r'\{' + escaped_key + r'\}'
                    text = re.sub(pattern_single, value_str, text)
                    
                    # Replace {{variable}} format (double braces for API calls/JSON)
                    pattern_double = r'\{\{' + escaped_key + r'\}\}'
                    text = re.sub(pattern_double, value_str, text)
        
        return text
    
    def replace_variables_in_json(self, json_str, session_data):
        """Replace variables in JSON string (supports {{variable}} format)"""
        if not json_str:
            return json_str
        
        try:
            # First replace variables in the string using extract_variables
            replaced_str = self.extract_variables(json_str, session_data)
            
            # Also handle {{variable}} format specifically for API calls
            if 'variables' in session_data:
                for key, value in session_data['variables'].items():
                    # Replace {{variable}} format (double braces for JSON)
                    replaced_str = replaced_str.replace(f'{{{{' + key + '}}}}', str(value))
            
            return replaced_str
        except Exception as e:
            print(f"Error replacing variables in JSON: {e}")
            return json_str
    
    def make_api_call(self, api_config, session_data):
        """
        Make an external API call based on configuration
        
        Args:
            api_config (dict): API configuration with url, method, headers, body
            session_data (dict): Session data containing variables
        
        Returns:
            tuple: (success: bool, response_data: dict or str, error: str or None)
        """
        try:
            # Extract and replace variables in URL (e.g., {{server_name}} in URL)
            url = self.extract_variables(api_config.get('url', ''), session_data)
            if not url:
                return (False, None, 'API URL is required')
            print(f"DEBUG: API Request URL (after variable replacement): {url}")
            
            # Validate URL
            try:
                parsed = urlparse(url)
                if not parsed.scheme or not parsed.netloc:
                    return (False, None, 'Invalid API URL format')
            except:
                return (False, None, 'Invalid API URL format')
            
            method = api_config.get('method', 'POST').upper()
            
            # Parse and replace variables in headers
            headers = {}
            headers_str = api_config.get('headers', '{}')
            if headers_str:
                try:
                    headers_str = self.replace_variables_in_json(headers_str, session_data)
                    headers = json.loads(headers_str)
                    if not isinstance(headers, dict):
                        headers = {}
                except json.JSONDecodeError:
                    return (False, None, 'Invalid headers JSON format')
            
            # Parse and replace variables in body
            # Session variables (like 'server_name') will be replaced in the body
            body = None
            body_str = api_config.get('body', '{}')
            if body_str and method in ['POST', 'PUT']:
                try:
                    # Replace variables in body string (e.g., {{server_name}} -> actual value)
                    body_str = self.replace_variables_in_json(body_str, session_data)
                    body = json.loads(body_str)
                    print(f"DEBUG: API Request Body (after variable replacement): {body}")
                except json.JSONDecodeError as e:
                    print(f"DEBUG: JSON decode error in body: {e}, body_str: {body_str}")
                    return (False, None, 'Invalid body JSON format')
            
            # Make API request with latency tracking
            timeout = 10  # 10 seconds timeout
            import time
            start_time = time.time()
            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, timeout=timeout)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=body, timeout=timeout)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=body, timeout=timeout)
                else:
                    return (False, None, f'Unsupported HTTP method: {method}', 0)
                
                latency = time.time() - start_time
                
                # Check response status
                response.raise_for_status()
                
                # Parse response
                try:
                    response_data = response.json()
                except:
                    response_data = response.text
                
                return (True, response_data, None, latency)
                
            except requests.exceptions.Timeout:
                latency = time.time() - start_time
                return (False, None, 'API request timeout', latency)
            except requests.exceptions.ConnectionError:
                latency = time.time() - start_time
                return (False, None, 'Failed to connect to API', latency)
            except requests.exceptions.HTTPError as e:
                latency = time.time() - start_time
                return (False, None, f'API HTTP error: {e.response.status_code} - {e.response.text[:100]}', latency)
            except Exception as e:
                latency = time.time() - start_time
                return (False, None, f'API request error: {str(e)}', latency)
                
        except Exception as e:
            return (False, None, f'API call error: {str(e)}', 0)
    
    def evaluate_condition(self, condition, session_data):
        """Evaluate a condition based on session data"""
        if not condition:
            return True
        
        condition_type = condition.get('type', 'always')
        
        if condition_type == 'always':
            return True
        elif condition_type == 'variable_equals':
            var_name = condition.get('variable')
            expected_value = condition.get('value')
            actual_value = session_data.get('variables', {}).get(var_name)
            return str(actual_value) == str(expected_value)
        elif condition_type == 'step_completed':
            step_index = condition.get('step_index')
            completed_steps = session_data.get('completed_steps', [])
            return step_index in completed_steps
        elif condition_type == 'contains_keyword':
            user_message = session_data.get('last_user_message', '')
            keywords = condition.get('keywords', [])
            return any(kw.lower() in user_message.lower() for kw in keywords)
        
        return True
    
    def process_step(self, step, session_data):
        """Process a step and return response with actions"""
        step_type = step.get('type', 'message')
        content = step.get('content', '')
        condition = step.get('condition')
        actions = step.get('actions', [])
        variables = step.get('variables', {})
        api_config = step.get('api_config', {})
        api_latency = None  # Initialize api_latency at the start
        
        # Check condition
        if not self.evaluate_condition(condition, session_data):
            return None, None, api_latency
        
        response = ""
        executed_actions = []
        
        # Handle webhook type (similar to API call but for external integrations)
        api_latency = None
        if step_type == 'webhook':
            webhook_config = step.get('webhook_config', {})
            if webhook_config:
                # Webhook is essentially an API call with different semantics
                # Use the same API call logic but mark it as webhook
                success, webhook_response, error, latency = self.make_api_call(webhook_config, session_data)
                api_latency = latency
                
                if success:
                    # Store webhook response
                    if 'variables' not in session_data:
                        session_data['variables'] = {}
                    session_data['variables']['webhook_result'] = webhook_response
                    
                    # Use response template if provided
                    response_template = webhook_config.get('response_template', 'Webhook triggered successfully.')
                    if response_template:
                        response = response_template.replace('{{webhook_response}}', str(webhook_response))
                        response = self.extract_variables(response, session_data)
                    else:
                        response = f"Webhook triggered. Response: {webhook_response}"
                    
                    executed_actions.append("Webhook executed successfully")
                else:
                    error_msg = error or "Unknown webhook error"
                    response = f"Webhook failed: {error_msg}"
                    executed_actions.append(f"Webhook failed: {error_msg}")
            else:
                response = "Webhook configuration not found"
        
        # Handle API call type
        elif step_type == 'api_call':
            if api_config:
                success, api_response, error, latency = self.make_api_call(api_config, session_data)
                api_latency = latency
                
                if success:
                    # Store API response in session variables as 'api_result'
                    if 'variables' not in session_data:
                        session_data['variables'] = {}
                    # Save API response as 'api_result' variable
                    if isinstance(api_response, (dict, list)):
                        session_data['variables']['api_result'] = api_response
                        # Also save as JSON string for text replacement
                        session_data['variables']['api_response'] = json.dumps(api_response, ensure_ascii=False)
                    else:
                        session_data['variables']['api_result'] = api_response
                        session_data['variables']['api_response'] = str(api_response)
                    print(f"DEBUG: Saved API response to 'api_result' variable: {session_data['variables'].get('api_result')}")
                    
                    # Use response template if provided
                    response_template = api_config.get('response_template', 'API call completed successfully.')
                    if response_template:
                        # Replace {{api_response}} in template
                        response = response_template.replace('{{api_response}}', str(api_response))
                        response = self.extract_variables(response, session_data)
                    else:
                        response = f"API call successful. Response: {api_response}"
                    
                    executed_actions.append("API call executed successfully")
                else:
                    # Handle API error
                    error_msg = error or "Unknown API error"
                    response = f"API call failed: {error_msg}"
                    executed_actions.append(f"API call failed: {error_msg}")
            else:
                response = "API configuration not found"
        else:
            # Handle message/question types
            # Check if content is empty
            if not content or not content.strip():
                # If content is empty, provide default message based on step type
                if step_type == 'question':
                    response = "ကျေးဇူးပြု၍ မေးခွန်း ထည့်သွင်းပါ။"
                elif step_type == 'message':
                    response = "Message content is empty. Please add content to this step."
                else:
                    response = "Step content is empty. Please configure this step."
            else:
                # Extract variables in content
                response = self.extract_variables(content, session_data)
            
            # Process actions
            for action in actions:
                action_type = action.get('type')
                if action_type == 'set_variable':
                    var_name = action.get('variable')
                    var_value = action.get('value')
                    if 'variables' not in session_data:
                        session_data['variables'] = {}
                    session_data['variables'][var_name] = var_value
                    executed_actions.append(f"Set variable {var_name} = {var_value}")
                elif action_type == 'save_answer':
                    var_name = action.get('variable', 'answer')
                    if 'variables' not in session_data:
                        session_data['variables'] = {}
                    session_data['variables'][var_name] = session_data.get('last_user_message', '')
                    executed_actions.append(f"Saved answer to {var_name}")
        
        # Set variables from step
        if variables:
            if 'variables' not in session_data:
                session_data['variables'] = {}
            session_data['variables'].update(variables)
        
        return response, executed_actions, api_latency
    
    def find_matching_step(self, user_message, session_data, current_step_index=None):
        """Find the best matching step for user message"""
        intent, confidence, keywords = self.recognize_intent(user_message)
        user_msg_lower = user_message.lower()
        
        # If there's a current step, prioritize next steps
        if current_step_index is not None and current_step_index < len(self.steps):
            current_step = self.steps[current_step_index]
            
            # If current step is a question, check for answer
            if current_step.get('type') == 'question':
                # Check if user message seems like an answer
                triggers = current_step.get('triggers', [])
                if triggers:
                    # Check if user message matches any trigger
                    for trigger in triggers:
                        if isinstance(trigger, str) and trigger.lower() in user_msg_lower:
                            return current_step_index, 'trigger_match', confidence
                
                # Default: accept any non-empty answer
                if user_message.strip():
                    return current_step_index, 'answer', 0.8
        
        # Search for matching step
        best_match_index = None
        best_match_type = None
        best_confidence = 0
        
        for i, step in enumerate(self.steps):
            step_content = step.get('content', '').lower()
            step_type = step.get('type', 'message')
            triggers = step.get('triggers', [])
            
            # Check triggers first
            if triggers:
                for trigger in triggers:
                    if isinstance(trigger, str) and trigger.lower() in user_msg_lower:
                        if confidence > best_confidence:
                            best_match_index = i
                            best_match_type = 'trigger'
                            best_confidence = confidence
            
            # Check keyword matching
            step_keywords = [w for w in step_content.split() if len(w) > 3]
            matches = [kw for kw in step_keywords if kw in user_msg_lower]
            if matches:
                match_confidence = len(matches) / max(len(step_keywords), 1)
                if match_confidence > best_confidence:
                    best_match_index = i
                    best_match_type = 'keyword'
                    best_confidence = match_confidence
            
            # Check direct content match
            if step_content in user_msg_lower or user_msg_lower in step_content:
                if 0.9 > best_confidence:
                    best_match_index = i
                    best_match_type = 'direct'
                    best_confidence = 0.9
        
        return best_match_index, best_match_type, best_confidence
    
    def process_message(self, user_message, session_data):
        """
        Main method to process user message and return bot response
        
        Returns:
            dict: {
                'bot_response': str,
                'session_data': dict,
                'intent': str,
                'confidence': float,
                'step_index': int or None
            }
        """
        # Initialize session if needed
        if not session_data:
            session_data = {
                'conversation_started': False,
                'current_step': None,
                'step_history': [],
                'completed_steps': [],
                'variables': {},
                'last_user_message': user_message,
                'waiting_for_answer': False,
                'question_step_id': None
            }
        
        session_data['last_user_message'] = user_message
        
        # First message - return greeting only, wait for user input
        if not session_data.get('conversation_started', False):
            greeting = self.extract_variables(self.initial_greeting, session_data)
            session_data['conversation_started'] = True
            
            # After greeting, set current_step to first step (if exists) but don't process it yet
            # Wait for user input before processing first step
            if len(self.steps) > 0:
                session_data['current_step'] = 0  # Set to first step, but wait for user input
                new_step_index = 0
            else:
                session_data['current_step'] = None
                new_step_index = None
            
            # Return only greeting, wait for user to respond
            return {
                'bot_response': greeting,
                'session_data': session_data,
                'intent': 'greeting',
                'confidence': 1.0,
                'step_index': new_step_index
            }
        
        # Get current step index
        current_step_index = session_data.get('current_step')
        
        # Recognize intent
        intent, intent_confidence, keywords = self.recognize_intent(user_message)
        
        bot_response = ""
        new_step_index = None
        api_latency = None  # Initialize api_latency to avoid "cannot access local variable" error
        
        # If we have a current step, process it based on its type
        if current_step_index is not None and current_step_index < len(self.steps):
            current_step = self.steps[current_step_index]
            current_step_type = current_step.get('type', 'message')
            
            if current_step_type == 'question':
                # Check if we're waiting for answer or showing question for first time
                waiting_for_answer = session_data.get('waiting_for_answer', False)
                question_step_id = session_data.get('question_step_id')
                
                if not waiting_for_answer or question_step_id != current_step_index:
                    # First time showing this question - show it and STOP, wait for answer
                    response, actions, api_latency = self.process_step(current_step, session_data)
                    if response:
                        bot_response = response
                        session_data['waiting_for_answer'] = True
                        session_data['question_step_id'] = current_step_index
                        new_step_index = current_step_index
                        # Stay on current step, wait for user answer
                        session_data['current_step'] = current_step_index
                    else:
                        bot_response = "ကျေးဇူးပြု၍ ထပ်မံ မေးခွန်း မေးပါ။"
                else:
                    # User is answering the question - accept answer and save to variable
                    # Save answer to variable (check both actions and variables field)
                    if 'variables' not in session_data:
                        session_data['variables'] = {}
                    
                    # Method 1: Check actions field for save_answer
                    if 'actions' in current_step and current_step.get('actions'):
                        for action in current_step.get('actions', []):
                            if isinstance(action, dict) and action.get('type') == 'save_answer':
                                var_name = action.get('variable', 'answer')
                                session_data['variables'][var_name] = user_message
                                print(f"DEBUG: Saved answer '{user_message}' to variable '{var_name}' via actions")
                    
                    # Method 2: Check variables field directly (from step configuration)
                    if 'variables' in current_step and current_step.get('variables'):
                        step_variables = current_step.get('variables', {})
                        if isinstance(step_variables, dict):
                            for var_name, var_value in step_variables.items():
                                # If variable value is '{answer}' or similar, save user message
                                if '{answer}' in str(var_value) or var_value == '' or var_value is None:
                                    session_data['variables'][var_name] = user_message
                                    print(f"DEBUG: Saved answer '{user_message}' to variable '{var_name}' via variables field")
                    
                    # Debug logging
                    print(f"DEBUG: Question step answered with: '{user_message}'")
                    print(f"DEBUG: Current step variables: {current_step.get('variables', {})}")
                    print(f"DEBUG: Current step actions: {current_step.get('actions', [])}")
                    print(f"DEBUG: Session variables after save: {session_data.get('variables', {})}")
                    
                    # Mark current step as completed
                    if current_step_index not in session_data.get('completed_steps', []):
                        if 'completed_steps' not in session_data:
                            session_data['completed_steps'] = []
                        session_data['completed_steps'].append(current_step_index)
                    
                    # Reset question flags
                    session_data['waiting_for_answer'] = False
                    session_data['question_step_id'] = None
                    
                    # After answering question, move to next step and process it
                    # But if next step is message/api, STOP after showing it (don't auto-continue)
                    next_index = current_step_index + 1
                    if next_index < len(self.steps):
                        next_step = self.steps[next_index]
                        next_response, _, _ = self.process_step(next_step, session_data)
                        if next_response:
                            bot_response = next_response
                            
                            # Mark next step as completed if it's message/api
                            if next_step.get('type') in ['message', 'api_call']:
                                if next_index not in session_data.get('completed_steps', []):
                                    if 'completed_steps' not in session_data:
                                        session_data['completed_steps'] = []
                                    session_data['completed_steps'].append(next_index)
                            
                            # If next step is a question, set waiting flag and STOP
                            if next_step.get('type') == 'question':
                                session_data['waiting_for_answer'] = True
                                session_data['question_step_id'] = next_index
                                new_step_index = next_index
                                session_data['current_step'] = next_index
                                # STOP - wait for user to answer the question
                            # If next step is message/api, STOP after showing it (FIXED: Don't auto-continue)
                            elif next_step.get('type') in ['message', 'api_call']:
                                # Move to next-next step index but DON'T process it yet - STOP and wait
                                next_next_index = next_index + 1
                                if next_next_index < len(self.steps):
                                    session_data['current_step'] = next_next_index
                                    new_step_index = next_next_index
                                else:
                                    session_data['current_step'] = None
                                    new_step_index = None
                                # STOP HERE - wait for user to send another message
                                # Don't automatically process next-next step
                        else:
                            # Condition not met, stay on next step
                            new_step_index = next_index
                            session_data['current_step'] = next_index
                    else:
                        # No more steps - conversation ended
                        bot_response = "ကျေးဇူးတင်ပါတယ်! စကားပြောဆိုမှု ပြီးဆုံးပါပြီ။"
                        new_step_index = None
                        session_data['current_step'] = None
                    
            elif current_step_type == 'message':
                # Current step is a message - process it and STOP, wait for user input
                response, actions, api_latency = self.process_step(current_step, session_data)
                if response:
                    bot_response = response
                    
                    # Mark current step as completed
                    if current_step_index not in session_data.get('completed_steps', []):
                        if 'completed_steps' not in session_data:
                            session_data['completed_steps'] = []
                        session_data['completed_steps'].append(current_step_index)
                    
                    # Move to next step index but DON'T process it yet - wait for user input
                    next_index = current_step_index + 1
                    if next_index < len(self.steps):
                        # Set current_step to next step, but don't process it
                        # Wait for user to send another message
                        new_step_index = next_index
                        session_data['current_step'] = next_index
                    else:
                        # No more steps
                        new_step_index = None
                        session_data['current_step'] = None
                else:
                    bot_response = "ကျေးဇူးပြု၍ ထပ်မံ မေးခွန်း မေးပါ။"
                    
            elif current_step_type in ['api_call', 'webhook']:
                # Process API call or webhook step and automatically continue to next step
                response, actions, api_latency = self.process_step(current_step, session_data)
                if response:
                    bot_response = response
                    
                    # Mark current step as completed
                    if current_step_index not in session_data.get('completed_steps', []):
                        if 'completed_steps' not in session_data:
                            session_data['completed_steps'] = []
                        session_data['completed_steps'].append(current_step_index)
                    
                    # After API call completes, automatically move to next step and process it
                    next_index = current_step_index + 1
                    if next_index < len(self.steps):
                        next_step = self.steps[next_index]
                        next_response, _, _ = self.process_step(next_step, session_data)
                        if next_response:
                            # Combine API response with next step response
                            bot_response = f"{bot_response}\n\n{next_response}"
                            
                            # Mark next step as completed if it's message/api
                            if next_step.get('type') in ['message', 'api_call']:
                                if next_index not in session_data.get('completed_steps', []):
                                    if 'completed_steps' not in session_data:
                                        session_data['completed_steps'] = []
                                    session_data['completed_steps'].append(next_index)
                            
                            # If next step is a question, set waiting flag and STOP
                            if next_step.get('type') == 'question':
                                session_data['waiting_for_answer'] = True
                                session_data['question_step_id'] = next_index
                                new_step_index = next_index
                                session_data['current_step'] = next_index
                                # STOP - wait for user to answer the question
                            # If next step is message/api, move to next-next step but DON'T process it yet
                            elif next_step.get('type') in ['message', 'api_call']:
                                next_next_index = next_index + 1
                                if next_next_index < len(self.steps):
                                    session_data['current_step'] = next_next_index
                                    new_step_index = next_next_index
                                else:
                                    session_data['current_step'] = None
                                    new_step_index = None
                                # STOP - wait for user input
                        else:
                            # Condition not met for next step, stay on next step
                            new_step_index = next_index
                            session_data['current_step'] = next_index
                    else:
                        # No more steps
                        new_step_index = None
                        session_data['current_step'] = None
                else:
                    bot_response = "API call failed. Please try again."
        else:
            # No current step - try to find matching step by triggers/keywords
            matched_index, match_type, confidence = self.find_matching_step(
                user_message, session_data, None
            )
            
            if matched_index is not None:
                # Found matching step
                step = self.steps[matched_index]
                response, actions, api_latency = self.process_step(step, session_data)
                if response:
                    bot_response = response
                    new_step_index = matched_index
                    session_data['current_step'] = matched_index
                    
                    # If it's a message step, also show next step if available
                    if step.get('type') == 'message':
                        next_index = matched_index + 1
                        if next_index < len(self.steps):
                            next_step = self.steps[next_index]
                            next_response, _, _ = self.process_step(next_step, session_data)
                            if next_response:
                                bot_response = f"{bot_response}\n\n{next_response}"
                                new_step_index = next_index
                                session_data['current_step'] = next_index
            else:
                # No match found
                if intent == 'question':
                    bot_response = "ကျေးဇူးပြု၍ ပိုမို ရှင်းလင်းစွာ မေးခွန်း မေးပါ။"
                elif intent == 'farewell':
                    bot_response = "ကျေးဇူးတင်ပါတယ်! ပြန်တွေ့မယ်။"
                else:
                    bot_response = "ကျွန်ုပ် နားမလည်ပါ။ ကျေးဇူးပြု၍ ထပ်မံ မေးခွန်း မေးပါ။"
                new_step_index = None
        
        # Update session (current_step already updated above)
        if 'step_history' not in session_data:
            session_data['step_history'] = []
        session_data['step_history'].append({
            'user_message': user_message,
            'bot_response': bot_response,
            'step_index': new_step_index,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get step type for logging
        step_type = None
        if new_step_index is not None and new_step_index < len(self.steps):
            step_type = self.steps[new_step_index].get('type')
        elif current_step_index is not None and current_step_index < len(self.steps):
            step_type = self.steps[current_step_index].get('type')
        
        # Final pass: Ensure all variables in bot_response are substituted
        # This catches any edge cases where variables might not have been replaced earlier
        if bot_response:
            bot_response = self.extract_variables(bot_response, session_data)
        
        return {
            'bot_response': bot_response,
            'session_data': session_data,
            'intent': intent,
            'confidence': max(intent_confidence, 0.8 if new_step_index is not None else 0.5),
            'step_index': new_step_index,
            'step_type': step_type,
            'api_latency': api_latency
        }

