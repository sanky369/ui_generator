import os
import json
from typing import Dict, Any, Tuple
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import logging
import re

load_dotenv()

# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise Exception("ANTHROPIC_API_KEY environment variable is not set")

anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)

TECH_STACKS = {
    "react-tailwind": {
        "name": "React + TypeScript + Tailwind CSS",
        "description": "Modern React with TypeScript and utility-first CSS",
        "cdn": '''<script src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/typescript@latest/lib/typescript.js"></script>'''
    },
    "html-tailwind": {
        "name": "HTML + JavaScript + Tailwind CSS",
        "description": "HTML with JavaScript and utility-first CSS framework",
        "cdn": '''<script src="https://cdn.tailwindcss.com"></script>
<script>
    tailwind.config = {
        darkMode: 'class',
        theme: {
            extend: {}
        }
    }
</script>
<script>
    // Add dark mode toggle functionality
    function toggleDarkMode() {
        document.documentElement.classList.toggle('dark');
    }
</script>'''
    },
    "html-bootstrap": {
        "name": "HTML + JavaScript + Bootstrap 5",
        "description": "HTML with JavaScript and Bootstrap components",
        "cdn": '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<style>
    /* Add dark mode support */
    [data-bs-theme="dark"] {
        color-scheme: dark;
    }
</style>
<script>
    // Add dark mode toggle functionality
    function toggleDarkMode() {
        document.documentElement.setAttribute('data-bs-theme',
            document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
        );
    }
</script>'''
    },
    "html-material": {
        "name": "HTML + JavaScript + Material UI",
        "description": "HTML with JavaScript and Material Design components",
        "cdn": '''<link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://unpkg.com/@material/web/dist/material.min.css" rel="stylesheet">
<script src="https://unpkg.com/@material/web/dist/material.min.js"></script>
<style>
    /* Add Material Design dark theme */
    :root {
        --mdc-theme-primary: #6200ee;
        --mdc-theme-secondary: #03dac6;
    }
    [data-theme="dark"] {
        --mdc-theme-primary: #bb86fc;
        --mdc-theme-secondary: #03dac6;
        --mdc-theme-background: #121212;
        --mdc-theme-surface: #121212;
        --mdc-theme-on-surface: #ffffff;
    }
    body {
        margin: 0;
        font-family: 'Roboto', sans-serif;
    }
</style>
<script>
    // Add dark mode toggle functionality
    function toggleDarkMode() {
        document.documentElement.setAttribute('data-theme',
            document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
        );
    }
</script>'''
    }
}

class AIService:
    @staticmethod
    async def analyze_app_idea_with_claude(prompt: str, tech_stack: str = "react-tailwind") -> Tuple[str, str]:
        """Analyze app idea with Claude and generate UI code"""

        # Get tech stack configuration
        stack_config = TECH_STACKS.get(tech_stack, TECH_STACKS["html-tailwind"])

        # Create stack-specific system prompt
        if tech_stack == "react-tailwind":
            system_prompt = AIService._get_react_system_prompt()
        elif tech_stack == "html-tailwind":
            system_prompt = f"""You are an expert UI developer specializing in {stack_config['name']}.
                Generate clean, modern, and responsive UI code based on the user's requirements.
                Focus on creating a beautiful and intuitive user interface.

                Rules for HTML + Tailwind:
                - Use semantic HTML5 elements
                - Follow Tailwind CSS best practices
                - Add proper dark mode classes (dark:)
                - Make the UI fully responsive
                - Add proper ARIA attributes for accessibility
                - Use the provided toggleDarkMode() function for dark mode
                - Add relevant unsplash images wherever needed or else have a placeholder
                - Include proper loading states and error handling"""
        elif tech_stack == "html-bootstrap":
            system_prompt = f"""You are an expert UI developer specializing in {stack_config['name']}.
                Generate clean, modern, and responsive UI code based on the user's requirements.
                Focus on creating a beautiful and intuitive user interface.

                Rules for Bootstrap:
                - Use Bootstrap 5 components and utilities
                - Follow Bootstrap best practices
                - Add proper dark mode support using data-bs-theme
                - Make the UI fully responsive using Bootstrap's grid
                - Add proper ARIA attributes for accessibility
                - Use the provided toggleDarkMode() function for dark mode
                - Include proper loading states and error handling"""
        else:  # Material UI
            system_prompt = f"""You are an expert UI developer specializing in {stack_config['name']}.
                Generate clean, modern, and responsive UI code based on the user's requirements.
                Focus on creating a beautiful and intuitive user interface.

                Rules for Material UI:
                - Use Material Design Web Components (MDC Web)
                - Follow Material Design principles
                - Add proper dark mode support using data-theme
                - Make the UI fully responsive
                - Add proper ARIA attributes for accessibility
                - Use the provided toggleDarkMode() function for dark mode
                - Include proper loading states and error handling"""

        messages = [
            {
                "role": "user",
                "content": f"Create a UI for the following app idea: {prompt}"
            }
        ]

        if tech_stack == "react-tailwind":
            template = AIService._get_react_template()
        elif tech_stack == "html-tailwind":
            template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Preview</title>
    {stack_config["cdn"]}
</head>
<body class="bg-gray-100 dark:bg-gray-900">
    <div class="min-h-screen">
        <!-- Your HTML code will be inserted here -->
    </div>
</body>
</html>'''
        elif tech_stack == "html-bootstrap":
            template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Preview</title>
    {stack_config["cdn"]}
</head>
<body class="bg-light">
    <div class="min-h-screen">
        <!-- Your HTML code will be inserted here -->
    </div>
</body>
</html>'''
        else:  # HTML + Material UI
            template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Preview</title>
    {stack_config["cdn"]}
</head>
<body>
    <div class="min-h-screen">
        <!-- Your HTML code will be inserted here -->
    </div>
</body>
</html>'''

        try:
            response = await anthropic_client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=6000,
                system=system_prompt,
                messages=messages
            )

            generated_code = response.content[0].text

            # Extract the code from markdown if present
            if "```" in generated_code:
                generated_code = generated_code.split("```")[1]
                if generated_code.startswith(("jsx", "tsx", "html", "javascript")):
                    generated_code = generated_code[generated_code.index("\n")+1:]
                if generated_code.endswith("```"):
                    generated_code = generated_code[:-3]

            if tech_stack == "react-tailwind":
                # Split the generated code into state declarations and JSX
                code_parts = generated_code.split("return")
                if len(code_parts) > 1:
                    state_code = code_parts[0].strip()
                    jsx_code = code_parts[1].strip()
                    
                    # Clean up the code
                    state_code = AIService._clean_react_code(state_code)
                    jsx_code = 'return ' + jsx_code
                    jsx_code = AIService._clean_react_code(jsx_code)
                    
                    # Insert the cleaned code into the template
                    preview_html = template.replace("// Generated state declarations will be inserted here", state_code)
                    preview_html = preview_html.replace("{/* Generated UI code will be inserted here */}", jsx_code)
                else:
                    # If there's no return statement, assume it's all JSX
                    cleaned_code = AIService._clean_react_code(generated_code.strip())
                    if not cleaned_code.startswith('return'):
                        cleaned_code = 'return (' + cleaned_code + ')'
                    preview_html = template.replace("{/* Generated UI code will be inserted here */}", cleaned_code)
            else:
                # Insert the generated HTML code into the div container
                preview_html = template.replace("<!-- Your HTML code will be inserted here -->", generated_code.strip())

            return preview_html, generated_code

        except Exception as e:
            logging.error(f"Error generating UI: {str(e)}")
            raise Exception(f"Failed to generate UI: {str(e)}")

    @staticmethod
    def _clean_react_code(code: str) -> str:
        """Clean and fix common React code issues"""
        # Remove any explanatory text before actual code
        code_start = code.find('const')
        if code_start != -1:
            code = code[code_start:]

        # Remove any text that's not part of the code
        lines = code.split('\n')
        cleaned_lines = []
        in_code_block = False
        code_starters = ('const ', 'let ', 'return ', 'function ', 'if ', 'for ', '{')

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Check if line starts with common code patterns
            if any(line.strip().startswith(starter) for starter in code_starters):
                in_code_block = True
            # Check if line is a closing brace or contains JSX
            elif line.strip().startswith(('<', '}')) or '/>' in line or '>' in line:
                in_code_block = True
            # Skip lines that don't look like code
            if not in_code_block or not line.strip():
                continue
            cleaned_lines.append(line.rstrip())

        code = '\n'.join(cleaned_lines)

        # Fix useState syntax
        code = re.sub(r'React\.useState', 'useState', code)
        code = re.sub(r'React:\s*"useState"', 'useState', code)
        code = re.sub(r'React:\s*useState', 'useState', code)

        # Fix string numbers in objects
        code = re.sub(r':\s*"(\d+(?:\.\d+)?)"', r': \1', code)

        # Fix string numbers with colons
        code = re.sub(r'"(\d+):\s*(\d+)"', r'\1.\2', code)

        # Remove any extra components
        code = re.sub(r'let \w+Component\s*=\s*\(\)\s*=>\s*{', '', code)
        code = re.sub(r'const \w+Component\s*=\s*\(\)\s*=>\s*{', '', code)

        # Clean up code
        code = code.strip()
        
        # Fix return statement
        if code.startswith('return'):
            # Ensure return statement has parentheses
            if not code.startswith('return ('):
                code = re.sub(r'^return\s*', 'return (', code)
                if code.endswith(';'):
                    code = code[:-1] + ');'
                else:
                    code += ')'
        
        # Only add semicolon if needed
        if code and not any(code.rstrip().endswith(x) for x in [';', '}', '>', '/>']):
            code += ';'

        return code

    @staticmethod
    def _get_react_system_prompt():
        return '''You are an expert UI developer. Generate a React component that implements the user's requested UI design.
Follow these rules strictly:
1. Use plain React with hooks (no TypeScript)
2. For state declarations:
   - Use useState (it's already destructured from React)
   - Place all state declarations at the top of the component
   - Use simple JavaScript objects/arrays
   Example:
   const [count, setCount] = useState(0);
   const [items, setItems] = useState([
     { id: 1, name: "Item 1", price: 10.99 },
     { id: 2, name: "Item 2", price: 20.50 }
   ]);

3. For numbers and prices:
   - Use actual numbers, not strings
   - Use dots for decimals, not colons
   Example:
   { price: 99.99 }  // Correct
   { price: "99:99" }  // Wrong

4. For JSX:
   - Use Tailwind CSS for styling
   - Ensure all JSX is wrapped in a single parent div
   Example:
   return (
     <div className="p-4 bg-white">
       <h1 className="text-2xl">Title</h1>
       {items.map(item => (
         <div key={item.id} className="mt-2">
           {item.name} - ${item.price}
         </div>
       ))}
     </div>
   );

5. Never:
   - Create additional components
   - Use TypeScript syntax
   - Use import/export statements
   - Use inline styles
   - Use React.useState (use useState directly)

Output Format:
const [state1, setState1] = useState(initialValue1);
const [state2, setState2] = useState(initialValue2);

return (
  <div className="...">
    {/* JSX content */}
  </div>
);'''

    @staticmethod
    def _get_react_template():
        """Get the React template using development build with JSX support"""
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {}
            }
        }
    </script>
</head>
<body>
    <div id="root"></div>
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script type="text/babel">
        (() => {
            const { useState, useEffect } = React;
            const rootElement = document.getElementById('root');
            const root = ReactDOM.createRoot(rootElement);

            function App() {
                const [darkMode, setDarkMode] = useState(
                    window.matchMedia('(prefers-color-scheme: dark)').matches
                );

                useEffect(() => {
                    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
                    const handleChange = (e) => setDarkMode(e.matches);
                    mediaQuery.addEventListener('change', handleChange);
                    return () => mediaQuery.removeEventListener('change', handleChange);
                }, []);

                // Generated state declarations will be inserted here

                return (
                    <div className={darkMode ? 'dark' : ''}>
                        <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
                            {/* Generated UI code will be inserted here */}
                        </div>
                    </div>
                );
            }

            root.render(
                <React.StrictMode>
                    <App />
                </React.StrictMode>
            );
        })();
    </script>
</body>
</html>'''