from datetime import datetime, timedelta, timezone


def _utc_now_iso(days_offset=0):
    dt = datetime.now(timezone.utc) + timedelta(days=days_offset)
    return dt.isoformat()


DEFAULT_CALLS = [
    {
        'title': 'Convocatoria Innova 2026',
        'description': 'Fomento a proyectos de innovación tecnológica con impacto social. Financiamiento hasta $50.000.000 COP.',
        'start_date': _utc_now_iso(0),
        'end_date': _utc_now_iso(90),
        'is_active': True,
        'requirements': [
            {
                'title': 'Carta de presentación del equipo',
                'description': 'Documento que describa la experiencia previa del equipo.',
                'is_required': True,
            },
            {
                'title': 'Presupuesto detallado',
                'description': 'Presupuesto con rubros y justificación económica del proyecto.',
                'is_required': True,
            },
            {
                'title': 'Documento de propuesta',
                'description': 'Documento principal con la propuesta técnica del proyecto.',
                'is_required': True,
            },
            {
                'title': 'Hoja de vida de integrantes',
                'description': 'CV corto de cada miembro del equipo postulante.',
                'is_required': False,
            },
            {
                'title': 'Anexos y referencias',
                'description': 'Material complementario opcional (links, artículos, etc.).',
                'is_required': False,
            },
        ],
    },
    {
        'title': 'Convocatoria Emprende Verde',
        'description': 'Proyectos de emprendimiento enfocados en sostenibilidad y medio ambiente.',
        'start_date': _utc_now_iso(10),
        'end_date': _utc_now_iso(120),
        'is_active': True,
        'requirements': [
            {
                'title': 'Resumen ejecutivo ambiental',
                'description': 'Resumen que destaque el componente ambiental del proyecto.',
                'is_required': True,
            },
            {
                'title': 'Modelo de negocio',
                'description': 'Canvas o documento que describa el modelo de negocio sostenible.',
                'is_required': True,
            },
            {
                'title': 'Plan de impacto ambiental',
                'description': 'Descripción de cómo el proyecto beneficia el medio ambiente.',
                'is_required': True,
            },
            {
                'title': 'Estudio de mercado',
                'description': 'Análisis del público objetivo y competencia.',
                'is_required': True,
            },
            {
                'title': 'Referencias y certificaciones',
                'description': 'Certificaciones o avales relacionados con sostenibilidad.',
                'is_required': False,
            },
        ],
    },
    {
        'title': 'Convocatoria Artesanía Digital',
        'description': 'Proyectos que combinen artesanía tradicional con herramientas digitales.',
        'start_date': _utc_now_iso(-30),
        'end_date': _utc_now_iso(60),
        'is_active': True,
        'requirements': [
            {
                'title': 'Portafolio de trabajo',
                'description': 'Muestra de trabajos anteriores relacionados con artesanía.',
                'is_required': True,
            },
            {
                'title': 'Propuesta creativa',
                'description': 'Documento describiendo la propuesta de fusión tecnológica.',
                'is_required': True,
            },
            {
                'title': 'Plan de producción',
                'description': 'Cronograma de actividades y recursos necesarios.',
                'is_required': True,
            },
            {
                'title': 'Plan de comercialización',
                'description': 'Canales de venta y estrategia de mercadeo.',
                'is_required': False,
            },
            {
                'title': 'Presupuesto',
                'description': 'Presupuesto estimado del proyecto.',
                'is_required': True,
            },
        ],
    },
    {
        'title': 'Convocatoria Investigación Aplicada',
        'description': 'Proyectos de investigación con resultados aplicables a la industria.',
        'start_date': _utc_now_iso(20),
        'end_date': _utc_now_iso(180),
        'is_active': True,
        'requirements': [
            {
                'title': 'Marco teórico',
                'description': 'Referentes teóricos y estado del arte.',
                'is_required': True,
            },
            {
                'title': 'Metodología',
                'description': 'Descripción detallada de la metodología de investigación.',
                'is_required': True,
            },
            {
                'title': 'Cronograma de actividades',
                'description': 'Diagrama de Gantt con las actividades y entregables.',
                'is_required': True,
            },
            {
                'title': 'Presupuesto de investigación',
                'description': 'Desglose de gastos de investigación.',
                'is_required': True,
            },
            {
                'title': 'Hoja de vida del investigador principal',
                'description': 'CV del investigador principal del proyecto.',
                'is_required': True,
            },
        ],
    },
    {
        'title': 'Convocatoria Cerrada: Cultura 2025',
        'description': 'Convocatoria de proyectos culturales del periodo 2025 (referencia histórica).',
        'start_date': _utc_now_iso(-180),
        'end_date': _utc_now_iso(-90),
        'is_active': False,
        'requirements': [
            {
                'title': 'Propuesta cultural',
                'description': 'Documento principal con la propuesta artística.',
                'is_required': True,
            },
            {
                'title': 'Curriculum artístico',
                'description': 'Trayectoria y experiencia del equipo artístico.',
                'is_required': True,
            },
            {
                'title': 'Rider técnico',
                'description': 'Necesidades técnicas y de producción.',
                'is_required': True,
            },
            {
                'title': 'Plan de difusión',
                'description': 'Estrategia de difusión y alcance al público.',
                'is_required': False,
            },
            {
                'title': 'Presupuesto general',
                'description': 'Presupuesto del proyecto cultural.',
                'is_required': True,
            },
        ],
    },
]
