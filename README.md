# Website Technology Detector

A command-line tool that detects what technologies, frameworks, and platforms a website is built with.

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
- No complex dependencies required

## Installation

1. Clone this repository:
```
git clone https://github.com/Nabeel-javaid/website-tech-detector
cd website-tech-detector
```

2. Install required packages:
```
pip install requests colorama
```

## Usage

### Basic Usage
```
python website_tech_detector.py --url example.com
```

### Interactive Mode
```
python website_tech_detector.py
```

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

For GitHub.com:
```
[+] CLASSIFICATION: Multiple Frameworks (primarily Angular) (Custom Development)
[+] CONFIDENCE: Medium
==================================================
DETECTED TECHNOLOGIES:
{
    "React": {
        "categories": [
            "JavaScript Framework"
        ],
        "confidence": "High"
    },
    "Angular": {
        "categories": [
            "JavaScript Framework"
        ],
        "confidence": "High"
    },
    "github.com": {
        "categories": [
            "Web Server"
        ],
        "confidence": "High"
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

## Extending

You can add more technology patterns by editing the `tech_patterns` dictionary in the `TechDetector` class.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
