#!/usr/bin/env python3
"""
Website Technology Detector
A simple tool to detect technologies used by websites
"""

import json
import time
import sys
import argparse
import requests
from urllib.parse import urlparse
import re

# Only initialize colorama when running as script
try:
    from colorama import init, Fore
    has_colorama = True
    # Initialize colorama for cross-platform colored output
    init()
except ImportError:
    has_colorama = False
    # Create dummy Fore class for API usage
    class Fore:
        RED = ""
        GREEN = ""
        CYAN = ""
        MAGENTA = ""
        YELLOW = ""

class TechDetector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Common technology signatures
        self.tech_patterns = {
            'WordPress': {
                'pattern': [r'wp-content', r'wp-includes', r'wordpress.org', r'\/wp-', r'\/wp-content\/', r'\/wp-includes\/'],
                'categories': ['CMS'],
                'weight': 10
            },
            'Joomla': {
                'pattern': [r'\/joomla', r'Joomla!', r'/administrator/'],
                'categories': ['CMS'],
                'weight': 10
            },
            'Drupal': {
                'pattern': [r'\/drupal', r'Drupal', r'/sites/default/files/'],
                'categories': ['CMS'],
                'weight': 10
            },
            'Wix': {
                'pattern': [r'wix.com', r'_wixCIDX', r'wix-dropdown'],
                'categories': ['Website Builder'],
                'weight': 10
            },
            'Squarespace': {
                'pattern': [r'squarespace', r'static.squarespace.com'],
                'categories': ['Website Builder'],
                'weight': 10
            },
            'Webflow': {
                'pattern': [r'webflow', r'assets.website-files.com'],
                'categories': ['Website Builder'],
                'weight': 10
            },
            'Shopify': {
                'pattern': [r'shopify.com', r'cdn.shopify.com', r'\.myshopify\.com'],
                'categories': ['E-commerce'],
                'weight': 10
            },
            'Ghost': {
                'pattern': [r'ghost.io', r'ghost-theme'],
                'categories': ['CMS'],
                'weight': 10
            },
            'TYPO3': {
                'pattern': [r'typo3', r'TYPO3'],
                'categories': ['CMS'],
                'weight': 10
            },
            'Bootstrap': {
                'pattern': [r'bootstrap\.'],
                'categories': ['UI Framework'],
                'weight': 4
            },
            'jQuery': {
                'pattern': [r'jquery'],
                'categories': ['JavaScript Library'],
                'weight': 3
            },
            'React': {
                'pattern': [r'react', r'reactjs', r'react-dom'],
                'categories': ['JavaScript Framework'],
                'weight': 5
            },
            'Angular': {
                'pattern': [r'angular', r'ng-'],
                'categories': ['JavaScript Framework'],
                'weight': 5
            },
            'Vue.js': {
                'pattern': [r'vue\.js', r'vuejs'],
                'categories': ['JavaScript Framework'],
                'weight': 5
            },
            'Node.js': {
                'pattern': [r'node\.js', r'nodejs'],
                'categories': ['JavaScript Runtime'],
                'weight': 3
            },
            'PHP': {
                'pattern': [r'\.php', r'php-'],
                'categories': ['Programming Language'],
                'weight': 3
            },
            'ASP.NET': {
                'pattern': [r'asp\.net', r'__VIEWSTATE'],
                'categories': ['Web Framework'],
                'weight': 7
            },
            'Laravel': {
                'pattern': [r'laravel'],
                'categories': ['PHP Framework'],
                'weight': 7
            },
            'Django': {
                'pattern': [r'django', r'csrfmiddlewaretoken'],
                'categories': ['Python Framework'],
                'weight': 7
            },
            'Flask': {
                'pattern': [r'flask'],
                'categories': ['Python Framework'],
                'weight': 7
            },
            'Ruby on Rails': {
                'pattern': [r'rails', r'ruby on rails'],
                'categories': ['Ruby Framework'],
                'weight': 7
            },
            'Nginx': {
                'pattern': [r'nginx'],
                'categories': ['Web Server'],
                'weight': 2
            },
            'Apache': {
                'pattern': [r'apache'],
                'categories': ['Web Server'],
                'weight': 2
            },
            'Cloudflare': {
                'pattern': [r'cloudflare'],
                'categories': ['CDN'],
                'weight': 2
            },
            'Google Analytics': {
                'pattern': [r'ga\.js', r'analytics\.js', r'gtag'],
                'categories': ['Analytics'],
                'weight': 1
            },
            'Google Tag Manager': {
                'pattern': [r'gtm\.js', r'googletagmanager'],
                'categories': ['Tag Manager'],
                'weight': 1
            },
            'Font Awesome': {
                'pattern': [r'font-awesome', r'fontawesome'],
                'categories': ['Icon Library'],
                'weight': 1
            },
            'WooCommerce': {
                'pattern': [r'woocommerce', r'is-wc-'],
                'categories': ['E-commerce'],
                'weight': 8
            },
            'Magento': {
                'pattern': [r'magento', r'Magento'],
                'categories': ['E-commerce'],
                'weight': 8
            }
        }
        
        # Group technologies by type
        self.cms_systems = ['WordPress', 'Joomla', 'Drupal', 'Ghost', 'TYPO3']
        self.website_builders = ['Wix', 'Squarespace', 'Webflow']
        self.ecommerce_platforms = ['Shopify', 'WooCommerce', 'Magento']
        self.frameworks = [
            'React', 'Angular', 'Vue.js', 'Laravel', 'Django', 
            'Flask', 'Ruby on Rails', 'ASP.NET'
        ]

    def normalize_url(self, url):
        """Add http:// prefix if not present"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url

    def detect_tech(self, url):
        """Detect technologies used by a website"""
        normalized_url = self.normalize_url(url)
        
        try:
            # Get website content
            response = requests.get(normalized_url, headers=self.headers, timeout=10)
            content = response.text
            headers = response.headers
            
            # Store detected technologies
            detected = {}
            tech_scores = {}
            
            # Check content and headers for technology signatures
            for tech, info in self.tech_patterns.items():
                patterns = info['pattern']
                match_count = 0
                
                for pattern in patterns:
                    content_matches = re.findall(pattern, content, re.IGNORECASE)
                    header_matches = []
                    for header_value in headers.values():
                        header_matches.extend(re.findall(pattern, str(header_value), re.IGNORECASE))
                    
                    match_count += len(content_matches) + len(header_matches)
                    
                    if content_matches or header_matches:
                        detected[tech] = {
                            "categories": info['categories'],
                            "confidence": "High" if match_count > 3 else "Medium",
                            "match_count": match_count
                        }
                        tech_scores[tech] = info['weight'] * match_count
            
            # Check for server information
            if 'Server' in headers:
                server = headers['Server']
                detected[server] = {
                    "categories": ["Web Server"],
                    "confidence": "High"
                }
            
            # Check for powered-by information
            if 'X-Powered-By' in headers:
                powered_by = headers['X-Powered-By']
                detected[powered_by] = {
                    "categories": ["Technology"],
                    "confidence": "High"
                }
            
            # Determine the primary platform
            platform_info = self.determine_platform(detected, tech_scores)
            detected["classification"] = platform_info
                
            return detected
            
        except requests.exceptions.RequestException as e:
            # Instead of printing to console, return error in response for API
            error_msg = f"Error: Unable to connect to {url}. Details: {str(e)}"
            if has_colorama:
                print(Fore.RED + error_msg)
            return {"error": error_msg, "classification": {"platform_type": "Unknown", "platform_name": "Unknown", "confidence": "Low"}}
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if has_colorama:
                print(Fore.RED + error_msg)
            return {"error": error_msg, "classification": {"platform_type": "Unknown", "platform_name": "Unknown", "confidence": "Low"}}
    
    def determine_platform(self, detected_tech, tech_scores):
        """Determine if the site is WordPress, another tool, or custom code"""
        if not detected_tech:
            return {
                "platform_type": "Unknown",
                "platform_name": "Unknown",
                "confidence": "Low"
            }
        
        # Check for WordPress with stronger validation
        if "WordPress" in detected_tech:
            # Get the match count for more accurate detection
            match_count = detected_tech["WordPress"].get("match_count", 0)
            
            # Require stronger evidence for WordPress
            if match_count >= 2:
                confidence = "High" if match_count > 5 else "Medium"
                if "WooCommerce" in detected_tech:
                    return {
                        "platform_type": "CMS with E-commerce",
                        "platform_name": "WordPress + WooCommerce",
                        "confidence": confidence
                    }
                return {
                    "platform_type": "CMS",
                    "platform_name": "WordPress",
                    "confidence": confidence
                }
            else:
                # Remove WordPress if it's a weak match
                del detected_tech["WordPress"]
                if "WordPress" in tech_scores:
                    del tech_scores["WordPress"]
        
        # Check for other CMS
        for cms in self.cms_systems:
            if cms in detected_tech:
                return {
                    "platform_type": "CMS",
                    "platform_name": cms,
                    "confidence": detected_tech[cms].get("confidence", "Medium")
                }
        
        # Check for website builders
        for builder in self.website_builders:
            if builder in detected_tech:
                return {
                    "platform_type": "Website Builder",
                    "platform_name": builder,
                    "confidence": detected_tech[builder].get("confidence", "Medium")
                }
        
        # Check for e-commerce platforms
        for ecomm in self.ecommerce_platforms:
            if ecomm in detected_tech:
                return {
                    "platform_type": "E-commerce Platform",
                    "platform_name": ecomm,
                    "confidence": detected_tech[ecomm].get("confidence", "Medium")
                }
        
        # Check for frameworks
        framework_count = 0
        framework_name = ""
        framework_score = 0
        
        for framework in self.frameworks:
            if framework in detected_tech:
                framework_count += 1
                if tech_scores.get(framework, 0) > framework_score:
                    framework_score = tech_scores[framework]
                    framework_name = framework
        
        if framework_count == 1:
            return {
                "platform_type": "Framework-based",
                "platform_name": framework_name,
                "confidence": "Medium"
            }
        elif framework_count > 1:
            return {
                "platform_type": "Custom Development",
                "platform_name": f"Multiple Frameworks (primarily {framework_name})",
                "confidence": "Medium"
            }
        
        # If we have PHP but no CMS or framework, likely custom
        if "PHP" in detected_tech:
            return {
                "platform_type": "Custom Development",
                "platform_name": "Custom PHP",
                "confidence": "Medium"
            }
        
        # If we have JavaScript frameworks/libraries but no CMS
        js_techs = ["jQuery", "React", "Angular", "Vue.js"]
        if any(tech in detected_tech for tech in js_techs):
            js_tech_name = next((tech for tech in js_techs if tech in detected_tech), "JavaScript")
            return {
                "platform_type": "Custom Development",
                "platform_name": f"Custom {js_tech_name}",
                "confidence": "Medium"
            }
        
        # If server header suggests GitHub Pages
        if "github" in str(detected_tech).lower():
            return {
                "platform_type": "Hosted Platform",
                "platform_name": "GitHub Pages",
                "confidence": "Medium"
            }
        
        # If very few technologies detected, might be static HTML
        if len(detected_tech) < 3:
            return {
                "platform_type": "Static Website",
                "platform_name": "HTML/CSS",
                "confidence": "Low"
            }
        
        # Default case
        return {
            "platform_type": "Custom Development",
            "platform_name": "Unknown Stack",
            "confidence": "Low"
        }

def main():
    parser = argparse.ArgumentParser(description='Detect technologies used on a website')
    parser.add_argument('--url', help='URL to detect tech stack', required=False)
    args = parser.parse_args()
    
    detector = TechDetector()
    
    if args.url:
        url = args.url
    else:
        if has_colorama:
            url = input(Fore.YELLOW + "Enter URL to analyze: ")
        else:
            url = input("Enter URL to analyze: ")
        
    if has_colorama:
        print(Fore.CYAN + f"[+] Detecting technologies from {url}\n")
    else:
        print(f"[+] Detecting technologies from {url}\n")
    
    start_time = time.time()
    
    results = detector.detect_tech(url)
    
    if results:
        # Display classification first
        if "classification" in results:
            classification = results["classification"]
            if has_colorama:
                print(Fore.GREEN + f"[+] CLASSIFICATION: {classification['platform_name']} ({classification['platform_type']})")
                print(Fore.GREEN + f"[+] CONFIDENCE: {classification['confidence']}")
                print(Fore.GREEN + "=" * 50)
            else:
                print(f"[+] CLASSIFICATION: {classification['platform_name']} ({classification['platform_type']})")
                print(f"[+] CONFIDENCE: {classification['confidence']}")
                print("=" * 50)
            
            # Remove classification from results for display
            results_copy = results.copy()
            del results_copy["classification"]
            
            # Clean up match_count from output for cleaner display
            for tech in results_copy:
                if isinstance(results_copy[tech], dict) and "match_count" in results_copy[tech]:
                    del results_copy[tech]["match_count"]
            
            if has_colorama:
                print(Fore.MAGENTA + "DETECTED TECHNOLOGIES:")
                print(Fore.MAGENTA + json.dumps(results_copy, indent=4))
            else:
                print("DETECTED TECHNOLOGIES:")
                print(json.dumps(results_copy, indent=4))
        else:
            if has_colorama:
                print(Fore.MAGENTA + json.dumps(results, indent=4))
            else:
                print(json.dumps(results, indent=4))
    else:
        if has_colorama:
            print(Fore.RED + "[+] No technologies detected or an error occurred")
        else:
            print("[+] No technologies detected or an error occurred")
    
    end_time = time.time()
    if has_colorama:
        print(Fore.CYAN + f"\n[+] Total Execution Time: {end_time - start_time:.2f} seconds\n")
    else:
        print(f"\n[+] Total Execution Time: {end_time - start_time:.2f} seconds\n")

if __name__ == '__main__':
    main() 