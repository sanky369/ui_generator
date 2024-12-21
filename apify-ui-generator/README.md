# UI Generator Apify Actor

Generate beautiful, modern UI designs from text descriptions using Claude AI.

## Features

- Generate complete HTML/CSS/JS code from text descriptions
- Customizable style preferences
- Production-ready code using Tailwind CSS
- Responsive design out of the box
- Caching support for faster responses
- Detailed error handling and logging

## Input

```json
{
    "prompt": "A modern landing page for a fitness app",
    "claude_api_key": "your-api-key",
    "style_preferences": {
        "colorScheme": "light",
        "style": "minimal"
    }
}
```

## Output

The actor outputs:
1. Generated HTML code in the dataset
2. Cached results in key-value store
3. Success/failure status for each generation

Example output:
```json
{
    "html": "<!DOCTYPE html>...",
    "prompt": "A modern landing page for a fitness app",
    "success": true
}
```

## Usage

### Via Apify Console
1. Go to the actor's page
2. Input your prompt and API key
3. Run the actor

### Via API
```python
from apify_client import ApifyClient

client = ApifyClient('your-apify-token')
run_input = {
    'prompt': 'A modern landing page for a fitness app',
    'claude_api_key': 'your-claude-api-key'
}

run = client.actor('username/ui-generator').call(run_input=run_input)
results = client.dataset(run['defaultDatasetId']).list_items().items
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
ANTHROPIC_API_KEY=your-key
```

3. Run locally:
```bash
python src/actor.py
```

## Deployment

1. Install Apify CLI:
```bash
npm install -g apify-cli
```

2. Login to Apify:
```bash
apify login
```

3. Push to Apify:
```bash
apify push
```

## Memory and Compute

- Minimum memory: 256 MB
- Timeout: 300 seconds
- Storage: Uses both Dataset and Key-value store

## Error Handling

The actor includes comprehensive error handling:
- Input validation
- API error handling
- Detailed error logging
- Error status in output
