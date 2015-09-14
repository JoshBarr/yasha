from datetime import timedelta, date

import re

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import django.db.models.options as options
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from bs4 import BeautifulSoup

from core.utilities import *
from core.snippets import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class RelatedLink(LinkFields):
    """
    Title + link class inheriting from LinkFields
    """
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class CarouselItem(models.Model):
    """
    A set of carousel images
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
    ]

    class Meta:
        abstract = True


class HomePage(Page):
    """
    HomePage class, inheriting from wagtailcore.Page straight away
    """
    subpage_types = [
        'core.AboutPage',
        'core.BlogIndexPage',
        'core.DonatePage',
        'core.ContactPage'
    ]

    class Meta:
        description = "The top level homepage for your site"
        verbose_name = "Homepage"

    # body = RichTextField(default='')
    intro = models.CharField(max_length=255, default='', help_text="Displayed below the headline")
    intro_button_label = models.CharField(max_length=128, default='', help_text="Displayed in the banner area")
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    quote = models.CharField(max_length=255, default='', help_text="The big homepage quote")
    citation = models.CharField(max_length=255, default='', help_text="Who authored the quote")
    issue_headline = models.CharField(max_length=255, default='', help_text="Headline for the issue block")
    issue_body = models.CharField(max_length=255, default='', help_text="Body text for the issue block")
    issue_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    stats_1_number = models.CharField(max_length=20, default='', help_text="Statistic")
    stats_1_text = models.CharField(max_length=255, default='', help_text="Statistic description")
    stats_2_number = models.CharField(max_length=20, default='', help_text="Statistic 2 (optional)")
    stats_2_text = models.CharField(max_length=255, default='', help_text="Statistic description 2 (optional)")
    # date = models.DateField("Post date", default=date.today)
    search_fields = ()

    def get_context(self, request):
        # Get pages
        pages = self.get_children().live()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            pages = pages.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 10)  # Show 10 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        # Update template context
        context = super(HomePage, self).get_context(request)
        context['pages'] = pages
        return context


HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('banner_image'),
    FieldPanel('intro', classname='full'),
    FieldPanel('intro_button_label', classname='full'),
    FieldPanel('quote', classname='full'),
    FieldPanel('citation', classname='full'),
    FieldPanel('issue_headline', classname='full'),
    FieldPanel('issue_body', classname='full'),
    ImageChooserPanel('issue_image'),
    FieldPanel('stats_1_number', classname='full'),
    FieldPanel('stats_1_text', classname='full'),
    FieldPanel('stats_2_number', classname='full'),
    FieldPanel('stats_2_text', classname='full'),
]

HomePage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('search_description')
]


#  Some classes to use as fields (Carousel, Related links and Tags)
class PageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('core.YashaPage', related_name='carousel_items')


class PageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('core.YashaPage', related_name='related_links')


class PageTag(TaggedItemBase):
    content_object = ParentalKey('core.YashaPage', related_name='tagged_items')


class YashaPage(Page):
    """
    Our main custom Page class. All content pages should inherit from this one.
    """
    body = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)
    comments = models.BooleanField(
        "Comments ON/OFF",
        default=False,
        help_text='''Comments are enabled by default. Uncheck the box if you would like to disable them for this\
         page.'''
    )
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=PageTag, blank=True)
    search_fields = (
        index.SearchField('intro_text', boost=1),
        index.SearchField('body_text', boost=1),
        # index.FilterField('date'),
    )

    @property
    def child(self):
        """
        Returns the name of the deepest sublass of the instance
        """
        for related_object in self._meta.get_all_related_objects():
            if not issubclass(related_object.model, self.__class__):
                continue
            try:
                return getattr(self, related_object.get_accessor_name())
            except ObjectDoesNotExist:
                pass

    def is_new(self):
        """
        Feel free to edit/delete this according to your needs
        """
        today = date.today()
        if today - self.date > timedelta(days=7):
            return False
        else:
            return True

    @property
    def body_text(self):
        """
        Returns body field contents text. Useful for search purposes
        """
        return BeautifulSoup(self.body).get_text()

    @property
    def intro_text(self):
        """
        Returns intro field contents text. Useful for search purposes
        """
        return BeautifulSoup(self.intro).get_text()

    @property
    def body_excerpt(self):
        """
        Return body text replacing end of lines (. ? ! chars) with a blank space
        """
        return re.sub(r'([\.?!])([a-zA-Z])', r'\1 \2', self.body_text)

    @property
    def og_image(self):
        # Returns image and image type of feed_image or image as fallback, if exists
        image = {'image': None, 'type': None}
        if self.feed_image:
            image['image'] = self.feed_image
        elif self.image:
            image['image'] = self.image
        name, extension = os.path.splitext(image['image'].file.url)
        image['type'] = extension[1:]
        return image

    class Meta:
        description = "Standard page for your Springload site"
        verbose_name = "Springload standard page"

YashaPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
    ImageChooserPanel('banner_image'),
    InlinePanel(YashaPage,
                'carousel_items',
                label="Carousel items",
                help_text="Add the carousel items that appear in the page."),
    FieldPanel('tags'),
]

YashaPage.promote_panels = [
    FieldPanel('comments'),
    MultiFieldPanel(Page.promote_panels, "SEO and metadata fields"),
    ImageChooserPanel('feed_image'),
]


class AboutPage(YashaPage):
    subpage_types = [
        'core.YashaPage'
    ]

    class Meta:
        description = "About Yasha"
        verbose_name = "About Page"

class DonatePage(YashaPage):
    class Meta:
        description = "The main donations page"
        verbose_name = "Donations Page"

class ContactPage(YashaPage):
    class Meta:
        description = "Contact information for Yasha"
        verbose_name = "Contact Page"


class BlogIndexPage(YashaPage):
    subpage_types = [
        'core.BlogPostPage'
    ]


class BlogPostPage(YashaPage):
    subpage_types = []
    pass

