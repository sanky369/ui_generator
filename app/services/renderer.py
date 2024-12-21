from typing import Dict, Any
import json
import traceback

class HTMLRenderer:
    @staticmethod
    def generate_html(ui_data: Dict[str, Any]) -> str:
        """Generate HTML from UI data."""
        try:
            print(f"[Renderer] Starting HTML generation")
            
            # Extract data
            components = ui_data.get("ui_components", [])
            layout = ui_data.get("layout", {})
            design_tokens = ui_data.get("design_tokens", {})
            
            print(f"[Renderer] Components: {json.dumps(components, indent=2)}")
            print(f"[Renderer] Layout: {json.dumps(layout, indent=2)}")
            
            # Generate CSS
            css = HTMLRenderer._generate_css(design_tokens)
            
            # Generate component HTML
            components_html = ""
            for component in components:
                try:
                    component_html = HTMLRenderer._render_component(component)
                    components_html += component_html
                except Exception as e:
                    print(f"[Renderer] Error rendering component: {str(e)}")
                    print(f"[Renderer] Component data: {json.dumps(component, indent=2)}")
                    continue
            
            # Apply layout
            layout_html = HTMLRenderer._render_layout(layout, components_html)
            
            # Final HTML
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>UI Preview</title>
                <style>
                    {css}
                </style>
            </head>
            <body>
                {layout_html}
            </body>
            </html>
            """
            
            print(f"[Renderer] Successfully generated HTML")
            return html
            
        except Exception as e:
            print(f"[Renderer] Error generating HTML: {str(e)}")
            print(f"[Renderer] Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to generate HTML: {str(e)}")

    @staticmethod
    def _generate_css(design_tokens: Dict[str, Any]) -> str:
        """Generate CSS from design tokens."""
        try:
            print(f"[Renderer] Generating CSS from design tokens")
            
            # Extract tokens
            colors = design_tokens.get("colors", {})
            typography = design_tokens.get("typography", {})
            spacing = design_tokens.get("spacing", {})
            
            # Base styles
            css = """
                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                
                body {
                    font-family: %(fontFamily)s;
                    font-size: %(fontSize)s;
                    line-height: %(lineHeight)s;
                    color: %(textColor)s;
                    background-color: %(bgColor)s;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: %(containerPadding)s;
                }
                
                .button {
                    background-color: %(primaryColor)s;
                    color: white;
                    border: none;
                    padding: %(buttonPadding)s;
                    border-radius: %(buttonRadius)s;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                
                .button:hover {
                    background-color: %(primaryDarkColor)s;
                }
                
                .input {
                    width: 100%%;
                    padding: %(inputPadding)s;
                    border: 1px solid %(borderColor)s;
                    border-radius: %(inputRadius)s;
                    font-size: %(inputFontSize)s;
                }
                
                .heading {
                    color: %(headingColor)s;
                    margin-bottom: %(headingMargin)s;
                }
                
                .text {
                    margin-bottom: %(textMargin)s;
                }
                
                .image {
                    max-width: 100%%;
                    height: auto;
                }
            """ % {
                "fontFamily": typography.get("fontFamily", "system-ui, -apple-system, sans-serif"),
                "fontSize": typography.get("fontSize", {}).get("base", "16px"),
                "lineHeight": typography.get("lineHeight", {}).get("normal", "1.5"),
                "textColor": colors.get("text", "#000000"),
                "bgColor": colors.get("background", "#FFFFFF"),
                "primaryColor": colors.get("primary", "#0066FF"),
                "primaryDarkColor": colors.get("primary", "#0052CC"),
                "borderColor": colors.get("border", "#E2E8F0"),
                "containerPadding": spacing.get("lg", "1.5rem"),
                "buttonPadding": spacing.get("sm", "0.5rem") + " " + spacing.get("md", "1rem"),
                "buttonRadius": "0.25rem",
                "inputPadding": spacing.get("sm", "0.5rem"),
                "inputRadius": "0.25rem",
                "inputFontSize": typography.get("fontSize", {}).get("base", "16px"),
                "headingColor": colors.get("text", "#000000"),
                "headingMargin": spacing.get("md", "1rem"),
                "textMargin": spacing.get("sm", "0.5rem")
            }
            
            print(f"[Renderer] Successfully generated CSS")
            return css
            
        except Exception as e:
            print(f"[Renderer] Error generating CSS: {str(e)}")
            print(f"[Renderer] Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to generate CSS: {str(e)}")

    @staticmethod
    def _render_component(component: Dict[str, Any]) -> str:
        """Render a single component to HTML."""
        try:
            component_type = component.get("type")
            props = component.get("props", {})
            
            if not component_type:
                raise ValueError("Component missing 'type' field")
            
            # Common attributes
            id_attr = f' id="{props.get("id", "")}"' if props.get("id") else ""
            class_attr = f' class="{props.get("className", "")}"' if props.get("className") else ""
            style_attr = f' style="{";".join([f"{k}:{v}" for k,v in props.get("style", {}).items()])}"' if props.get("style") else ""
            
            # Render based on type
            if component_type == "input":
                return f"""
                    <div class="form-group">
                        <label for="{props.get("id")}">{props.get("label", "")}</label>
                        <input type="{props.get("type", "text")}"
                               name="{props.get("name", "")}"
                               placeholder="{props.get("placeholder", "")}"
                               value="{props.get("value", "")}"
                               {"required" if props.get("required") else ""}
                               {id_attr}
                               class="input{class_attr}"
                               {style_attr}>
                    </div>
                """
            elif component_type == "button":
                return f"""
                    <button{id_attr} 
                            class="button{class_attr}"
                            {"disabled" if props.get("disabled") else ""}
                            {style_attr}>
                        {props.get("text", "Button")}
                    </button>
                """
            elif component_type == "image":
                return f"""
                    <img src="{props.get("src", "")}"
                         alt="{props.get("alt", "")}"
                         style="object-fit: {props.get("objectFit", "cover")}{style_attr}"
                         {id_attr}
                         class="image{class_attr}">
                """
            elif component_type == "heading":
                level = props.get("level", 1)
                return f"""
                    <h{level}{id_attr} 
                           class="heading{class_attr}"
                           {style_attr}>
                        {props.get("text", "")}
                    </h{level}>
                """
            elif component_type == "text":
                return f"""
                    <p{id_attr} 
                       class="text{class_attr}"
                       {style_attr}>
                        {props.get("text", "")}
                    </p>
                """
            else:
                raise ValueError(f"Unknown component type: {component_type}")
                
        except Exception as e:
            print(f"[Renderer] Error rendering component: {str(e)}")
            print(f"[Renderer] Component data: {json.dumps(component, indent=2)}")
            raise Exception(f"Failed to render component: {str(e)}")

    @staticmethod
    def _render_layout(layout: Dict[str, Any], content: str) -> str:
        """Render the layout with content."""
        try:
            layout_type = layout.get("type", "flex")
            props = layout.get("props", {})
            
            # Generate style based on layout type
            style = ""
            if layout_type == "flex":
                style = f"""
                    display: flex;
                    flex-direction: {props.get("direction", "column")};
                    gap: {props.get("spacing", "1rem")};
                    align-items: {props.get("align", "center")};
                    justify-content: {props.get("justify", "center")};
                """
            elif layout_type == "grid":
                style = f"""
                    display: grid;
                    grid-template-columns: {props.get("columns", "1fr")};
                    gap: {props.get("spacing", "1rem")};
                    align-items: {props.get("align", "center")};
                    justify-content: {props.get("justify", "center")};
                """
            
            return f"""
                <div class="container" style="{style}">
                    {content}
                </div>
            """
            
        except Exception as e:
            print(f"[Renderer] Error rendering layout: {str(e)}")
            print(f"[Renderer] Layout data: {json.dumps(layout, indent=2)}")
            raise Exception(f"Failed to render layout: {str(e)}")
