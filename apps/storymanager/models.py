from django.db import models


class Content(models.Model):
    type = models.CharField(max_length=100)
    index = models.IntegerField()

    date_created = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    date_modified = models.DateTimeField(auto_now=True)  # dateModified

    creator_path = models.CharField(max_length=1024)

    def save(self, *args, **kwargs):
        """
        Saving the data to the database
        """
        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            if hasattr(Content, 'self.version'):
                self.version += 1
            else:
                self.version = 2

        super(Content, self).save(*args, **kwargs)

    class Meta:
        # Standard sorting by date
        ordering = ['-date_created']

    def __str__(self):
        return str(self.type)


class Chapter(models.Model):
    title = models.CharField(max_length=100, blank=True, default="")
    text = models.TextField()
    number = models.IntegerField()

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    date_modified = models.DateTimeField(auto_now=True)  # dateModified

    creator_path = models.CharField(max_length=1024)

    # Private property to handle the contents
    _content = None

    # Get all Content IDs
    @property
    def contents(self):
        return self.chapter_contents.all()

    @contents.setter
    def contents(self, value):
        self._contents = value

    def save(self, *args, **kwargs):
        """
        Saving the data to the database
        """
        update = False
        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            if hasattr(Chapter, 'self.version'):
                self.version += 1
            else:
                self.version = 2
            update = True

        super(Chapter, self).save(*args, **kwargs)

        # When it is just an update
        if update:
            if self._contents:
                # Delete old content relations
                self.chapter_contents.all().delete()
                # Create new relations
                for c in self._contents:
                    self.chapter_contents.create(content=c)
        else:
            if self._contents:
                # Create Content relations
                for c in self._contents:
                    self.chapter_contents.create(content=c)

    class Meta:
        # Standard sorting by date
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class Story(models.Model):
    title = models.CharField(max_length=100, unique=True)

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)  # dateAddedtoPC
    date_modified = models.DateTimeField(auto_now=True)  # dateModified

    creator_path = models.CharField(max_length=1024)

    is_draft = models.BooleanField(blank=False, default=False)

    derived_from_id = models.IntegerField(blank=True, null=True)

    _chapters = None

    # Get all Chapter IDs
    @property
    def chapters(self):
        return self.story_chapters.all()

    @chapters.setter
    def chapters(self, value):
        self._chapters = value

    def save(self, *args, **kwargs):
        """
        Saving the data to the database
        """
        update = False
        # Increasing the version on every update
        if self.pk is None:
            self.version = 1
        else:
            if hasattr(Story, 'self.version'):
                self.version += 1
            else:
                self.version = 2
            update = True

        super(Story, self).save(*args, **kwargs)

        # When it is just an update
        if update:
            if self._chapters:
                # Delete old content relations
                self.story_chapters.all().delete()
                # Create new relations
                for ch in self._chapters:
                    self.story_chapters.create(chapter=ch)
        else:
            if self._chapters:
                # Create Content relations
                for ch in self._chapters:
                    self.story_chapters.create(chapter=ch)

    class Meta:
        # Standard sorting by date
        ordering = ['-date_created']

    def __str__(self):
        return self.title


class ChapterInContent(models.Model):
    """
    Represents the 1:m relation between a Chapter and Contents
    """
    content = models.IntegerField()
    # Set the relation
    story = models.ForeignKey(Chapter, related_name='chapter_contents')

    class Meta:
        verbose_name = "Chapter in Content"
        verbose_name_plural = "Chapter in Contents"

    def __str__(self):
        return str(self.content)


class StoryInChapter(models.Model):
    """
    Represents the 1:m relation between a Story and Chapters
    """

    chapter = models.IntegerField()
    # Set the relation
    story = models.ForeignKey(Story, related_name='story_chapters')

    class Meta:
        verbose_name = "Story in Chapter"
        verbose_name_plural = "Story in Chapters"

    def __str__(self):
        return str(self.chapter)
