from typing import Dict, Any

class UITemplates:
    @staticmethod
    def get_component_template(component_type: str, props: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get a template for a specific UI component type."""
        props = props or {}
        
        templates = {
            "button": {
                "type": "button",
                "style": {
                    "padding": "0.75rem 1.5rem",
                    "borderRadius": "0.375rem",
                    "fontSize": "1rem",
                    "fontWeight": "500",
                    "cursor": "pointer",
                    "border": "none",
                    "backgroundColor": props.get("backgroundColor", "#007AFF"),
                    "color": props.get("color", "#FFFFFF"),
                    "width": props.get("width", "auto"),
                },
                "hover": {
                    "opacity": "0.9"
                }
            },
            "input": {
                "type": "input",
                "style": {
                    "padding": "0.75rem 1rem",
                    "borderRadius": "0.375rem",
                    "fontSize": "1rem",
                    "border": "1px solid #E2E8F0",
                    "width": props.get("width", "100%"),
                    "backgroundColor": props.get("backgroundColor", "#FFFFFF"),
                },
                "focus": {
                    "borderColor": "#007AFF",
                    "outline": "none",
                    "boxShadow": "0 0 0 3px rgba(0,122,255,0.1)"
                }
            },
            "card": {
                "type": "div",
                "style": {
                    "padding": "1.5rem",
                    "borderRadius": "0.5rem",
                    "backgroundColor": props.get("backgroundColor", "#FFFFFF"),
                    "boxShadow": "0 1px 3px 0 rgba(0,0,0,0.1)",
                    "width": props.get("width", "100%"),
                },
                "hover": {
                    "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.1)"
                }
            },
            "text": {
                "type": "p",
                "style": {
                    "fontSize": props.get("fontSize", "1rem"),
                    "color": props.get("color", "#1A202C"),
                    "lineHeight": "1.5",
                    "margin": props.get("margin", "0 0 1rem 0")
                }
            },
            "heading": {
                "type": "h1",
                "style": {
                    "fontSize": props.get("fontSize", "2rem"),
                    "fontWeight": "bold",
                    "color": props.get("color", "#1A202C"),
                    "lineHeight": "1.2",
                    "margin": props.get("margin", "0 0 1.5rem 0")
                }
            },
            "image": {
                "type": "img",
                "style": {
                    "width": props.get("width", "100%"),
                    "height": props.get("height", "auto"),
                    "objectFit": props.get("objectFit", "cover"),
                    "borderRadius": props.get("borderRadius", "0.5rem")
                }
            },
            "container": {
                "type": "div",
                "style": {
                    "width": props.get("width", "100%"),
                    "maxWidth": props.get("maxWidth", "1200px"),
                    "margin": props.get("margin", "0 auto"),
                    "padding": props.get("padding", "1rem")
                }
            },
            "navbar": {
                "type": "nav",
                "style": {
                    "width": "100%",
                    "height": "4rem",
                    "backgroundColor": props.get("backgroundColor", "#FFFFFF"),
                    "boxShadow": "0 1px 3px 0 rgba(0,0,0,0.1)",
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "0 1.5rem"
                }
            },
            "form": {
                "type": "form",
                "style": {
                    "width": props.get("width", "100%"),
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "1rem"
                }
            }
        }
        
        return templates.get(component_type, templates["container"])

    @staticmethod
    def get_layout_template(layout_type: str, props: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get a template for a specific layout type."""
        props = props or {}
        
        layouts = {
            "centered": {
                "type": "div",
                "style": {
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "minHeight": props.get("minHeight", "100vh"),
                    "width": "100%"
                }
            },
            "grid": {
                "type": "div",
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": props.get("columns", "repeat(auto-fit, minmax(250px, 1fr))"),
                    "gap": props.get("gap", "1rem"),
                    "width": "100%"
                }
            },
            "flex": {
                "type": "div",
                "style": {
                    "display": "flex",
                    "flexDirection": props.get("direction", "row"),
                    "gap": props.get("gap", "1rem"),
                    "flexWrap": props.get("wrap", "wrap"),
                    "width": "100%"
                }
            }
        }
        
        return layouts.get(layout_type, layouts["flex"])
