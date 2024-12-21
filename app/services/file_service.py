import os
import zipfile
import tempfile
from pathlib import Path
from typing import Optional
import uuid
import re

class FileService:
    @staticmethod
    def generate_unique_id() -> str:
        """Generate a unique ID for a design"""
        return uuid.uuid4().hex[:8]

    @staticmethod
    def create_zip_from_html(html_content: str, filename: Optional[str] = None) -> tuple[str, str]:
        """
        Creates a zip file containing the HTML content and returns the file path
        """
        if not filename:
            filename = f"ui_design_{uuid.uuid4().hex[:8]}"
            
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"{filename}.zip")
        
        # Create HTML file
        html_file_path = os.path.join(temp_dir, "index.html")
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # Create zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(html_file_path, "index.html")
            
        return zip_path, f"{filename}.zip"

    @staticmethod
    def create_react_project(content: str) -> tuple[str, str]:
        """
        Creates a zip file containing a React + TypeScript project structure
        """
        # Generate unique filename
        filename = f"react_ui_{uuid.uuid4().hex[:8]}"
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        project_dir = os.path.join(temp_dir, filename)
        os.makedirs(project_dir)
        
        # Extract TypeScript interfaces, React components, and main App
        interfaces_match = re.search(r'(interface.*?}\s*)+', content, re.DOTALL)
        components_match = re.search(r'(const\s+\w+\s*=.*?}\);?\s*)+', content, re.DOTALL)
        app_match = re.search(r'const\s+App\s*=.*?}\);?\s*', content, re.DOTALL)
        
        # Create project structure
        os.makedirs(os.path.join(project_dir, 'src'))
        os.makedirs(os.path.join(project_dir, 'src', 'components'))
        os.makedirs(os.path.join(project_dir, 'src', 'types'))
        
        # Write package.json
        package_json = '''{
  "name": "generated-ui",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@types/node": "^16.18.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^4.9.5",
    "tailwindcss": "^3.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}'''
        
        with open(os.path.join(project_dir, 'package.json'), 'w') as f:
            f.write(package_json)
        
        # Write tsconfig.json
        tsconfig_json = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}'''
        
        with open(os.path.join(project_dir, 'tsconfig.json'), 'w') as f:
            f.write(tsconfig_json)
        
        # Write tailwind.config.js
        tailwind_config = '''module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}'''
        
        with open(os.path.join(project_dir, 'tailwind.config.js'), 'w') as f:
            f.write(tailwind_config)
        
        # Write TypeScript interfaces
        if interfaces_match:
            with open(os.path.join(project_dir, 'src', 'types', 'interfaces.ts'), 'w') as f:
                f.write(interfaces_match.group())
        
        # Write all components and scripts to their respective files
        if components_match:
            components = components_match.group()
            with open(os.path.join(project_dir, 'src', 'components', 'Components.tsx'), 'w') as f:
                f.write('''import React from 'react';
import { } from '../types/interfaces';

''' + components)

        # Write App.tsx
        if app_match:
            with open(os.path.join(project_dir, 'src', 'App.tsx'), 'w') as f:
                f.write('''import React from 'react';
import { } from './types/interfaces';
import { } from './components/Components';

''' + app_match.group())

        # Write index.tsx
        index_tsx = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''

        with open(os.path.join(project_dir, 'src', 'index.tsx'), 'w') as f:
            f.write(index_tsx)

        # Write index.css with Tailwind imports
        index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;'''

        with open(os.path.join(project_dir, 'src', 'index.css'), 'w') as f:
            f.write(index_css)

        # Create README.md
        readme = '''# Generated UI Project

This is a React + TypeScript project generated with Tailwind CSS.

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```'''

        with open(os.path.join(project_dir, 'README.md'), 'w') as f:
            f.write(readme)

        # Create zip file
        zip_path = os.path.join(temp_dir, f"{filename}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, project_dir))

        return zip_path, f"{filename}.zip"

    @staticmethod
    def cleanup_file(file_path: str) -> None:
        """Clean up a temporary file and its parent directory"""
        try:
            # Remove the file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove the parent directory if it's empty
            parent_dir = os.path.dirname(file_path)
            if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                os.rmdir(parent_dir)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {str(e)}")

    @staticmethod
    def cleanup_temp_files(file_path: str):
        """
        Cleans up temporary files and directories
        """
        try:
            # Remove the zip file
            if os.path.exists(file_path):
                os.remove(file_path)
                
            # Remove the parent temp directory
            parent_dir = os.path.dirname(file_path)
            if os.path.exists(parent_dir):
                for root, dirs, files in os.walk(parent_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(parent_dir)
        except Exception as e:
            print(f"Error cleaning up temp files: {str(e)}")
