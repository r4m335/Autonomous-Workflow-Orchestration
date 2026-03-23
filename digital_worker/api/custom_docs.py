from fastapi.responses import HTMLResponse

def get_premium_swagger_ui_html(openapi_url: str, title: str):
    """
    Constructs a custom Swagger UI HTML with premium CSS and 
    Response Visualization JS injected.
    """
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="stylesheet" href="/static/swagger_premium.css">
        <link rel="icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <style>
            /* Extra injection for the visualizer button */
            .visualize-btn:hover {{
                filter: brightness(1.2);
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({{
                url: '{openapi_url}',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true
            }});
        </script>
        <script src="/static/swagger_visualizer.js"></script>
    </body>
    </html>
    """)
