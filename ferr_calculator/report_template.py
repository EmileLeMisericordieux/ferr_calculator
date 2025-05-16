from pretty_html_table import build_table
import plotly.io as pio
import base64


def report_template(
        start_value,
        start_age,
        end_age,
        interest_rate,
        start_paying_on_year,
        paying_type,
        fix_value,
        inflation_rate,
        df,
        fig,
        selection
    ):

    image_html = get_base64_image("ferr_calculator/static/1743878344560-26372b5e-087c-4937-b368-72e4aa19caae_1.jpg")

    fig.update_layout(
        width=1000,   # width in pixels
        height=600,  # height in pixels
        margin=dict(l=50, r=50, t=50, b=50)
    )

    info_to_add = ""
    if paying_type != "Minimum":
        info_to_add = f"Versement fixe: **{format_money(fix_value)}**  \n"
        info_to_add += f"Taux d'inflation: **{format_percent(inflation_rate)}**  \n"


    report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f0f0f0;
        }}
        .graph-container {{
            break-inside: avoid;
            page-break-inside: avoid;
            margin-top: 40px;
        }}
    </style>
</head>
<body>

# Versement de {selection}

<img src={image_html} alt="logo" width="200"/>

Valeur du {selection}: **{format_money(start_value)}** <br>
Début du {selection} à l'âge de: **{start_age}** <br>
Fin du {selection} à l'âge de: **{end_age}** <br>
Taux de rendement: **{format_percent(interest_rate)}** <br>
Commencer les versements durant l'année: **{start_paying_on_year}** <br>
Type de versement: **{paying_type}** <br>
{info_to_add}

{build_table(df, 'blue_dark')}

<div class="graph-container">
    <h2>Graphique de la valeur du {selection}</h2>
    {pio.to_html(fig, full_html=False, include_plotlyjs='cdn')}
</div>


"""

    return report


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"

def format_money(value):
    return f"{value:,.0f}".replace(",", " ") + "$"

def format_percent(value):
    return f"{value:.2f}%"
