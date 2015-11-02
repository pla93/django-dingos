import importlib
from menu import Menu, MenuItem
from django.core.urlresolvers import reverse, resolve

from dingos.core import http_helpers
from view_classes import ViewMethodMixin


def get_saved_searches_submenu(request):
    class ssDummy(ViewMethodMixin):
        pass

    submenu = ()
    ssd = ssDummy()
    ssd.request = request
    saved_searches = ssd.get_user_data().get('saved_searches', {})

    for source_name, source_saved_search in saved_searches.iteritems():
        for ss in source_saved_search:
            submenu += (MenuItem(ss.get('title', '<NONE>'),
                                 http_helpers.saved_search_url(ss),
                                 weight = ss.get('weight', 10) ),)
    return submenu

def get_context_menu(request):
    c_view, args, kwargs = resolve(request.path)
    m_view = importlib.import_module(c_view.__module__)
    view_class = getattr(m_view, c_view.__name__)

    try:
        context_submenu = view_class.context_menu_items
    except AttributeError:
        context_submenu = []

    return context_submenu


Menu.add_item( "mantis_main",
               MenuItem("List, Filter & Search", "",
                        weight = 50,
                        children = (
                            MenuItem("Info Object List (generic filter)", "%s?&o=-create_timestamp" % reverse("url.dingos.list.infoobject.generic"), ),
                            MenuItem("Info Object List (filter by ID)", "%s?&o=-create_timestamp" % reverse("url.dingos.list.infoobject.by_id"), ),
                            MenuItem("Fact Search (simple)", reverse("url.dingos.search.fact.simple"),  ),
                            MenuItem("Fact Search (unique)", reverse("url.dingos.search.fact.simple.unique"),  ),
                            MenuItem("Info Object Query", reverse("url.dingos.admin.custominfoobjectsearch"),
                                     ),
                            MenuItem("Fact Query", reverse("url.dingos.admin.customfactsearch"),
                                     ),
                        ),
                        check = lambda request: request.user.is_authenticated()
                    )
)



Menu.add_item( "mantis_main",
               MenuItem("Saved Filters/Searches", "",
                        weight = 50,
                        children = get_saved_searches_submenu,
                        check = lambda request: request.user.is_authenticated()
                    )
)

level2 = (
    MenuItem("LEV2","test"),
    MenuItem("LEV2","test"),
    MenuItem("LEV2","test"),
)

level1 = (
    MenuItem("LEV1","",children=level2),
    MenuItem("LEV1","",children=level2),
    MenuItem("LEV1","",children=level2),
)

Menu.add_item("mantis_main",
              MenuItem("LEV0","",children=level1)
              )