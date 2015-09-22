from django.db import models
import django.db.models.options as options

from wagtail.wagtailadmin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.fields import RichTextField


from modelcluster.fields import ParentalKey
from wagtail.wagtailsearch import index


from core.utilities import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class LinkFields(models.Model):
    """
    Represents a link to an external page, a document or a fellow page
    """
    link_external = models.URLField(
        "External link",
        blank=True,
        null=True,
        help_text='Set an external link if you want the link to point somewhere outside the CMS.'
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page if you want the link to point somewhere inside the CMS.'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing document if you want the link to open a document.'
    )
    link_email = models.EmailField(
        blank=True,
        null=True,
        help_text='Set the recipient email address if you want the link to send an email.'
    )
    link_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Set the number if you want the link to dial a phone number.'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_external:
            return self.link_external
        elif self.link_document:
            return self.link_document.url
        elif self.link_email:
            return 'mailto:%s' % self.link_email
        elif self.link_phone:
            return 'tel:%s' % self.link_phone.strip()
        else:
            return "#"

    panels = [
        MultiFieldPanel([
            PageChooserPanel('link_page'),
            FieldPanel('link_external'),
            DocumentChooserPanel('link_document'),
            FieldPanel('link_email'),
            FieldPanel('link_phone'),
            ],
            "Link"
        ),
    ]

    class Meta:
        abstract = True


class MenuElement(LinkFields):
    explicit_name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text='If you want a different name than the page title.'
    )
    short_name = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text='If you need a custom name for responsive devices.'
    )
    css_class = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="CSS Class",
        help_text="Optional styling for the menu item"
    )
    icon_class = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Icon Class",
        help_text="In case you need an icon element <i> for the menu item"
    )

    @property
    def title(self):
        if self.explicit_name:
            return self.explicit_name
        elif self.link_page:
            return self.link_page.title
        elif self.link_document:
            return self.link_document.title
        else:
            return None

    @property
    def url(self):
        return self.link

    def __unicode__(self):
        if self.explicit_name:
            title = self.explicit_name
        elif self.link_page:
            title = self.link_page.title
        else:
            title = ''
        return "%s ( %s )" % (title, self.short_name)

    class Meta:
        verbose_name = "Menu item"
        description = "Elements appearing in the main menu"

    panels = LinkFields.panels + [
        FieldPanel('explicit_name'),
        FieldPanel('short_name'),
        FieldPanel('css_class'),
        FieldPanel('icon_class'),
    ]


class NavigationMenuMenuElement(Orderable, MenuElement):
    parent = ParentalKey(to='core.NavigationMenu', related_name='menu_items')


class NavigationMenuManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(menu_name=name)


@register_snippet
class NavigationMenu(models.Model):

    objects = NavigationMenuManager()
    menu_name = models.CharField(max_length=255, null=False, blank=False)

    @property
    def items(self):
        return self.menu_items.all()

    def __unicode__(self):
        return self.menu_name

    class Meta:
        verbose_name = "Navigation menu"
        description = "Navigation menu"


NavigationMenu.panels = [
    FieldPanel('menu_name', classname='full title'),
    InlinePanel('menu_items', label="Menu Items", help_text='Set the menu items for the current menu.')
]



@register_snippet
class Footer(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    text = models.CharField(max_length=255)
    partner_text = RichTextField(max_length=255, blank=True)

    contact_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose a page to point this link to.'
    )

    signup_title = models.CharField(max_length=255)
    signup_text = models.CharField(max_length=255)

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('address'),
        FieldPanel('phone_number'),
        PageChooserPanel('contact_link'),
        FieldPanel('signup_title'),
        FieldPanel('signup_text'),
        FieldPanel('partner_text'),
    ]

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    class Meta:
        verbose_name = "Footer"
        description = "Info that belongs in the site footer."

    search_fields = [
        index.SearchField('text', partial_match=True),
        index.SearchField('phone_number', partial_match=True),
        index.SearchField('email_address', partial_match=True),
        index.SearchField('signup_title', partial_match=True),
        index.SearchField('signup_text', partial_match=True),
        index.SearchField('partner_text', partial_match=True),
    ]

