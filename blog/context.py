# CUSTOM CONTEXT PROCESSORS
def site_data(request):
    data = {
        'sitename': 'Blogio',
        'framework': 'Django Web Framework',
        'host': 'Heroku',
        'language': 'Python',
        'developer': 'Timileyin Pelumi',
        'domain': 'https://djangoblog.com',
        'tagline': 'Web development using django is fun!'


    }
    return data
