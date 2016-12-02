# inlibraries.com

[Flask](http://flask.pocoo.org) web application that runs the **inlibraries.com** website

The application generates a random library conference website based on the subdomain of the request URL. Underscores in the subdomain will be replaced with spaces.

Examples:
* http://badgers.inlibraries.com  
* http://rabid_badgers.inlibraries.com

## Artist's Statement

Inspired by and in dialogue (without the creator's knowledge) with [Tiff Zhang's Startup Generator](http://tiffzhang.com/startup/), *inlibraries.com* builds on the creator's previous static piece *Smartwatches in Libraries* to more fully engage with the exciting world of **library repackaging**, where careers can be built on convincing library administrators with money to spend (and travel budgets still available, if the conference takes place somewhere nice) that they need someone to tell them all about well-understood (or even outdated) concepts or technologies from the wider world, but while using the word "library" a lot, talking about the unique value of libraries, and including pictures of books in their Powerpoint slides while talking about how libraries are about more than just books these days. All may then retire for a vendor-sponsored reception.

Using aleatoric generation techniques, *inlibraries.com* invites critique of the process of popular dissemination of outside ideas to libraries, and specifically at the rhetorical strategy of simultaneous wide-eyed technocratic utopianism and existential threat fearmongering designed to create a feeling of disempowerment and reliance on outside parties for innovation among library administrators. Also, you can send your friends URLs like http://butts.inlibraries.com/.

## Contributing

I welcome contribution via [fork and pull](https://help.github.com/articles/using-pull-requests/); for feature requests or suggestions, you can contact me on [Twitter](https://twitter.com/waharnum) or the repository's [Issues](https://github.com/waharnum/inlibraries.com/issues) section.

If you have [session madlibs](https://github.com/waharnum/inlibraries.com/blob/master/session_madlibs.json) or [synonms](https://github.com/waharnum/inlibraries.com/blob/master/synonyms.json) to contribute, I'm happy to accept those via [Twitter](https://twitter.com/waharnum) from people who don't feel like dealing with the somewhat unfriendly format. The session madlibs are used in combination with the synonyms file (not a really accurate name at this point) to generate the random verbiage. More of them means the site generation gets more random, which is a good thing!

## Future Development

I'm maintaining the [issues list](https://github.com/waharnum/inlibraries.com/issues) as a means of recording enhancements or other work I'd like to do. My immediate goal is to have something that looks (at first glance) like a legitimate conference homepage; longer-term, I think something that generated random session pages, speaker bios, etc would also be cool.

## Running Your Own

You will want to look at the [production branch](https://github.com/waharnum/inlibraries.com/tree/production); this also includes a Docker container definition, for those into *Docker Docker Docker*.

As with any web application, I recommend running this in production behind a real web server in a reverse-proxy configuration.

## License

My own code uses the [MIT License](https://opensource.org/licenses/MIT)
