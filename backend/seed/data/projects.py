import os

SEED_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(SEED_DIR)
PROJECTS_UPLOAD_DIR = os.path.join(BACKEND_DIR, 'src', 'static', 'uploads', 'projects', '1')

DEFAULT_PROJECTS = [
    {
        'title': 'Plataforma de Monitoreo de Calidad del Aire',
        'description': 'Sistema IoT de bajo costo para medir PM2.5 y PM10 en barrios populares, con dashboard público en tiempo real.',
        'status': 'submitted',
        'call_index': 0,
        'user_index': 0,
        'documents': [
            {
                'original_filename': 'carta_presentacion_equipo.docx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'presupuesto_detallado.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'propuesta_tecnica.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'hv_integrantes.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'anexos_referencias.zip',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
        ],
    },
    {
        'title': 'EcoPack: Empaques Compostables de Hongos',
        'description': 'Desarrollo de empaques biodegradables fabricados con micelio de hongos agrícolas locales para reemplazar plástico de un solo uso.',
        'status': 'in_review',
        'call_index': 1,
        'user_index': 1,
        'documents': [
            {
                'original_filename': 'resumen_ejecutivo_ambiental.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'modelo_negocio_canvas.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'plan_impacto_ambiental.docx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'estudio_mercado.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'certificaciones_ambientales.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
        ],
    },
    {
        'title': 'Tejido 3D de Fibras Naturales',
        'description': 'Combinación de tejido tradicional en telar manual con modelado 3D para crear prendas y accesorios de moda sostenible.',
        'status': 'draft',
        'call_index': 2,
        'user_index': 2,
        'documents': [
            {
                'original_filename': 'portafolio_artesania.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'propuesta_creativa.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'plan_produccion.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'plan_comercializacion.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'presupuesto_artesania.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
        ],
    },
    {
        'title': 'Detección Temprana de Plagas Agrícolas con IA',
        'description': 'Aplicación móvil que usa visión por computador para detectar plagas y enfermedades en cultivos, con recomendaciones locales.',
        'status': 'approved',
        'call_index': 3,
        'user_index': 3,
        'documents': [
            {
                'original_filename': 'marco_teorico.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'metodologia_investigacion.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'cronograma_gantt.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'presupuesto_investigacion.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'cv_investigador_principal.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
        ],
    },
    {
        'title': 'Festival Itinerante de Teatro Callejero',
        'description': 'Festival de teatro callejero itinerante que recorre municipios rurales con obras participativas y talleres comunitarios.',
        'status': 'rejected',
        'call_index': 4,
        'user_index': 4,
        'documents': [
            {
                'original_filename': 'propuesta_cultural.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'curriculum_artistico.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'rider_tecnico.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'plan_difusion.pdf',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
            {
                'original_filename': 'presupuesto_cultural.xlsx',
                'source_file': os.path.join(PROJECTS_UPLOAD_DIR, 'c8459257c83241d181f55bb33801c669_DxDiag.txt'),
                'mime_type': 'text/plain',
            },
        ],
    },
]
