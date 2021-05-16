FLPFile
========

A simple Python3 FL Studio Project File / stream parser / decoder

Introduction
------------

API
---
The top-level namespace is **FLP**, which contains two classes: **FLP.FLPFile** and **FLP.FLPTrack**.

Class **FLP.FLPFile**
^^^^^^^^^^^^^^^^^^^^^^^

Represents a FL Studio Project data file.  **FLP.FLPFile** objects are iterable and array-like.

Constructor
"""""""""""

**FLP.FLPFile**.__init__(*self*, ``filename``)

    .. list-table::

        * - ``filename`` 
          - the name of an SMF file to read and parse.  Raises an exception if the file does not exist / cannot be read.

Methods
"""""""

    .. list-table::

        * - **FLP.FLPFile**.readHeader(*self*)
          - Determine whether the file starts with a FLP header; returns **True** if it does, **False** otherwise.
        * - **FLP.FLPFile**.parse(*self*)
          - Parse the file.  Determines the file's type and populates an array of content tracks, each of which contains one track from the file and is represented by a **FLP.FLPTrack** instance.
        * - **FLP.FLPFile**.__len__(*self*)
          - The number of tracks in the file (0 if ``parse`` has not yet been invoked).
        * - **FLP.FLPFile**.__iter__(*self*) 
          - Iterates over the tracks in the file
        * - **FLP.FLPFile**.__get_item__(*self*, ``n``)
          - A **FLP.FLPTrack** object, representing the ``n``'th track in the file (or throws a **RangeError** if ``n`` is out of range)
        * - **FLP.FLPFile**.__str__(*self*)
          - Useful information about the file as a whole, number of tracks and their sizes

Properties
""""""""""

If *self* is an **FLP.FLPFile** instance then

    .. list-table::


        * - *self*.division
          - uint16
          - Time quantum of the Fl Studio data encoded in the file (or ``None`` if the ``parse`` method has not yet been invoked).  


Class **FLP.FLPTrack**
^^^^^^^^^^^^^^^^^^^^^^
Class representing a single track from an FL Studio project file, or a collection of FLP events.  **FLP.FLPTrack** objects are iterable and array-like.

Constructor
"""""""""""

**FLP.FLPTrack**.__init__(*self*, ``data``)

Arguments:


    .. list-table::

        * - ``data``
          - binary string or array 
          - data comprising one track from an FL Studio Project file, or a sequence of FLP events
        


So, for example

    .. code-block:: python

        track = Track(data)

    initialises ``track`` for parsing ``data`` representing a track taken from an FL Studio Project file; while

    .. code-block:: python

        track = Track(data)

    initialises ``track`` for parsing ``data`` consisting of a sequence of one or more raw FLP events, e.g. captured from an observed FLP stream.

Methods
"""""""

    .. list-table::

        * - **FLP.FLPTrack**.parse(*self*)
          - Parse the track into an array of events, ordered based on their appearance in the track.  Events are represented by instances of **FLP.chunks.Event**.
        * - **FLP.Track**.__len__(*self*)
          - Returns the number of messages in the track (0 if ``parse`` has not yet been invoked).
        * - **FLP.FLPTrack**.__iter__(*self*)
          - Iterates over the events / messages in the track, in the order in which they appeared.
        * - **FLP.FLPTrack**.__get_item__(*self*, ``n``)
          - Returns a **FLP.chunks.Event** instance representing  the ``n``'th event in the track (or throws a **RangeError** if ``n`` is out of range).
        * - **FLP.FLPTrack**.__str__(*self*)
          - Returns string representations of all the track's events, concatenated and separated by newline ``'\n'``.


Class **FLP.chunks.Event**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Represents a general event as found in FL Project files.  Specific kinds of event are represented by subclasses (for which, see below).

Constructor
"""""""""""
    **FLP.chunks.Event**.__init__(*self*, ``buffer``)

    Arguments:

    .. list-table::

      * -  ``buffer`` 
        -  binary string or array 
        -  bytes making up the event.

Methods
"""""""

   .. list-table::


    * - **FLP.chunks.Event**.__len__(*self*)
      - The total length of the event.
    * - **FLP.chunks.Event**.__str__(*self*)
      - String representation of the event.  By default, a representation of the raw bytes as a binary string.

Properties
""""""""""

If *self* is an **FLP.chunks.Event** instance then

    .. list-table::

        * - *self*.time
          -  the timestamp with which the event instance was initialised; measured in units of the quantum of time defined by the value of the ``division`` property of the **FLP.FLPFile** instance containing the track of which this event forms a part.
        * - *self*.header
          - the event's initial byte, which serves to identify its kind.
        * - *self*.data
          - binary string or array containing the event's *body*, i.e. its data content, with the header byte and other formatting removed

Specialisations of this class, describing specific kinds of FL Studio event, offer various dynamically generated read-only properties, describing properties specific to them.  Each kind of event makes efforts to represent the message content in the most appropriate manner.


Examples
--------

Included in the package is the following simple test script:

    .. code-block:: python

        from FLP import FLPFile
        from sys import argv

        def parse(file):
            c=FLPFile(file)
            c.parse()
            print(str(c))
            for idx, track in enumerate(c):
                track.parse()
                print(f'Track {idx}:')
                print(str(track))


        parse(argv[1])  

The first few lines of the output from applying this to a FL Studio Project file are as follows: ::

        Header is Format 0x0 nTracks 0x2 division 0x60
        Buffer32 has length 4
        Format 0x0 nTracks 0x2 division 0x60
	       Track 0 of length 0
        Track 0:
        VAR 199(Version) = 20.8.3.2304.
        DWORD 159(Unknown) = 589824
        BYTE 28(Registered) = 1 (01)
        BYTE 37(Unknown) = 1
        VAR 200(RegName) = \@Fz0b879vDC>?CD;;
        DWORD 156(FineTempo) = 3235119360 (C0D40100)
        WORD 67(CurrentPatNum) = 256 (0100)
        BYTE 9(LoopActive) = 1 (01)
        BYTE 11(Shuffle) = 0 (00)       
        WORD 80(MainPitch) = 0 (0000)
        BYTE 17(Numerator) = 4 (04)
        BYTE 18(Denominator) = 4 (04)
        BYTE 35(Unknown) = 1
        BYTE 23(PanVolumeTab) = 0 (00)
        BYTE 30(TruncateClipNotes) = 1 (01)
        BYTE 10(ShowInfo) = 0 (00)
        VAR 194(Title) = 
        VAR 206(Genre) = 
        VAR 207(Author) = 
        VAR 202(ProjDataPath) = 
        VAR 195(Comment) = 
        VAR 237(ProjectTime) = 10 DF D7 ED 3B A4 E5 40 00 00 00 E0 C9 BE 32 3F
        VAR 231(ChanGroupName) = Audio
        VAR 231(ChanGroupName) = Unsorted
        DWORD 146(CurrentFilterNum) = 0 (00000000)
        VAR 216(CtrlRecChan) = 
        VAR 226(RemoteCtrl_MIDI) = 01 00 00 00 00 00 00 00 01 90 FF 0F 04 00 00 00 D5 01 00 00
        VAR 226(RemoteCtrl_MIDI) = FD 00 00 00 00 00 00 00 80 90 FF 0F 04 00 00 00 D5 01 00 00
        VAR 226(RemoteCtrl_MIDI) = FF 00 00 00 FF 00 00 00 04 00 FF 0F 04 00 00 00 00 FE FF FF
        WORD 64(NewChan) = 0 (0000)
        BYTE 21(ChannelType) = 0 (00)
        VAR 201(DefPluginName) = 
        VAR 212(NewPlugin) = 00 00 00 00 00 00 00 00 FF FF FF FF 00 00 00 00 50 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C2 00 00 00 16 01 00 00 00 00 00 00 00 00 00 00
        VAR 203(PluginName) = Sampler


Requirements
------------

FLPFile is a pure python module requiring Python 3.6 or later to run (this could be reduced by using more long-winded equivalents to Python 3.6's ``f'...{x}'`` string interpolation syntax).

It is known to run on MacOS and Linux.  It should run on Windows, but then, nothing is certain when Windows is involved, is it?  Attempts to make it run on Windows are at your own risk.


