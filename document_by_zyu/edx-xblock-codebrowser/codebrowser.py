import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

import os

class CodeBrowserBlock(XBlock):
    """
    An XBlock providing CodeBrowser capabilities for video
    """

    src = String(help="the directory of your code", default=None, scope=Scope.content)
    width = Integer(help="width of the frame", default=800, scope=Scope.content)
    height = Integer(help="height of the frame", default=900, scope=Scope.content)

    def student_view(self, context=None):
        """
        The primary view of the CodeBrowserBlock, shown to students
        when viewing courses.
        """
        student_id = self.runtime.anonymous_student_id

	real_user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
	email = real_user.email
	"""
	if it is the first time for user to browser code ,the gitlab will initialize all the info
	"""
	os.system("/edx/var/edxapp/staticfiles/xblock-script/initialize_user.sh " + student_id + " " + email)

	"""
	pull the code from gitlab and generate the static html files
	"""
	
	os.system("/edx/var/edxapp/staticfiles/xblock-script/generator.sh "  + student_id + " " + email)
        
	 # Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__, "static/html/codebrowser_view.html")
	
        frag = Fragment(unicode(html_str).format(
		width=self.width, 
		height=self.height,
		student_id=student_id,
		email=email,
	))
        # Load CSS
        css_str = pkg_resources.resource_string(__name__, "static/css/codebrowser.css")
        frag.add_css(unicode(css_str))
	

        js_str = pkg_resources.resource_string(__name__, "static/js/src/codebrowser_view.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('CodeBrowserViewBlock')

        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/codebrowser_edit.html")
        src = self.src or ''
        frag = Fragment(unicode(html_str).format(width=self.width, height=self.height))

        js_str = pkg_resources.resource_string(__name__, "static/js/src/codebrowser_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('CodeBrowserEditBlock')

        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.width = data.get('width')
        self.height = data.get('height')
        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Code Browser",
            """
            <vertical_demo>
            </vertical_demo>
            """)
        ]
