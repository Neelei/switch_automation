from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os
import uuid


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'firmware'  # Définir le dossier de téléchargement


@app.route('/')
def index():
    return render_template('config_form3.html')

# Autoriser URL dynamique pour donwload n'importe quel fichier
@app.route('/firmware/<path:filename>')
def firmware(filename):
    # Remplacer '%20' ou '+' par des espaces
    corrected_filename = filename.replace('%20', ' ').replace('+', ' ')
    return send_from_directory(app.config['UPLOAD_FOLDER'], corrected_filename)

@app.route('/submit', methods=['POST'])
def submit():
    # Traitement du fichier de firmware
    # Récupération du fichier depuis la requête
    file = request.files.get('file')
    if file and file.filename != '':
        # Générer un nom de fichier unique
        unique_filename = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = unique_filename + file_extension

        # Construire le chemin complet pour enregistrer le fichier
        print("Fichier reçu:", file.filename)  # Ligne de débogage
        filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # Créer le dossier s'il n'existe pas
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Enregistrer le fichier
        file.save(filename)
        nom_fichier = new_filename
    else:
        print("fichier pas reçu")
        nom_fichier = None

    config_data = {
        'ip-client' : request.form['ip-client'],
        'ip': request.form['ip'],
        'nomfichier': nom_fichier,
        'switch_name': request.form['switch_name'],
        'username': request.form['username'],
        'password': request.form['password'],
        'domain': request.form['domain'],
        'dns1': request.form['dns1'],
        'dns2': request.form['dns2'],
        'ntp': request.form['ntp'],
        'snmp': request.form['snmp'],
        'ports': [],
        'vlans': [],
        'aggregates':[],
        # Ajoutez ici les autres données du formulaire
    }
    vlan_ids = request.form.getlist('vlan_id')
    vlan_names = request.form.getlist('vlan_name')

    for id, name in zip(vlan_ids, vlan_names):
        config_data['vlans'].append({'vlan_id': id, 'name': name})

    port_ids = request.form.getlist('port_id')
    port_names = request.form.getlist('port_name')
    port_untagged = request.form.getlist('port_untagged')
    port_vlans = request.form.getlist('port_vlans')

    port_id = 1
    for id, name, untagged, vlans in zip(port_ids, port_names, port_untagged, port_vlans):
        vlans_list = []
        #try...except pour gérer les cas où la valeur VLAN untagged n'est pas un entier valide
        try:
            untagged_value = int(untagged)
        except ValueError:
            untagged_value = None

        if vlans:
            # Gérez les VLANs séparés par des virgules ou un range
            parts = vlans.split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    vlans_list.extend(range(start, end + 1))
                else:
                    vlans_list.append(int(part))

        config_data['ports'].append({
            'port_id': id,
            'port_name': name,
            'vlan_untagged': untagged_value,
            'vlans': vlans_list
        })



    # Récupérez les données des agrégats depuis le formulaire
    aggregate_names = request.form.getlist('aggregat_name')
    aggregate_ports = request.form.getlist('aggregat_ports')
    aggregate_untagged = request.form.getlist('aggregat_untagged')
    aggregate_tagged_vlans = request.form.getlist('aggregat_vlans')

    aggregates = []

    # Boucle pour traiter chaque agrégat
    for name, ports, untagged, tagged_vlans in zip(aggregate_names, aggregate_ports, aggregate_untagged, aggregate_tagged_vlans):
        ports_list = []
        for p in ports.split(','):
            ports_list.append(p)
        # Initialisez untagged_value avant le bloc try...except
        untagged_value = None
        try:
            untagged_value = int(untagged)
        except ValueError:
            # Vous pouvez gérer l'exception ici si nécessaire
            pass
        tagged_vlans_list = []
        if tagged_vlans:
            parts = tagged_vlans.split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    tagged_vlans_list.extend(range(start, end + 1))
                else:
                    tagged_vlans_list.append(int(part))

        aggregates.append({
            'aggregat_name': name,
            'aggregat_ports': ports_list,
            'vlan_untagged': untagged_value,
            'vlans_tagged': tagged_vlans_list
        })

    # Ajoutez la liste d'agrégats à votre configuration
    config_data['aggregates'] = aggregates
    # Utilisez le nom du switch pour créer un nom de fichier unique
    switch_name = request.form['switch_name']
    filename = f"data/{switch_name}.json"
    with open(filename, 'w') as file:
        json.dump(config_data, file, separators=(',', ':'), indent=4)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=f'0.0.0.0', port=50000,debug=True)
