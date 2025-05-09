import os
import json
import re
import matplotlib.pyplot as plt
from androguard.misc import AnalyzeAPK
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Dangerous permissions
DANGEROUS_PERMISSIONS = [
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.INTERNET"
]

# Regex patterns for secrets
PATTERNS = [
    r"(AKIA|AIza)[0-9A-Z]{16,}",
    r"([A-Za-z0-9]{32,})",
    r"AIza[0-9A-Za-z_-]{35}",
    r"aws_secret_access_key[\"']?\s*[:=]?\s*[\"']?([A-Za-z0-9+/=]{40})",
    r"([A-Za-z0-9]{16,32})"
]

def analyze_apk(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    manifest = a.get_android_manifest_xml()
    debuggable = manifest.find("application").get("debuggable", "false") == "true"

    analysis = {
        "package_name": a.get_package(),
        "permissions": a.get_permissions(),
        "dangerous_permissions": list(filter(lambda p: p in DANGEROUS_PERMISSIONS, a.get_permissions())),
        "activities": a.get_activities(),
        "services": a.get_services(),
        "receivers": a.get_receivers(),
        "providers": a.get_providers(),
        "is_debuggable": debuggable,
        "hardcoded_secrets": find_hardcoded_secrets(dx)
    }

    return analysis

def find_hardcoded_secrets(dx):
    secrets = []
    for method in dx.get_methods():
        try:
            m = method.get_method()
            if m is None:
                continue  # Skip if no method object
            
            code = m.get_source()
            if code:
                if "password" in code.lower() or "apikey" in code.lower() or "secret" in code.lower():
                    secrets.append(m.get_name())
        except Exception as e:
            # Skip any method that causes an error during source extraction
            continue
    return secrets



def save_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def create_graph(data, graph_path):
    categories = ['Activities', 'Services', 'Receivers', 'Providers', 'Dangerous Permissions']
    values = [
        len(data['activities']),
        len(data['services']),
        len(data['receivers']),
        len(data['providers']),
        len(data['dangerous_permissions'])
    ]

    # Danger Level based on dangerous permissions
    danger_count = len(data['dangerous_permissions'])
    if danger_count == 0:
        danger_status = "Safe"
        color = 'lightgreen'
    elif 1 <= danger_count <= 3:
        danger_status = "Risky"
        color = 'orange'
    else:
        danger_status = "Highly Risky"
        color = 'red'

    # Set colors for each bar
    colors_list = ['skyblue', 'lightgreen', 'salmon', 'violet', color]

    plt.figure(figsize=(9, 6))
    bars = plt.bar(categories, values, color=colors_list)
    plt.title('APK Components & Security Overview')
    plt.xlabel('Component Type')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotate each bar with value
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, int(yval), ha='center', va='bottom', fontsize=10)

    # Save chart
    plt.savefig(graph_path)
    plt.close()

    return danger_status

def create_pdf(json_data, output_path):
    # Generate graph and get danger level
    graph_path = 'results/graph.png'
    danger_status = create_graph(json_data, graph_path)

    # Setup PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    title_style.textColor = colors.HexColor('#4F46E5')
    story.append(Paragraph("APK Static Analysis Report", title_style))
    story.append(Spacer(1, 20))

    # Insert graph
    if os.path.exists(graph_path):
        story.append(Image(graph_path, width=450, height=280))
        story.append(Spacer(1, 20))

    # Danger Status Section
    danger_style = ParagraphStyle(
        'DangerStatus',
        parent=styles['Heading2'],
        textColor=colors.red if danger_status == "Highly Risky" else (colors.orange if danger_status == "Risky" else colors.green),
        fontSize=16,
        spaceAfter=10
    )
    story.append(Paragraph(f"Security Status: {danger_status}", danger_style))
    story.append(Spacer(1, 20))

    # Analysis Sections
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        textColor=colors.HexColor('#2563EB'),
        fontSize=14,
        spaceAfter=8
    )

    for key, value in json_data.items():
        if value:
            story.append(Paragraph(f"{key.replace('_', ' ').capitalize()}:", section_style))
            if isinstance(value, list):
                for item in value:
                    story.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                story.append(Paragraph(str(value), styles['Normal']))
            story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)
