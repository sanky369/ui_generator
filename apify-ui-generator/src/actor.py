from apify_client import ApifyClient
from apify import Actor
import asyncio
import logging
from typing import Dict, Any
from anthropic import AsyncAnthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UIGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        
    async def generate_ui(self, prompt: str, style_preferences: Dict[str, Any] = None) -> str:
        """Generate UI design using Anthropic's Claude."""
        try:
            system_prompt = """You are an expert UI/UX designer specializing in creating beautiful, modern web interfaces. 
            Your task is to generate pixel-perfect, production-ready frontend code taking inspiration from thousands of UI templates you are trained on.
            
            Guidelines for the UI:
            1. Visual Design:
               - Use a clean, modern aesthetic with proper spacing and typography
               - Implement a cohesive color scheme that enhances usability
               - Include subtle animations and transitions for better UX
               - Add meaningful icons and visual elements where appropriate
               - Ensure proper contrast ratios for accessibility

            2. Layout & Structure:
               - Create a responsive design that works on all devices
               - Use a logical visual hierarchy
               - Implement proper grid systems and spacing
               - Include a navigation system if needed
               - Add a footer with relevant links

            3. Components & Interactivity:
               - Include form validation with helpful error messages
               - Add loading states and success/error feedback
               - Implement hover states and focus indicators
               - Use micro-interactions to enhance UX
               - Include tooltips or help text where needed

            4. Technical Requirements:
               - Use semantic HTML5 elements
               - Implement Tailwind CSS for styling
               - Add necessary JavaScript for interactivity
               - Ensure WCAG 2.1 accessibility compliance
               - Include proper meta tags and SEO elements

            IMPORTANT: Return ONLY the complete, production-ready HTML code with embedded Tailwind CSS and JavaScript. Do not include any explanations."""

            response = await self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=8192,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Create a modern, professional UI for: {prompt}. Focus on creating a polished, production-ready interface that follows current design trends and best practices."
                    }
                ]
            )

            # Extract the generated HTML
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = response['content']

            if isinstance(content, list):
                generated_html = content[0].text.strip()
            else:
                generated_html = content.strip()
            
            # Ensure proper HTML structure
            if not generated_html.lower().startswith('<!doctype html'):
                generated_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
{generated_html}
</body>
</html>'''

            return generated_html

        except Exception as e:
            logger.error(f"Error generating UI: {str(e)}")
            raise

async def main():
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        prompt = actor_input.get('prompt')
        if not prompt:
            raise ValueError("No prompt provided in input")
            
        api_key = actor_input.get('claude_api_key')
        if not api_key:
            raise ValueError("No Claude API key provided")
            
        style_preferences = actor_input.get('style_preferences', {})
        
        # Initialize generator
        generator = UIGenerator(api_key)
        
        try:
            # Generate UI
            logger.info(f"Generating UI for prompt: {prompt}")
            result = await generator.generate_ui(prompt, style_preferences)
            
            # Save to dataset
            await Actor.push_data({
                'html': result,
                'prompt': prompt,
                'success': True
            })
            
            # Store in key-value store for caching
            await Actor.get_value_store().set('last_generated_ui', {
                'html': result,
                'prompt': prompt,
                'timestamp': Actor.get_env().get('ACTOR_STARTED_AT')
            })
            
            logger.info("Successfully generated and stored UI")
            
        except Exception as e:
            logger.error(f"Failed to generate UI: {str(e)}")
            await Actor.push_data({
                'error': str(e),
                'prompt': prompt,
                'success': False
            })
            raise

if __name__ == "__main__":
    asyncio.run(main())
