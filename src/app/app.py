from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import shutil

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        files = request.files.getlist('files[]')
        paths = request.form.getlist('paths[]')

        if not files:
            return jsonify({'status': 'error', 'message': 'No files received'}), 400

        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)

        file_info = []
        for i, file in enumerate(files):
            if file.filename:
                # Utiliser le chemin fourni ou le nom du fichier
                relative_path = paths[i] if i < len(paths) else file.filename

                # Construire le chemin complet
                filepath = os.path.join(upload_dir, relative_path)

                # Créer tous les sous-dossiers nécessaires
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Sauvegarder le fichier
                file.save(filepath)

                file_info.append({
                    'name': relative_path,
                    'size': os.path.getsize(filepath)
                })

        return jsonify({
            'status': 'success',
            'message': f'{len(file_info)} uploaded file(s)',
            'files': file_info
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/files', methods=['GET'])
def get_files():
    try:
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            return jsonify({'tree': []})

        tree = build_tree(upload_dir)
        return jsonify({'tree': tree})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def build_tree(path, is_root=True):
    """Construit une arborescence des fichiers et dossiers"""
    try:
        items = []

        # Si le dossier est vide ou n'existe pas
        if not os.path.exists(path):
            return []

        entries = sorted(os.listdir(path))

        for entry in entries:
            full_path = os.path.join(path, entry)

            if os.path.isdir(full_path):
                children = build_tree(full_path, False)
                items.append({
                    'name': entry,
                    'type': 'folder',
                    'children': children
                })
            else:
                size = os.path.getsize(full_path)
                items.append({
                    'name': entry,
                    'type': 'file',
                    'size': size
                })

        return items
    except Exception as e:
        print(f"Erreur dans build_tree: {e}")
        return []


@app.route('/clear', methods=['POST'])
def clear_uploads():
    try:
        upload_dir = 'uploads'
        if os.path.exists(upload_dir):
            # Supprimer tout le contenu du dossier uploads
            import shutil
            shutil.rmtree(upload_dir)

            return jsonify({
                'status': 'success',
                'message': 'All files have been deleted'
            })
        else:
            return jsonify({
                'status': 'success',
                'message': 'No files to delete'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error while deleting: {str(e)}'
        }), 500

@app.route('/ai-treatment', methods=['POST'])
def ai_treatment():
    try:
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            return jsonify({
                'status': 'error',
                'message': 'No files to process'
            }), 400

        # Compter les fichiers et collecter des informations
        total_files = 0
        total_size = 0
        file_types = {}

        for root, dirs, files in os.walk(upload_dir):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)

                # Compter les types de fichiers
                ext = os.path.splitext(file)[1].lower()
                file_types[ext] = file_types.get(ext, 0) + 1

        # Générer une analyse plus détaillée
        analysis_parts = [f'Analysis completed: {total_files} file(s) processed']

        if file_types:
            types_str = ', '.join([f'{count} {ext or "without extension"}' for ext, count in file_types.items()])
            analysis_parts.append(f'Types: {types_str}')

        result = {
            'status': 'success',
            'message': 'Traitement IA complété',
            'summary': {
                'total_files': total_files,
                'total_size': total_size,
                'formatted_size': format_size(total_size),
                'analysis': ' | '.join(analysis_parts)
            }
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def format_size(bytes):
    """Formate la taille en bytes en unité lisible"""
    if bytes == 0:
        return '0 B'
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB']
    i = 0
    while bytes >= k and i < len(sizes) - 1:
        bytes /= k
        i += 1
    return f'{round(bytes, 2)} {sizes[i]}'


if __name__ == '__main__':
    app.run(debug=True)