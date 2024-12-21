from typing import Dict, Any, List
import json

class UIService:
    @staticmethod
    def generate_layout(components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate layout structure for UI components."""
        return {
            "type": "flex",
            "props": {
                "direction": "column",
                "spacing": "1rem",
                "align": "center",
                "justify": "center"
            },
            "children": components
        }

    @staticmethod
    def generate_design_tokens(style_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate design tokens based on style preferences."""
        return {
            "colors": {
                "primary": style_preferences.get("primary_color", "#0066FF"),
                "secondary": style_preferences.get("secondary_color", "#5856D6"),
                "background": style_preferences.get("background_color", "#FFFFFF"),
                "text": style_preferences.get("text_color", "#000000"),
                "border": style_preferences.get("border_color", "#E2E8F0")
            },
            "typography": {
                "fontFamily": style_preferences.get("font_family", "system-ui, -apple-system, sans-serif"),
                "fontSize": {
                    "base": "16px",
                    "small": "14px",
                    "large": "18px",
                    "heading": "24px"
                },
                "fontWeight": {
                    "normal": "400",
                    "medium": "500",
                    "bold": "600"
                },
                "lineHeight": {
                    "normal": "1.5",
                    "tight": "1.25",
                    "loose": "1.75"
                }
            },
            "spacing": {
                "xs": "0.25rem",
                "sm": "0.5rem",
                "md": "1rem",
                "lg": "1.5rem",
                "xl": "2rem"
            },
            "borderRadius": {
                "sm": "0.25rem",
                "md": "0.375rem",
                "lg": "0.5rem",
                "full": "9999px"
            }
        }
