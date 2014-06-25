# Copyright (c) Siemens AG, 2013
#
# This file is part of MANTIS.  MANTIS is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2
# of the License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import json

from django import http
from django.http import HttpResponse
from django.db.models import F
from django.forms.formsets import formset_factory

from django.contrib import messages
from django.db import DataError
from django.core.exceptions import FieldError

from braces.views import SuperuserRequiredMixin

from dingos.models import InfoObject2Fact, InfoObject, UserData, get_or_create_fact
from dingos.view_classes import BasicJSONView

import csv

from dingos.filter import InfoObjectFilter, CompleteInfoObjectFilter,FactTermValueFilter, IdSearchFilter , OrderedFactTermValueFilter
from dingos.forms import EditSavedSearchesForm, EditInfoObjectFieldForm,  CustomQueryForm

from dingos import DINGOS_TEMPLATE_FAMILY, DINGOS_INTERNAL_IOBJECT_FAMILY_NAME, DINGOS_USER_PREFS_TYPE_NAME, DINGOS_SAVED_SEARCHES_TYPE_NAME, DINGOS_DEFAULT_SAVED_SEARCHES


from braces.views import LoginRequiredMixin
from view_classes import BasicFilterView, BasicDetailView, BasicTemplateView, BasicListView, BasicCustomQueryView
from queryparser.queryparser import QueryParser
from queryparser.querylexer import QueryLexerException
from queryparser.querytree import FilterCollection, QueryParserException


from dingos.graph_traversal import follow_references


class InfoObjectList(BasicFilterView):

    counting_paginator = False

    exclude_internal_objects = True

    template_name = 'dingos/%s/lists/InfoObjectList.html' % DINGOS_TEMPLATE_FAMILY

    breadcrumbs = (('Dingo',None),
                   ('List',None),
                   ('InfoObject',None))


    filterset_class= InfoObjectFilter

    title = 'List of Info Objects (generic filter)'


    @property
    def queryset(self):
        queryset = InfoObject.objects.\
            exclude(latest_of=None)

        if self.exclude_internal_objects:
            queryset = queryset.exclude(iobject_family__name__exact=DINGOS_INTERNAL_IOBJECT_FAMILY_NAME)

        queryset = queryset.prefetch_related(
            'iobject_type',
            'iobject_type__iobject_family',
            'iobject_family',
            'identifier__namespace',
            'iobject_family_revision',
            'identifier').order_by('-latest_of__pk')
        return queryset

class InfoObjectListIncludingInternals(SuperuserRequiredMixin,InfoObjectList):

    counting_paginator = False

    filterset_class= CompleteInfoObjectFilter

    exclude_internal_objects=False

class InfoObjectList_Id_filtered(BasicFilterView):

    template_name = 'dingos/%s/lists/InfoObjectList.html' % DINGOS_TEMPLATE_FAMILY

    breadcrumbs = (('Dingo',None),
                   ('List',None),
                   ('InfoObject',None))

    filterset_class= IdSearchFilter

    title = 'ID-based filtering'

    queryset = InfoObject.objects.exclude(latest_of=None). \
        exclude(iobject_family__name__exact=DINGOS_INTERNAL_IOBJECT_FAMILY_NAME). \
        prefetch_related(
        'iobject_type',
        'iobject_family',
        'iobject_family_revision',
        'identifier').select_related().distinct().order_by('-latest_of__pk')

class InfoObjectsEmbedded(BasicListView):
    template_name = 'dingos/%s/lists/InfoObjectEmbedded.html' % DINGOS_TEMPLATE_FAMILY

    breadcrumbs = (('Dingo',None),
                   ('List',None),
                   ('InfoObject',None))

    filterset_class = InfoObjectFilter

    @property
    def title(self):
        return 'Objects that embed object "%s" (id %s)' % (self.iobject.name,
                                                           self.iobject.identifier)
    @property
    def iobject(self):
        return InfoObject.objects.get(pk=int(self.kwargs['pk']))

    def get_queryset(self):

        queryset = InfoObject2Fact.objects.exclude(iobject__latest_of=None). \
            filter(fact__value_iobject_id__id=self.iobject.identifier.id). \
            filter(iobject__timestamp=F('iobject__identifier__latest__timestamp')). \
            order_by('-iobject__timestamp')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(InfoObjectsEmbedded, self).get_context_data(**kwargs)
        context['iobject'] = self.iobject
        return context


class SimpleFactSearch(BasicFilterView):

    counting_paginator = False

    template_name = 'dingos/%s/searches/SimpleFactSearch.html' % DINGOS_TEMPLATE_FAMILY

    title = 'Fact-based filtering'


    filterset_class = OrderedFactTermValueFilter
    @property
    def queryset(self):
        if self.get_query_string() == '?':
          queryset = InfoObject2Fact.objects.filter(id=-1)
        else:
           queryset =  InfoObject2Fact.objects.all().\
              exclude(iobject__latest_of=None). \
              exclude(iobject__iobject_family__name__exact=DINGOS_INTERNAL_IOBJECT_FAMILY_NAME)

           queryset = queryset.\
              prefetch_related('iobject',
                        'iobject__iobject_type',
                        'fact__fact_term',
                        'fact__fact_values').select_related()#.distinct().order_by('iobject__id')
        return queryset

class UniqueSimpleFactSearch(BasicFilterView):

    counting_paginator = False

    template_name = 'dingos/%s/searches/UniqueSimpleFactSearch.html' % DINGOS_TEMPLATE_FAMILY

    title = 'Fact-based filtering (unique)'


    filterset_class = FactTermValueFilter

    
    @property
    def queryset(self):
        if self.get_query_string() == '?':
          queryset = InfoObject2Fact.objects.filter(id=-1)
        else:

          queryset =  InfoObject2Fact.objects.all().\
            exclude(iobject__latest_of=None). \
            exclude(iobject__iobject_family__name__exact=DINGOS_INTERNAL_IOBJECT_FAMILY_NAME). \
            order_by('iobject__iobject_type','fact__fact_term','fact__fact_values').distinct('iobject__iobject_type','fact__fact_term','fact__fact_values')

          queryset = queryset.\
            prefetch_related('iobject',
              'iobject__iobject_type',
              'fact__fact_term',
              'fact__fact_values').select_related()

        return queryset


    def get_reduced_query_string(self):
        return self.get_query_string(remove=['fact__fact_term','fact__fact_values','page'])



class InfoObjectView_wo_login(BasicDetailView):
    """
    View for viewing an InfoObject.

    Note that below we generate a query set for the facts by hand
    rather than carrying out the queries through the object-query.
    This is because the prefetch_related
    is treated leads to a prefetching of *all* facts, even though
    pagination only displays 100 or 200 or so.
    """



    # Config for Prefetch/SelectRelated Mixins_
    select_related = ()
    prefetch_related = ('iobject_type',
                        'iobject_type__namespace',
                        'identifier__namespace',
    )

    breadcrumbs = (('Dingo',None),
                   ('View',None),
                   ('InfoObject','url.dingos.list.infoobject.generic'),
                   ('[RELOAD]',None)
    )
    model = InfoObject

    template_name = 'dingos/%s/details/InfoObjectDetails.html' % DINGOS_TEMPLATE_FAMILY

    title = 'Info Object Details'

    show_datatype = False


    @property
    def iobject2facts(self):
        return self.object.fact_thru.all().prefetch_related(
                                                             'fact__fact_term',
                                                             'fact__fact_values',
                                                             'fact__fact_values__fact_data_type',
                                                             'fact__value_iobject_id',
                                                             'fact__value_iobject_id__latest',
                                                             'fact__value_iobject_id__latest__iobject_type',
                                                             'node_id')



    def graph_iobject2facts(self):
        obj_pk = self.object.id
        graph = InfoObject.annotated_graph([obj_pk])
        edges_from_top = graph.edges(nbunch=[obj_pk], data = True)
        # show edges to/from top-level object
        print edges_from_top
        # extract nodes that are 'Indicators'
        indicators =  [e[1] for e in edges_from_top if "Indicator" in e[2]['term'][0]]
        return graph.node[indicators[0]]['facts']




    template_name = 'dingos/%s/details/InfoObjectDetails.html' % DINGOS_TEMPLATE_FAMILY

    title = 'Info Object Details'

    def get_context_data(self, **kwargs):

        context = super(InfoObjectView_wo_login, self).get_context_data(**kwargs)

        context['show_datatype'] = self.request.GET.get('show_datatype',False)
        context['show_NodeID'] = self.request.GET.get('show_nodeid',False)
        context['iobject2facts'] = self.iobject2facts
        try:
            context['highlight'] = self.request.GET['highlight']
        except KeyError:
            context['highlight'] = None

        return context


class InfoObjectView(LoginRequiredMixin,InfoObjectView_wo_login):
    """
    View for viewing an InfoObject.
    """

    pass


class BasicInfoObjectEditView(LoginRequiredMixin,InfoObjectView_wo_login):
    """
    Attention: this view overwrites an InfoObject without creating
    a new revision. It is currently only used for editing the
    UserConfigs or for edits carried out by the superuser.
    """
    template_name = 'dingos/%s/edits/InfoObjectsEdit.html' % DINGOS_TEMPLATE_FAMILY
    title = 'Edit Info Object Details'

    attr_editable = False # set to True to also allow editing of attributes

    # we use a formset to deal with a varying number of forms

    form_class = formset_factory(EditInfoObjectFieldForm, extra=0)



    index = {}
    form_builder = []

    def build_form(self):

        self.form_builder = []
        self.index = {}
        cnt = 0

        for io2f in self.iobject2facts:

            if len(io2f.fact.fact_values.all()) == 1 and io2f.fact.value_iobject_id == None \
                and ( (self.attr_editable and io2f.fact.fact_term.attribute != "") or \
                          not io2f.fact.fact_term.attribute ):
                value_obj = io2f.fact.fact_values.all()[0]
                self.form_builder.append( { 'value' : value_obj.value } )
                self.index.update( { io2f.node_id.name :  (cnt,value_obj) } )
                cnt += 1



    def get_context_data(self, **kwargs):
        context = super(InfoObjectView_wo_login, self).get_context_data(**kwargs)
        context.update(super(LoginRequiredMixin, self).get_context_data(**kwargs))

        self.build_form()

        context['formset'] = self.form_class(initial=self.form_builder)
        context['formindex'] = self.index


        return context

    def get(self, request, *args, **kwargs):

        return super(InfoObjectView_wo_login,self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super(InfoObjectView_wo_login,self).get(request, *args, **kwargs)
        self.build_form()

        user_data = self.get_user_data()
        self.formset = self.form_class(request.POST.dict())

        if self.formset.is_valid() and request.user.is_authenticated():

            for io2f in self.iobject2facts:
                if io2f.node_id.name in self.index:
                    current_value = self.index[io2f.node_id.name][1]
                    post_value = self.formset.forms[self.index[io2f.node_id.name][0]].cleaned_data['value']

                    if current_value.value != post_value:

                        new_fact,created = get_or_create_fact(io2f.fact.fact_term,
                                                      fact_dt_name=current_value.fact_data_type.name,
                                                      fact_dt_namespace_uri=current_value.fact_data_type.namespace.uri,
                                                      values=[post_value],
                                                      value_iobject_id=None,
                                                      value_iobject_ts=None,
                                                      )
                        io2f.fact = new_fact
                        io2f.save()

        return super(InfoObjectView_wo_login,self).get(request, *args, **kwargs)

class InfoObjectEditView(SuperuserRequiredMixin,BasicInfoObjectEditView):
    """
    Attention: this view overwrites an InfoObject without creating
    a new revision. It is currently only used for editing the
    UserConfigs or for edits carried out by the superuser.
    """
    pass

class UserPrefsView(BasicInfoObjectEditView):
    """
    View for editing the user configuration of a user.
    """

    def get_object(self):
        # We delete the session data in  order to achieve a reload
        # when viewing this page.




        try:
            del(self.request.session['customization'])
            del(self.request.session['customization_for_authenticated'])
        except KeyError, err:
            pass
        return UserData.get_user_data_iobject(user=self.request.user,data_kind=DINGOS_USER_PREFS_TYPE_NAME)


class CustomSearchesEditView(BasicTemplateView):
    """
    View for editing the saved searches of a user.
    """

    template_name = 'dingos/%s/edits/SavedSearchesEdit.html' % DINGOS_TEMPLATE_FAMILY
    title = 'Saved searches'

    form_class = formset_factory(EditSavedSearchesForm, can_order=True, can_delete=True,extra=0)
    formset = None

    def get_context_data(self, **kwargs):
        context = super(CustomSearchesEditView, self).get_context_data(**kwargs)

        context['formset'] = self.formset

        return context

    def get(self, request, *args, **kwargs):
        user_data = self.get_user_data(load_new_settings=True)
        saved_searches = user_data['saved_searches'].get('dingos',[])

        initial = []

        counter = 0

        for saved_search in saved_searches:
            initial.append({'new_entry': False,
                            'position' : counter,
                            'title': saved_search['title'],
                            'view' : saved_search['view'],
                            'parameter' : saved_search['parameter'],
                            'custom_query': saved_search.get('custom_query','')})
            counter +=1
        if self.request.session.get('new_search'):
            initial.append({'position' : counter,
                            'new_entry' : True,
                            'title': "",
                            'view' : self.request.session['new_search']['view'],
                            'parameter' : self.request.session['new_search']['parameter'],
                            'custom_query' : self.request.session['new_search'].get('custom_query','')
            })
            del(self.request.session['new_search'])
            self.request.session.modified = True

        self.formset = self.form_class(initial=initial)
        return super(BasicTemplateView,self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        user_data = self.get_user_data()
        self.formset = self.form_class(request.POST.dict())
        saved_searches = user_data['saved_searches']

        if self.formset.is_valid() and request.user.is_authenticated():
            dingos_saved_searches = []

            for form in self.formset.ordered_forms:
                search = form.cleaned_data
                # Search has the following form::
                #
                #     {'view': u'url.dingos.list.infoobject.generic',
                #      'parameter': u'iobject_type=72',
                #      u'ORDER': None,
                #      u'DELETE': False,
                #     'title': u'Filter for STIX Packages'
                #     }
                #

                if (search['title'] != '' or not search['new_entry']) and not search['DELETE']:
                    dingos_saved_searches.append( { 'view' : search['view'],
                                                    'parameter' : search['parameter'],
                                                    'custom_query' : search.get('custom_query',''),
                                                    'title' : search['title'],
                                                    }
                    )

            saved_searches['dingos'] = dingos_saved_searches
            UserData.store_user_data(user=request.user,
                                     data_kind=DINGOS_SAVED_SEARCHES_TYPE_NAME,
                                     user_data=saved_searches,
                                     iobject_name = "Saved searches of user '%s'" % request.user.username)

            # enforce reload of session
            del request.session['customization']
            request.session.modified = True

        else:
            # Form was not valid, we return the form as is

            return super(BasicTemplateView,self).get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

class InfoObjectJSONView(BasicDetailView):
    """
    View for JSON representation of InfoObjects.
    """

    select_related = ()
    prefetch_related = () # The to_dict function itself defines the necessary prefetch_stuff

    model = InfoObject

    def render_to_response(self, context):
        #return self.get_json_response(json.dumps(context['object'].show_elements(""),indent=2))
        include_node_id = self.request.GET.get('include_node_id',False)

        return self.get_json_response(json.dumps(context['object'].to_dict(include_node_id=include_node_id,track_namespaces=True),indent=2))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)


class CustomInfoObjectSearchView(BasicCustomQueryView):
    #list_actions = [ ('Share', 'url.dingos.action_demo', 0),
    #                 ('Do something else', 'url.dingos.action_demo', 0),
    #                 ('Or yet something else', 'url.dingos.action_demo', 2),
    #                  ]

    pass



class CustomFactSearchView(BasicCustomQueryView):
    counting_paginator = False

    template_name = 'dingos/%s/searches/CustomFactSearch.html' % DINGOS_TEMPLATE_FAMILY
    title = 'Custom Fact Search'

    distinct = ('iobject__iobject_type', 'fact__fact_term', 'fact__fact_values')

    query_base = InfoObject2Fact.objects

    col_headers = ["IO-Type", "Fact Term", "Value"]
    selected_cols = ["iobject.iobject_type.name", "fact.fact_term", "fact.fact_values.all"]

    prefetch_related = ('iobject',
                        'iobject__iobject_type',
                        'fact__fact_term',
                        'fact__fact_values',
                        'fact__fact_values__fact_data_type',
                        'fact__value_iobject_id',
                        'fact__value_iobject_id__latest',
                        'fact__value_iobject_id__latest__iobject_type',
                        'node_id')
    pass



class InfoObjectJSONGraph(BasicJSONView):
    """
    View for JSON representation of InfoObjects Graph data.
    Used in the front-end detail view to display a reference graph of the current InfoObject
    """

    # When building the graph, we skip references to the kill chain. This is because
    # in STIX reports where the kill chain information is consistently used, it completly
    # messes up the graph display.

    skip_terms = [
        # The kill chain links completely mess up the graph
        {'attribute':'kill_chain_id'},
        {'term':'Kill_Chain','operator':'icontains'},
        # Since most STIX Packages list all observables in the 'Observables' element,
        # displaying these links makes the display really messy.
        # The better way to deal with this would be to go through the graph
        # and remove all links from STIX-Package to Observables/Observable, where
        # there is a second such link to from the Observable to something else.
        {'term':'Observables/Observable'}]

    max_objects = 100
    @property
    def returned_obj(self):
        res = {
            'status': False,
            'msg': 'An error occured.',
            'data': None
        }


        iobject_id = self.kwargs.get('pk', None)
        if not iobject_id:
            POST = self.request.POST
            iobject_id = POST.get('iobject_id', None)

        graph = follow_references([iobject_id],
                                  skip_terms = self.skip_terms,
                                  direction='up',
                                  reverse_direction=True,
                                  max_nodes=self.max_objects)


        graph= follow_references([iobject_id],
                                 skip_terms = self.skip_terms,
                                 direction='down',
                                 max_nodes=self.max_objects,
                                 graph=graph)

        if iobject_id:
            res['status'] = True
            if graph.graph['max_nodes_reached']:
                res['msg'] = "Partial reference graph (%s InfoObjects)" % self.max_objects
            else:
                res['msg'] = "Reference graph"

            res['data'] = {
                'node_id': iobject_id,
                'nodes': graph.nodes(data=True),
                'edges': graph.edges(data=True),
            }

        return res
