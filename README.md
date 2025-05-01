# Website Technology Detector

A tool that detects what technologies, frameworks, and platforms a website is built with. Available as both a command-line tool and a REST API.

## Features

- Identifies if a website uses WordPress, another CMS, or custom code
- Detects various technologies including:
  - Content Management Systems (WordPress, Joomla, Drupal)
  - Website Builders (Wix, Squarespace, Webflow)
  - E-commerce Platforms (Shopify, WooCommerce, Magento)
  - JavaScript Frameworks (React, Angular, Vue.js)
  - Programming Languages (PHP, etc.)
  - Web Servers (Nginx, Apache)
- Provides confidence levels for each detection
- Works cross-platform with colorized output
- Available as a command-line tool and REST API

## Installation

### Command Line Tool

1. Clone this repository:
```
git clone https://github.com/your-username/website-tech-detector.git
cd website-tech-detector
```

2. Install required packages:
```
pip install requests colorama
```

### API Server

1. Clone this repository:
```
git clone https://github.com/your-username/website-tech-detector.git
cd website-tech-detector
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Run the API server:
```
python api.py
```

The API will be available at http://localhost:8000 with Swagger documentation at http://localhost:8000/docs

## Usage

### Command Line Tool
```
python website_tech_detector.py --url example.com
```

### Interactive Mode
```
python website_tech_detector.py
```

### API Requests

The API is deployed and available at:
```
https://website-tech-detector-api.onrender.com
```

#### Endpoint
```
POST /detect
```

#### Request Body
```json
{
  "url": "example.com"
}
```

#### Example cURL Command
```
curl -X POST "https://website-tech-detector-api.onrender.com/detect" -H "Content-Type: application/json" -d '{"url":"wordpress.org"}'
```

## Testing with Postman

1. Open Postman
2. Create a new POST request to `https://website-tech-detector-api.onrender.com/detect`
3. Set the request body to raw JSON:
   ```json
   {
     "url": "wordpress.org"
   }
   ```
4. Send the request to receive the technology detection results

## Example Websites to Test

- WordPress: `wordpress.org`
- E-commerce: `shopify.com`
- Framework-based: `reactjs.org`
- GitHub: `github.com`

## Example Output

For WordPress.org:
```
[+] CLASSIFICATION: WordPress (CMS)
[+] CONFIDENCE: High
==================================================
DETECTED TECHNOLOGIES:
{
    "WordPress": {
        "categories": [
            "CMS"
        ],
        "confidence": "High"
    },
    "Angular": {
        "categories": [
            "JavaScript Framework"
        ],
        "confidence": "High"
    },
    "PHP": {
        "categories": [
            "Programming Language"
        ],
        "confidence": "Medium"
    },
    "Nginx": {
        "categories": [
            "Web Server"
        ],
        "confidence": "Medium"
    }
}
```

## How It Works

The tool works by:
1. Fetching the HTML content of the target website
2. Analyzing the content for technology signatures using regex patterns
3. Examining HTTP headers for server information
4. Weighing and scoring the detected technologies to determine the most likely platform
5. Presenting the findings with confidence levels

## Deployment

The API is deployed on Render.com. To deploy your own instance:

1. Fork this repository
2. Create a new web service on Render.com
3. Connect your GitHub repository
4. Configure with:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Select Python environment

## Extending

You can add more technology patterns by editing the `tech_patterns` dictionary in the `TechDetector` class.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
