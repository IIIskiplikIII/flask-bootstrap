from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator



# To keep things clean, keep Flask-Nav instance in here. 

nav = Nav()


# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
@nav.navigation()
def mynavbar():
    return Navbar(
        'TEST',
    View('Flask-Bootstrap', '.index'),    ##### Ganz Easy, links der Name des Buttons, rechts das Ziel also .index im Templateverz.
    View('Home', '.index'),
    Subgroup(
        'Docs',
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Separator(),
        Text('Bootstrap'),
        Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        Link('CSS', 'http://getbootstrap.com/css/'),
        Link('Components', 'http://getbootstrap.com/components/'),
        Link('Javascript', 'http://getbootstrap.com/javascript/'),
        Link('Customize', 'http://getbootstrap.com/customize/'), )
    )