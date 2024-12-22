from apify import Actor
import os
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from anthropic import AsyncAnthropic
from playwright.async_api import async_playwright
import tempfile
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UIGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        
    async def generate_ui(self, prompt: str, style_preferences: Dict[str, Any] = None) -> str:
        """Generate UI code based on the prompt"""
        try:
            # Create the system prompt
            system_prompt = """You are an expert UI developer specializing in modern web development.
            Generate clean, modern, and responsive HTML code based on the user's requirements.
            Focus on creating a beautiful and intuitive user interface.
            
            Rules:
            - Use semantic HTML5 elements
            - Follow Tailwind CSS best practices
            - Make the UI fully responsive
            - Add proper ARIA attributes for accessibility
            - Use proper loading states and error handling
            - Add relevant unsplash images wherever needed or else have a placeholder
            """
            
            messages = [
                {
                    "role": "user",
                    "content": f"Create a UI for the following app idea: {prompt}"
                }
            ]
            
            # Add any style preferences to the prompt
            if style_preferences:
                style_prompt = "Please incorporate these style preferences:\n"
                for key, value in style_preferences.items():
                    style_prompt += f"- {key}: {value}\n"
                messages.append({
                    "role": "user",
                    "content": style_prompt
                })
            
            # Generate the UI code
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=6000,
                temperature=0.7,
                system=system_prompt,
                messages=messages
            )
            
            generated_code = response.content[0].text
            
            # Extract the code from markdown if present
            if "```" in generated_code:
                generated_code = generated_code.split("```")[1]
                if generated_code.startswith("html"):
                    generated_code = generated_code[4:]
                generated_code = generated_code.strip()
            
            return generated_code
            
        except Exception as e:
            logger.error(f"Failed to generate UI: {str(e)}")
            raise

    async def capture_preview(self, html_code: str) -> bytes:
        """Capture a screenshot of the generated UI"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <script src="https://cdn.tailwindcss.com"></script>
                </head>
                <body>
                    {html_code}
                </body>
                </html>
                """)
                temp_path = f.name
            
            try:
                # Load the page and wait for network idle
                await page.goto(f"file://{temp_path}")
                await page.wait_for_load_state("networkidle")
                
                # Get full page height
                page_height = await page.evaluate("""
                    Math.max(
                        document.documentElement.scrollHeight,
                        document.documentElement.offsetHeight,
                        document.documentElement.clientHeight
                    )
                """)
                
                # Set viewport to full page height
                await page.set_viewport_size({"width": 1920, "height": page_height})
                
                # Take screenshot
                screenshot = await page.screenshot(
                    full_page=True,
                    type="png"
                )
                
                return screenshot
                
            finally:
                await browser.close()
                os.unlink(temp_path)

async def main():
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        prompt = actor_input.get('prompt', 'landing page of a health tracker app')
        claude_api_key = actor_input.get('claude_api_key', os.getenv('ANTHROPIC_API_KEY'))
        style_preferences = actor_input.get('style_preferences', {})

        # Log the start of generation
        logging.info(f"Generating UI for prompt: {prompt}")

        try:
            # Initialize the UI generator
            generator = UIGenerator(claude_api_key)
            
            # Generate the UI
            ui_code = await generator.generate_ui(prompt, style_preferences)
            
            # Capture preview image
            preview_image = await generator.capture_preview(ui_code)
            
            # Get key-value store
            kvs = await Actor.open_key_value_store()
            
            # Save screenshot to key-value store
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_key = f"preview_image_{timestamp}.png"
            
            logging.info(f"Saving screenshot with key: {screenshot_key}")
            
            # Store the image directly
            await kvs.set_value(
                screenshot_key,
                preview_image,
                content_type="image/png"
            )
            
            # Get the store ID from environment variable
            store_id = os.environ.get('APIFY_DEFAULT_KEY_VALUE_STORE_ID')
            
            if store_id:
                # Construct the URL using the store ID
                screenshot_url = f"https://api.apify.com/v2/key-value-stores/{store_id}/records/{screenshot_key}?disableRedirect=true"
                logging.info(f"Screenshot URL: {screenshot_url}")
            else:
                # Fallback if store ID is not available
                screenshot_url = None
                logging.warning("Could not get key-value store ID from environment")
            
            # Push data to dataset with screenshot URL
            await Actor.push_data({
                'prompt': prompt,
                'generated_code': ui_code,
                'preview_image_url': screenshot_url,
                'timestamp': datetime.now().isoformat()
            })
            
            # Store the last generated UI and preview in key-value store
            await kvs.set_value('last_generated_ui', {
                'prompt': prompt,
                'code': ui_code,
                'preview_image_url': screenshot_url,
                'timestamp': datetime.now().isoformat()
            })

            # Set output
            await Actor.set_value('OUTPUT', {
                'prompt': prompt,
                'code': ui_code,
                'preview_image_url': screenshot_url,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logging.error(f"Failed to generate UI: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(main())
