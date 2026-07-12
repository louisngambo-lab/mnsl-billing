import flet as ft
from datetime import datetime, timedelta
import threading
import time
import os
import webbrowser
import urllib.parse

# Importations ReportLab pour correspondre fidèlement à ton modèle de facture
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Création du dossier pour stocker les factures s'il n'existe pas
OS_FACTURES_DIR = "Factures"
if not os.path.exists(OS_FACTURES_DIR):
    os.makedirs(OS_FACTURES_DIR)

# --- BASE DE DONNÉES COMPLÈTE DU RÉPERTOIRE MNSL NETWORK ---
base_clients = [
    {"id_client": "CLI-001", "nom": "Justin Tomeh (Marocain)", "telephone": "+237675588736", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-03"},
    {"id_client": "CLI-002", "nom": "Issia", "telephone": "+237655122642", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 5000, "solde_restant": 0, "date_paiement": "2026-07-04"},
    {"id_client": "CLI-003", "nom": "Fotso Alex", "telephone": "+237698757990", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-07"},
    {"id_client": "CLI-004", "nom": "Blondel Tcheuno (Dagalo)", "telephone": "+237698467331", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-09"},
    {"id_client": "CLI-005", "nom": "Nana Larissa", "telephone": "+237676670440", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-09"},
    {"id_client": "CLI-006", "nom": "Nkong Armel", "telephone": "+237683226153", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-10"},
    {"id_client": "CLI-007", "nom": "Chimela Victor", "telephone": "+237671865767", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-13"},
    {"id_client": "CLI-008", "nom": "Dibo Morgan", "telephone": "+237675851225", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-14"},
    {"id_client": "CLI-009", "nom": "Harison Ndikum (Solution)", "telephone": "+237675603821", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-21"},
    {"id_client": "CLI-010", "nom": "Emma", "telephone": "+237653211952", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-21"},
    {"id_client": "CLI-011", "nom": "Martial", "telephone": "+237690809789", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-23"},
    {"id_client": "CLI-012", "nom": "Gustave Print", "telephone": "+237676732641", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-24"},
    {"id_client": "CLI-013", "nom": "Derick Che", "telephone": "+237673254690", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-25"},
    {"id_client": "CLI-014", "nom": "Justin Menguene", "telephone": "+237679667929", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-26"},
    {"id_client": "CLI-015", "nom": "Hommie (Soft Deal Trade)", "telephone": "+237677313421", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-28"},
    {"id_client": "CLI-016", "nom": "Solo", "telephone": "+237671499431", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-29"},
    {"id_client": "CLI-017", "nom": "Martini", "telephone": "+237698243064", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-30"},
    {"id_client": "CLI-018", "nom": "Ice Man", "telephone": "+237651666758", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 15000, "solde_restant": 0, "date_paiement": "2026-07-30"},
    {"id_client": "CLI-019", "nom": "Guisnel Pempeme (Bob)", "telephone": "+237695728556", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 5000, "solde_restant": 0, "date_paiement": "2026-07-30"},
    {"id_client": "CLI-020", "nom": "Toguem Blondel", "telephone": "+237655282745", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 20000, "solde_restant": 0, "date_paiement": "2026-07-30"},
    {"id_client": "CLI-021", "nom": "Conrald Mudi", "telephone": "+237672523244", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-30"},
    {"id_client": "CLI-022", "nom": "Patrice", "telephone": "+237656307332", "offre": "Abonnement Internet MNSL NETWORK Période: Juillet 2026", "prix": 10000, "solde_restant": 0, "date_paiement": "2026-07-30"}
]

# --- GÉNÉRATEUR DE PDF CONFORME À TON MODÈLE ---
def generer_pdf_facture(num_facture, client):
    fichier_path = os.path.join(OS_FACTURES_DIR, f"{num_facture}.pdf")
    doc = SimpleDocTemplate(fichier_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    style_titre = ParagraphStyle('TitreCompany', fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#0D47A1"))
    style_soustitre = ParagraphStyle('SousTitre', fontName='Helvetica', fontSize=10, textColor=colors.gray)
    style_section = ParagraphStyle('SectionTitle', fontName='Helvetica-Bold', fontSize=12, spaceBefore=10, spaceAfter=5)
    style_normal = styles['Normal']
    style_avis = ParagraphStyle('Avis', fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor("#D32F2F"))
    
    story.append(Paragraph("<b>MNSL NETWORK</b>", style_titre))
    story.append(Paragraph("Fournisseur d'accès Internet", style_soustitre))
    story.append(Paragraph("Responsable : Ngambo Louis", style_normal))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>FACTURE</b>", ParagraphStyle('FactureHeader', fontName='Helvetica-Bold', fontSize=16, alignment=1)))
    if client["solde_restant"] > 0:
        story.append(Spacer(1, 5))
        story.append(Paragraph("⚠️ <b>AVIS :</b> Cette facture inclut un solde restant à régulariser.", style_avis))
    story.append(Spacer(1, 15))
    
    date_emission = datetime.now().strftime('%d %B %Y')
    # Conversion lisible de la date d'échéance du client
    try:
        dt_echeance = datetime.strptime(client["date_paiement"], "%Y-%m-%d")
        date_echeance_texte = dt_echeance.strftime('%d %B %Y')
    except:
        date_echeance_texte = client["date_paiement"]

    meta_donnees = [
        ["N° FACTURE", "DATE D'ÉMISSION", "DATE D'ÉCHÉANCE"],
        [num_facture, date_emission, date_echeance_texte]
    ]
    t_meta = Table(meta_donnees, colWidths=[180, 160, 160])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADD9G', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.gray),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(f"<b>FACTURÉ À :</b> {client['nom']}", style_section))
    story.append(Paragraph(f"Client N° : {client['id_client']}", style_normal))
    story.append(Spacer(1, 15))
    
    total_du = client['prix'] + client['solde_restant']
    donnees_facture = [
        ["DESCRIPTION", "QTÉ", "PRIX UNIT.", "MONTANT"],
        [client['offre'], "1", f"{client['prix']:,} FCFA", f"{client['prix']:,} FCFA"]
    ]
    
    if client['solde_restant'] > 0:
        donnees_facture.append(["Solde restant période précédente", "1", f"{client['solde_restant']:,} FCFA", f"{client['solde_restant']:,} FCFA"])
        
    donnees_facture.append(["", "", "TOTAL DÛ :", f"{total_du:,} FCFA"])
    
    t_facture = Table(donnees_facture, colWidths=[260, 40, 100, 100])
    t_facture.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D47A1")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey),
        ('FONTNAME', (-2,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (-2,-1), (-1,-1), colors.HexColor("#FFF9C4")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_facture)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>MOYENS DE PAIEMENT</b>", style_section))
    donnees_paiement = [
        ["Mobile Money (MOMO)", "Orange Money (OM)"],
        ["652 466 029", "695 084 521"],
        ["Ngambo Louis", "Ngambo Louis"]
    ]
    t_paiement = Table(donnees_paiement, colWidths=[250, 250])
    t_paiement.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F5F5F5")),
        ('TEXTCOLOR', (0,0), (0,1), colors.HexColor("#FBC02D")),
        ('TEXTCOLOR', (1,0), (1,1), colors.HexColor("#E65100")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_paiement)
    story.append(Spacer(1, 20))
    
    statut_texte = "STATUT : EN ATTENTE DE PAIEMENT"
    if client["solde_restant"] > 0:
        statut_texte += " - SOLDE À RÉGULARISER"
        
    story.append(Paragraph(f"<b>{statut_texte}</b>", ParagraphStyle('Statut', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#D32F2F"), alignment=1)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<center><i>MNSL NETWORK — Merci de votre confiance</i></center>", style_soustitre))
    
    doc.build(story)
    return fichier_path

# --- ENVOI VERS APPLICATION WHATSAPP WINDOWS ---
def ouvrir_dans_whatsapp_windows(numero, message):
    try:
        num_propre = numero.replace("+", "").replace(" ", "")
        texte_encode = urllib.parse.quote(message)
        url_windows = f"whatsapp://send?phone={num_propre}&text={texte_encode}"
        webbrowser.open(url_windows)
        return True
    except Exception as e:
        print(f"Erreur WhatsApp : {e}")
        return False

# --- COMPOSANT GRAPHIQUE PRINCIPAL FLET ---
def main(page: ft.Page):
    page.title = "MNSL Network - CRM & Billing System"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    liste_logs = ft.ListView(expand=True, spacing=10, padding=10)

    # Statistiques du haut
    stat_clients = ft.Text(f"Clients Actifs : {len(base_clients)}", size=16, weight="bold", color="green")
    total_ca = sum([c["prix"] for c in base_clients])
    stat_ca = ft.Text(f"Total Mensuel : {total_ca:,} FCFA", size=16, weight="bold", color="blue")

    def generer_lignes_clients():
        return [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(c["id_client"])),
                ft.DataCell(ft.Text(c["nom"])),
                ft.DataCell(ft.Text(c["telephone"], color="green")),
                ft.DataCell(ft.Text(f"{c['prix']:,} F")),
                ft.DataCell(ft.Text(c["date_paiement"].split("-")[-1], color="blue")), # Affiche juste le jour J
            ]) for c in base_clients
        ]

    table_clients = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nom complet")),
            ft.DataColumn(ft.Text("Téléphone")),
            ft.DataColumn(ft.Text("Montant")),
            ft.DataColumn(ft.Text("Jour Éch.")),
        ],
        rows=generer_lignes_clients()
    )

    # Champs Formulaire pour nouveaux ajouts
    txt_nom = ft.TextField(label="Nom Complet", width=180)
    txt_tel = ft.TextField(label="Téléphone", width=140, value="+237")
    txt_prix = ft.TextField(label="Montant (F)", width=100)
    txt_jour = ft.TextField(label="Jour (ex: 15)", width=90)
    
    def ajouter_nouveau_client(e):
        if txt_nom.value and txt_tel.value and txt_prix.value and txt_jour.value:
            num_cli = f"CLI-{len(base_clients) + 1:03d}"
            jour_str = f"{int(txt_jour.value):02d}"
            base_clients.append({
                "id_client": num_cli,
                "nom": txt_nom.value,
                "telephone": txt_tel.value,
                "offre": f"Abonnement Internet MNSL NETWORK Période: Juillet 2026",
                "prix": int(txt_prix.value),
                "solde_restant": 0,
                "date_paiement": f"2026-07-{jour_str}"
            })
            table_clients.rows = generer_lignes_clients()
            
            # Mise à jour compteurs
            stat_clients.value = f"Clients Actifs : {len(base_clients)}"
            stat_ca.value = f"Total Mensuel : {sum([c['prix'] for c in base_clients]):,} FCFA"
            
            # Reset champs
            txt_nom.value = ""
            txt_prix.value = ""
            txt_jour.value = ""
            log_message(f"👤 Client {num_cli} ({txt_nom.value}) ajouté au répertoire MNSL.")
            page.update()

    # Logique d'analyse et de transmission
    def execution_tache_facturation():
        # Cibler l'échéance de demain pour les relances automatiques J-1
        date_demain_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        log_message(f"⏰ [SYSTEM] Scan J-1 en cours pour la date cible : {date_demain_str}...")
        
        compteur = 0
        for client in base_clients:
            if client["date_paiement"] == date_demain_str:
                compteur += 1
                num_facture = f"FAC-2026-{datetime.now().strftime('%m%d')}L"
                
                # 1. Fabrique la facture PDF
                pdf_genere = generer_pdf_facture(num_facture, client)
                log_message(f"📁 PDF Facture archivé : {pdf_genere}")
                
                # 2. Prépare la relance
                total_du = client['prix'] + client['solde_restant']
                msg_whatsapp = (
                    f"Bonjour *{client['nom']}*,\n\n"
                    f"Ceci est une relance automatique de *MNSL Network*.\n"
                    f"Votre facture arrive à échéance demain.\n\n"
                    f"• Service : {client['prix']:,} FCFA\n"
                    f"*TOTAL À RÉGULARISER : {total_du:,} FCFA*\n\n"
                    f" Paiements : Orange Money (695084521) ou Mobile Money (652466029) au nom de Ngambo Louis.\n"
                    f"Merci pour votre confiance !"
                )
                
                log_message(f"🚀 Transfert de la relance vers WhatsApp Bureau pour : {client['nom']}...")
                ouvrir_dans_whatsapp_windows(client["telephone"], msg_whatsapp)
                time.sleep(4)
                
        if compteur == 0:
            log_message("💤 Aucun client ne passe à échéance demain.")
        else:
            log_message(f"✅ Opération achevée. {compteur} action(s) poussée(s) vers Windows.")
        page.update()

    def log_message(texte):
        liste_logs.controls.insert(0, ft.Text(texte, size=13, font_family="Courier"))
        page.update()

    btn_scan = ft.ElevatedButton(
        content=ft.Text("VÉRIFIER ÉCHÉANCES J-1 & RELANCER SUR WHATSAPP", size=14, weight=ft.FontWeight.BOLD),
        on_click=lambda e: execution_tache_facturation(),
        width=480, height=50, style=ft.ButtonStyle(bgcolor="green", color="white")
    )

    page.add(
        ft.Text("MNSL BILLING SYSTEM & CLIENTS MANAGEMENT", size=24, weight=ft.FontWeight.BOLD, color="blue"),
        ft.Row([stat_clients, stat_ca], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
        ft.Container(height=10),
        
        ft.Text("Inscrire un nouvel abonné :", size=14, weight="bold"),
        ft.Row([txt_nom, txt_tel, txt_prix, txt_jour, ft.ElevatedButton("Inscrire", icon="add", on_click=ajouter_nouveau_client)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=10),
        
        ft.Text("Répertoire des infrastructures actives :", size=14, weight="bold"),
        table_clients,
        ft.Container(height=15),
        btn_scan,
        ft.Container(height=10),
        ft.Container(content=liste_logs, height=180, width=780, border_radius=8, bgcolor="#111111", padding=10)
    )

ft.app(target=main, assets_dir="assets")
