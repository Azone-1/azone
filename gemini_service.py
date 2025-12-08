"""
Gemini AI Service Integration
Provides conversational AI capabilities using Google's Gemini API
"""
import os
import json
from typing import Optional, Dict, Any

# Try to import config for API key
try:
    import config
    DEFAULT_API_KEY = config.Config.GEMINI_API_KEY
except ImportError:
    DEFAULT_API_KEY = None

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini service
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment variable GEMINI_API_KEY
        """
        # Try to get API key from parameter, environment variable, or config
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or DEFAULT_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. "
                "Please set GEMINI_API_KEY environment variable or pass api_key parameter."
            )
        
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Try to find an available model
        # Free API keys support these models (tested and working)
        # List of models to try in order of preference
        model_names = [
            'gemini-2.5-flash',      # ✅ WORKING - Fast and efficient (free tier)
            'gemini-flash-latest',   # Latest flash version (free tier)
            'gemini-2.0-flash',      # Alternative flash version
            'gemini-1.5-flash',      # Older but stable
            'gemini-1.5-pro',        # More capable (may have quota limits)
            'gemini-1.0-pro',        # Alternative
        ]
        
        self.model = None
        self.model_name = None
        
        # First, try to list available models from API
        try:
            available_models = []
            print("Checking available Gemini models...")
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.split('/')[-1]  # Extract model name
                    available_models.append(model_name)
                    print(f"  Found: {model_name}")
            
            if available_models:
                # Try to use a preferred model from available ones
                for preferred in model_names:
                    if preferred in available_models:
                        self.model = genai.GenerativeModel(preferred)
                        self.model_name = preferred
                        print(f"✓ Using model: {preferred}")
                        break
                
                # If no preferred model found, use first available
                if self.model is None:
                    model_name = available_models[0]
                    self.model = genai.GenerativeModel(model_name)
                    self.model_name = model_name
                    print(f"✓ Using available model: {model_name}")
            else:
                print("No models found with generateContent support")
        
        except Exception as e:
            print(f"Could not list models: {e}")
            print("Trying direct model initialization...")
            # Fallback: try direct initialization
            for model_name in model_names:
                try:
                    # Test if model works by creating it
                    test_model = genai.GenerativeModel(model_name)
                    # Try a simple test (this will fail if model doesn't exist)
                    # Actually, just creating the model doesn't test it, so we'll catch error in chat
                    self.model = test_model
                    self.model_name = model_name
                    print(f"✓ Initialized model: {model_name} (will test on first use)")
                    break
                except Exception as model_error:
                    print(f"  Model {model_name} not available: {str(model_error)[:100]}")
                    continue
        
        # If still no model, raise error with helpful message
        if self.model is None:
            raise ValueError(
                "Could not initialize any Gemini model with your API key.\n\n"
                "Free API keys usually support:\n"
                "- gemini-1.5-flash (recommended for free tier)\n"
                "- gemini-1.5-pro\n"
                "- gemini-1.0-pro\n\n"
                "Please check:\n"
                "1. Your API key is valid (get a new one from https://makersuite.google.com/app/apikey)\n"
                "2. Your API key has not exceeded rate limits\n"
                "3. Your API key has access to Gemini models\n"
                "4. Try creating a new API key if this one doesn't work"
            )
    
    def chat(self, message: str, conversation_history: Optional[list] = None) -> Dict[str, Any]:
        """
        Send a message to Gemini and get response
        
        Args:
            message: User message to send
            conversation_history: Optional list of previous messages for context
                Format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        
        Returns:
            dict with keys:
                - success: bool
                - response: str (if success)
                - error: str (if not success)
        """
        try:
            # Prepare conversation context
            if conversation_history and len(conversation_history) > 0:
                # Convert conversation history to Gemini format
                # Gemini expects history as list of Content objects with 'parts' and 'role'
                gemini_history = []
                for msg in conversation_history:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        # Convert to Gemini format: {'role': 'user'/'model', 'parts': [{'text': 'content'}]}
                        role = msg['role']
                        # Gemini uses 'model' instead of 'assistant'
                        if role == 'assistant':
                            role = 'model'
                        gemini_history.append({
                            'role': role,
                            'parts': [{'text': str(msg['content'])}]
                        })
                
                # Start chat with formatted history
                if gemini_history:
                    chat = self.model.start_chat(history=gemini_history)
                    response = chat.send_message(message)
                else:
                    # If history conversion failed, use single message
                    response = self.model.generate_content(message)
            else:
                # Single message without history
                response = self.model.generate_content(message)
            
            return {
                'success': True,
                'response': response.text,
                'model': self.model_name
            }
        
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error message for model not found
            if '404' in error_msg or 'not found' in error_msg.lower():
                error_msg = f"Model not available. Please check your API key has access to Gemini models. Original error: {error_msg}"
            return {
                'success': False,
                'error': error_msg
            }
    
    def chat_stream(self, message: str, conversation_history: Optional[list] = None):
        """
        Send a message to Gemini and get streaming response
        
        Args:
            message: User message to send
            conversation_history: Optional list of previous messages for context
        
        Yields:
            dict with keys:
                - chunk: str (text chunk)
                - done: bool (if stream is complete)
        """
        try:
            if conversation_history and len(conversation_history) > 0:
                # Convert conversation history to Gemini format
                gemini_history = []
                for msg in conversation_history:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        role = msg['role']
                        if role == 'assistant':
                            role = 'model'
                        gemini_history.append({
                            'role': role,
                            'parts': [{'text': str(msg['content'])}]
                        })
                
                if gemini_history:
                    chat = self.model.start_chat(history=gemini_history)
                    response = chat.send_message(message, stream=True)
                else:
                    response = self.model.generate_content(message, stream=True)
            else:
                response = self.model.generate_content(message, stream=True)
            
            for chunk in response:
                yield {
                    'chunk': chunk.text,
                    'done': False
                }
            
            yield {
                'chunk': '',
                'done': True
            }
        
        except Exception as e:
            yield {
                'chunk': '',
                'done': True,
                'error': str(e)
            }
    
    @staticmethod
    def is_available() -> bool:
        """Check if Gemini service is available (package installed and key configured)"""
        if not GEMINI_AVAILABLE:
            return False
        
        api_key = os.getenv('GEMINI_API_KEY') or DEFAULT_API_KEY
        return api_key is not None and api_key.strip() != ''


def get_gemini_service() -> Optional[GeminiService]:
    """
    Get a GeminiService instance if available
    
    Returns:
        GeminiService instance or None if not configured
    """
    try:
        return GeminiService()
    except (ValueError, ImportError) as e:
        print(f"Gemini service not available: {e}")
        return None

