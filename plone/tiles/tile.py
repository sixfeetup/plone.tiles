import logging

from zope.interface import implements
from zope.component import getMultiAdapter, queryUtility

from zope.publisher.browser import BrowserView

from plone.tiles.interfaces import ITile, IPersistentTile
from plone.tiles.interfaces import ITileType, ITileDataManager

from plone.tiles.data import decode

#Application tile imports
import z3c.form.form
from z3c.form import button
from plone.autoform.form import AutoExtensibleForm
from plone.directives import form
from zope import schema
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


LOGGER = logging.getLogger('plone.tiles')

class Tile(BrowserView):
    """Basic implementation of a transient tile. Subclasses should override
    __call__ or set an 'index' variable to point to a view page template file.
    """
    
    implements(ITile)
    
    __name__ = None
    __type_name__ = None
    
    __cached_data = None
    
    def __call__(self, *args, **kwargs):
        if not hasattr(self, 'index'):
            raise NotImplemented(u"Override __call__ or set a class variable 'index' to point to a view page template file")
        return self.index(*args, **kwargs)
    
    @property
    def data(self):
        if self.__cached_data is None:
            tile_type = queryUtility(ITileType, name=self.__type_name__)
            if tile_type is None or tile_type.schema is None:
                self.__cached_data = {}
            else:
                try:
                    self.__cached_data = decode(self.request.form, tile_type.schema, missing=True)
                except (ValueError, UnicodeDecodeError,):
                    LOGGER.exception(u"Could not convert form data to schema")
                    self.__cached_data = self.request.form
        return self.__cached_data

class PersistentTile(Tile):
    """Base class for persistent tiles. Identical to `Tile`, except that the
    data dict is never serialized with the URL.
    """
    
    implements(IPersistentTile)
    
    __cached_data = None
    
    @property
    def data(self):
        if self.__cached_data is None:
            reader = getMultiAdapter((self.context, self,), ITileDataManager)
            self.__cached_data = reader.get()
        return self.__cached_data

class ApplicationTile(PersistentTile):
    
    def __call__(self):
        return

class ApplicationTileSchema(form.Schema):
    name = schema.TextLine(title=u"Name")

class ApplicationTileAddForm(AutoExtensibleForm, form.AddForm):
    """View class for application tile adding
    TODO If there is no form schema, do not show the form
    """

    schema = ApplicationTileSchema
    autoGroups = True
    ignoreContext = True # don't use context to get widget data
    index = ViewPageTemplateFile('formlayer.pt')
    
    
    @button.buttonAndHandler((u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            self.status = "Saved"

    #Add form, this should close the layer with the iFrame that contains this form
    @z3c.form.button.buttonAndHandler((u'Cancel'), name='cancel')
    def handleCancel(self, action):
        #IStatusMessage(self.request).addStatusMessage((u"Edit cancelled"), "info")
        #self.request.response.redirect(self.context.absolute_url())
        print "kekjo"
        #"window.parent.jQuery.deco.dialog.close" #How to close when the cancel button is hit
        print self.request.RESPONSE.redirect('@@applicationtile-form-processed')
        return self.request.RESPONSE.redirect('@@applicationtile-form-processed')
        
        #return ViewPageTemplateFile('cancel.pt')
      
ApplicationTileAddView = wrap_form(ApplicationTileAddForm)
      
class ApplicationTileEditForm(AutoExtensibleForm, form.EditForm):
    
    schema = ApplicationTileSchema
    autoGroups = True
    ignoreContext = True # don't use context to get widget data
    
ApplicationTileEditView = wrap_form(ApplicationTileEditForm)

class ApplicationTileFormProcessed(BrowserView):
    
    def __call__(self):
        print "klaar"
        return