from django.shortcuts import render


def index(request):
    context = {
        'owner': 'Sergio Adrián Cargua Oñate',
        'title': 'Sergio Cargua | Full Stack Developer',
        'projects': [
            {
                'name': 'E-Commerce Platform',
                'description': 'Plataforma de comercio electrónico escalable con Django REST Framework, Vue.js y Stripe.',
                'tags': ['Django', 'Vue.js', 'PostgreSQL', 'Stripe'],
                'icon': '🛒',
                'color': '#0080ff',
            },
            {
                'name': 'Data Analytics Dashboard',
                'description': 'Panel de visualización de datos en tiempo real con gráficos interactivos y exportación a PDF.',
                'tags': ['Python', 'Pandas', 'Chart.js', 'Redis'],
                'icon': '📊',
                'color': '#ffd700',
            },
            {
                'name': 'API REST Microservices',
                'description': 'Arquitectura de microservicios con Docker, JWT auth y documentación Swagger automática.',
                'tags': ['FastAPI', 'Docker', 'JWT', 'Swagger'],
                'icon': '⚡',
                'color': '#00d4aa',
            },
            {
                'name': 'Portfolio Personal',
                'description': 'Portfolio profesional con Django, tema oscuro moderno y animaciones CSS avanzadas.',
                'tags': ['Django', 'CSS3', 'JavaScript', 'Heroku'],
                'icon': '🚀',
                'color': '#b347ff',
            },
            {
                'name': 'Sistema de Inventarios',
                'description': 'Sistema de control de inventarios con reportes automáticos y alertas de stock crítico.',
                'tags': ['Django', 'Celery', 'PostgreSQL', 'Bootstrap'],
                'icon': '📦',
                'color': '#ff6b35',
            },
            {
                'name': 'Chat en Tiempo Real',
                'description': 'Aplicación de mensajería instantánea con WebSockets, salas privadas y notificaciones.',
                'tags': ['Django Channels', 'WebSockets', 'Redis', 'React'],
                'icon': '💬',
                'color': '#0080ff',
            },
        ],
        'skills': [
            {'name': 'Python', 'level': 90, 'icon': '🐍'},
            {'name': 'Django', 'level': 88, 'icon': '🎸'},
            {'name': 'JavaScript', 'level': 80, 'icon': '⚡'},
            {'name': 'React / Vue.js', 'level': 72, 'icon': '⚛️'},
            {'name': 'PostgreSQL', 'level': 82, 'icon': '🐘'},
            {'name': 'Docker', 'level': 75, 'icon': '🐳'},
            {'name': 'Git & GitHub', 'level': 85, 'icon': '🔧'},
            {'name': 'REST APIs', 'level': 87, 'icon': '🌐'},
        ],
        'timeline': [
            {
                'year': '2024',
                'title': 'Full Stack Developer Senior',
                'company': 'Tech Solutions Corp.',
                'description': 'Lideré el desarrollo de plataformas web escalables con Django y microservicios.',
                'type': 'work',
            },
            {
                'year': '2023',
                'title': 'Backend Developer',
                'company': 'Digital Innovations S.A.',
                'description': 'Construí APIs REST robustas con autenticación JWT y documentación automática.',
                'type': 'work',
            },
            {
                'year': '2022',
                'title': 'Ingeniería en Sistemas',
                'company': 'Universidad Técnica',
                'description': 'Titulado con honores. Proyecto de grado: Sistema de IA para análisis predictivo.',
                'type': 'edu',
            },
            {
                'year': '2021',
                'title': 'Desarrollador Junior',
                'company': 'StartupTech Ecuador',
                'description': 'Primer rol profesional, desarrollo frontend con React y backend con Python.',
                'type': 'work',
            },
            {
                'year': '2020',
                'title': 'Certificación AWS',
                'company': 'Amazon Web Services',
                'description': 'AWS Certified Solutions Architect – Associate. Cloud computing y arquitecturas en la nube.',
                'type': 'edu',
            },
        ],
    }
    return render(request, 'portfolio/index.html', context)
