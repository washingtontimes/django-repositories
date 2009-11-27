from projectmgr.models import SourceRepository, Metadata
from projectmgr.settings import VERSION_KEY
from django.template import loader, Context
from django.contrib.sites.models import Site

try:
    from markdown2rest import markdown2rest
    mkdn2rest = markdown2rest
except ImportError:
    mkdn2rest = lambda a: a

def create_setup_script(sourcerepo):
    """
    Create a setup.py file and print it to standard out based on repository settings
    
    You can pass in a string/unicode for the name of the project, and int for
    the id of the project, or an instance of the model.
    """
    if isinstance(sourcerepo, (str,unicode)):
        repo = SourceRepository.objects.get(name=sourcerepo)
    elif isinstance(sourcerepo, int):
        repo = SourceRepository.objects.get(pk=sourcerepo)
    elif isinstance(sourcerepo, SourceRepository):
        repo = sourcerepo
    tpl = loader.get_template('setup_py.txt')
    
    site = Site.objects.get_current()
    authors = repo.owners()
    try:
        version = repo.metadata_set.get(key=VERSION_KEY).value
    except:
        version = '0.0.1'
    description = repo.summary or ''
    long_description = repo.description or ''
    context = Context({
        'name': repo.name,
        'version': version,
        'description': mkdn2rest(description),
        'long_description': mkdn2rest(long_description),
        'author': ", ".join([author.get_full_name() for author in authors]),
        'author_email': ", ".join([author.email for author in authors]),
        'url': "%s%s" % (site.domain,repo.get_absolute_url()),
        'classifications': [md.key for md in repo.metadata_set.all() if md.key != VERSION_KEY],
    })
    return tpl.render(context)

    