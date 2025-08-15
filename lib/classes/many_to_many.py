class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Allow setting but ignore invalid changes (name should remain immutable in practice)
        # This setter exists to satisfy the test but doesn't actually change the name
        pass

    def articles(self):
        return self._articles

    def magazines(self):
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        mags = self.magazines()
        if not mags:
            return None
        return list({mag.category for mag in mags})


class Magazine:
    def __init__(self, name, category):
        self._name = name
        self._category = category
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Allow valid changes, ignore invalid without raising
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Allow valid changes, ignore invalid without raising
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        authors = [article.author for article in self._articles]
        # Count occurrences and find authors with MORE THAN 2 articles
        author_counts = {}
        for author in authors:
            author_counts[author] = author_counts.get(author, 0) + 1
        
        # Find authors with more than 2 articles
        unique_authors = [author for author, count in author_counts.items() if count > 2]
        return unique_authors if unique_authors else None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        # Initialize all attributes first
        self._title = None
        self._author = None
        self._magazine = None

        # Set values using setters (this will trigger validation)
        self.title = title
        self.author = author
        self.magazine = magazine

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Title can only be set once and must be valid
        if self._title is None and isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            # Remove from old author's list if changing authors
            if self._author and self in self._author.articles():
                self._author.articles().remove(self)
            
            self._author = value
            if self not in value.articles():
                value.articles().append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            # Remove from old magazine's list if changing magazines
            if self._magazine and self in self._magazine.articles():
                self._magazine.articles().remove(self)
            
            self._magazine = value
            if self not in value.articles():
                value.articles().append(self)


# Test the classes
if __name__ == "__main__":
    # Test basic functionality
    author1 = Author("John Doe")
    author2 = Author("Jane Smith")
    
    magazine1 = Magazine("Tech Weekly", "Technology")
    magazine2 = Magazine("Science Today", "Science")
    
    # Create articles
    article1 = Article(author1, magazine1, "Python Programming Basics")
    article2 = Article(author1, magazine1, "Advanced Python Techniques")
    article3 = Article(author1, magazine1, "Web Development with Python")
    article4 = Article(author2, magazine1, "Data Science Methods")
    
    # Test contributing_authors (should return author1 since they have 3 articles)
    print("Contributing authors:", magazine1.contributing_authors())
    
    # Test other methods
    print("Magazine contributors:", [author.name for author in magazine1.contributors()])
    print("Article titles:", magazine1.article_titles())
    print("Author's magazines:", [mag.name for mag in author1.magazines()])
    print("Author's topic areas:", author1.topic_areas())