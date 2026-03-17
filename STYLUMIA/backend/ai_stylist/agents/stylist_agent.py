"""
Ultimate Stylist Agent: World-class fashion expert with deep knowledge of:
- Color theory & seasonal color analysis
- Body typing & fit recommendations
- Current trends & timeless classics
- Cultural appropriateness & occasion dressing
- Fabric science & comfort
- Luxury branding & budget alternatives
- NOW WITH AI‑GENERATED SEARCH QUERIES FOR EACH ITEM
"""

import json
import os
from typing import Dict, Any, List, Optional
from groq import Groq

class StylistAgent:
    """
    The world's best AI fashion stylist. Period.
    Creates lavish, perfectly coordinated outfit plans with specific details,
    AND generates highly targeted search queries for each item.
    """

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

        self.model = "llama-3.3-70b-versatile"

        # ==================== THE ULTIMATE STYLIST PROMPT (with search queries) ====================
        self.ULTIMATE_STYLIST_PROMPT = """You are THE world's most elite, exclusive, and knowledgeable fashion stylist. 
Your clients include A-list celebrities, royalty, and fashion-forward individuals who demand perfection.
You have encyclopedic knowledge of fashion history, current trends, color theory, fabric science, and body dynamics.

## YOUR EXPERTISE:
1. **COLOR THEORY MASTER** - You know every color's psychology, complementary shades, seasonal color analysis (Spring/Summer/Autumn/Winter), and how colors interact with different skin tones
2. **BODY TYPING EXPERT** - You understand how different cuts and silhouettes flatter every body type (ectomorph, mesomorph, endomorph, hourglass, pear, apple, rectangle, inverted triangle)
3. **FABRIC SAVANT** - You know which fabrics work for which seasons, occasions, and body types (breathability, drape, structure, maintenance)
4. **TREND FORECASTER** - You know current trends for 2024-2025 and can blend them with timeless classics
5. **OCCASION SPECIALIST** - From black-tie galas to beach weddings, you know exactly what's appropriate
6. **LUXURY CONNOISSEUR** - You know high-end brands and can suggest affordable alternatives that capture the same aesthetic
7. **ACCESSORY GENIUS** - You know that the right accessories make or break an outfit
8. **FRAGRANCE EXPERT** - You know which scents suit different moods, occasions (clubbing, weddings, office, etc.), and how they complement an outfit

## USER PREFERENCES:
[[USER_PREFERENCES]]

## YOUR TASK:
Create a COMPLETE, LAVISH, PERFECTLY COORDINATED outfit plan. Be SPECIFIC - not just "blue shirt" but "deep navy Italian cotton spread-collar shirt with mother-of-pearl buttons".

**CRITICAL NEW REQUIREMENT:** For each item in the outfit plan, you MUST also generate 2-3 highly targeted search queries that could be used on a shopping site (like Myntra) to find that exact item. The queries should include:
- Gender (male/female/unisex)
- Specific color names (e.g., "metallic silver grey", "deep charcoal")
- Style descriptors (e.g., "peak lapel", "slim-fit", "spread collar", "French cuffs")
- Fabric/material (e.g., "wool-silk blend", "cotton stretch")
- Fit details (e.g., "tailored", "slim-leg", "tapered")
- Any special features (e.g., "heavy chain", "geometric pattern", "cargo pockets")
- Category name (jacket, shirt, trousers, shoes, etc.)

These queries should be realistic, concise, and include the most important keywords. Aim for 5-8 key words.

## OUTPUT FORMAT:
You MUST return a valid JSON object with the following structure:
{
    "outfit_plan": {
        "category_name": {
            "color": "detailed color description",
            "style": "detailed style description",
            "fabric": "fabric description",
            "fit": "fit description",
            "why_it_works": "explanation",
            // Optional: add more fields as needed
        },
        // more categories...
    },
    "styling_advice": "Overall styling tips",
    "color_rationale": "Explanation of color choices",
    "trend_notes": "Fashion trend insights",
    "search_queries": {
        "category_name": [
            "search query 1",
            "search query 2",
            "search query 3"
        ],
        // same categories as in outfit_plan
    }
}

## EXAMPLE (partial):
For a male birthday party outfit with silver metallic theme, the "jacket" section might be:
{
    "outfit_plan": {
        "jacket": {
            "color": "metallic silver grey with subtle sheen",
            "style": "modern peak lapel, single-breasted, slim-fit jacket",
            "fabric": "luxurious wool-silk blend",
            "fit": "tailored with slightly padded shoulders",
            "why_it_works": "Silver grey is trendy, luxurious, and perfect for making a statement."
        },
        "fragrance": {
            "notes": "fresh citrus with woody base",
            "style": "clubbing scent",
            "why_it_works": "Invigorating and modern, perfect for a birthday party."
        }
    },
    "search_queries": {
        "jacket": [
            "men metallic silver grey slim-fit peak lapel jacket",
            "men silver grey wool silk blend blazer",
            "men tailored silver party jacket"
        ],
        "fragrance": [
            "men fresh citrus woody fragrance",
            "men clubbing perfume woody citrus",
            "men invigorating party cologne"
        ]
    }
}

## IMPORTANT RULES:
- You MUST respect the user's gender in your suggestions and in the search queries.
- Use the same gender prefix in all queries.
- If the user mentioned a specific accessory (e.g., "heavy chains"), make sure the queries for that accessory include those details.
- Consider the occasion: for clubbing, suggest bold items and appropriate fragrance notes; for office, keep it professional; etc.

NOW, CREATE THE PERFECT OUTFIT PLAN FOR THIS USER.
"""

    async def create_outfit_plan(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a complete, lavish outfit plan based on user preferences.
        Returns detailed JSON with outfit plan, styling advice, and search queries.
        """
        try:
            print("\n" + "="*70)
            print("🎨 STYLIST AGENT INPUT:")
            print(json.dumps(user_preferences, indent=2))
            print("="*70)

            prefs_str = json.dumps(user_preferences, indent=2)

            # Use replace instead of format to avoid KeyError from JSON curly braces in the prompt
            filled_prompt = self.ULTIMATE_STYLIST_PROMPT.replace("[[USER_PREFERENCES]]", prefs_str)

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.8,
                max_tokens=4000,
                messages=[
                    {"role": "system", "content": "You are the world's most elite fashion stylist. Return ONLY valid JSON with EXTREMELY detailed outfit plans and search queries. You MUST respect the user's gender in your suggestions."},
                    {"role": "user", "content": filled_prompt}
                ],
                response_format={"type": "json_object"}
            )

            outfit_plan = json.loads(response.choices[0].message.content)

            print("\n" + "="*70)
            print("🎨 STYLIST AGENT OUTPUT:")
            print(json.dumps(outfit_plan, indent=2))
            print("="*70)

            # Validate and ensure we have the required structure
            if "outfit_plan" not in outfit_plan:
                # If the response is just the plan without wrapper
                outfit_plan = {
                    "outfit_plan": outfit_plan,
                    "styling_advice": "Here's your perfectly curated outfit!",
                    "color_rationale": "Colors chosen to complement each other harmoniously",
                    "trend_notes": "Incorporating current trends while maintaining timeless appeal",
                    "search_queries": {}
                }

            # If search_queries is missing (should not happen with good LLM), create an empty dict
            if "search_queries" not in outfit_plan:
                outfit_plan["search_queries"] = {}

            # Ensure every item has specific details (your existing enhancement)
            outfit_plan = self._enhance_details(outfit_plan, user_preferences)

            return outfit_plan

        except Exception as e:
            print(f"❌ Stylist agent error: {e}")
            import traceback
            traceback.print_exc()
            # Return a lavish fallback outfit based on preferences
            return self._get_lavish_fallback(user_preferences)

    def _enhance_details(self, plan: Dict, prefs: Dict) -> Dict:
        """Ensure every item has specific, detailed descriptions (unchanged from your original)"""
        if "outfit_plan" not in plan:
            return plan

        outfit = plan["outfit_plan"]

        # Add specific details to each item if missing
        for category, item in outfit.items():
            if isinstance(item, dict):
                # Ensure color has shade
                if "color" in item and item["color"] and "shade" not in item["color"].lower():
                    shades = {
                        "blue": ["navy", "cobalt", "sky", "royal", "teal"],
                        "red": ["burgundy", "crimson", "scarlet", "maroon"],
                        "green": ["emerald", "olive", "sage", "forest", "mint"],
                        "purple": ["lavender", "plum", "aubergine", "lilac"],
                        "pink": ["blush", "rose", "magenta", "coral", "fuchsia"],
                        "brown": ["cognac", "tan", "chocolate", "caramel", "beige"],
                        "grey": ["charcoal", "silver", "heather", "slate"],
                        "yellow": ["mustard", "saffron", "lemon", "gold"]
                    }
                    for base, shade_list in shades.items():
                        if base in item["color"].lower():
                            if item["color"].lower() == base:
                                item["color"] = f"{shade_list[0]} {base}"
                            break

                # Ensure fabric is specified
                if "fabric" not in item or not item["fabric"]:
                    season = prefs.get("season", "all")
                    if season in ["winter", "fall", "autumn"]:
                        item["fabric"] = "premium wool blend with luxurious texture"
                    elif season in ["summer", "spring"]:
                        item["fabric"] = "high-quality breathable cotton or linen"
                    else:
                        item["fabric"] = "luxury fabric blend for comfort and style"

                # Ensure fit is specified
                if "fit" not in item or not item["fit"]:
                    item["fit"] = "tailored slim fit that flatters the physique"

                # Ensure "why_it_works" is specified
                if "why_it_works" not in item:
                    item["why_it_works"] = f"Perfectly complements the overall look with its {item.get('color', 'elegant')} hue and sophisticated style"

        return plan

    def _get_lavish_fallback(self, prefs: Dict) -> Dict:
        """
        Ultra-lavish fallback outfit if LLM fails.
        This is your existing fallback, but we add an empty search_queries field
        so the retrieval agent doesn't break.
        """
        occasion = prefs.get("occasion", "casual")
        gender = prefs.get("gender", "unisex")
        primary_color = prefs.get("color_preference", "navy")
        style = prefs.get("style_preference", "elegant")
        season = prefs.get("season", "all")

        complements = {
            "navy": ["cream", "cognac", "gold"],
            "blue": ["white", "brown", "silver"],
            "black": ["white", "red", "gold"],
            "burgundy": ["cream", "navy", "gold"],
            "green": ["cream", "brown", "gold"],
            "pink": ["white", "navy", "rose gold"],
            "purple": ["grey", "silver", "cream"],
            "red": ["black", "white", "gold"],
            "brown": ["cream", "navy", "olive"],
            "grey": ["white", "black", "burgundy"],
            "white": ["navy", "black", "gold"]
        }
        comp = complements.get(primary_color, ["cream", "gold", "navy"])

        # Create lavish outfit based on gender
        if gender == "male":
            if occasion in ["wedding", "reception", "engagement"]:
                return {
                    "outfit_plan": {
                        "sherwani": {
                            "color": f"rich {primary_color} with subtle silver-grey thread work",
                            "style": "classic bandhgala collar, floor-length, with intricate embroidery on collar and placket",
                            "fabric": "luxurious silk velvet blend for royal drape and comfort",
                            "fit": "custom-tailored slim fit that enhances the silhouette",
                            "why_it_works": f"The {primary_color} is sophisticated and regal, perfect for a {occasion}"
                        },
                        "churidar": {
                            "color": f"ivory {comp[0]} with subtle sheen",
                            "style": "classic churidar with perfect gathers",
                            "fabric": "silk cotton blend for comfort and elegant drape",
                            "fit": "perfectly fitted with classic ankle gathers",
                            "why_it_works": f"Provides perfect contrast to the {primary_color} sherwani"
                        },
                        "mojari": {
                            "color": f"rich {comp[1]} brown with gold thread work",
                            "style": "traditional mojari with pointed toe and minimal embellishment",
                            "fabric": "soft premium leather",
                            "why_it_works": f"Warm {comp[1]} tones tie the whole look together"
                        },
                        "watch": {
                            "color": f"{comp[2]}-tone case with cream dial",
                            "style": "elegant dress watch with leather strap",
                            "brand_suggestion": "Tissot or Frederique Constant for luxury feel",
                            "why_it_works": f"{comp[2].capitalize()} complements both primary and accent colors"
                        },
                        "shawl": {
                            "color": f"ivory with {primary_color} and {comp[2]} embroidery",
                            "style": "lightweight pashmina shawl with delicate border",
                            "fabric": "pure pashmina for warmth and luxury",
                            "why_it_works": "Adds sophistication and practicality for evening events"
                        },
                        "fragrance": {
                            "notes": f"warm woody with hints of amber and {comp[2]}",
                            "why_it_works": "Complements the overall luxurious vibe"
                        }
                    },
                    "styling_advice": f"Your {primary_color} sherwani sets a sophisticated foundation. Pair with the ivory churidar for striking contrast. The {comp[1]} mojari adds warmth, while {comp[2]} accessories tie everything together.",
                    "color_rationale": f"{primary_color.capitalize()} and ivory create timeless elegance. {comp[1].capitalize()} adds warmth, while {comp[2].capitalize()} accents provide luxury.",
                    "trend_notes": "Rich jewel tones and velvet textures are trending this season.",
                    "search_queries": {}
                }
            else:
                return {
                    "outfit_plan": {
                        "shirt": {
                            "color": f"crisp white with {primary_color} micro-check pattern",
                            "style": "spread collar, classic fit",
                            "fabric": "premium Egyptian cotton with perfect wrinkle resistance",
                            "fit": "tailored slim fit",
                            "why_it_works": "Versatile base that pairs with everything"
                        },
                        "pants": {
                            "color": f"rich {primary_color}",
                            "style": "flat-front tailored trousers",
                            "fabric": "premium wool blend for perfect drape",
                            "fit": "tailored with slight taper",
                            "why_it_works": f"{primary_color.capitalize()} is sophisticated and versatile"
                        },
                        "blazer": {
                            "color": f"charcoal with subtle {primary_color} overcheck",
                            "style": "single-breasted, two-button, notched lapel",
                            "fabric": "luxury wool blend",
                            "fit": "tailored fit with natural shoulders",
                            "why_it_works": "Adds polish and sophistication"
                        },
                        "shoes": {
                            "color": f"rich {comp[1]} brown leather",
                            "style": "oxford or derby with classic broguing",
                            "material": "premium full-grain leather",
                            "why_it_works": f"{comp[1].capitalize()} brown leather adds warmth and character"
                        },
                        "watch": {
                            "color": f"{comp[2]}-tone case with navy dial",
                            "style": "classic dress watch on leather strap",
                            "why_it_works": f"{comp[2].capitalize()} accents tie the look together"
                        }
                    },
                    "styling_advice": f"Start with the crisp white shirt with {primary_color} pattern, then add the {primary_color} trousers for a coordinated base. The charcoal blazer adds sophistication, while {comp[1]} shoes and {comp[2]} watch provide warm accents.",
                    "color_rationale": f"{primary_color.capitalize()} and charcoal create a professional palette, warmed by {comp[1]} accessories. {comp[2].capitalize()} adds a touch of luxury.",
                    "trend_notes": "Pattern mixing is trending - the micro-check shirt under a solid blazer shows confident styling.",
                    "search_queries": {}
                }
        else:  # female
            if occasion in ["wedding", "reception", "engagement"]:
                return {
                    "outfit_plan": {
                        "lehenga": {
                            "color": f"rich {primary_color} with {comp[2]} and ivory dupatta",
                            "style": "flared A-line lehenga with intricate embroidery",
                            "fabric": "luxurious silk with velvet border",
                            "fit": "perfectly fitted blouse with back detail",
                            "why_it_works": f"{primary_color.capitalize()} is festive yet sophisticated"
                        },
                        "choli": {
                            "color": f"{primary_color} with {comp[2]} accents",
                            "style": "designer blouse with elegant neckline and sleeve detail",
                            "fabric": "silk with embroidery matching the lehenga",
                            "fit": "custom-fitted for perfect silhouette",
                            "why_it_works": "Coordinates perfectly with the lehenga while adding design interest"
                        },
                        "dupatta": {
                            "color": f"ivory {comp[0]} with {primary_color} and {comp[2]} embroidery",
                            "style": "lightweight dupatta with intricate border and fall",
                            "fabric": "chiffon or net for graceful drape",
                            "why_it_works": f"Adds ethereal beauty and completes the bridal look"
                        },
                        "jewelry_set": {
                            "necklace": {
                                "color": f"{comp[2]} with {primary_color} enamel work",
                                "style": "choker set with matching earrings",
                                "material": f"{comp[2].capitalize()}-plated with uncut diamonds or crystals",
                                "why_it_works": f"Traditional yet modern, {comp[2]} jewelry complements {primary_color} perfectly"
                            },
                            "earrings": {
                                "style": "matching chandbalis or jhumkas",
                                "why_it_works": "Frames the face beautifully"
                            },
                            "bangles": {
                                "color": f"set of {comp[2]} and {primary_color} bangles",
                                "style": "traditional set with minimal design",
                                "why_it_works": "Adds the perfect finishing touch"
                            }
                        },
                        "footwear": {
                            "color": f"{comp[1]} or gold embellished",
                            "style": "comfortable heels or embellished juttis",
                            "why_it_works": f"{comp[1].capitalize()} ties to the warm undertones"
                        },
                        "clutch": {
                            "color": f"{comp[2]} with {primary_color} embroidery",
                            "style": "potli bag or box clutch",
                            "why_it_works": "Practical yet perfectly coordinated"
                        },
                        "fragrance": {
                            "notes": f"floral with warm {comp[2]} and vanilla base",
                            "why_it_works": "Creates a memorable impression"
                        }
                    },
                    "styling_advice": f"Your {primary_color} lehenga is the star. The ivory dupatta with {primary_color} and {comp[2]} embroidery adds ethereal beauty. Complete with the {comp[2]} jewelry set - let it be the statement.",
                    "color_rationale": f"{primary_color.capitalize()} is rich and festive. Ivory softens the look, while {comp[2]} adds traditional bridal warmth.",
                    "trend_notes": f"{primary_color.capitalize()} is the new red for weddings. Minimal but statement jewelry is preferred.",
                    "search_queries": {}
                }
            else:
                return {
                    "outfit_plan": {
                        "dress": {
                            "color": f"{primary_color} in a rich jewel tone",
                            "style": "fit-and-flare midi dress with elegant neckline",
                            "fabric": "premium crepe or silk blend",
                            "fit": "tailored fit that skims the body beautifully",
                            "why_it_works": "Flattering silhouette suitable for various occasions"
                        },
                        "jacket": {
                            "color": f"cream {comp[0]}",
                            "style": "tailored blazer or structured topper",
                            "fabric": "luxury wool blend",
                            "fit": "slightly oversized for modern appeal",
                            "why_it_works": "Adds sophistication and versatility"
                        },
                        "footwear": {
                            "color": f"{comp[1]} nude or metallic",
                            "style": "pointed-toe pumps or elegant block heels",
                            "material": "quality leather or suede",
                            "why_it_works": "Lengthens the leg and adds polish"
                        },
                        "bag": {
                            "color": f"{comp[2]}",
                            "style": "structured top-handle bag or elegant clutch",
                            "why_it_works": "The perfect accessory to complete the look"
                        },
                        "jewelry": {
                            "earrings": {
                                "style": "statement earrings in complementary metal",
                                "why_it_works": "Frames the face and adds personality"
                            },
                            "watch": {
                                "color": f"{comp[2]} with minimalist design",
                                "style": "elegant timepiece",
                                "why_it_works": "Adds sophistication while being functional"
                            }
                        }
                    },
                    "styling_advice": f"Let the {primary_color} dress be your canvas. Layer with the cream blazer for sophistication. {comp[1]} heels elongate your silhouette, while {comp[2]} accessories add the perfect finishing touches.",
                    "color_rationale": f"{primary_color.capitalize()} is the hero - confident and elegant. Cream softens and adds sophistication.",
                    "trend_notes": "Monochromatic dressing with one statement color is trending.",
                    "search_queries": {}
                }