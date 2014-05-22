from projects.views import CCCSDetailView

import cvs.models as cm


class CVDetailView(CCCSDetailView):
    model = cm.CV

