# MIMEWrapper

> Wrap an arbitrary file into an email-style MIME document, using a
> sidecar file to obtain metadata header values.

## Usage

Download the `mimewrapper.py` file (or clone the repo) and run it in a
terminal:

    python3 mimewrapper.py [--debug] [--output OUTPUTFILE] \
    [--sidecar HEADERFILE] INPUTFILE

The script will take the `INPUTFILE` and wrap it into a MIME document,
adding the metadata headers provided in `HEADERFILE`.

## General Notes

Although it can be used directly from the terminal, this script is
probably most useful when called by a higher-level script or other
tools as part of a batch process which also creates the `HEADERFILE`
sidecar files, typically by pulling data from the filesystem or by
parsing the payload files themselves.

The `INPUTFILE` payload can be any readable file.  Maximum size is
probably limited only by system memory and your patience; files up to
several megabytes in length seem to be fine, however downstream
systems (particularly those designed for email) may have limits that
you should consider.

If `HEADERFILE` is not explicitly given with the `--sidecar` (or `-s`)
option, the script will look for a file with the same name as the
input plus the suffix `.headers`.  If this file cannot be found, you
will receive an error and the script will terminate.

The format for `HEADERFILE` is based loosely on [RFC822][rfc] [section
3.1.2 "Structure of Header Fields"][rfcsect] in that it should consist
of a series of lines, each containing a "field-name" followed by a
colon (":"), followed by a "field-body" (aka a value), followed by a
newline.  Although RFC822 specifies that only printable ASCII should
be used, Python3 and this script should be more tolerant (in theory,
all UTF-8 should be usable, although I haven't extensively tested it).

[rfc]: https://datatracker.ietf.org/doc/html/rfc822
[rfcsect]: https://datatracker.ietf.org/doc/html/rfc822#section-3.1.2

Comments are allowed in the `HEADERFILE` but must be demarcated by a
"#" *in the first column*.

If an output file name is not provided with the `--output` (or `-o`)
option, the script will output to a file with the same input file name
plus the suffix `.eml` appended.  This file will be overwritten if it
exists, making the operation idempotent.

It should be noted that the `.eml` file extension is not well-defined,
and while it is frequently used for MIME, this is by no means
universal, and many applications capable of parsing the MIME wrapper
may choke on an unexpected payload file type.  (E.g. many email
programs assume that all MIME documents will contain text or limited
subsets of HTML.)

## Rationale

There are many cases where it is useful to encapsulate an arbitrary
file along with metadata information, but there are few
broadly-accepted standards for this.  Metadata information tends to be
stored in filetype-specific ways, e.g. image files have [Exif][], MP3
audio files use [ID3][], text documents have informal semi-standards
like [MultiMarkDown][mmd], office-suite documents generally have
internal proprietary metadata storage mechanisms, etc., plus there's
filesystem-level metadata that is frequently lost when data is moved
between systems.  Metadata preservation is, bluntly, *a hot mess*.

[Exif]: https://en.wikipedia.org/wiki/Exif
[ID3]: https://en.wikipedia.org/wiki/ID3
[mmd]: https://fletcherpenney.net/multimarkdown/

One format that is both well-documented and widely implemented, which
has the capability of carrying arbitrary data payloads *and* flexible
metadata, is [MIME][].

[MIME]: https://en.wikipedia.org/wiki/MIME

MIME doesn't get a lot of use outside of email transmission and
on-disk storage (by some MTAs), which I think is a bit of a shame
because it's actually quite flexible.

At the cost of some storage space (much of which can be recovered via
standard compression tools, if needed), you can ensure that metadata
travels along with the payload regardless of the underlying storage or
transmission mechanisms (even if it passes through antique systems
that aren't 8-bit clean!), and libraries exist for parsing it in most
programming languages and environments, from microcontrollers to
mainframes.

In addition, once wrapped into a MIME document, files can be stored in
email-style databases and moved (e.g. for backup purposes) using
existing mechanisms like SMTP or IMAP, and email MTAs can be used to
provide read-only access to users over a network.

Although many "document management systems" and databases certainly
exist at various levels of scale, in my experience (having implemented
them professionally for many years) they are frequently overkill and
create maintenance hassles out of proportion to their utility for
individuals and small organizations.  In contrast, most users and
organizations already have some way of storing and retrieving email.
So: *why not leverage that?*

Please feel free to use the script as a starting point and inspiration
for your own work.  Contributions in the form of pull requests are
welcome.
