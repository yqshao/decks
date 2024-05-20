# Anki deck snippets

This is a small collection of my snippets for creating [Anki] decks
for language learning (only Swedish at this point). You can get the
[shared decks] on ankiweb.

Feel free to generate the decks by yourself to suit your needs. I run
the scripts manually to generate the deck (.csv) and media (.mp3)
files to be imported into Anki.  All downloaded and generated files
(csv, xml, mp3) are placed in `~/.cache/decks`, see [here][import csv]
and [here][import media] for import instructions.

[Anki]: https://apps.ankiweb.net/
[shared decks]: https://ankiweb.net/shared/by-author/120881044
[import csv]: https://docs.ankiweb.net/importing/text-files.html
[import media]: https://docs.ankiweb.net/media.html

## Usage

To generate the deck for yourself simply run the script, e.g., clone
the repo somewhere, then `python3 swedish.py`. The script does not
depend on many libraries (you need [requests] for TTS, and that's it).

[requests]: https://docs.python-requests.org/en/latest/user/install/#install

The code uses Google's
[Text-to-Speech](https://cloud.google.com/text-to-speech) API to
generate audio. If you want to use that, you will have to register a
google cloud account (credit card is needed for registration but you
get enough free quota per month for TTS, see their price table in the
link to be certain). AwesomeTTS has some [example][gcloud_api_key] of
how you can get the API key in their wiki.  The snippet assumes you
have the key in the `GCLOUD_TTS_API_KEY` variable.

[gcloud_api_key]: https://github.com/AwesomeTTS/awesometts-anki-addon/wiki/Google-Cloud-Text-to-Speech

## License

Below is the list of resources used in the decks, licenses are noted
but please refer to the original for details:

- [Swedish Kelly list] from University of Gothenburg (CC BY-SA 3.0, LGPL 3.0);
- [The People's Dictionary] from KTH (CC BY-SA 2.5).

[Swedish Kelly list]: https://spraakbanken.gu.se/en/resources/kelly
[The People's Dictionary]: https://folkets-lexikon.csc.kth.se/folkets/om.en.html

The code is simple enough so I don't see a need for license; but if
needed it is licensed under GPLv3, you can find a copy of the license
in the repo (the snippets does borrow some codes from [AwesomeTTS]
under GPLv3).

[AwesomeTTS]: https://github.com/AwesomeTTS/awesometts-anki-addon
