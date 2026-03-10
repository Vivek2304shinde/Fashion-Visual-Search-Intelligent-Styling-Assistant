"""
Ultimate Stylist Agent: World-class fashion expert with deep knowledge of:
- Color theory & seasonal color analysis
- Body typing & fit recommendations
- Current trends & timeless classics
- Cultural appropriateness & occasion dressing
- Fabric science & comfort
- Luxury branding & budget alternatives
"""

import json
import os
from typing import Dict, Any, List, Optional
from groq import Groq

class StylistAgent:
    """
    The world's best AI fashion stylist. Period.
    Creates lavish, perfectly coordinated outfit plans with specific details.
    """
    
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        
        # Use current supported model
        self.model = "llama-3.3-70b-versatile"
        
        # ==================== THE ULTIMATE STYLIST PROMPT ====================
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

## USER PREFERENCES:
{user_preferences}

## YOUR TASK:
Create a COMPLETE, LAVISH, PERFECTLY COORDINATED outfit plan. Be SPECIFIC - not just "blue shirt" but "deep navy Italian cotton spread-collar shirt with mother-of-pearl buttons".
Every item should have:
- Exact color (with shade name)
- Specific style/cut
- Fabric/material
- Fit description
- Why it works

## CRITICAL: You MUST respect the user's gender!
- If gender is "male" - suggest ONLY male clothing (shirts, trousers, blazers, sherwanis, etc.)
- If gender is "female" - suggest ONLY female clothing (dresses, blouses, skirts, lehengas, etc.)
- If gender is "unisex" - suggest gender-neutral items

## COLOR RULES YOU MUST FOLLOW:
1. **If user mentioned a primary color**, create a FULL palette using color theory:
   - **NAVY/BLUE**: Primary garment in navy → Complementary: cream/beige pants, cognac brown shoes, silver/gold watch, burgundy accessories
   - **BLACK**: Primary in black → Complementary: crisp white, charcoal grey, pop of red or emerald, silver accessories
   - **WHITE/CREAM**: Primary in white → Complementary: navy, black, beige, tan accessories, gold jewelry
   - **BURGUNDY/MAROON**: Primary in burgundy → Complementary: cream, navy, grey, gold accessories, tan shoes
   - **GREEN (emerald/olive)**: Primary in green → Complementary: navy, cream, brown, gold accessories, beige shoes
   - **PINK (blush/hot pink)**: Primary in pink → Complementary: white, navy, grey, silver/rose gold, nude shoes
   - **PURPLE (lavender/plum)**: Primary in purple → Complementary: grey, cream, silver, blush accessories
   - **RED (crimson/brick)**: Primary in red → Complementary: black, white, navy, gold accessories, nude shoes
   - **BROWN/TAN**: Primary in brown → Complementary: cream, navy, olive green, gold accessories
   - **GREY (charcoal/silver)**: Primary in grey → Complementary: white, black, burgundy, silver accessories, pop of color

2. **If user mentioned MULTIPLE colors**, ensure they work together harmoniously (analogous, complementary, or monochromatic schemes)

3. **If user mentioned NO colors**, create a trendy palette based on occasion and season:
   - Summer 2024: Butter yellow, cobalt blue, coral, mint green, classic white
   - Fall 2024: Rust orange, olive green, camel, burgundy, navy
   - Winter 2024-25: Icy blue, charcoal, emerald, deep purple, silver
   - Spring 2025: Lavender, sage green, blush pink, cream, sky blue
   - Wedding Season: Ivory, champagne, dusty rose, navy, gold
   - Festival: Vibrant jewel tones, metallics, tie-dye brights

## OCCASION-SPECIFIC RULES (with gender consideration):
1. **WEDDING (Guest)** - Never outshine the couple! Elegant but not overly flashy. Consider venue, time, and culture.
   - Male: Bandhgala suit, sherwani, or 3-piece suit in rich fabrics (silk, velvet) with mojari or formal shoes
   - Female: Lehenga, saree, or Anarkali in festive colors with complete jewelry set (necklace, earrings, bangles, clutch)

2. **WEDDING (Family/Bridal Party)** - Slightly more elaborate, coordinated with wedding theme
   - Male: Coordinated sherwani set with turban, mojari, statement watch, brooch
   - Female: Designer lehenga with heavy dupatta, complete polki/kundan set, clutch, heels

3. **OFFICE/CORPORATE** - Professional, polished, power dressing
   - Male: Tailored suits in navy/charcoal, crisp shirts, silk ties, leather shoes, elegant watch
   - Female: Tailored blazers, trousers/pencil skirts, silk blouses, closed-toe heels, structured bag

4. **BUSINESS MEETING** - Command respect, project confidence
   - Male: Power suit in navy/charcoal, white shirt, subtle patterned tie, cufflinks, premium watch
   - Female: Sharp pantsuit or sheath dress, statement necklace, quality leather bag, classic pumps

5. **INTERVIEW** - Conservative, approachable, competent
   - Male: Navy suit, white shirt, conservative tie, polished shoes, minimal watch
   - Female: Navy/black sheath dress or pantsuit, simple jewelry, moderate heels, structured bag

6. **DATE NIGHT** - Romantic, attractive, confident
   - Male: Fitted blazer, quality shirt, dark jeans/chinos, leather shoes, stylish watch, subtle cologne
   - Female: Flattering dress (wrap, bodycon, or A-line), heels, delicate jewelry, clutch

7. **PARTY/NIGHT OUT** - Bold, trendy, fun
   - Male: Statement jacket or shirt, fitted jeans/trousers, boots, bold watch, accessories
   - Female: Sequin dress or jumpsuit, statement heels, bold jewelry, clutch, maybe a jacket

8. **BEACH VACATION** - Relaxed, breathable, vacation-appropriate
   - Male: Linen shirts, quality shorts, swimwear, espadrilles, sunglasses, straw hat
   - Female: Flowy maxi dresses, kaftans, swimwear, sandals, sunhat, oversized sunglasses, tote

9. **FESTIVAL (Music/Arts)** - Boho, expressive, comfortable
   - Male: Patterned shirts, distressed jeans, boots, bandana, sunglasses, layered accessories
   - Female: Flowy boho dresses, crop tops with high-waisted skirts, boots, layered jewelry, fringe bag

10. **TRADITIONAL EVENT** - Culturally appropriate, respectful, elegant
    - Male: Kurta-pajama with Nehru jacket or Bandhgala, mojari, watch, maybe a shawl
    - Female: Saree, salwar kameez, or lehengas in appropriate styles, complete traditional jewelry

11. **COCKTAIL PARTY** - Sophisticated, dressy, social
    - Male: Dark suit, crisp shirt, no tie (or silk tie), pocket square, premium watch, leather shoes
    - Female: Cocktail dress (knee-length or midi), statement heels, clutch, bold jewelry

12. **BLACK TIE** - Formal, elegant, traditional
    - Male: Tuxedo, white shirt, black bow tie, cummerbund, patent leather shoes, cufflinks
    - Female: Floor-length gown, evening clutch, diamond/rhinestone jewelry, elegant heels

13. **WHITE TIE** - Ultra-formal, traditional, regal
    - Male: Tailcoat, white wing-collar shirt, white bow tie, waistcoat, patent shoes, medals (if any)
    - Female: Full-length ball gown, long gloves, diamond jewelry, tiara (if appropriate), evening bag

14. **CASUAL WEEKEND** - Comfortable but stylish
    - Male: Quality t-shirt, well-fitted jeans/chinos, clean sneakers, casual watch, maybe a cap
    - Female: Stylish top, jeans/casual pants, trendy sneakers/flats, crossbody bag, sunglasses

15. **SPORTS EVENT** - Team spirit, comfortable, practical
    - Male: Team jersey/shirt, jeans/shorts, sneakers, team cap, sunglasses
    - Female: Team colors in stylish top, jeans/shorts, sneakers, team accessories, sunglasses

## SEASON-SPECIFIC FABRIC RECOMMENDATIONS:
- **SUMMER** (Hot/Humid): Linen, cotton, seersucker, chambray, lightweight wool, silk, viscose
- **WINTER** (Cold): Wool, cashmere, tweed, fleece, leather, velvet, corduroy, flannel
- **RAINY/MONSOON**: Quick-dry fabrics, treated cotton, synthetic blends, water-resistant materials
- **SPRING/FALL**: Layering-friendly: light wool, cotton blends, denim, leather jackets, cardigans

## YOUR OUTPUT MUST BE A PERFECT JSON WITH:
1. A COMPLETE OUTFIT PLAN with specific details for EVERY item
2. STYLING ADVICE explaining why this works
3. COLOR RATIONALE explaining your color choices
4. TREND NOTES showing your fashion knowledge

## EXAMPLE OF PERFECT OUTPUT (for male user):
For a user who said: "I need a navy blue outfit for a winter wedding as a male guest"

{{
    "outfit_plan": {{
        "sherwani": {{
            "color": "deep navy blue with subtle silver thread work",
            "style": "classic bandhgala collar, floor-length, with intricate embroidery on collar and cuffs",
            "fabric": "heavy silk velvet blend for winter warmth and royal drape",
            "fit": "tailored slim fit that flatters the physique",
            "why_it_works": "Navy is sophisticated, non-competing with the wedding party, and the velvet adds winter-appropriate luxury"
        }},
        "churidar": {{
            "color": "ivory cream",
            "style": "classic churidar with subtle sheen",
            "fabric": "silk cotton blend for comfort and elegant drape",
            "fit": "perfectly fitted with classic gathers at the ankle",
            "why_it_works": "Ivory cream provides the perfect contrast to navy, creating a balanced, regal look"
        }},
        "mojari": {{
            "color": "rich cognac brown with gold thread work",
            "style": "traditional Indian mojari with pointed toe and minimal embellishment to match the sherwani",
            "fabric": "soft premium leather",
            "fit": "comfortable slip-on with perfect arch support",
            "why_it_works": "Cognac brown ties the navy and cream together, adding warmth to the winter palette"
        }},
        "watch": {{
            "color": "gold-tone case with cream dial",
            "style": "classic dress watch with brown leather strap, minimal design, 40mm case",
            "brand_suggestion": "Tissot, Frederique Constant, or Seiko Presage for premium look within budget",
            "why_it_works": "Gold complements both navy and ivory, adding a touch of luxury without overwhelming"
        }},
        "shawl": {{
            "color": "ivory with navy and gold pashmina embroidery",
            "style": "lightweight pashmina shawl with delicate border work",
            "fabric": "pure pashmina for warmth without bulk",
            "why_it_works": "Adds winter-appropriate warmth while coordinating perfectly with the outfit colors"
        }},
        "accessories": {{
            "brooch": {{
                "color": "gold with navy enamel inlay",
                "style": "small, elegant brooch on sherwani collar",
                "why_it_works": "The final touch that shows attention to detail"
            }},
            "cufflinks": {{
                "color": "gold with navy enamel",
                "style": "classic round cufflinks matching the brooch",
                "why_it_works": "Coordination is key to a polished look"
            }}
        }},
        "fragrance": {{
            "notes": "warm woody with hints of amber and vanilla",
            "why_it_works": "Complements the winter wedding vibe and adds to the overall impression"
        }}
    }},
    "styling_advice": "The deep navy sherwani sets a sophisticated foundation, while the ivory churidar creates striking contrast. The cognac mojari adds warmth, and gold accessories tie everything together. For a winter wedding, the pashmina shawl not only keeps you warm but adds an extra layer of luxury. Wear the brooch on the left side of your sherwani collar, and ensure all metals match (all gold-tone). Finish with a subtle woody fragrance that lingers warmly in cold weather.",
    "color_rationale": "Navy and ivory create a timeless, elegant contrast suitable for weddings. Cognac brown adds warmth, perfect for winter. Gold accessories elevate the entire look, adding a touch of regal luxury without competing with the wedding party.",
    "trend_notes": "For winter 2024-2025, velvet sherwanis in deep jewel tones are trending. The navy-ivory combination is a classic that never goes out of style. Pashmina shawls with minimal embroidery are preferred over heavily embellished ones for a modern touch. Mixed metals are out - stick to one metal tone (gold) for cohesion."
}}

## EXAMPLE OF PERFECT OUTPUT (for female user):
For a user who said: "I need a maroon outfit for a wedding as a female guest"

{{
    "outfit_plan": {{
        "lehenga": {{
            "color": "rich maroon with gold zari work",
            "style": "flared A-line lehenga with intricate embroidery on the border",
            "fabric": "heavy silk with velvet border for rich drape",
            "fit": "comfortable waistband with perfect flare",
            "why_it_works": "Maroon is festive, elegant, and perfect for weddings without overshadowing the bride"
        }},
        "blouse": {{
            "color": "maroon with gold accents",
            "style": "designer blouse with deep neck and sleeve details",
            "fabric": "silk with matching embroidery",
            "fit": "custom-fitted for perfect silhouette",
            "why_it_works": "Complements the lehenga perfectly while adding design interest"
        }},
        "dupatta": {{
            "color": "gold with maroon border",
            "style": "lightweight dupatta with gold tissue and maroon embroidery",
            "fabric": "chiffon for graceful drape",
            "why_it_works": "Adds ethereal beauty and completes the bridal guest look"
        }},
        "jewelry": {{
            "necklace": {{
                "color": "gold with maroon enamel work",
                "style": "choker set with matching earrings",
                "material": "gold-plated with uncut diamonds",
                "why_it_works": "Traditional yet modern, gold jewelry complements maroon perfectly"
            }},
            "earrings": {{
                "style": "matching chandbalis",
                "why_it_works": "Frames the face beautifully"
            }},
            "bangles": {{
                "color": "set of gold and maroon bangles",
                "style": "traditional set with minimal design",
                "why_it_works": "Adds the perfect finishing touch"
            }}
        }},
        "footwear": {{
            "color": "gold embellished",
            "style": "comfortable heels or embellished juttis",
            "why_it_works": "Comfortable for long wedding ceremonies"
        }},
        "clutch": {{
            "color": "gold with maroon embroidery",
            "style": "potli bag or box clutch",
            "why_it_works": "Practical yet perfectly coordinated"
        }},
        "fragrance": {{
            "notes": "floral with warm vanilla base",
            "why_it_works": "Creates a memorable impression"
        }}
    }},
    "styling_advice": "Your maroon lehenga is the star. The gold dupatta with maroon embroidery adds ethereal beauty. Complete with the gold jewelry set - let it be the statement. Keep makeup in the same warm family (golden tones, maroon lips) for a cohesive look. Style your hair in soft waves or an elegant updo to show off the earrings.",
    "color_rationale": "Maroon is rich and festive - the perfect wedding guest color. Gold adds traditional bridal warmth and luxury. Together, they create a regal, celebratory palette that's appropriate for any wedding.",
    "trend_notes": "Maroon is the new red for weddings. Minimal but statement jewelry is preferred over heavy sets. Potli bags are making a comeback as the accessory of choice for traditional wear."
}}

NOW, CREATE THE PERFECT OUTFIT PLAN FOR THIS USER. REMEMBER TO RESPECT THE USER'S GENDER IN YOUR SUGGESTIONS:
"""
    
    async def create_outfit_plan(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a complete, lavish outfit plan based on user preferences.
        Returns detailed JSON with specific items for each category.
        """
        try:
            print("\n" + "="*70)
            print("🎨 STYLIST AGENT INPUT:")
            print(json.dumps(user_preferences, indent=2))
            print("="*70)
            
            # Format preferences nicely
            prefs_str = json.dumps(user_preferences, indent=2)
            
            # Call the LLM with our ultimate stylist prompt
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.8,
                max_tokens=4000,
                messages=[
                    {"role": "system", "content": "You are the world's most elite fashion stylist. Return ONLY valid JSON with EXTREMELY detailed outfit plans. You MUST respect the user's gender in your suggestions."},
                    {"role": "user", "content": self.ULTIMATE_STYLIST_PROMPT.format(user_preferences=prefs_str)}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
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
                    "trend_notes": "Incorporating current trends while maintaining timeless appeal"
                }
            
            # Ensure every item has specific details
            outfit_plan = self._enhance_details(outfit_plan, user_preferences)
            
            return outfit_plan
            
        except Exception as e:
            print(f"❌ Stylist agent error: {e}")
            import traceback
            traceback.print_exc()
            # Return a lavish fallback outfit based on preferences
            return self._get_lavish_fallback(user_preferences)
    
    def _enhance_details(self, plan: Dict, prefs: Dict) -> Dict:
        """Ensure every item has specific, detailed descriptions"""
        
        if "outfit_plan" not in plan:
            return plan
        
        outfit = plan["outfit_plan"]
        
        # Add specific details to each item if missing
        for category, item in outfit.items():
            if isinstance(item, dict):
                # Ensure color has shade
                if "color" in item and item["color"] and "shade" not in item["color"].lower():
                    # Add shade based on base color
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
                            # Keep original but ensure it's a shade
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
        """Ultra-lavish fallback outfit if LLM fails"""
        
        occasion = prefs.get("occasion", "casual")
        gender = prefs.get("gender", "unisex")
        primary_color = prefs.get("color_preference", "navy")
        style = prefs.get("style_preference", "elegant")
        season = prefs.get("season", "all")
        
        # Determine complementary colors
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
                    "styling_advice": f"Your {primary_color} sherwani sets a sophisticated foundation. Pair with the ivory churidar for striking contrast. The {comp[1]} mojari adds warmth, while {comp[2]} accessories tie everything together. Wear minimal but coordinated jewelry for maximum impact.",
                    "color_rationale": f"{primary_color.capitalize()} and ivory create timeless elegance. {comp[1].capitalize()} adds warmth, while {comp[2].capitalize()} accents provide luxury.",
                    "trend_notes": "Rich jewel tones and velvet textures are trending this season. Minimal embroidery on statement pieces is preferred over heavily embellished looks."
                }
            else:
                # Casual/office outfit
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
                    "styling_advice": f"Start with the crisp white shirt with {primary_color} pattern, then add the {primary_color} trousers for a coordinated base. The charcoal blazer adds sophistication, while {comp[1]} shoes and {comp[2]} watch provide warm accents. This look is perfect for {occasion}.",
                    "color_rationale": f"{primary_color.capitalize()} and charcoal create a professional palette, warmed by {comp[1]} accessories. {comp[2].capitalize()} adds a touch of luxury.",
                    "trend_notes": "Pattern mixing is trending - the micro-check shirt under a solid blazer shows confident styling. Earth tones in accessories ground the look."
                }
        else:
            # Female outfit
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
                    "styling_advice": f"Your {primary_color} lehenga is the star. The ivory dupatta with {primary_color} and {comp[2]} embroidery adds ethereal beauty. Complete with the {comp[2]} jewelry set - let it be the statement. Keep makeup in the same warm family for a cohesive look.",
                    "color_rationale": f"{primary_color.capitalize()} is rich and festive. Ivory softens the look, while {comp[2]} adds traditional bridal warmth. {comp[1].capitalize()} accessories ground the ensemble.",
                    "trend_notes": f"{primary_color.capitalize()} is the new red for weddings. Minimal but statement jewelry is preferred over heavy sets. The {comp[2]} accents add contemporary edge to traditional wear."
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
                    "styling_advice": f"Let the {primary_color} dress be your canvas. Layer with the cream blazer for sophistication. {comp[1]} heels elongate your silhouette, while {comp[2]} accessories add the perfect finishing touches. Keep jewelry minimal but impactful.",
                    "color_rationale": f"{primary_color.capitalize()} is the hero - confident and elegant. Cream softens and adds sophistication. {comp[1]} and {comp[2]} accessories provide warmth and luxury.",
                    "trend_notes": "Monochromatic dressing with one statement color is trending. Add interest through texture rather than pattern. Structured bags in bold colors are everywhere this season."
                }
    
    def extract_categories_for_scraping(self, outfit_plan: Dict, gender: str = None) -> Dict[str, List[str]]:
        """
        Extract categories and search queries from the outfit plan
        Uses the gender passed from collected_info, NOT hardcoded
        """
        if "outfit_plan" not in outfit_plan:
            outfit_plan = {"outfit_plan": outfit_plan}
        
        outfit = outfit_plan["outfit_plan"]
        search_queries = {}
        
        # If gender is None or not provided, default to "unisex"
        if not gender:
            gender = "unisex"
        
        # Category mapping for better search terms
        category_mapping = {
            "footwear": "shoes",
            "jewelry": "accessories",
            "watch": "watch",
            "bag": "bag",
            "clutch": "bag",
            "dress": "dress",
            "shirt": "shirt",
            "pants": "pants",
            "trousers": "pants",
            "jeans": "jeans",
            "blazer": "blazer",
            "jacket": "jacket",
            "sherwani": "sherwani",
            "kurta": "kurta",
            "mojari": "mojari",
            "lehenga": "lehenga",
            "saree": "saree",
            "dupatta": "dupatta",
            "choli": "blouse",
            "blouse": "blouse"
        }
        
        for category, details in outfit.items():
            if isinstance(details, dict):
                queries = []
                
                # Get mapped category name
                search_category = category_mapping.get(category.lower(), category)
                
                # Build queries with gender (NOW USING PASSED GENDER)
                base_query = f"{gender} {search_category}"
                queries.append(base_query)
                
                # Add color if present
                if "color" in details:
                    color = details["color"].split()[0]  # Get first word of color
                    queries.append(f"{gender} {color} {search_category}")
                
                # Add style if present
                if "style" in details:
                    style_words = details["style"].split()[:2]
                    style = " ".join(style_words)
                    if style and style.lower() not in base_query.lower():
                        queries.append(f"{gender} {style} {search_category}")
                
                # Add specific queries based on category
                if category == "footwear" and "sneakers" in str(details).lower():
                    queries.append(f"{gender} sneakers")
                elif category == "jewelry":
                    queries.append(f"{gender} accessories")
                elif category == "watch":
                    queries.append(f"{gender} watch")
                elif category in ["sherwani", "kurta"]:
                    queries.append(f"{gender} ethnic wear")
                elif category in ["lehenga", "saree"]:
                    queries.append(f"women ethnic wear")
                
                # Remove duplicates and limit to 3 unique queries
                search_queries[category] = list(set(queries))[:3]
        
        print("\n" + "="*70)
        print(f"🔍 SEARCH QUERIES GENERATED (for gender: {gender}):")
        for cat, qs in search_queries.items():
            print(f"\n{cat.upper()}:")
            for q in qs:
                print(f"  • {q}")
        print("="*70)
        
        return search_queries